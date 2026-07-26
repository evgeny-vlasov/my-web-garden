# Private-safe archive photo manifest

- Archive: `Photos-1-001.zip`
- Inspected: 2026-07-26
- Raw files committed: **none**
- Public derivatives committed: **none — not created in this corrective PR**
- Parental permission for publication, advertising, modification, and
  derivative work confirmed by owner; evidence retained privately.

This manifest contains source filenames but no student names, coordinates,
release documents, contact details, or other personal data.

## Mandatory status notes

- The archive contains 13 JPEG photographs.
- All filenames begin `20211119_`.
- Embedded capture timestamps record 19 November 2021. The owner confirms this
  as the ground-truth capture date.
- These photographs are private visual references. They are not a documentary
  collection of School of Code Calgary cohorts and must not be presented as
  one.
- Do not publish their source location, former institution, student names, or
  other student identities. The capture date is internal provenance and need
  not appear in public materials.
- Every raw file contains EXIF with GPS data and device/capture information.
  Any eventual derivative must be metadata-stripped and verified.
- The owner confirms that parental permission covers publication, advertising,
  modification, and derivative work. The private evidence is not committed and
  this manifest does not identify parents or students.
- Photographer rights, venue rights, withdrawal process, permission expiry,
  and other third-party rights are separate questions. They remain open until
  independently confirmed; parental permission does not silently resolve them.

Rights/status value for every row:

`PARENTAL CONFIRMED / OTHER RIGHTS OPEN` means that the owner has confirmed
parental permission for publication, advertising, modification, and derivative
work. Photographer, venue, withdrawal, expiry, and other third-party-rights
questions remain separate. Keep all evidence outside Git.

## Image-by-image review

