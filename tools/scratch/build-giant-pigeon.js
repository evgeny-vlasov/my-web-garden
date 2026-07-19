#!/usr/bin/env node
"use strict";

const crypto = require("crypto");
const fs = require("fs");
const path = require("path");
const JSZip = require("jszip");

const REPO_ROOT = path.resolve(__dirname, "../..");
const CONTENT_PATH = path.join(
  REPO_ROOT,
  "sites/shkolakoda/scratch_projects/escape-from-the-giant-pigeon.json"
);
const OUTPUT_ROOT = path.join(
  REPO_ROOT,
  "sites/shkolakoda/static/projects/escape-from-the-giant-pigeon"
);
const ASSET_ROOT = path.join(OUTPUT_ROOT, "assets");
const VENDOR_ROOT = path.join(REPO_ROOT, "sites/shkolakoda/static/vendor/scratchblocks");
const FIXED_DATE = new Date("2026-01-01T00:00:00.000Z");
const TOOL_PACKAGE = require("./package.json");
const VM_VERSION = TOOL_PACKAGE.devDependencies["scratch-vm"];
const SCRATCHBLOCKS_VERSION = TOOL_PACKAGE.devDependencies.scratchblocks;
const spec = JSON.parse(fs.readFileSync(CONTENT_PATH, "utf8"));

const VARIABLES = {
  "Game State": {id: "var_game_state", initial: "READY"},
  Panic: {id: "var_panic", initial: 0},
  "Survival Time": {id: "var_survival_time", initial: 0},
  "Pigeon Speed": {id: "var_pigeon_speed", initial: 2}
};
const BROADCASTS = {
  "Reset Game": "broadcast_reset_game",
  "Reset Actors": "broadcast_reset_actors",
  Caught: "broadcast_caught",
  "Reached Safety": "broadcast_reached_safety"
};

function ensureDirectories() {
  for (const directory of [OUTPUT_ROOT, ASSET_ROOT, VENDOR_ROOT]) {
    fs.mkdirSync(directory, {recursive: true});
  }
}

function normalized(value) {
  return `${value.trim()}\n`;
}

function md5(buffer) {
  return crypto.createHash("md5").update(buffer).digest("hex");
}

function xml(body, viewBox, title, description) {
  const [x, y, width, height] = viewBox;
  return normalized(`
<svg xmlns="http://www.w3.org/2000/svg" viewBox="${x} ${y} ${width} ${height}" role="img" aria-labelledby="title desc">
  <title id="title">${title}</title>
  <desc id="desc">${description}</desc>
  ${body.trim()}
</svg>`);
}

