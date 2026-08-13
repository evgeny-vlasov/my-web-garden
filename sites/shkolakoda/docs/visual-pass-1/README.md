# SoCCL Visual Integration Pass 1

This directory records the visual review evidence for the first integration
pass and its post-editorial refresh.

captured commit: `1c9850525fcf9b370f4d6dfaf38160371833ccc8`

capture date: 2026-08-13 UTC

The captured commit is the exact public website revision rendered in every
current `after-*` website image. The subsequent visual-QA fix changes the
Story master, its export helper, tests, documentation, and this evidence only;
it does not change the rendered website, CSS, or public copy. The Story preview
was generated from the guide-free production SVG created by that fix.

The five `before-*` files are intentionally retained as historical baseline
evidence from `7ac4146b348871a050d4d761e9d52db2df7ed807`. The original July
`after-*` files from `c153987cd12acff38166b45d2c85a968fb5b3a7d` were replaced
because their text and wrapping predated the editorial rewrite.

## Capture method

- local server: one temporary Gunicorn worker bound to `127.0.0.1:8765`;
- browser: Playwright 1.54.2 with Chromium 139.0.7258.5, headless;
- device scale: 1×;
- colour: light mode with Chromium's sRGB output;
- stability: `networkidle`, `document.fonts.ready`, reduced motion, and CSS
  animation/transition suppression;
- checks: HTTP 200, no console errors, no failed requests, and no horizontal
  overflow at each website viewport;
- script: `capture.js`, using named section selectors for scrolled evidence;
- format: JPEG at quality 88 for website captures and 92 for the committed
  Story preview; full production verification uses lossless PNG.

The Story workflow first removes the `editor-guide` layer, then captures only
the production SVG:

```bash
cd sites/shkolakoda
venv/bin/python brand/export_story.py /tmp/soccl-story-production.svg
SOCCL_CAPTURE_BASE_URL=http://127.0.0.1:8765 \
SOCCL_STORY_SVG=/tmp/soccl-story-production.svg \
node docs/visual-pass-1/capture.js
```

Playwright must be available to Node (locally or through `NODE_PATH`). The
capture script never uses the editable Story master as its raster source.

## Viewports

Primary comparison sizes:

- desktop: 1440 × 1100;
- tablet: 768 × 1024;
- mobile: 390 × 844;
- Story preview: 540 × 960, representing the 1080 × 1920 SVG at 50%.

Top-of-page captures use 1440 × 1100, 768 × 1024, or 390 × 844 as indicated by
their desktop, tablet, and mobile names. Desktop component captures use
1440 × 1000. Mobile component and menu captures use 390 × 844. The scrolled
captures cover project and article cards, homepage transitions, both mascot
placements, the mobile menu, program navigation, and topic navigation.

Browser QA found no horizontal overflow, console errors, failed requests, or
non-200 pages at the tested sizes. Existing automated tests separately check
broken images, image alternatives, and intrinsic image dimensions.

No private reference photography appears in these captures or in the pass.