| Source filename | Proposed use | Crop / aspect-ratio suggestion | Visible branding or privacy warning | Rights / status | Honest public-caption suggestion |
| --- | --- | --- | --- | --- | --- |
| `20211119_184202.jpg` | **Candidate master 1:** wide archive group context with robots | Apply orientation; 3:2 or 16:9. Crop the chess strip at left and excess white wall at right; keep robots visible. | Identifiable children; several apparel wordmarks/logos. No former-institution name visible in the proposed crop. | PARENTAL CONFIRMED / OTHER RIGHTS OPEN | “Group portrait with tabletop robotics builds.” |
| `20211119_184206.jpg` | Alternate to 184202; do not retain if master 1 is selected | 3:2; remove left chess strip and right table. | Identifiable children and apparel branding. Similar frame to 184202, with less candid activity. | PARENTAL CONFIRMED / OTHER RIGHTS OPEN | Same activity-only caption; do not imply active collaboration in this posed frame. |
| `20211119_184211.jpg` | Vertical group portrait option | 4:5. Trim top curtain and right white wall; keep robots in lower third. | Identifiable children; apparel and footwear logos. No former-institution name visible. | PARENTAL CONFIRMED / OTHER RIGHTS OPEN | “Group portrait with tabletop robotics builds.” |
| `20211119_184212.jpg` | **Candidate master 2:** strongest vertical group portrait | Apply orientation; 4:5 or 3:4. Keep the robots and full group; reduce empty wall. | Identifiable children; apparel and footwear logos. No former-institution name visible. | PARENTAL CONFIRMED / OTHER RIGHTS OPEN | “Group portrait with tabletop robotics builds.” |
| `20211119_184252.jpg` | Do not use as a master | No safe general crop. A very tight equipment crop may be reviewed, but other frames are stronger. | Large former-institution names, emblems, and Russian signage dominate the background; identifiable children; apparel marks. | PARENTAL CONFIRMED / OTHER RIGHTS OPEN / REJECT FOR GENERAL USE | If an equipment-only crop is ever approved: “Tabletop robotics builds and workshop materials.” |
| `20211119_184533.jpg` | **Candidate master 3:** hands-and-robots detail only | 16:9 or 2:1 crop from the lower portion; exclude all faces, top text, and both emblems. | Large former-institution banner and logos; identifiable children in the raw; apparel marks. Proposed crop must remove every institutional identifier. | PARENTAL CONFIRMED / OTHER RIGHTS OPEN | “Hands and tabletop robots during a build session.” |
| `20211119_184536.jpg` | Alternate equipment/group detail; do not retain if 184533 works | Wide lower-third crop only, with all banner text and emblems excluded. | Same dominant former-institution banner/logos; identifiable children; apparel marks; raised robot may be motion-soft. | PARENTAL CONFIRMED / OTHER RIGHTS OPEN | Same activity-only caption; avoid assigning a visible robot to a named participant. |
| `20211119_184539.jpg` | Reject as a master | No preferred crop; motion and overlapping figures make a clean safe crop difficult. | Former-institution banner/logos, identifiable children, apparel marks, motion blur. | PARENTAL CONFIRMED / OTHER RIGHTS OPEN / REJECT | No proposed public use. |
| `20211119_184618.jpg` | **Candidate master 4:** quiet individual build moment | Apply orientation; 4:5 for context or 3:2 hands/robot crop. A detail crop can exclude the face and tonal chest wordmark. | Identifiable child in raw; tonal sportswear wordmark. No former-institution signage visible. | PARENTAL CONFIRMED / OTHER RIGHTS OPEN | “A tabletop robot being adjusted during a build session.” |
| `20211119_184624.jpg` | Alternate to 184618 | 4:5; exclude the partial hand/robot entering from left. | Identifiable child; tonal apparel wordmark; partial person at left edge. | PARENTAL CONFIRMED / OTHER RIGHTS OPEN | Same activity-only adjustment caption. |
| `20211119_184638.jpg` | Reject as a master | No preferred crop. | Identifiable child; apparel mark; partial arm at left; subject motion blur. | PARENTAL CONFIRMED / OTHER RIGHTS OPEN / REJECT | No proposed public use. |
| `20211119_184644.jpg` | **Candidate master 5:** individual with two robots and negative space | Apply orientation; 4:5. Crop above or around prominent footwear branding while retaining both robots. | Identifiable child; prominent footwear logo; no former-institution signage visible. | PARENTAL CONFIRMED / OTHER RIGHTS OPEN | “Two tabletop robotics builds during a workshop.” |
| `20211119_184800.jpg` | Strong activity alternate; first replacement if a selected master fails its crop | Apply orientation; 4:5 or 3:4 centred on hands, robots, and worktable. Review whether to exclude the phone and printed red shirt. | Identifiable children; phone/device screen; printed apparel; room safety fixtures. No former-institution name visible. | PARENTAL CONFIRMED / OTHER RIGHTS OPEN | “Robots being tested on a workshop table.” |

## Planned retained set

If the separate rights questions are resolved and a future photo-specific
change is authorized, prepare derivatives only from:

1. `20211119_184202.jpg` — wide group context;
2. `20211119_184212.jpg` — vertical group context;
3. `20211119_184533.jpg` — branding-free equipment detail crop;
4. `20211119_184618.jpg` — individual build/detail;
5. `20211119_184644.jpg` — individual and robots.

Use `20211119_184800.jpg` as the first alternate. Do not retain near-duplicate
masters merely for storage.

## Derivative gate

No student-photo derivative belongs in this corrective PR. Before any future
derivative is prepared:

1. Resolve the separate photographer, venue, withdrawal, expiry, and
   third-party-rights questions, recording only a non-identifying status here.
2. Work from private storage outside the repository.
3. Apply EXIF orientation.
4. Crop former-institution signage and review third-party marks.
5. Export sRGB web files with a maximum long edge near 2400 px.
6. Remove EXIF, GPS, XMP, embedded thumbnails, comments, and device data.
7. Verify metadata absence, dimensions, crop, and caption linkage.
8. If separately authorized, commit only the 4–5 selected derivatives, never
   the ZIP or all raw files.

Until a future photo-specific change is authorized, this manifest remains the
complete repository inventory for the private visual-reference set.
