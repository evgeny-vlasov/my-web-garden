# School of Code Computer Lab Brand System v0.1

Status: working brand standard for the approved public website direction.

This system formalizes what already exists at `shkolakoda.com`. It does not
replace the website’s visual language, introduce a second token set, or turn
the robot mascot into a new institutional logo.

## Brand position

School of Code is a small independent Calgary school for practical
programming, game design, and robotics. Computer Lab is its guided project
mode: a place to build, test, explain, and improve real systems.

The public name is **School of Code Computer Lab**. Use **School of Code** when
the shorter master-brand name is sufficient. `<SC/>` is a compact visual mark,
not the written name. Do not use “Shkola Coda” or “SHKOLA CODA” as the primary
public wordmark.

The brand should feel:

- curious, exact, and hands-on;
- editorial rather than corporate;
- technically literate without performing complexity;
- inventive, warm, and calm;
- honest about what exists now and what is planned.

It should not feel like a generic coding franchise, an esports team, a toy
catalogue, or a futuristic “Matrix” interface.

## Source of truth and asset map

The website remains the source of truth for the design tokens and component
language:

- tokens and components: `static/css/styles.css`;
- live favicon: `static/favicon.svg`;
- canonical logo masters: `static/brand/logos/`;
- mascot derivatives: `static/brand/mascot/`;
- reusable composition templates: `static/brand/templates/`;
- approved campaign and documentary masters: `brand/photo-masters/`;
- responsive web photographs: `static/brand/photos/`;
- upload-ready social exports and guidance: `brand/social/`;
- machine-readable photo inventory: `brand/photo-asset-manifest.json`;
- exact campaign prompts: `brand/CAMPAIGN_PROMPTS.md`;
- designer-source technical audit: `brand/DESIGNER_ASSET_AUDIT.md`;
- private-safe archive review: `brand/PHOTO_MANIFEST.md`.

The values below mirror the existing CSS variables. If the website tokens
change later, update this document and the standalone SVG masters together.

## Photographic production standard

The owner confirms that all 81 source photographs in the private intake are authorized for editing and dramatic reconstruction, identifiable adult and child use, website and social publication, paid advertising, compositing, and reference-based generation. Private release evidence, names, GPS data, raw metadata, the uploaded archive and review contact sheets remain outside Git.

Published imagery has two explicit classes:

- **reconstructed campaign image:** a deliberately composed scene grounded in authorized real School of Code people, machines and activity references. It may reconstruct a room or background, but must not invent a large permanent facility, equipment, class or claim that does not exist. It must not be captioned as a literal current class photograph.
- **Historical workshop photograph:** a truthful derivative of one source event. Exposure, colour, crop, screen simplification, cleanup and brand removal are permitted; people and activity are not replaced or invented. It must not be described as a current Calgary cohort or current facility.

The approved campaign family is `campaign-robotics-hero-v1.png`, `campaign-scratch-lab-v1.png`, `campaign-eugene-builder-v1.png`, and `campaign-project-workbench-v1.png`. Website pages reference only tracked derivatives under `static/brand/photos/`, never `.photo-review` or private intake files.

Every public raster must be sRGB and verified without EXIF, GPS, XMP, comments or embedded thumbnails. Keep photographic masters text-free. Add only canonical repository logos in deterministic delivery compositions; never regenerate or approximate a logo.

## Institutional logo system

The institutional system has two source marks:

1. `</>` — the smallest, most reduced mark and favicon.
2. `<SC/>` — the compact badge used in the website header.

The public wordmarks combine `<SC/>` with the written name. The robot is a
mascot, not a replacement for either source mark.

### Hierarchy and responsive variants