function makeSvgAssets() {
  const ink = "#20201d";
  const paper = "#fffdf4";
  const yellow = "#f4c542";
  const green = "#147d64";
  const blue = "#2257b5";
  const red = "#c93d32";
  const grey = "#a9b0b2";

  return {
    "player.svg": xml(`
      <g stroke="${ink}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
        <path fill="${paper}" d="M22 38 Q18 52 21 70 L15 84 L29 85 L35 68 L42 85 L56 83 L49 68 Q53 52 47 38 Z"/>
        <path fill="#f2b48c" d="M21 21 Q21 6 36 5 Q52 7 51 23 Q48 37 36 38 Q24 36 21 21 Z"/>
        <path fill="${blue}" d="M19 18 Q25 2 39 5 Q49 6 53 15 Q44 12 34 14 Q25 17 19 18 Z"/>
        <path fill="${yellow}" d="M20 37 Q35 43 50 35 L51 46 Q35 51 18 43 Z"/>
        <circle cx="31" cy="22" r="1.8" fill="${ink}" stroke="none"/>
        <circle cx="43" cy="21" r="1.8" fill="${ink}" stroke="none"/>
        <path fill="none" d="M32 29 Q37 33 43 28"/>
        <path fill="none" d="M21 50 L10 64 M49 50 L61 61"/>
      </g>`, [0, 0, 70, 90], "Player — normal costume", "Original sketch-style child adventurer with a yellow scarf."),
    "player-caught.svg": xml(`
      <g stroke="${ink}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
        <path fill="${paper}" d="M22 38 Q18 52 21 70 L15 84 L29 85 L35 68 L42 85 L56 83 L49 68 Q53 52 47 38 Z"/>
        <path fill="#f2b48c" d="M21 21 Q21 6 36 5 Q52 7 51 23 Q48 37 36 38 Q24 36 21 21 Z"/>
        <path fill="${blue}" d="M19 18 Q25 2 39 5 Q49 6 53 15 Q44 12 34 14 Q25 17 19 18 Z"/>
        <path fill="${red}" d="M20 37 Q35 43 50 35 L51 46 Q35 51 18 43 Z"/>
        <path fill="none" d="M27 18 L34 25 M34 18 L27 25 M40 18 L47 25 M47 18 L40 25"/>
        <ellipse cx="37" cy="31" rx="5" ry="3" fill="none"/>
        <path fill="none" d="M21 49 L7 38 M49 49 L63 37"/>
        <path fill="${grey}" d="M4 10 L11 5 L13 14 L22 11 L18 20 L8 19 Z"/>
      </g>`, [0, 0, 70, 90], "Player — caught costume", "Original sketch-style player looking surprised after being caught."),
    "giant-pigeon.svg": xml(`
      <g stroke="${ink}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round">
        <path fill="${grey}" d="M37 55 Q12 18 4 10 Q32 13 58 36 Q65 20 87 23 Q112 26 112 49 Q136 45 147 58 Q127 75 104 70 Q93 96 60 90 Q39 84 37 55 Z"/>
        <path fill="#c9d0d1" d="M48 54 Q20 41 11 24 Q45 26 69 50 Q51 22 58 7 Q83 26 84 53 Z"/>
        <path fill="${paper}" d="M83 24 Q101 7 119 19 Q131 30 119 48 Q110 58 95 48 Z"/>
        <circle cx="109" cy="29" r="8" fill="${paper}"/>
        <circle cx="112" cy="29" r="3" fill="${ink}"/>
        <path fill="${yellow}" d="M119 36 L145 42 L120 49 Z"/>
        <path fill="none" d="M61 90 L57 104 M73 91 L76 104 M49 105 L63 104 M68 105 L83 104"/>
        <path fill="none" d="M42 62 Q65 75 92 62"/>
      </g>`, [0, 0, 150, 110], "Giant Pigeon — wings up", "Original funny oversized pigeon with raised wings and a dramatic stare."),
    "giant-pigeon-wings-down.svg": xml(`
      <g stroke="${ink}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round">
        <path fill="${grey}" d="M27 50 Q18 27 39 20 Q55 18 65 33 Q72 20 91 23 Q111 27 112 48 Q136 45 147 58 Q128 74 105 69 Q95 95 61 91 Q33 87 27 50 Z"/>
        <path fill="#c9d0d1" d="M38 50 Q9 54 4 79 Q37 79 70 57 Q49 88 56 103 Q82 81 85 54 Z"/>
        <path fill="${paper}" d="M83 24 Q101 7 119 19 Q131 30 119 48 Q110 58 95 48 Z"/>
        <circle cx="109" cy="29" r="8" fill="${paper}"/>
        <circle cx="112" cy="29" r="3" fill="${ink}"/>
        <path fill="${yellow}" d="M119 36 L145 42 L120 49 Z"/>
        <path fill="none" d="M61 91 L57 105 M73 91 L77 105 M49 106 L63 105 M69 106 L84 105"/>
        <path fill="none" d="M43 62 Q66 75 93 61"/>
      </g>`, [0, 0, 150, 110], "Giant Pigeon — wings down", "Original funny oversized pigeon with lowered wings for a two-frame flap."),
    "safe-zone.svg": xml(`
      <g stroke="${ink}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
        <path fill="${paper}" d="M10 94 L10 35 L45 7 L80 35 L80 94 Z"/>
        <path fill="${green}" d="M5 36 L45 3 L85 36 L78 45 L45 18 L12 45 Z"/>
        <path fill="#dce7dc" d="M29 94 L29 49 Q45 38 61 49 L61 94 Z"/>
        <path stroke="${red}" d="M31 52 L58 79 M30 68 L55 93 M43 44 L61 62"/>
        <path stroke="${paper}" d="M29 60 L58 89 M34 46 L61 73"/>
        <path fill="${yellow}" d="M15 28 L23 22 L28 30 L20 35 Z"/>
      </g>`, [0, 0, 90, 105], "Safe Zone — inactive", "Original striped shelter waiting at the edge of the chase stage."),
    "safe-zone-active.svg": xml(`
      <g stroke="${ink}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
        <path fill="#dff5e7" d="M10 94 L10 35 L45 7 L80 35 L80 94 Z"/>
        <path fill="${green}" d="M5 36 L45 3 L85 36 L78 45 L45 18 L12 45 Z"/>
        <path fill="${yellow}" d="M29 94 L29 49 Q45 38 61 49 L61 94 Z"/>
        <path fill="none" d="M37 67 L44 75 L56 57" stroke-width="6"/>
        <path fill="${yellow}" d="M7 10 L12 17 L20 14 L15 22 L21 28 L12 25 L6 32 L8 22 L1 17 L10 18 Z"/>
        <path fill="${yellow}" d="M74 10 L78 17 L87 17 L80 22 L83 31 L76 25 L68 30 L72 21 L66 15 L75 17 Z"/>
      </g>`, [0, 0, 90, 105], "Safe Zone — active", "Original striped shelter glowing after the player reaches safety."),
    "stage-backdrop.svg": xml(`
      <rect width="480" height="360" fill="${paper}"/>
      <path d="M0 52 Q118 38 237 53 T480 47 M0 299 Q120 286 242 301 T480 295" fill="none" stroke="#e7e1cf" stroke-width="3"/>
      <path d="M58 41 L71 22 L85 41 M76 41 L91 14 L107 41 M91 41 L110 25 L128 41" fill="none" stroke="#89959a" stroke-width="5"/>
      <path d="M329 43 L343 15 L355 43 M348 43 L362 27 L377 43 M370 43 L388 10 L403 43 M396 43 L415 24 L431 43" fill="none" stroke="#89959a" stroke-width="5"/>
      <path d="M28 315 Q54 292 83 311 T139 309" fill="none" stroke="${green}" stroke-width="7"/>
      <path d="M169 294 Q201 268 234 291 T301 289" fill="none" stroke="#d8d0b7" stroke-width="9" stroke-dasharray="7 12"/>
      <path d="M349 307 L455 307 L455 196" fill="none" stroke="${yellow}" stroke-width="12" stroke-linecap="round"/>
      <path d="M18 333 L152 333" stroke="${blue}" stroke-width="4" stroke-dasharray="9 8"/>
      <text x="22" y="350" font-family="Arial, sans-serif" font-size="13" fill="${ink}">START — x -190, y -110</text>
      <text x="354" y="332" font-family="Arial, sans-serif" font-size="13" font-weight="bold" fill="${ink}">SAFE ZONE</text>
      <path d="M220 87 q16 -19 33 0 q-19 -7 -33 0 M251 83 q13 -15 27 1" fill="none" stroke="#687174" stroke-width="3"/>
      <path d="M18 18 H462 V342 H18 Z" fill="none" stroke="${ink}" stroke-width="3" stroke-dasharray="8 5"/>
    `, [0, 0, 480, 360], "Escape from the Giant Pigeon stage", "Original paper-like top-down chase backdrop with a lower-left start, skyline doodles, stage boundary, and lower-right safe zone." )
  };
}

