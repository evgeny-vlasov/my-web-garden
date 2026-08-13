#!/usr/bin/env node
"use strict";

const path = require("path");
const { chromium } = require("playwright");

const baseUrl = process.env.SOCCL_CAPTURE_BASE_URL || "http://127.0.0.1:8765";
const storySvg = process.env.SOCCL_STORY_SVG;
const outputDir = __dirname;

if (!storySvg) {
  throw new Error("SOCCL_STORY_SVG must point to the guide-free production SVG");
}

const captures = [
  ["after-home-desktop.jpg", "/", 1440, 1100],
  ["after-home-tablet.jpg", "/", 768, 1024],
  ["after-home-mobile.jpg", "/", 390, 844],
  ["after-home-components-desktop.jpg", "/", 1440, 1000, ".verb-grid", 96],
  ["after-home-programs-desktop.jpg", "/", 1440, 1000, ".program-grid-active", 96],
  ["after-home-mascot-note-desktop.jpg", "/", 1440, 1000, ".school-lab-grid", 96],
  ["after-home-board-mobile.jpg", "/", 390, 844, ".build-board", 82],
  ["after-home-mobile-menu.jpg", "/", 390, 844, null, 0, true],
  ["after-programs-tablet.jpg", "/programs", 768, 1024],
  ["after-projects-desktop.jpg", "/projects", 1440, 1100],
  ["after-projects-mobile.jpg", "/projects", 390, 844],
  ["after-project-cards-desktop.jpg", "/projects", 1440, 1000, "#scratch-projects .project-grid", 96],
  ["after-project-card-mobile.jpg", "/projects", 390, 844, "#scratch-projects .project-grid", 82],
  ["after-topics-mobile.jpg", "/topics", 390, 844],
  ["after-blog-desktop.jpg", "/blog", 1440, 1100],
  ["after-blog-mobile.jpg", "/blog", 390, 844],
  ["after-blog-cards-desktop.jpg", "/blog", 1440, 1000, "#coding-for-kids .blog-grid", 96],
  ["after-blog-card-mobile.jpg", "/blog", 390, 844, "#coding-for-kids .blog-grid", 82],
];

async function settle(page, injectStyle = true) {
  await page.evaluate(() => document.fonts.ready);
  if (injectStyle) {
    await page.addStyleTag({
      content: "*,*::before,*::after{animation:none!important;transition:none!important;caret-color:transparent!important}",
    });
  }
}

async function capturePage(browser, definition) {
  const [filename, route, width, height, selector, offset = 0, openMenu = false] = definition;
  const context = await browser.newContext({
    viewport: { width, height },
    deviceScaleFactor: 1,
    colorScheme: "light",
    reducedMotion: "reduce",
  });
  const page = await context.newPage();
  const failures = [];
  page.on("console", (message) => {
    if (message.type() === "error") failures.push(`console: ${message.text()}`);
  });
  page.on("requestfailed", (request) => {
    failures.push(`request: ${request.url()} (${request.failure()?.errorText || "failed"})`);
  });
  const response = await page.goto(`${baseUrl}${route}`, { waitUntil: "networkidle" });
  if (!response || response.status() !== 200) {
    failures.push(`HTTP ${response ? response.status() : "none"} for ${route}`);
  }
  await settle(page);
  if (openMenu) {
    await page.locator("details.mobile-nav").evaluate((element) => { element.open = true; });
  }
  if (selector) {
    const target = page.locator(selector).first();
    await target.waitFor({ state: "visible" });
    await target.evaluate((element, topOffset) => {
      const top = element.getBoundingClientRect().top + window.scrollY - topOffset;
      window.scrollTo(0, Math.max(0, top));
    }, offset);
  } else {
    await page.evaluate(() => window.scrollTo(0, 0));
  }
  await page.waitForTimeout(120);
  const overflow = await page.evaluate(() => ({
    viewport: document.documentElement.clientWidth,
    content: document.documentElement.scrollWidth,
  }));
  if (overflow.content > overflow.viewport) {
    failures.push(`horizontal overflow ${overflow.content} > ${overflow.viewport}`);
  }
  await page.screenshot({
    path: path.join(outputDir, filename),
    type: "jpeg",
    quality: 88,
    animations: "disabled",
  });
  await context.close();
  if (failures.length) throw new Error(`${filename}: ${failures.join("; ")}`);
  process.stdout.write(`captured ${filename} (${width}x${height})\n`);
}

async function captureStory(browser, filename, width, height) {
  const context = await browser.newContext({
    viewport: { width, height },
    deviceScaleFactor: 1,
    colorScheme: "light",
  });
  const page = await context.newPage();
  await page.goto(`file://${path.resolve(storySvg)}`, { waitUntil: "load" });
  await settle(page, false);
  const destination = path.isAbsolute(filename) ? filename : path.join(outputDir, filename);
  const screenshot = {
    path: destination,
    animations: "disabled",
  };
  if (/\.jpe?g$/i.test(destination)) {
    screenshot.type = "jpeg";
    screenshot.quality = 92;
  } else if (/\.png$/i.test(destination)) {
    screenshot.type = "png";
  } else {
    throw new Error(`Story output must use .jpg, .jpeg, or .png: ${destination}`);
  }
  await page.screenshot(screenshot);
  await context.close();
  process.stdout.write(`captured ${filename} (${width}x${height})\n`);
}

(async () => {
  const browser = await chromium.launch({ headless: true });
  try {
    if (process.env.SOCCL_STORY_ONLY !== "1") {
      for (const definition of captures) await capturePage(browser, definition);
    }
    await captureStory(browser, "after-story-template.jpg", 540, 960);
    if (process.env.SOCCL_STORY_FULL_EXPORT) {
      await captureStory(browser, path.resolve(process.env.SOCCL_STORY_FULL_EXPORT), 1080, 1920);
    }
    if (process.env.SOCCL_STORY_PHONE_EXPORT) {
      await captureStory(browser, path.resolve(process.env.SOCCL_STORY_PHONE_EXPORT), 390, 693);
    }
  } finally {
    await browser.close();
  }
})().catch((error) => {
  console.error(error);
  process.exit(1);
});
