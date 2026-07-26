# Designer asset audit

- Source archive: `shkola coda logos.zip`
- Inspected: 2026-07-26
- Archive committed: **no**
- SHA-256: `c471278ba04546db29116ce467a9049145a94d4462c87c8ea246bfb651929a62`

This audit records technical facts without reproducing the unused source
exports or their embedded creator/account identifiers.

## Source inventory

| Source | Dimensions / mode | Metadata | Decision |
| --- | --- | --- | --- |
| `20.png` | 500 × 500 RGB; no alpha | XMP present | Reference only. Uses “SHKOLA CODA” lettering and is not the public identity. |
| `21.png` | 500 × 500 RGB; no alpha | XMP present | Reject for canonical use. Busy Matrix background and old lettering. |
| `22.png` | 500 × 500 RGB; no alpha | XMP present | Reject for canonical use. Busy code-tunnel background and old lettering. |
| `23.png` | 500 × 500 RGB; no alpha | XMP present | Reject for canonical use. Busy code background and old lettering. |
| `24.png` | 500 × 500 RGB; no alpha | XMP present | Reject for canonical use. Busy code background and old lettering. |
| `25.png` | 500 × 500 RGB; no alpha | XMP present | Reject for canonical use. Busy binary background and old lettering. |
| `robot.jpg` | 1024 × 1024 RGB; no alpha | EXIF and ICC profile present | Selected as an editorial illustration source only. |
| `Shkola Coda full logo.png` | 500 × 500 RGB; no alpha | XMP present | Reference only. Flattened old-lettering lockup. |
| `Shkola Coda logo circle.png` | 500 × 500 RGBA | XMP present | Selected. Strongest supplied avatar and mascot reference. |

The PNG XMP identifies a flattened Canva export and includes creation,
creator, and account/document identifiers. The selected derivatives remove
that metadata. Provenance and usage rights should instead be recorded in the
private source register, not carried as public account IDs inside web files.

## Transparency and crop

The selected circular avatar has:

- a 500 × 500 RGBA canvas;
- visible alpha content from `(30, 30)` through `(470, 470)`;
- a 441 × 441 visible-content box;
- approximately 38.68% fully transparent pixels;
- antialiased partial transparency at the circular edge.

The 30 px transparent margin is useful safe area and is preserved. Do not trim
the circle to the contour for an avatar export.

The 1024 px editorial JPEG is square, opaque, and flattened onto a light grey
background. It is not a true robot cutout. Do not use automatic background
removal or generative fill as a substitute for an editable transparent source.

## Selected optimized derivatives

| Derivative | Dimensions | Alpha | Metadata result | Intended use |
| --- | ---: | --- | --- | --- |
| `static/brand/mascot/robot-avatar-500.png` | 500 × 500 | Yes | No EXIF, ICC, or XMP | Preferred uploaded social avatar and highest retained circular raster |
| `static/brand/mascot/robot-avatar-256.png` | 256 × 256 | Yes | No EXIF, ICC, or XMP | Embedded cover composition and medium UI |
| `static/brand/mascot/robot-avatar-96.png` | 96 × 96 | Yes | No EXIF, ICC, or XMP | Native 2× source for the 48 px minimum |
| `static/brand/mascot/robot-editorial-1024.webp` | 1024 × 1024 | No | No EXIF, ICC, or XMP | High-density editorial card or project illustration |
| `static/brand/mascot/robot-editorial-640.webp` | 640 × 640 | No | No EXIF, ICC, or XMP | Smaller web editorial placement |

No derivative is upscaled. The other seven source exports are not copied into
the repository.

## Small-size review

The circular avatar was rendered at 128, 96, 64, 48, 32, and 24 px.

| Size | Result |
| ---: | --- |
| 128 px | Full character, laptop, hands, eyes, and contour remain clear. |
| 96 px | Strong avatar; secondary mechanical shading remains useful. |
| 64 px | Preferred minimum; robot, laptop, face plate, and circle remain identifiable. |
| 48 px | Acceptable floor; hands and laptop simplify but the character remains recognizable. |
| 32 px | Context-dependent only; most body detail collapses into the face/circle silhouette. |
| 24 px | Too detailed. Use the `</>` favicon instead. |

## Source files to request

The complete request is maintained in `BRAND.md`. Highest priority:

1. original editable Canva or layered source plus rights/provenance;
2. unlettered transparent full-body robot at 3000 px or larger, preferably
   vector;
3. 2000 × 2000 or larger circular avatar with separate robot, yellow disc,
   outline, and background layers;
4. true one-colour and two-colour masters;
5. character sheet, exact swatches, contour weights, and approved poses.

Do not request a new “SHKOLA CODA” public wordmark. The institutional identity
remains `</>`, `<SC/>`, and “School of Code Computer Lab.”
