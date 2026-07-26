# SoCCL Visual Integration Pass 1

This directory records the visual review evidence for the first integration
pass. The `before-*` captures are from the unchanged `main` baseline at
`7ac4146b348871a050d4d761e9d52db2df7ed807`; the `after-*` captures are from
this branch. All captures use Chromium at 1× device scale.

Primary comparison sizes:

- desktop: 1440 × 1100;
- tablet: 768 × 1024;
- mobile: 390 × 844;
- Story preview: 540 × 960, representing the 1080 × 1920 SVG at 50%.

The scrolled component captures cover project and article cards, homepage
transitions, both mascot placements, the mobile menu, program navigation, and
topic navigation. Browser QA found no horizontal overflow, broken images,
missing image alternatives, missing intrinsic image dimensions, console
errors, or failed asset requests at the tested sizes.

No private reference photography appears in these captures or in the pass.