function makeProjectSketch() {
  return xml(`
    <defs>
      <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="#d9e6eb" stroke-width="1"/></pattern>
      <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="#20201d"/></marker>
    </defs>
    <rect width="960" height="700" fill="#fffdf4"/>
    <rect width="960" height="700" fill="url(#grid)"/>
    <path d="M44 45 Q480 36 914 48 L907 650 Q476 665 48 649 Z" fill="none" stroke="#20201d" stroke-width="4" stroke-dasharray="11 7"/>
    <text x="72" y="92" font-family="Georgia,serif" font-size="34" font-weight="bold" fill="#20201d">ESCAPE SYSTEM — inventor's sketch</text>
    <text x="73" y="122" font-family="Arial,sans-serif" font-size="16" fill="#555">Provisional School of Code project artwork · stage coordinates 480 × 360</text>
    <g transform="translate(75 160)">
      <rect width="520" height="390" rx="8" fill="#fffef8" stroke="#20201d" stroke-width="4"/>
      <path d="M20 20H500V370H20Z" fill="none" stroke="#c93d32" stroke-width="3" stroke-dasharray="9 7"/>
      <circle cx="75" cy="305" r="23" fill="#2257b5" stroke="#20201d" stroke-width="3"/><text x="66" y="313" font-family="Arial" font-size="22" font-weight="bold" fill="white">A</text>
      <path d="M384 82 q46 -54 92 0 q-50 -18 -92 0" fill="#a9b0b2" stroke="#20201d" stroke-width="4"/><circle cx="443" cy="58" r="17" fill="white" stroke="#20201d" stroke-width="3"/><text x="438" y="65" font-family="Arial" font-size="19" font-weight="bold">B</text>
      <path d="M403 337V248L454 210L501 249V337Z" fill="#e2f4ed" stroke="#20201d" stroke-width="4"/><text x="442" y="295" font-family="Arial" font-size="24" font-weight="bold">C</text>
      <text x="28" y="46" font-family="Arial" font-size="20" font-weight="bold" fill="#c93d32">D — STAGE BOUNDARIES</text>
      <path d="M99 294 Q242 250 402 111" fill="none" stroke="#20201d" stroke-width="4" marker-end="url(#arrow)"/>
      <text x="146" y="236" font-family="Arial" font-size="17" transform="rotate(-17 146 236)">pigeon points toward Player</text>
      <path d="M95 314 Q252 352 397 302" fill="none" stroke="#147d64" stroke-width="4" marker-end="url(#arrow)"/>
      <text x="174" y="360" font-family="Arial" font-size="17">Player moves with x / y</text>
      <text x="34" y="345" font-family="Arial" font-size="14">x -190, y -110</text>
      <text x="365" y="106" font-family="Arial" font-size="14">x 155, y 100</text>
      <text x="379" y="361" font-family="Arial" font-size="14">x 190, y -115</text>
    </g>
    <g transform="translate(630 158)" font-family="Arial,sans-serif" fill="#20201d">
      <rect width="250" height="116" rx="7" fill="#fff4bd" stroke="#20201d" stroke-width="3"/>
      <text x="18" y="31" font-size="20" font-weight="bold">E — PANIC METER</text>
      <rect x="19" y="52" width="211" height="26" fill="white" stroke="#20201d" stroke-width="2"/>
      <rect x="22" y="55" width="148" height="20" fill="#c93d32"/>
      <text x="19" y="101" font-size="14">100 − round(distance ÷ 4)</text>
      <text x="0" y="160" font-size="21" font-weight="bold">F — MAIN GAME-STATE FLOW</text>
      <rect x="7" y="181" width="104" height="42" rx="20" fill="#fff4bd" stroke="#20201d" stroke-width="3"/><text x="27" y="208" font-size="17" font-weight="bold">READY</text>
      <path d="M111 202H146" stroke="#20201d" stroke-width="3" marker-end="url(#arrow)"/>
      <rect x="151" y="181" width="98" height="42" rx="20" fill="#e9effb" stroke="#20201d" stroke-width="3"/><text x="167" y="208" font-size="17" font-weight="bold">PLAYING</text>
      <path d="M200 224V271" stroke="#20201d" stroke-width="3" marker-end="url(#arrow)"/>
      <path d="M200 246H58V271" fill="none" stroke="#20201d" stroke-width="3" marker-end="url(#arrow)"/>
      <rect x="7" y="277" width="104" height="42" rx="20" fill="#fde9e5" stroke="#20201d" stroke-width="3"/><text x="21" y="304" font-size="17" font-weight="bold">CAUGHT</text>
      <rect x="151" y="277" width="98" height="42" rx="20" fill="#e2f4ed" stroke="#20201d" stroke-width="3"/><text x="176" y="304" font-size="17" font-weight="bold">SAFE</text>
      <text x="2" y="350" font-size="15">touch pigeon → CAUGHT</text>
      <text x="2" y="376" font-size="15">touch safe zone → SAFE</text>
      <text x="2" y="414" font-size="15" font-weight="bold">R or green flag</text>
      <path d="M124 421 C270 450 278 95 127 100" fill="none" stroke="#c93d32" stroke-width="3" stroke-dasharray="7 6" marker-end="url(#arrow)"/>
    </g>
    <text x="75" y="615" font-family="Arial,sans-serif" font-size="18" fill="#20201d">Collision priority note: safety is checked only when the Player is NOT touching the pigeon.</text>
  `, [0, 0, 960, 700], "Escape from the Giant Pigeon — project system sketch", "Inventor notebook diagram labelling A Player start, B Giant Pigeon start, C Safe Zone, D boundaries, E Panic meter, and F the READY, PLAYING, CAUGHT, SAFE state flow." );
}

