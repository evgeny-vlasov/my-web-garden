# School of Code photo production manifest

- Production authorization confirmed: 2026-08-17
- Private intake: 81 source photographs
- Raw files or archives committed: **none**
- Public campaign masters: **4**
- Public historical workshop masters: **6**
- Machine-readable derivative register: `brand/photo-asset-manifest.json`

The user confirms all 81 source photographs are authorized for editing and dramatic reconstruction; identifiable adult and child use; website and social-media publication; paid advertising; compositing; and generation by reference. Screens contain no important private information. Release evidence, identities, raw GPS, timestamps, device metadata, contact sheets, the intake archive and private filesystem locations stay outside Git.

## Authenticity classes

**Reconstructed campaign image** means a deliberate composition grounded in authorized real School of Code people, activity and machine references. It is not documentary evidence of a literal current class, cohort or facility.

The label **historical workshop photograph** means a truthful derivative of one historical source photograph. Colour, exposure, crop, cleanup, screen simplification and removal of irrelevant branding are permitted. People and activity are not replaced or invented. Never describe one as a current Calgary cohort or current facility.

## Approved campaign masters

| Tracked master | Approved origin | Primary role |
| --- | --- | --- |
| `photo-masters/campaign-robotics-hero-v1.png` | Concept 1 v1.1 | Home and Robotics hero; Page cover; Robotics feed placements |
| `photo-masters/campaign-scratch-lab-v1.png` | Concept 2 | Scratch and Computer Lab; Group cover; Scratch/Lab placements |
| `photo-masters/campaign-eugene-builder-v1.png` | Concept 3 v1.1 | Method, Parents and teacher identity; Eugene placements |
| `photo-masters/campaign-project-workbench-v1.png` | Authorized apparatus references | Projects, Lessons, Event cover and technical-detail cards |

Concept 3 identity direction is user-approved as recognizably Eugene. Do not make him younger, slimmer, smoother, corporate or generic in future adaptations.

## Historical workshop set

| Tracked master | Source filename | Honest visible-activity description |
| --- | --- | --- |
| `photo-masters/documentary/historical-robot-testing.jpg` | `20211119_184800.jpg` | Children testing tabletop robots during a historical workshop. |
| `photo-masters/documentary/historical-coding-together.jpg` | `20200704_115925.jpg` | Children comparing a block-based program during a historical workshop. |
| `photo-masters/documentary/historical-workbench-apparatus.jpg` | `20200609_015805.jpg` | A relay, test-lead and container apparatus on a historical workbench. |
| `photo-masters/documentary/historical-robot-adjustment.jpg` | `20211119_184618.jpg` | A tabletop robot being adjusted during a historical workshop. |
| `photo-masters/documentary/historical-scratch-use.jpg` | `DSC_0070.JPG` | A Scratch project being tested during a historical workshop. |
| `photo-masters/documentary/historical-classroom-context.jpg` | `DSC_0042.JPG` | A compact computer setup used in an earlier workshop setting. |

Source timestamps are retained only as private provenance and are not treated as current-event dates. Captions identify visible activity only and disclose no child names, former institutions or source locations.

## Derivative workflow

1. Keep raw intake and review material outside Git.
2. Run `brand/build_photo_assets.py` with explicit private input directories and a local-only cache.
3. Apply EXIF orientation, truthful crop and restrained correction to documentary files.
4. Remove third-party marks and irrelevant screen identifiers without inventing activity.
5. Export sRGB AVIF, WebP and JPEG website sizes; export exact-dimension social files.
6. Regenerate `brand/photo-asset-manifest.json` with roles, origins, classifications, focal points, placements, alt text, rights status, dimensions and SHA-256.
7. Verify file signatures, dimensions, metadata absence, accessibility, route references, page weights and visual crops.

Future photographs require the same private rights record and an explicit documentary or campaign classification before they enter production. Add only selected metadata-clean masters and derivatives; never add the raw archive.
