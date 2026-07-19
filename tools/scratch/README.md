# School of Code Scratch production tooling

This isolated Node workspace builds and validates downloadable Scratch 3
projects. Node is a production tool only; the Flask site serves the generated
files and has no Node runtime dependency.

All packages are therefore declared as development dependencies. A full
`npm audit` currently reports upstream advisories inherited by the official
Scratch VM (`hull.js`, for which the advisory names no published patched
version, and an old `uuid` buffer API). This tool accepts only checked-in,
generated project input, never runs as a network service, does not attach the
Scratch renderer that calls `hull.js`, and does not call UUID v3/v5 buffer APIs.
`npm audit --omit=dev` is clean. Recheck the full audit whenever the pinned
official VM is upgraded.

## Giant Pigeon pilot

The authoritative pilot content is
`sites/shkolakoda/scratch_projects/escape-from-the-giant-pigeon.json`. It holds
the page copy, ten build sections, editable scratchblocks text, and a small
structured block AST for every finished-project script.

`build-giant-pigeon.js` performs these steps:

1. regenerates each scratchblocks script from the AST and stops on drift;
2. generates original SVG costumes, the backdrop, the project sketch, and WAV
   effects;
3. serializes starter and finished Scratch 3 `project.json` records;
4. names embedded media from the MD5 hash required by the Scratch format;
5. writes deterministic ZIP/SB3 archives with a fixed member timestamp;
6. creates the readable art-and-sound pack; and
7. copies the pinned scratchblocks browser bundle and MIT licence into the
   self-hosted static vendor directory.

Build from a clean checkout:

```bash
cd tools/scratch
npm ci
npm run build
npm run validate
```

`validate-giant-pigeon.js` checks ZIP CRCs and structure, parses `project.json`,
verifies every asset filename and MD5 digest, checks targets, variables,
costumes, sounds, block opcodes, starter/reference separation, content-source
consistency, the source asset pack, and the self-hosted renderer licence. It
then loads both SB3 buffers with the pinned official `scratch-vm` package and a
Scratch storage instance. The headless VM intentionally has no renderer or
audio engine; warnings about those absent output devices are expected, while
all costume and sound assets must still exist in VM storage.

## Changing media

Edit the SVG strings or tone functions in `build-giant-pigeon.js`, then rebuild.
Keep each SVG viewBox and the matching `rotationCenterX/Y` values together.
Readable filenames belong in the generated `assets/` directory and asset pack;
inside an SB3, Scratch requires `<md5>.<extension>` names. The validator checks
both conventions.

The current costume centres are also documented in the generated `README.txt`:

- Player: 35, 45
- Giant Pigeon: 75, 55
- Safe Zone: 45, 52.5
- backdrop: 240, 180

Students may replace all original media. If a sprite, costume, sound, or
broadcast name changes, update both its AST dropdown value and its media record.

## Changing code or instructions

Make the semantic change in the script AST and update its adjacent `source`
text. The build will reject either half if they disagree. The Flask content
loader resolves code-section `script_ids` to those same script records, while
the SB3 compiler consumes their AST. This is the anti-drift boundary between
the guide and reference project.

Use stable script IDs and keep each top-level script assigned to a named target.
The starter is produced from scripts marked `"starter": true`; do not mark a
completed movement, pursuit, collision, outcome, or restart script as starter.

## Reproducing the pattern

For a future project:

1. add one enriched record under `sites/shkolakoda/scratch_projects/`;
2. merge it into the existing `PROJECTS` curriculum record—do not add a second
   routing or CMS system;
3. define original media generators and clear costume centres;
4. use a shared AST/source record for page blocks and SB3 code;
5. emit starter, reference, asset pack, README, licences, and sketch;
6. add the downloads to the existing project route and pilot template model;
7. copy or generalize the structural/package tests; and
8. require one final manual opening in the graphical Scratch editor.

## Provisional pieces

The sketch-style SVG art, limited palette, technical sketch, and five-role art
slot model are the pilot visual language. A human designer may refine them
later. Sprite names, viewBoxes, costume centres, content IDs, state names, and
download contracts should remain stable during that pass.

See `PRODUCTION_CHECKLIST.md` for the release gate used by the remaining
Scratch project backlog.