function makeWav(durationSeconds, sampleFunction) {
  const sampleRate = 22050;
  const sampleCount = Math.floor(durationSeconds * sampleRate);
  const dataSize = sampleCount * 2;
  const buffer = Buffer.alloc(44 + dataSize);
  buffer.write("RIFF", 0);
  buffer.writeUInt32LE(36 + dataSize, 4);
  buffer.write("WAVEfmt ", 8);
  buffer.writeUInt32LE(16, 16);
  buffer.writeUInt16LE(1, 20);
  buffer.writeUInt16LE(1, 22);
  buffer.writeUInt32LE(sampleRate, 24);
  buffer.writeUInt32LE(sampleRate * 2, 28);
  buffer.writeUInt16LE(2, 32);
  buffer.writeUInt16LE(16, 34);
  buffer.write("data", 36);
  buffer.writeUInt32LE(dataSize, 40);
  for (let index = 0; index < sampleCount; index += 1) {
    const time = index / sampleRate;
    const attack = Math.min(1, time / 0.018);
    const release = Math.min(1, (durationSeconds - time) / 0.06);
    const envelope = Math.max(0, Math.min(attack, release));
    const sample = Math.max(-1, Math.min(1, sampleFunction(time, durationSeconds))) * envelope * 0.2;
    buffer.writeInt16LE(Math.round(sample * 32767), 44 + index * 2);
  }
  return buffer;
}

function makeSounds() {
  return {
    "start.wav": makeWav(0.34, (time) => {
      const note = time < 0.11 ? 392 : time < 0.22 ? 523.25 : 659.25;
      return Math.sin(2 * Math.PI * note * time) + 0.18 * Math.sin(4 * Math.PI * note * time);
    }),
    "caught.wav": makeWav(0.42, (time, duration) => {
      const frequency = 290 - 165 * (time / duration);
      return 0.75 * Math.sin(2 * Math.PI * frequency * time) + 0.25 * Math.sin(2 * Math.PI * 37 * time);
    }),
    "safe.wav": makeWav(0.5, (time) => {
      const gate = time < 0.16 ? [523.25] : time < 0.32 ? [523.25, 659.25] : [523.25, 659.25, 783.99];
      return gate.reduce((sum, frequency) => sum + Math.sin(2 * Math.PI * frequency * time) / gate.length, 0);
    })
  };
}

function renderScratchValue(value) {
  if (Object.hasOwn(value, "number")) return `(${value.number})`;
  if (Object.hasOwn(value, "text")) return `[${value.text}]`;
  if (Object.hasOwn(value, "variable")) return `(${value.variable})`;
  const binary = {
    operator_equals: "=",
    operator_gt: ">",
    operator_lt: "<",
    operator_add: "+",
    operator_subtract: "-",
    operator_multiply: "*",
    operator_divide: "/"
  };
  if (binary[value.op]) {
    const expression = `${renderScratchValue(value.left)} ${binary[value.op]} ${renderScratchValue(value.right)}`;
    return ["operator_equals", "operator_gt", "operator_lt"].includes(value.op) ? `<${expression}>` : `(${expression})`;
  }
  if (value.op === "operator_round") return `(round ${renderScratchValue(value.value)})`;
  if (value.op === "operator_not") return `<not ${renderScratchValue(value.value)}>`;
  if (value.op === "sensing_keypressed") return `<key [${value.key} v] pressed?>`;
  if (value.op === "sensing_touchingobject") return `<touching [${value.object} v]?>`;
  if (value.op === "sensing_distanceto") return `(distance to [${value.object} v])`;
  if (value.op === "sensing_timer") return `(timer)`;
  if (value.op === "motion_xposition") return `(x position)`;
  if (value.op === "motion_yposition") return `(y position)`;
  throw new Error(`No scratchblocks value renderer for ${JSON.stringify(value)}`);
}

function renderScratchNode(node) {
  const command = {
    event_whenflagclicked: "when green flag clicked",
    sensing_resettimer: "reset timer",
    looks_show: "show",
    looks_nextcostume: "next costume",
    sound_stopallsounds: "stop all sounds"
  };
  if (command[node.op]) return command[node.op];
  if (node.op === "event_whenkeypressed") return `when [${node.key} v] key pressed`;
  if (node.op === "event_whenbroadcastreceived") return `when I receive [${node.message} v]`;
  if (node.op === "event_broadcastandwait") return `broadcast [${node.message} v] and wait`;
  if (node.op === "event_broadcast") return `broadcast [${node.message} v]`;
  if (node.op === "data_setvariableto") return `set [${node.variable} v] to ${renderScratchValue(node.value)}`;
  if (node.op === "control_wait") return `wait ${renderScratchValue(node.duration)} seconds`;
  if (node.op === "motion_setrotationstyle") return `set rotation style [${node.style} v]`;
  if (node.op === "motion_gotoxy") return `go to x: ${renderScratchValue(node.xValue)} y: ${renderScratchValue(node.yValue)}`;
  if (node.op === "motion_pointindirection") return `point in direction ${renderScratchValue(node.direction)}`;
  if (node.op === "motion_pointtowards") return `point towards [${node.object} v]`;
  if (node.op === "motion_movesteps") return `move ${renderScratchValue(node.value)} steps`;
  if (node.op === "motion_changexby") return `change x by ${renderScratchValue(node.value)}`;
  if (node.op === "motion_changeyby") return `change y by ${renderScratchValue(node.value)}`;
  if (node.op === "motion_setx") return `set x to ${renderScratchValue(node.value)}`;
  if (node.op === "motion_sety") return `set y to ${renderScratchValue(node.value)}`;
  if (node.op === "looks_switchcostumeto") return `switch costume to [${node.costume} v]`;
  if (node.op === "looks_say") return `say ${renderScratchValue(node.message)}`;
  if (node.op === "sound_playuntildone") return `play sound [${node.sound} v] until done`;
  throw new Error(`No scratchblocks command renderer for ${node.op}`);
}