| Context | Asset | Rule |
| --- | --- | --- |
| Browser favicon, 16–32 px | `logos/favicon.svg` | Use `</>` only. Never add letters. |
| Mobile header | `logos/compact-badge.svg` | Use at the existing 44 × 38 CSS px. |
| Desktop header | `logos/compact-badge.svg` | Use at the existing 50 × 42 CSS px. |
| Complete horizontal use | `logos/wordmark-horizontal.svg` | Use at 540 px / 120 mm wide or larger so the descriptor remains readable. |
| Reduced horizontal use | `logos/wordmark-horizontal-reduced.svg` | Descriptor-free responsive lockup for 240–539 px screen use or 45–119 mm print use. |
| Narrow or centred use | `logos/wordmark-stacked.svg` | Use where a horizontal lockup would be cramped. |
| One-colour production | `*-mono.svg` | One dark ink on a light substrate. |
| Dark field | `*-reversed.svg` | Use the supplied reversed master; do not invert ad hoc. |
| Institutional avatar fallback | `logos/social-avatar.svg` | Use when an account must be represented by a logo rather than the mascot. |
| Social account avatar | `mascot/robot-avatar-500.png` | Preferred where the account name appears beside it; see mascot rules. |
| Facebook Page cover | `logos/facebook-cover.svg` | Logo and mascot remain visibly separate. |

The reduced horizontal variant is a responsive lockup, not a shortened public
name. Use it only where the surrounding page, account name, or adjacent copy
identifies School of Code Computer Lab in full.

