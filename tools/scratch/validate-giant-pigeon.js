#!/usr/bin/env node
"use strict";

const assert = require("assert/strict");
const crypto = require("crypto");
const fs = require("fs");
const path = require("path");
const JSZip = require("jszip");
const {JSDOM} = require("jsdom");
const VirtualMachine = require("scratch-vm");
const {ScratchStorage} = require("scratch-storage");
const {renderScratchChain} = require("./build-giant-pigeon");

const REPO_ROOT = path.resolve(__dirname, "../..");
const OUTPUT_ROOT = path.join(REPO_ROOT, "sites/shkolakoda/static/projects/escape-from-the-giant-pigeon");
const CONTENT_PATH = path.join(REPO_ROOT, "sites/shkolakoda/scratch_projects/escape-from-the-giant-pigeon.json");
const STARTER_PATH = path.join(OUTPUT_ROOT, "escape-from-the-giant-pigeon-starter.sb3");
const FINISHED_PATH = path.join(OUTPUT_ROOT, "escape-from-the-giant-pigeon-finished.sb3");
const ASSET_PACK_PATH = path.join(OUTPUT_ROOT, "escape-from-the-giant-pigeon-assets.zip");
const REQUIRED_SPRITES = ["Player", "Giant Pigeon", "Safe Zone"];
const REQUIRED_VARIABLES = ["Game State", "Panic", "Survival Time", "Pigeon Speed"];
const REQUIRED_FINISHED_OPCODES = [
  "event_whenflagclicked",
  "event_whenkeypressed",
  "event_whenbroadcastreceived",
  "event_broadcast",
  "event_broadcastandwait",
  "data_setvariableto",
  "control_forever",
  "control_if",
  "control_wait",
  "motion_gotoxy",
  "motion_changexby",
  "motion_changeyby",
  "motion_setx",
  "motion_sety",
  "motion_pointtowards",
  "motion_movesteps",
  "sensing_keypressed",
  "sensing_touchingobject",
  "sensing_distanceto",
  "sensing_resettimer",
  "sensing_timer",
  "operator_equals",
  "operator_not",
  "operator_round",
  "looks_switchcostumeto",
  "sound_playuntildone",
  "sound_stopallsounds"
];

function digest(buffer) {
  return crypto.createHash("md5").update(buffer).digest("hex");
}

async function openProject(filename) {
  const buffer = fs.readFileSync(filename);
  const archive = await JSZip.loadAsync(buffer, {checkCRC32: true});
  assert(archive.file("project.json"), `${path.basename(filename)} is missing project.json`);
  const project = JSON.parse(await archive.file("project.json").async("string"));
  return {buffer, archive, project};
}

async function validateMedia(packageName, archive, project) {
  const records = project.targets.flatMap((target) => [...target.costumes, ...target.sounds]);
  assert(records.length >= 10, `${packageName} should contain the complete original media set`);
  for (const record of records) {
    assert.match(record.md5ext, /^[a-f0-9]{32}\.(svg|wav)$/);
    assert.equal(record.assetId, record.md5ext.slice(0, 32));
    const entry = archive.file(record.md5ext);
    assert(entry, `${packageName} references missing asset ${record.md5ext}`);
    const content = await entry.async("nodebuffer");
    assert.equal(digest(content), record.assetId, `${packageName} asset hash mismatch for ${record.md5ext}`);
    if (record.dataFormat === "svg") {
      const source = content.toString("utf8");
      assert.match(source, /^<svg[\s>]/);
      assert.match(source, /<title[^>]*>/);
    }
    if (record.dataFormat === "wav") {
      assert.equal(content.subarray(0, 4).toString("ascii"), "RIFF");
      assert.equal(content.subarray(8, 12).toString("ascii"), "WAVE");
    }
  }
}

function inspectProject(packageName, project) {
  assert.equal(project.meta.semver, "3.0.0");
  assert.equal(project.targets[0].isStage, true);
  assert.equal(project.targets[0].name, "Stage");
  const spriteNames = project.targets.filter((target) => !target.isStage).map((target) => target.name);
  for (const name of REQUIRED_SPRITES) assert(spriteNames.includes(name), `${packageName} missing sprite ${name}`);
  const variableNames = Object.values(project.targets[0].variables).map(([name]) => name);
  for (const name of REQUIRED_VARIABLES) assert(variableNames.includes(name), `${packageName} missing variable ${name}`);
  for (const target of project.targets) {
    assert(target.costumes.length >= 1, `${packageName} target ${target.name} has no costume`);
    assert(target.comments && Object.keys(target.comments).length, `${packageName} target ${target.name} has no instructions/comment`);
  }
  const opcodes = new Set(project.targets.flatMap((target) => Object.values(target.blocks).map((block) => block.opcode)));
  return {spriteNames, variableNames, opcodes, blockCount: project.targets.reduce((count, target) => count + Object.keys(target.blocks).length, 0)};
}