function renderScratchChain(nodes, depth = 0) {
  const lines = [];
  for (const node of nodes) {
    const indent = "    ".repeat(depth);
    if (node.op === "control_forever") {
      lines.push(`${indent}forever`);
      lines.push(renderScratchChain(node.body, depth + 1));
      lines.push(`${indent}end`);
    } else if (node.op === "control_if") {
      lines.push(`${indent}if ${renderScratchValue(node.condition)} then`);
      lines.push(renderScratchChain(node.body, depth + 1));
      lines.push(`${indent}end`);
    } else {
      lines.push(`${indent}${renderScratchNode(node)}`);
    }
  }
  return lines.filter((line) => line !== "").join("\n");
}

function verifyContentSources() {
  const ids = new Set();
  for (const script of spec.scripts) {
    if (ids.has(script.id)) throw new Error(`Duplicate script id: ${script.id}`);
    ids.add(script.id);
    const generated = renderScratchChain(script.blocks);
    if (generated !== script.source) {
      throw new Error(`Scratch source drift in ${script.id}\nEXPECTED:\n${generated}\nACTUAL:\n${script.source}`);
    }
  }
  for (const section of spec.code_sections) {
    for (const scriptId of section.script_ids) {
      if (!ids.has(scriptId)) throw new Error(`Unknown script ${scriptId} in ${section.title}`);
    }
  }
}

class BlockCompiler {
  constructor(targetName) {
    this.targetName = targetName;
    this.blocks = {};
    this.counter = 0;
  }

  nextId() {
    this.counter += 1;
    return `block_${this.targetName.toLowerCase().replace(/[^a-z0-9]+/g, "_")}_${String(this.counter).padStart(4, "0")}`;
  }

  addBlock(opcode, parent, options = {}) {
    const id = this.nextId();
    this.blocks[id] = {
      opcode,
      next: null,
      parent,
      inputs: {},
      fields: {},
      shadow: options.shadow || false,
      topLevel: options.topLevel || false
    };
    if (options.topLevel) {
      this.blocks[id].x = options.x;
      this.blocks[id].y = options.y;
    }
    return id;
  }

  menu(owner, opcode, field, value) {
    const id = this.addBlock(opcode, owner, {shadow: true});
    this.blocks[id].fields[field] = [value, null];
    return [1, id];
  }

  value(owner, value) {
    if (Object.hasOwn(value, "number")) return [1, [4, String(value.number)]];
    if (Object.hasOwn(value, "text")) return [1, [10, value.text]];
    if (Object.hasOwn(value, "variable")) {
      const variable = VARIABLES[value.variable];
      if (!variable) throw new Error(`Unknown variable ${value.variable}`);
      return [3, [12, value.variable, variable.id], [10, ""]];
    }
    const id = this.reporter(owner, value);
    return [2, id];
  }

  reporter(parent, node) {
    const id = this.addBlock(node.op, parent);
    const block = this.blocks[id];
    const binaryInputs = {
      operator_equals: ["OPERAND1", "OPERAND2"],
      operator_gt: ["OPERAND1", "OPERAND2"],
      operator_lt: ["OPERAND1", "OPERAND2"],
      operator_add: ["NUM1", "NUM2"],
      operator_subtract: ["NUM1", "NUM2"],
      operator_multiply: ["NUM1", "NUM2"],
      operator_divide: ["NUM1", "NUM2"]
    };
    if (binaryInputs[node.op]) {
      block.inputs[binaryInputs[node.op][0]] = this.value(id, node.left);
      block.inputs[binaryInputs[node.op][1]] = this.value(id, node.right);
    } else if (node.op === "operator_round") {
      block.inputs.NUM = this.value(id, node.value);
    } else if (node.op === "operator_not") {
      block.inputs.OPERAND = this.value(id, node.value);
    } else if (node.op === "sensing_keypressed") {
      block.inputs.KEY_OPTION = this.menu(id, "sensing_keyoptions", "KEY_OPTION", node.key);
    } else if (node.op === "sensing_touchingobject") {
      block.inputs.TOUCHINGOBJECTMENU = this.menu(id, "sensing_touchingobjectmenu", "TOUCHINGOBJECTMENU", node.object);
    } else if (node.op === "sensing_distanceto") {
      block.inputs.DISTANCETOMENU = this.menu(id, "sensing_distancetomenu", "DISTANCETOMENU", node.object);
    } else if (!["sensing_timer", "motion_xposition", "motion_yposition"].includes(node.op)) {
      throw new Error(`No reporter compiler for ${node.op}`);
    }
    return id;
  }

  compileChain(nodes, parent = null, topLevel = null) {
    let previous = null;
    let first = null;
    for (const node of nodes) {
      const blockParent = previous || parent;
      const id = this.compileNode(node, blockParent, first === null ? topLevel : null);
      if (previous) this.blocks[previous].next = id;
      if (!first) first = id;
      previous = id;
    }
    return first;
  }