The current photographic Facebook Page cover is exported at 1920 × 800. The
older `logos/facebook-cover.svg` remains a code-native identity fallback, not
the photographic production master. Facebook may crop or resize covers and
may partially cover the left side with the profile image, so all important
content is kept in the central desktop/mobile intersection. Recheck the
[current Page cover guidance](https://www.facebook.com/help/125379114252045/)
before publishing.

### Clear space, scale, and placement

- Let `u` equal one quarter of the compact badge height. Keep at least `u` of
  clear space around a logo lockup.
- Keep the complete horizontal wordmark at least 540 px wide on screen. At
  that size its 16-unit descriptor is 12 CSS px.
- Keep the complete horizontal wordmark at least 120 mm wide in print. At that
  size its descriptor is approximately 7.6 pt.
- From 240–539 px on screen or 45–119 mm in print, use the descriptor-free
  reduced horizontal wordmark. Its name is approximately 21 px at the 240 px
  screen minimum and 11 pt at the 45 mm print minimum.
- Below 240 px on screen or 45 mm in print, switch to the compact badge rather
  than shrinking either wordmark.
- Keep the compact badge at 44 px wide or larger on screen.
- Keep the favicon geometry unchanged at 16 px.
- The approved badge rotation is approximately −2°. Do not increase it or
  rotate every object in a composition.
- Align a wordmark to a real layout edge, grid line, or text column. A small
  optical offset is welcome; accidental misalignment is not.

### Logo do / don’t

| Do | Don’t |
| --- | --- |
| Use `</>` when space is truly small. | Squeeze “School of Code” into a favicon. |
| Use `<SC/>` in the site header and compact navigation. | Replace `<SC/>` with the robot. |
| Use the full written name in public-facing lockups. | Publish “SHKOLA CODA” as the main wordmark. |
| Use the reduced horizontal wordmark when the complete descriptor would be too small. | Delete the descriptor ad hoc or shrink the complete wordmark below its minimum. |
| Use the supplied mono or reversed master. | Apply gradients, glows, bevels, or Matrix effects. |
| Preserve clear space and proportions. | Stretch, skew, outline twice, or crop through the mark. |
| Let one mark identify the composition. | Repeat the favicon, badge, wordmark, and mascot as four competing logos. |

## Colour

### Existing core tokens

| Token | Value | Primary role |
| --- | --- | --- |
| Ink | `#151515` | Text, borders, axes, dark fields |
| Paper | `#fffef8` | Default page and editorial background |
| White | `#ffffff` | Cards and high-clarity reverse areas |
| Muted | `#5c5c57` | Secondary body copy |
| Line | `#d8d6ca` | Rules and card borders |
| Soft line | `#ebe9de` | Graph grids and quiet divisions |
| Yellow | `#f4c542` | Primary signal, focus, offset shadow |
| Yellow soft | `#fff4bd` | Large section field |
| Green | `#147d64` | Instructional emphasis and progress |
| Green soft | `#e2f4ed` | Large instructional field |
| Blue | `#2257b5` | Links, information, coordinates |
| Blue soft | `#e9effb` | Large information field |
| Red | `#c93d32` | Warnings and mistakes, used sparingly |
| Red soft | `#fde9e5` | Warning field |
| Violet | `#6946a4` | A fourth data series or occasional project accent |

Yellow is the primary brand signal, not a body-text colour. Green is the
default instructional accent. Blue remains the functional link colour. Red
communicates a warning, error, or deliberate contrast; do not use it simply to
make a layout louder. Violet is supporting colour, not a second primary.

Do not distribute yellow, green, blue, red, and violet equally in every
composition. A useful default is paper + ink + yellow, with one supporting
colour.

### Mascot colours

The supplied mascot is identified by the combination below. Raster masters
contain shading, so these are redraw anchors rather than instructions to
posterize the existing art.

| Feature | Redraw anchor | Rule |
| --- | --- | --- |
| Yellow circular field | Brand yellow `#f4c542` | Future redraws should use the site yellow; do not sample a new neon yellow. |
| Helmet and blue panels | Cyan `#50c0f0` | Keep a bright cyan family with darker blue modelling. |
| Face plate and joints | Orange `#ff8c3f` | Orange is an identifying mascot colour, not a new site-wide UI token. |
| Deep mechanical shade | Navy `#0b1e3f` | Use for internal detail; institutional text still uses Ink. |
| Body shell | Warm off-white `#f4f2e6` | Avoid cold pure white over the whole robot. |
| Outline | Ink `#151515` | Preserve the bold dark contour at every usable size. |

Do not recolour the robot differently for each program. Future poses must keep
the cyan helmet, orange face plate, large dark eyes, warm white torso, circular
ear pieces, articulated orange/cyan arms, and bold ink contour.

## Typography

The typography is intentionally practical and system-based.

- Headlines: `Georgia, "Times New Roman", serif`.
- Body and interface: `"Aptos", "Segoe UI", Helvetica, Arial, sans-serif`.
- Technical labels: `"Courier New", ui-monospace, SFMono-Regular, Consolas, monospace`.

Use serif for meaningful display hierarchy, not every label. Use the sans
stack for readable explanation. Use monospace for coordinates, code, state,
metadata, project numbers, and short technical annotations—not for long body
paragraphs.

Keep the existing site proportions:

- headlines are compact, with line-height close to `1.08`;
- body copy is open, with line-height close to `1.65`;
- labels are small, bold, uppercase, and tracked;
- long reading columns stay near 65–75 characters.

Do not add a webfont merely to make the wordmark feel more “logo-like.” The
brand’s recognizability comes from the marks, hierarchy, colour, and layout.

## Graphic motifs

Use the existing motifs as working instruments, not decoration pasted onto
every surface.

### Graph paper

- Use one-pixel soft-line grids on paper or white.
- Existing web modules use 24–28 px grid intervals; diagrams may use a
  percentage grid.
- Fade or stop the grid before it competes with body copy.
- Keep graphs orthogonal even when a containing card has a small rotation.

### Code blocks and technical labels

- Use two-pixel ink borders for active build objects.
- Use monospace labels such as `PROJECT / 04`, `STATE: TESTING`, or
  coordinates that actually describe the content.
- Code-like fragments must be syntactically plausible and pedagogically
  relevant. Never use walls of fake code as atmosphere.

### Borders and shadows

- Default rules are one pixel; active boards and badge-like objects use two.
- Corners may be square or use the site’s restrained 8 px card radius.
- Use hard offset shadows, normally `6px 6px 0 rgba(21, 21, 21, 0.12)`.
- Yellow may be used as the solid offset shadow on a hero board.
- Use one dominant shadow direction per composition.
- “Imperfect” means a deliberate 0.5–2° rotation or slight optical offset,
  not distressed edges, noise, or reduced legibility.

### Coordinates and diagrams

Axes, plot points, circuit lines, arrows, and state diagrams should explain a
real idea. Labels must remain readable and cannot rely on colour alone. Use
shape, letters, or line styles in addition to the palette.

## Layout grammar

- Use the existing `--content: 1160px` maximum for website layouts.
- Start from a clear text column, then add one asymmetrical technical object.
- Preserve generous paper space. Empty space is part of the editorial tone.
- Use section fields from the existing soft palette rather than new gradients.
- Alternate dense build material with quieter explanation.
- Prefer two strong alignments and one deliberate offset.
- Let photographs and project art meet a caption, rule, coordinate, or label;
  do not float them as anonymous decoration.

The reusable SVG templates contain editable groups marked with `data-edit`.
Replace copy deliberately, maintain the safe areas, and export an sRGB PNG or
WebP after validation. They are masters, not screenshots of finished posts.
The template family covers 1080 × 1080 and 1080 × 1350 feed posts, a
1080 × 1920 Story/Reel, a 1200 × 630 card, a 1920 × 1005 event, a bilingual
English/Russian layout, a project illustration frame, and the private-safe
photograph-plus-caption treatment.

### Story safe area and export

The Story master uses these named coordinates on its 1080 × 1920 canvas:

| Constant | Coordinate |
| --- | ---: |
| `SAFE_LEFT` | 65 px |
| `SAFE_TOP` | 269 px |
| `SAFE_RIGHT` | 1015 px |
| `SAFE_BOTTOM` | 1248 px |

The live-content rectangle is therefore 950 × 979 px. It reserves approximately
6% at both sides, 14% at the top and 35% at the bottom for platform controls,
captions and CTA overlays. Keep
the wordmark, headings, labels, CTA copy, and URL entirely within this
rectangle. Background colour, grids, dots, and other non-essential decoration
may extend to the full canvas. Meta recommends 9:16 Reels and safe placement of
key creative; its Story CTA guidance describes roughly 14% top / 20% bottom
exclusions. The 35% bottom reserve is the project's deliberately conservative
production rule. Guidance checked 2026-08-17:
[Reels ads](https://www.facebook.com/business/ads/facebook-instagram-reels-ads)
and [Story CTA placement](https://www.facebook.com/help/instagram/192168966243613).

The editable master keeps its dashed rectangle and instruction inside
`id="editor-guide"`, marked `data-export="exclude"`. Never rasterize the
editable master directly. First prepare a guide-free production SVG:

```bash
cd sites/shkolakoda
venv/bin/python brand/export_story.py /tmp/social-story-production.svg
```

Rasterize `/tmp/social-story-production.svg` to an sRGB PNG or WebP with the
approved design tool. The export helper fails unless it removes exactly the
expected editor guide, preventing the border or instruction from entering the
production asset.

## Mascot system

The robot is a secondary mascot and illustration source. It can welcome,
point, demonstrate, react, or add warmth. It must not replace `</>`, `<SC/>`,
or the written name.

### Approved source selection

- Preferred avatar source: the supplied transparent circular robot.
- Preferred editorial source: the supplied 1024 px robot-at-laptop image.
- Reference only: the 500 px “SHKOLA CODA” lockups and busy
  Matrix/code-background variants.

Only optimized, metadata-stripped derivatives of the two selected sources
belong in Git. The raw ZIP and unused flat exports stay outside Git.

### Crops and treatments

Permitted:

- the complete circular avatar with its black contour intact;
- a full robot cutout, once a true transparent high-resolution source exists;
- head-and-shoulders crops that retain both eyes, the orange face plate, and at
  least one cyan ear piece;
- a simple one-colour silhouette derived from an approved master;
- a one- or two-colour halftone on paper, provided the eyes and head contour
  remain recognizable;
- masking the mascot behind a graph-paper frame or straight editorial crop.

Not permitted:

- cropping through the eyes or face plate;
- removing the laptop from the current editorial raster by generative fill;
- placing the circular avatar inside another circle, seal, or faux logo;
- adding speech, tools, costumes, or poses that imply an unapproved service;
- using the robot as a letter in the wordmark;
- mixing the mascot with “SHKOLA CODA” lettering in public identity.

### Small-size behaviour

- 64 px is the preferred minimum for the detailed mascot.
- 48 px is the absolute minimum for the circular avatar.
- At 32 px, use only when context already identifies the account; fine
  mechanical details will disappear.
- Below 32 px, switch to the institutional `</>` favicon.
- Never sharpen the eyes independently or redraw details in only one export.

### Future poses and generated derivatives

Create a pose only from an approved character sheet or editable master. Keep
the same head proportions, eye placement, ear construction, face-plate shape,
torso language, contour weight, and canonical colours. New expressions should
change pose or mouth modestly; the eyes and face geometry stay consistent.

No generated derivative may resemble a real child or use a student photograph
as a face reference. Do not use image generation to repair, extend, or
de-brand a student photograph. Review every proposed mascot derivative against
the canonical avatar at 100%, 64 px, and one-colour silhouette size.

## Photography, privacy, and captions

Photography should show building, testing, explanation, collaboration, and
physical evidence. The private reference archive may inform composition and
subject choices, but it is not documentary photography of School of Code
Calgary cohorts and must not be presented as such.

### Publication gate

Before any identifiable photograph is modified for public use or published,
confirm in writing that permission covers:

1. identifiable minors in the specific source image;
2. cropping, colour correction, resizing, and format conversion;
3. website, organic social, and paid advertising;
4. the relevant organization and geographic audience;
5. a withdrawal/contact process and any expiry;
6. third-party venue and photographer rights.

Release documents, private correspondence, names, and crosswalks do not belong
in Git. Record only a non-identifying status in the manifest.

For the current 81-photo production archive, the owner confirms full permission
for publication, advertising, modification, identifiable adult and child use,
compositing, and reference-based generation. The evidence is retained
privately. Public files record only this non-identifying rights status.

### Private-reference archive facts

The inspected archive contains 13 photographs. Every filename begins
`20211119_`, and embedded capture timestamps record 19 November 2021. The owner
confirms that capture date as ground truth.

These photographs are private visual references. Do not publish their source
location, former institution, student names, or other student identities. Do
not use them to document or imply a School of Code Calgary cohort. Any future
Calgary classroom photographs are a separate documentary collection with
their own provenance, permissions, and manifest.

### Selection and cropping

- Prefer active work over a posed lineup.
- Prefer clear robots, hands, materials, and teaching moments.
- A hands/equipment crop can reduce identification, but it does not replace
  required permission.
- Crop out former institution names, logos, emblems, and signage. If doing so
  makes the image misleading or unusable, do not publish it.
- Review clothing marks, phone screens, room labels, badges, and reflected
  information.
- Never blur or generatively replace institutional branding as a shortcut.
- Do not create synthetic facial lookalikes or alter a student’s appearance.

### Derivatives and metadata

- Raw photographs and raw ZIP archives stay in private storage, not Git.
- Apply EXIF orientation before cropping.
- Export sRGB web derivatives only after the permission gate passes.
- Strip EXIF, XMP, GPS, thumbnails, device identifiers, and comments.
- Verify the resulting file, not merely the export settings.
- Use a maximum long edge near 2400 px for a retained web master and smaller
  task-specific derivatives as needed.
- Keep neutral colour and skin tones. Do not apply a heavy brand filter.

### Honest captions

If a separately cleared image from the private reference set is used, describe
only visible activity. Good:

> A tabletop robot being adjusted during a workshop.

The confirmed capture date is internal provenance and need not appear in public
copy. Never include the source location, former institution, student names, or
other student identities. Do not connect the image to a School of Code Calgary
cohort.

Do not write:

- captions assigning the image to a School of Code Calgary cohort;
- a source location, former institution, student name, or other identifying
  student detail;
- invented testimonials, names, ages, outcomes, or enrolment claims;
- captions that call a posed group “collaboration” without visible evidence.

## Illustration

Illustration is code-native where practical: SVG diagrams, coordinate planes,
circuit paths, project objects, and typographic build boards. Use the mascot
only when a character adds meaning.

- Keep project illustrations specific to the project.
- Use flat paper fields, ink outlines, and one primary accent.
- Avoid glossy 3D icon packs and generic stock “coding” imagery.
- Do not depict a synthetic child as if they were a student.
- Label demonstration projects honestly.

## Writing voice

Write as a capable teacher beside a workbench.

- Lead with what the learner will build, notice, test, or change.
- Use concrete verbs and short technical nouns.
- Explain why a step matters.
- Prefer “students can” or “the project asks” to inflated outcome promises.
- Distinguish current programs, future programs, demonstrations, and archive
  material.
- Use Canadian English for public copy.
- Keep humour dry, kind, and connected to the project.

Good:

> Build a sensor rule, test the edge cases, then explain what the robot still
> gets wrong.

Avoid:

> Unlock limitless future-ready innovation with our revolutionary coding
> journey.

## Accessibility and contrast

Target WCAG 2.2 AA as a minimum:

- 4.5:1 for normal text;
- 3:1 for large text and meaningful non-text graphics;
- visible keyboard focus;
- no information communicated by colour alone;
- meaningful alternative text for content images;
- empty alternative text for purely decorative motifs.

Verified core pairs:

| Foreground / background | Contrast |
| --- | ---: |
| Ink / Paper | 18.07:1 |
| Muted / Paper | 6.65:1 |
| Green / Paper | 5.01:1 |
| Blue / Paper | 6.71:1 |
| Red / Paper | 4.95:1 |
| Violet / Paper | 6.90:1 |
| Ink / Yellow | 11.23:1 |
| White / Green | 5.06:1 |
| White / Blue | 6.78:1 |
| White / Red | 5.00:1 |
| White / Violet | 6.97:1 |

Yellow on Paper is not a text pair. Soft palette fields use Ink for text.
Recheck contrast after opacity, overlays, photography, or export compression.

SVG rules:

- include a `viewBox`;
- include a concise `<title>` and `<desc>` for meaningful standalone art;
- avoid external scripts and remote assets;
- keep live copy editable in templates;
- provide HTML alternative text when an SVG is embedded as an image;
- do not place critical copy below the documented minimum sizes.

## Release checklist

Before a logo, mascot, photograph, or template export is published:

1. Use the right identity level: institutional logo first, mascot second.
2. Confirm the public name reads “School of Code Computer Lab.”
3. Confirm minimum size, clear space, and crop safety.
4. Verify contrast and do not rely on colour alone.
5. Confirm private-reference captions describe only visible activity and do
   not identify the source or a student.
6. Confirm photo modification and advertising permission where applicable.
7. Remove former institution and third-party branding unless authorized.
8. Strip and verify metadata.
9. Check the asset at final display size, including 16, 32, 48, or 64 px where
   relevant.
10. Keep raw archives, releases, personal data, and unused exports out of Git.

## Designer source request

The supplied designer package contains flattened 500 px Canva PNG exports and
one flattened 1024 px JPEG. Request:

- the original editable Canva document or layered source file;
- a rights and provenance note for the robot artwork and every incorporated
  element;
- a transparent full-body robot master at least 3000 px high, or preferably
  vector SVG/PDF/AI;
- separate editable layers for robot, laptop, yellow circle, outline, and
  background;
- an unlettered circular avatar at 2000 × 2000 or larger;
- a two-colour and one-colour master, not an auto-traced bitmap;
- a model sheet with front, three-quarter, side, head crop, silhouette, colour
  swatches, and contour weights;
- a small approved pose set with consistent hands, joints, eyes, and
  expressions;
- export instructions and the exact colour values used.

Do not request “SHKOLA CODA” lettering as the new public wordmark. The
institutional identity remains the code-mark system and the public English
name.
