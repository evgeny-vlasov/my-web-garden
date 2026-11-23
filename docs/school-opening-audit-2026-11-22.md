# School website operational audit — November 22, 2026

## Operational truth

The owner confirms no venue is secured and physical classes are not open.
Opening in the coming months is a hope, contingent on a venue and confirmed
dates, not a promise. Scratch / Creative Programming and Robotics are the first
development priorities. Roblox and AI are later/by-interest possibilities, not
available classes. Science and day camps remain on hold.

This clarifies “active first” in curriculum/project briefs: development priority
does not mean enrollment is open. Creative Programming leads toward AI
Development and Robotics toward Autonomous Systems; no new successor program
or launch commitment is created by this correction.

## Sources and scope

- Owner's current request and referenced `soccl main` conversation.
- Repository `sites/shkolakoda/README.md`, `BRAND.md`, curriculum status records,
  public templates, blog content, Russian copy, and Science README/templates.
- GitHub source of truth: `evgeny-vlasov/my-web-garden`, `main`.
- Starting live School release and remote main: `f1fcad2d705c35c655aa34dc89348d2dd2c41731`.
- Direct HTTPS audit: 154 URLs returned 200, comprising 70 public application
  paths on each School language domain, four Science paths, and ten published
  notes/index URLs across both domains. Search-engine cached English pages were
  stale; direct live responses and the active release controlled this audit.
- `schoolofcode.ca` is the current English site and `shkolakoda.com` the Russian
  site. Both require the same operational truth. The earlier bilingual release
  had already corrected home/program navigation badges and several launch claims.

## Findings and exact changes

| Area | Mismatch | Correction |
| --- | --- | --- |
| Shared School shell and metadata | No universal explicit closed/no-venue status; generic description could imply an operating school | English/Russian pre-opening notice, no venue, no classes, dates only once confirmed; interest CTA explicitly not enrollment; English metadata/footer describe preparation |
| English Roblox and AI pages | Scratch and Robotics “available now” | Planned first, not open; interest in later programs does not reserve places |
| English contact | “current scheduling,” vague venue details, class-question email CTA | Register-interest email subject/button; no venue/classes; tentative coming-months wording; preferred days rather than existing timetable; conditions confirmed before enrollment; no reservation |
| Russian contact and shared CTAs | General contact wording, no explicit lack of venue on contact page | Launch-interest CTA and email subject, explicit no venue/classes, tentative opening, no enrollment/reservation, conditions confirmed first |
| English Scratch, Robotics and home CTAs | Generic contact conversion | Register-interest buttons using the existing contact route |
| Computer Lab, both languages | Read as an available guided workspace | Explicitly a planned format, not an open venue; English comparison/interest buttons clarified |
| English lesson index | Outlines “used in class”; “current scheduling” | Future curriculum materials, not scheduled sessions |
| Gallery, both languages | Images could imply current Calgary cohort or venue | Past-workshop/reconstructed context; explicit no current Calgary class/venue; English room caption identified as historical |
| Two English blog articles | “Scratch and Robotics are active now” | Planned first; classes not open (`roblox-as-a-creative-coding-platform`, `from-scratch-to-robots-to-ai`) |
| Curriculum status data | “Active now” hidden by template substitutions | Source records now say “Planned first”; existing status assertions updated accordingly; educational question about active program state preserved |
| School and Science READMEs | “Active first” ambiguous; Science not explicitly parked | Record closed/no-venue, development priority, later programs, and interest-only policy |
| Science shared shell, title, metadata/footer | Offered weekend camps as an operating service | On-hold notice on all four pages, no venue/dates/bookings; future activity identity; coding cross-link describes future programs |
| Science home | $76/day, limited spots, fixed format/group size, implied backyard space and current safety setup | Unconfirmed price, provisional ages/format/group size, future activity/safety language, no venue or available places; themes and layout retained |
| Science camps | $76 price, fixed pilot capacity, details after registration | No confirmed price/date/venue; cards labeled provisional; all conditions confirmed before registration |
| Science contact | Location after registration, active pilot language | No venue; on hold; interest does not reserve a place; questions about future activities |
| Science safety | Current pilot/supervision/equipment promises and location after registration | Future arrangements to be confirmed before any registration; no venue |

Existing email/phone destinations, visual assets, CSS, navigation structure,
curriculum, project downloads, domain-language routing, SEO alternates, and
publication cadence are preserved. No intake backend, payment, reservation,
new science offering, or social message was created. Published notes had no
matching current-availability claims and were not edited. Educational descriptions
in the present tense are retained where they describe teaching concepts rather
than claim a currently operating class.

## Validation and deployment

- 76 existing School tests pass; three publication records validate.
- All 140 candidate School routes render successfully in English/Russian, with
  no positive “active now,” “available now,” or “current scheduling” claims.
- All four candidate Science routes render with on-hold/no-venue notices and
  without the $76 price or after-registration location claim.
- Git whitespace checks pass. Browser preview could not initialize on this
  desktop; no visual-browser verification is claimed. No CSS/layout was changed.
- Work is isolated at `/home/fluffy/projects/soccl-opening-status`; existing
  dirty curriculum, project, Psyling and preview work is untouched.
- School must deploy through `/usr/local/bin/soccl-deploy` at the committed
  main SHA. Science runs from the shared checkout and needs only the five
  corrected templates installed and its own service restarted. Stage backups,
  baseline checks and rollback for those templates; do not update the whole
  shared checkout.
- At preparation time, production remains unchanged: `sudo -n true` reports
  that an administrator password is required. The owner must run the staged
  deployment command privately. This is a host privilege blocker, not an
  automatic approval-review rejection.