  compileNode(node, parent, topLevel) {
    const id = this.addBlock(node.op, parent, topLevel ? {topLevel: true, x: topLevel.x, y: topLevel.y} : {});
    const block = this.blocks[id];
    if (node.op === "event_whenkeypressed") {
      block.fields.KEY_OPTION = [node.key, null];
    } else if (node.op === "event_whenbroadcastreceived") {
      block.fields.BROADCAST_OPTION = [node.message, BROADCASTS[node.message]];
    } else if (["event_broadcast", "event_broadcastandwait"].includes(node.op)) {
      block.inputs.BROADCAST_INPUT = [1, [11, node.message, BROADCASTS[node.message]]];
    } else if (node.op === "data_setvariableto") {
      block.fields.VARIABLE = [node.variable, VARIABLES[node.variable].id];
      block.inputs.VALUE = this.value(id, node.value);
    } else if (node.op === "control_wait") {
      block.inputs.DURATION = this.value(id, node.duration);
    } else if (node.op === "control_forever") {
      const body = this.compileChain(node.body, id);
      if (body) block.inputs.SUBSTACK = [2, body];
    } else if (node.op === "control_if") {
      block.inputs.CONDITION = this.value(id, node.condition);
      const body = this.compileChain(node.body, id);
      if (body) block.inputs.SUBSTACK = [2, body];
    } else if (node.op === "motion_setrotationstyle") {
      block.fields.STYLE = [node.style, null];
    } else if (node.op === "motion_gotoxy") {
      block.inputs.X = this.value(id, node.xValue);
      block.inputs.Y = this.value(id, node.yValue);
    } else if (node.op === "motion_pointindirection") {
      block.inputs.DIRECTION = this.value(id, node.direction);
    } else if (node.op === "motion_pointtowards") {
      block.inputs.TOWARDS = this.menu(id, "motion_pointtowards_menu", "TOWARDS", node.object);
    } else if (node.op === "motion_movesteps") {
      block.inputs.STEPS = this.value(id, node.value);
    } else if (node.op === "motion_changexby") {
      block.inputs.DX = this.value(id, node.value);
    } else if (node.op === "motion_changeyby") {
      block.inputs.DY = this.value(id, node.value);
    } else if (node.op === "motion_setx") {
      block.inputs.X = this.value(id, node.value);
    } else if (node.op === "motion_sety") {
      block.inputs.Y = this.value(id, node.value);
    } else if (node.op === "looks_switchcostumeto") {
      block.inputs.COSTUME = this.menu(id, "looks_costume", "COSTUME", node.costume);
    } else if (node.op === "looks_say") {
      block.inputs.MESSAGE = this.value(id, node.message);
    } else if (node.op === "sound_playuntildone") {
      block.inputs.SOUND_MENU = this.menu(id, "sound_sounds_menu", "SOUND_MENU", node.sound);
    } else if (!["event_whenflagclicked", "sensing_resettimer", "looks_show", "looks_nextcostume", "sound_stopallsounds"].includes(node.op)) {
      throw new Error(`No command compiler for ${node.op}`);
    }
    return id;
  }
}

function mediaAsset(name, content, dataFormat, rotationCenterX, rotationCenterY, extra = {}) {
  const buffer = Buffer.isBuffer(content) ? content : Buffer.from(content, "utf8");
  const assetId = md5(buffer);
  return {
    sourceName: name,
    buffer,
    projectRecord: {
      assetId,
      name: extra.costumeName || path.basename(name, path.extname(name)),
      bitmapResolution: 1,
      md5ext: `${assetId}.${dataFormat}`,
      dataFormat,
      rotationCenterX,
      rotationCenterY
    }
  };
}

function soundAsset(name, content, soundName) {
  const buffer = Buffer.from(content);
  const assetId = md5(buffer);
  return {
    sourceName: name,
    buffer,
    projectRecord: {
      assetId,
      name: soundName,
      dataFormat: "wav",
      format: "",
      rate: 22050,
      sampleCount: (buffer.length - 44) / 2,
      md5ext: `${assetId}.wav`
    }
  };
}

function makeTarget(name, isStage, costumes, sounds, options, scripts) {
  const compiler = new BlockCompiler(name);
  for (const script of scripts) compiler.compileChain(script.blocks, null, {x: script.x, y: script.y});
  const target = {
    isStage,
    name,
    variables: isStage ? Object.fromEntries(Object.entries(VARIABLES).map(([variableName, variable]) => [variable.id, [variableName, variable.initial]])) : {},
    lists: {},
    broadcasts: isStage ? Object.fromEntries(Object.entries(BROADCASTS).map(([broadcastName, broadcastId]) => [broadcastId, broadcastName])) : {},
    blocks: compiler.blocks,
    comments: {
      [`comment_${name.toLowerCase().replace(/[^a-z0-9]+/g, "_")}`]: {
        blockId: null,
        x: 20,
        y: 20,
        width: 310,
        height: 105,
        minimized: false,
        text: options.comment
      }
    },
    currentCostume: 0,
    costumes: costumes.map((asset) => asset.projectRecord),
    sounds: sounds.map((asset) => asset.projectRecord),
    volume: 85,
    layerOrder: options.layerOrder || 0
  };
  if (isStage) {
    Object.assign(target, {tempo: 60, videoTransparency: 50, videoState: "on", textToSpeechLanguage: null});
  } else {
    Object.assign(target, {
      visible: true,
      x: options.x,
      y: options.y,
      size: options.size || 100,
      direction: options.direction || 90,
      draggable: false,
      rotationStyle: options.rotationStyle || "all around"
    });
  }
  return target;
}

function variableMonitor(variableName, x, y, visible = true) {
  const variable = VARIABLES[variableName];
  return {
    id: variable.id,
    mode: "default",
    opcode: "data_variable",
    params: {VARIABLE: variableName},
    spriteName: null,
    value: variable.initial,
    width: 0,
    height: 0,
    x,
    y,
    visible,
    sliderMin: 0,
    sliderMax: 100,
    isDiscrete: true
  };
}