function validateSourceConsistency() {
  const content = JSON.parse(fs.readFileSync(CONTENT_PATH, "utf8"));
  const scriptIds = new Set(content.scripts.map((script) => script.id));
  assert.equal(scriptIds.size, content.scripts.length, "Scratch script ids must be unique");
  for (const script of content.scripts) {
    assert.equal(renderScratchChain(script.blocks), script.source, `Website/SB3 source drift in ${script.id}`);
  }
  for (const section of content.code_sections) {
    assert(section.pseudocode && section.test && section.mistake && section.teacher_checkpoint);
    for (const scriptId of section.script_ids) assert(scriptIds.has(scriptId), `Unknown script ${scriptId}`);
  }
  assert.equal(content.code_sections.length, 10);
  return content.scripts.length;
}

function validateRenderedBlocks(vendorScript) {
  const content = JSON.parse(fs.readFileSync(CONTENT_PATH, "utf8"));
  const markup = content.scripts.map((script) => `<pre class="scratchblocks">${script.source.replace(/&/g, "&amp;").replace(/</g, "&lt;")}</pre>`).join("");
  const dom = new JSDOM(markup, {runScripts: "dangerously"});
  dom.window.HTMLCanvasElement.prototype.getContext = () => ({measureText: (text) => ({width: String(text).length * 6})});
  dom.window.eval(fs.readFileSync(vendorScript, "utf8"));
  assert(dom.window.scratchblocks, "Self-hosted renderer did not create window.scratchblocks");
  dom.window.scratchblocks.renderMatching("pre.scratchblocks", {style: "scratch3", languages: ["en"], scale: 0.82});
  assert.equal(dom.window.document.querySelectorAll("svg").length, content.scripts.length, "Not every Scratch source rendered to SVG blocks");
  return content.scripts.length;
}

async function validateOfficialLoad(filename) {
  const vm = new VirtualMachine();
  vm.attachStorage(new ScratchStorage());
  await vm.loadProject(fs.readFileSync(filename));
  const targets = vm.runtime.targets.map((target) => target.getName());
  assert.deepEqual(targets, ["Stage", "Safe Zone", "Giant Pigeon", "Player"]);
  for (const target of vm.runtime.targets) {
    assert(target.sprite.costumes.every((costume) => costume.asset), `${path.basename(filename)} failed to load a costume asset`);
    assert(target.sprite.sounds.every((sound) => sound.asset), `${path.basename(filename)} failed to load a sound asset`);
  }
  vm.stopAll();
  vm.quit();
  return targets.length;
}

function pause(milliseconds) {
  return new Promise((resolve) => setTimeout(resolve, milliseconds));
}

async function validateRuntimeSmoke(filename) {
  const vm = new VirtualMachine();
  vm.attachStorage(new ScratchStorage());
  await vm.loadProject(fs.readFileSync(filename));
  const stage = vm.runtime.getTargetForStage();
  const sprite = (name) => vm.runtime.targets.find((target) => target.getName() === name);
  const variable = (name) => Object.values(stage.variables).find((item) => item.name === name);
  const player = sprite("Player");
  player.setXY(20, 30);
  player.setVisible(false);
  player.setCostume(1);
  variable("Game State").value = "CAUGHT";
  variable("Panic").value = 99;
  variable("Survival Time").value = 44;
  vm.start();
  try {
    vm.greenFlag();
    await pause(220);
    assert.equal(variable("Game State").value, "READY");
    assert.equal(Number(variable("Panic").value), 0);
    assert.equal(Number(variable("Survival Time").value), 0);
    assert.equal(Number(variable("Pigeon Speed").value), 2);
    assert.deepEqual([player.x, player.y, player.currentCostume, player.visible], [-190, -110, 0, true]);
    assert.deepEqual([sprite("Giant Pigeon").x, sprite("Giant Pigeon").y], [155, 100]);
    assert.deepEqual([sprite("Safe Zone").x, sprite("Safe Zone").y], [190, -115]);
    const startDistance = Math.hypot(sprite("Giant Pigeon").x - player.x, sprite("Giant Pigeon").y - player.y);
    assert(startDistance > 350, "Pigeon fair-start distance is too small");
    await pause(1050);
    assert.equal(variable("Game State").value, "PLAYING");
    player.setXY(217, -110);
    vm.postIOData("keyboard", {key: "ArrowRight", isDown: true});
    await pause(180);
    vm.postIOData("keyboard", {key: "ArrowRight", isDown: false});
    assert.equal(player.x, 218, "Player right boundary clamp did not run");
    variable("Game State").value = "SAFE";
    player.setXY(0, 0);
    vm.runtime.startHats("event_whenkeypressed", {KEY_OPTION: "r"});
    await pause(220);
    assert.equal(variable("Game State").value, "READY");
    assert.deepEqual([player.x, player.y], [-190, -110]);
    await pause(1050);
    assert.equal(variable("Game State").value, "PLAYING");
    return "green flag, fair start, variable/visibility/costume reset, movement boundary, and R restart";
  } finally {
    vm.stopAll();
    vm.quit();
  }
}