function makeProject(kind, svgAssets, sounds) {
  const finished = kind === "finished";
  const selectedScripts = spec.scripts.filter((script) => finished || script.starter);
  const stageCostumes = [mediaAsset("stage-backdrop.svg", svgAssets["stage-backdrop.svg"], "svg", 240, 180, {costumeName: "Pigeon Chase Map"})];
  const playerCostumes = [
    mediaAsset("player.svg", svgAssets["player.svg"], "svg", 35, 45, {costumeName: "normal"}),
    mediaAsset("player-caught.svg", svgAssets["player-caught.svg"], "svg", 35, 45, {costumeName: "caught"})
  ];
  const pigeonCostumes = [
    mediaAsset("giant-pigeon.svg", svgAssets["giant-pigeon.svg"], "svg", 75, 55, {costumeName: "wings up"}),
    mediaAsset("giant-pigeon-wings-down.svg", svgAssets["giant-pigeon-wings-down.svg"], "svg", 75, 55, {costumeName: "wings down"})
  ];
  const safeCostumes = [
    mediaAsset("safe-zone.svg", svgAssets["safe-zone.svg"], "svg", 45, 52.5, {costumeName: "inactive"}),
    mediaAsset("safe-zone-active.svg", svgAssets["safe-zone-active.svg"], "svg", 45, 52.5, {costumeName: "active"})
  ];
  const stageSounds = [soundAsset("start.wav", sounds["start.wav"], "start")];
  const playerSounds = [soundAsset("caught.wav", sounds["caught.wav"], "caught")];
  const safeSounds = [soundAsset("safe.wav", sounds["safe.wav"], "safe")];
  const targetScripts = (targetName) => selectedScripts.filter((script) => script.target === targetName);
  const starterInstructions = "STARTER: Original media and setup are ready. Build movement, boundaries, chase, collision, panic, endings, and R restart using the guide. Sprite names and costume centres already match the reference.";
  const finishedInstructions = "FINISHED REFERENCE: Generated from the same structured Scratch scripts rendered on the School of Code project page. Green flag or R performs a complete reset.";
  const project = {
    targets: [
      makeTarget("Stage", true, stageCostumes, stageSounds, {layerOrder: 0, comment: finished ? finishedInstructions : starterInstructions}, targetScripts("Stage")),
      makeTarget("Safe Zone", false, safeCostumes, safeSounds, {x: 190, y: -115, size: 84, direction: 90, rotationStyle: "don't rotate", layerOrder: 1, comment: "Safe Zone: inactive while READY/PLAYING; active only after Reached Safety."}, targetScripts("Safe Zone")),
      makeTarget("Giant Pigeon", false, pigeonCostumes, [], {x: 155, y: 100, size: 112, direction: -90, rotationStyle: "all around", layerOrder: 2, comment: "Giant Pigeon: reset far away, then point toward Player and move by Pigeon Speed only during PLAYING."}, targetScripts("Giant Pigeon")),
      makeTarget("Player", false, playerCostumes, playerSounds, {x: -190, y: -110, size: 72, direction: 90, rotationStyle: "left-right", layerOrder: 3, comment: "Player: arrow keys change x/y. CAUGHT has priority when pigeon and shelter contacts look simultaneous."}, targetScripts("Player"))
    ],
    monitors: [
      variableMonitor("Game State", 5, 5),
      variableMonitor("Panic", 5, 34),
      variableMonitor("Survival Time", 5, 63),
      variableMonitor("Pigeon Speed", 5, 92, false)
    ],
    extensions: [],
    meta: {
      semver: "3.0.0",
      vm: VM_VERSION,
      agent: "School of Code deterministic Scratch builder 1.0.0"
    }
  };
  const allMedia = [...stageCostumes, ...playerCostumes, ...pigeonCostumes, ...safeCostumes, ...stageSounds, ...playerSounds, ...safeSounds];
  return {project, allMedia};
}

async function zipProject(projectBundle) {
  const zip = new JSZip();
  zip.file("project.json", `${JSON.stringify(projectBundle.project)}\n`, {date: FIXED_DATE});
  const uniqueMedia = new Map();
  for (const asset of projectBundle.allMedia) uniqueMedia.set(asset.projectRecord.md5ext, asset.buffer);
  for (const filename of [...uniqueMedia.keys()].sort()) {
    zip.file(filename, uniqueMedia.get(filename), {binary: true, date: FIXED_DATE});
  }
  return zip.generateAsync({type: "nodebuffer", compression: "DEFLATE", compressionOptions: {level: 9}, platform: "UNIX"});
}

const ROOT_README = normalized(`
ESCAPE FROM THE GIANT PIGEON — SCRATCH PRODUCTION PILOT

This directory is generated by tools/scratch/build-giant-pigeon.js.

Files
-----
- escape-from-the-giant-pigeon-starter.sb3: setup, media, variables, positions,
  and short in-editor instructions; students still build the game systems.
- escape-from-the-giant-pigeon-finished.sb3: complete playable reference.
- escape-from-the-giant-pigeon-assets.zip: readable original source media.
- assets/: the readable SVG and WAV source files used by the packages.
- project-sketch.svg: responsive system sketch used by the project page.

Sprite and costume mapping
--------------------------
Player: player.svg (normal), player-caught.svg (caught); centre 35, 45.
Giant Pigeon: giant-pigeon.svg (wings up), giant-pigeon-wings-down.svg
(wings down); centre 75, 55.
Safe Zone: safe-zone.svg (inactive), safe-zone-active.svg (active); centre 45,
52.5.
Stage: stage-backdrop.svg (Pigeon Chase Map); centre 240, 180.

Sound mapping
-------------
Stage: start.wav. Player: caught.wav. Safe Zone: safe.wav.

Students may redraw, repaint, rename, or replace every original asset. If a
sprite or costume name changes, update any matching Scratch dropdowns. Preserve
the suggested costume centres when swapping equivalent-size SVGs.

Regenerate and validate
-----------------------
cd tools/scratch
npm ci
npm run build
npm run validate

The builder reads the structured scripts in
sites/shkolakoda/scratch_projects/escape-from-the-giant-pigeon.json. It refuses
to build if the editable scratchblocks text disagrees with the shared block AST.
The validator checks archives, hashes, media, scripts, and loads both projects
through the pinned official Scratch VM.

Manual release gate
-------------------
After automated validation, open both SB3 files once in the graphical Scratch
editor. Confirm the starter opens as incomplete and the finished reference can
win, be caught, and restart with R. This graphical check remains required before
public deployment.
`);

const LICENSES = normalized(`
ESCAPE FROM THE GIANT PIGEON — LICENCE AND ATTRIBUTION

Original project content
------------------------
The Player, Giant Pigeon, Safe Zone, backdrop, project sketch, WAV effects,
Scratch scripts, and written project instructions were created for School of
Code in 2026. They contain no copied Scratch characters, library media,
screenshots, protected logos, or external project layouts.

These original educational materials are licensed under the Creative Commons
Attribution 4.0 International licence (CC BY 4.0):
https://creativecommons.org/licenses/by/4.0/

Scratch clarity
---------------
Scratch is a project of the Scratch Foundation. School of Code is an independent
educational project and is not affiliated with or endorsed by the Scratch
Foundation. Scratch names are used only to identify the programming language,
editor, and project format.

Tooling
-------
scratchblocks 3.7.1 is self-hosted separately under its MIT licence. See
sites/shkolakoda/static/vendor/scratchblocks/LICENSE.txt.
The official Scratch VM is a pinned development/validation dependency and is not
shipped as a website runtime dependency.
`);

async function makeAssetPack(svgAssets, sounds, projectSketch) {
  const zip = new JSZip();
  zip.file("assets/", null, {dir: true, date: FIXED_DATE});
  zip.file("README.txt", ROOT_README, {date: FIXED_DATE});
  zip.file("LICENSES.txt", LICENSES, {date: FIXED_DATE});
  zip.file("project-sketch.svg", projectSketch, {date: FIXED_DATE});
  for (const filename of Object.keys(svgAssets).sort()) zip.file(`assets/${filename}`, svgAssets[filename], {date: FIXED_DATE});
  for (const filename of Object.keys(sounds).sort()) zip.file(`assets/${filename}`, sounds[filename], {binary: true, date: FIXED_DATE});
  return zip.generateAsync({type: "nodebuffer", compression: "DEFLATE", compressionOptions: {level: 9}, platform: "UNIX"});
}

function installScratchblocksVendor() {
  const packageRoot = path.join(__dirname, "node_modules/scratchblocks");
  const source = path.join(packageRoot, "build/scratchblocks.min.js");
  const license = path.join(packageRoot, "LICENSE");
  fs.copyFileSync(source, path.join(VENDOR_ROOT, `scratchblocks-${SCRATCHBLOCKS_VERSION}.min.js`));
  fs.copyFileSync(license, path.join(VENDOR_ROOT, "LICENSE.txt"));
  fs.writeFileSync(path.join(VENDOR_ROOT, "VERSION.txt"), normalized(`scratchblocks ${SCRATCHBLOCKS_VERSION}\nSource: https://github.com/scratchblocks/scratchblocks\nLicence: MIT (see LICENSE.txt)`));
}

async function main() {
  ensureDirectories();
  verifyContentSources();
  const svgAssets = makeSvgAssets();
  const sounds = makeSounds();
  const projectSketch = makeProjectSketch();
  for (const [filename, content] of Object.entries(svgAssets)) fs.writeFileSync(path.join(ASSET_ROOT, filename), content);
  for (const [filename, content] of Object.entries(sounds)) fs.writeFileSync(path.join(ASSET_ROOT, filename), content);
  fs.writeFileSync(path.join(OUTPUT_ROOT, "project-sketch.svg"), projectSketch);
  fs.writeFileSync(path.join(OUTPUT_ROOT, "README.txt"), ROOT_README);
  fs.writeFileSync(path.join(OUTPUT_ROOT, "LICENSES.txt"), LICENSES);
  const starter = await zipProject(makeProject("starter", svgAssets, sounds));
  const finished = await zipProject(makeProject("finished", svgAssets, sounds));
  const assetPack = await makeAssetPack(svgAssets, sounds, projectSketch);
  fs.writeFileSync(path.join(OUTPUT_ROOT, "escape-from-the-giant-pigeon-starter.sb3"), starter);
  fs.writeFileSync(path.join(OUTPUT_ROOT, "escape-from-the-giant-pigeon-finished.sb3"), finished);
  fs.writeFileSync(path.join(OUTPUT_ROOT, "escape-from-the-giant-pigeon-assets.zip"), assetPack);
  installScratchblocksVendor();
  console.log(`Built Giant Pigeon starter (${starter.length} bytes), finished (${finished.length} bytes), and assets (${assetPack.length} bytes).`);
  console.log(`Verified ${spec.scripts.length} shared scratchblocks sources before packaging.`);
}

if (require.main === module) {
  main().catch((error) => {
    console.error(error.stack || error);
    process.exitCode = 1;
  });
}

module.exports = {renderScratchChain};