async function validateAssetPack() {
  const archive = await JSZip.loadAsync(fs.readFileSync(ASSET_PACK_PATH), {checkCRC32: true});
  const required = [
    "README.txt",
    "LICENSES.txt",
    "project-sketch.svg",
    "assets/player.svg",
    "assets/giant-pigeon.svg",
    "assets/safe-zone.svg",
    "assets/stage-backdrop.svg",
    "assets/start.wav",
    "assets/caught.wav",
    "assets/safe.wav"
  ];
  for (const filename of required) assert(archive.file(filename), `Asset pack is missing ${filename}`);
  assert((await archive.file("README.txt").async("string")).includes("Students may redraw"));
  assert((await archive.file("LICENSES.txt").async("string")).includes("Scratch Foundation"));
  return Object.keys(archive.files).filter((filename) => !archive.files[filename].dir).length;
}

async function main() {
  for (const filename of [STARTER_PATH, FINISHED_PATH, ASSET_PACK_PATH]) assert(fs.existsSync(filename), `Missing generated file ${filename}`);
  const starter = await openProject(STARTER_PATH);
  const finished = await openProject(FINISHED_PATH);
  await validateMedia("starter", starter.archive, starter.project);
  await validateMedia("finished", finished.archive, finished.project);
  const starterInspection = inspectProject("starter", starter.project);
  const finishedInspection = inspectProject("finished", finished.project);
  assert.notEqual(digest(starter.buffer), digest(finished.buffer), "Starter and finished packages must differ");
  assert(finishedInspection.blockCount > starterInspection.blockCount * 2, "Finished package should contain substantially more code");
  for (const opcode of ["motion_changexby", "motion_pointtowards", "sensing_touchingobject", "event_whenkeypressed"]) {
    assert(!starterInspection.opcodes.has(opcode), `Starter unexpectedly contains completed opcode ${opcode}`);
  }
  for (const opcode of REQUIRED_FINISHED_OPCODES) assert(finishedInspection.opcodes.has(opcode), `Finished package missing opcode ${opcode}`);
  const sourceCount = validateSourceConsistency();
  const assetPackCount = await validateAssetPack();
  const starterTargets = await validateOfficialLoad(STARTER_PATH);
  const finishedTargets = await validateOfficialLoad(FINISHED_PATH);
  const runtimeSmoke = await validateRuntimeSmoke(FINISHED_PATH);
  const vendorScript = path.join(REPO_ROOT, "sites/shkolakoda/static/vendor/scratchblocks/scratchblocks-3.7.1.min.js");
  const vendorLicense = path.join(REPO_ROOT, "sites/shkolakoda/static/vendor/scratchblocks/LICENSE.txt");
  assert(fs.existsSync(vendorScript) && fs.statSync(vendorScript).size > 100000, "Pinned self-hosted scratchblocks renderer is missing");
  assert(fs.existsSync(vendorLicense) && fs.readFileSync(vendorLicense, "utf8").includes("Permission is hereby granted"), "scratchblocks MIT licence is missing");
  const renderedCount = validateRenderedBlocks(vendorScript);
  console.log("Giant Pigeon Scratch validation passed:");
  console.log(`- starter: ${starterInspection.blockCount} blocks, ${starterTargets} official-VM targets`);
  console.log(`- finished: ${finishedInspection.blockCount} blocks, ${finishedTargets} official-VM targets`);
  console.log(`- shared website/package scripts: ${sourceCount}`);
  console.log(`- scratchblocks browser renderings: ${renderedCount}`);
  console.log(`- runtime smoke: ${runtimeSmoke}`);
  console.log(`- asset pack files: ${assetPackCount}`);
  console.log("- ZIP CRCs, project.json, media hashes, SVG/WAV signatures, names, variables, opcodes, and vendor licence: valid");
}

main().catch((error) => {
  console.error(error.stack || error);
  process.exitCode = 1;
});
