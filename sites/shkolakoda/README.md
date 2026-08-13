# School of Code

This Flask application serves the School of Code public website at
`shkolakoda.com` and `www.shkolakoda.com`.

School of Code is a small independent Calgary school for programming, game
design, and robotics. The Computer Lab is a guided project mode inside the
school. Scratch & Game Design and Robotics are the active first programs;
Roblox Studio / Lua and AI & Smart Machines are documented as future programs.

Version 1 is a public educational portal, not only a brochure. It publishes
program, topic, lesson, guided-project, Computer Lab project, parent-guide,
gallery-foundation, and evergreen blog content. It has no database,
registration backend, admin area, migrations, or upload storage. Contact is
handled directly through `hello@shkolakoda.com` and the published phone number.

The preserved Happy Science site is a separate application in `sites/science`
and is served at `science.shkolakoda.com`.

## Content architecture

- `curriculum.py` stores the 11 public topics and 10 public lessons.
- `project_library.py` stores 18 project pages: 8 Scratch, 6 robotics and
  electronics, 2 future Roblox previews, and 2 future AI previews.
- `blog_content.py` stores 16 evergreen parent and curriculum guides.
- `app.py` owns route lookup, sitemap generation, infrastructure routes, and
  the custom 404 handler.
- `templates/_macros.html` contains shared cards, badges, breadcrumbs,
  metadata, tags, related-content links, and parent explanations.
- `scratch_projects/` contains enriched records for complete downloadable
  Scratch productions. These records are merged into the same project library;
  they do not create a second content or routing system.

The first production pilot is **Escape from the Giant Pigeon**. Its isolated
builder, validator, shared-code architecture, regeneration instructions, and
future-project checklist are documented in `../../tools/scratch/README.md`.

Content is deliberately file-backed. Adding a topic, lesson, project, or post
does not require a database or a generic CMS.

## Route families

- `/`
- `/programs`
- `/programs/scratch`
- `/programs/robotics`
- `/programs/roblox`
- `/programs/ai`
- `/topics` and `/topics/<slug>`
- `/lessons` and `/lessons/<slug>`
- `/projects`
- `/projects/<slug>`
- `/computer-lab`
- `/parents`
- `/method`
- `/blog` and `/blog/<slug>`
- `/gallery`
- `/contact`
- `/sitemap.xml`
- `/robots.txt`
- `/favicon.svg`
- custom 404 handling, with `/404` available as a review path

The retired Happy Science paths `/camps` and `/safety` intentionally return
404 on this application.

## Local development

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run the Flask development server:

```bash
flask --app app run
```

Test the production WSGI entry:

```bash
venv/bin/python -m gunicorn --bind 127.0.0.1:8000 wsgi:app
```

Run the public-site integrity tests:

```bash
PYTHONDONTWRITEBYTECODE=1 venv/bin/python -m unittest -v tests.test_public_site
```

Run the Scratch production tests after generating the pilot:

```bash
PYTHONDONTWRITEBYTECODE=1 venv/bin/python -m unittest -v tests.test_scratch_project
cd ../../tools/scratch
npm ci
npm run check
```

## Production and deployment

Production runs as `soccl-app` through `webgarden-shkolakoda.service` on
`127.0.0.1:8000`. The runtime is `/var/www/soccl/current/app`, an immutable
release selected by a symlink. It is not this source directory.

Changing `/var/www/webgarden/sites/shkolakoda` and restarting systemd does not
deploy new School of Code code. The canonical exact-SHA deployment procedure,
validation, atomic activation, health checks, and automatic rollback are
documented once in [the Webgarden deployment guide](../../docs/deployment.md).
When inspecting a release manually, invoke Gunicorn through
`venv/bin/python -m gunicorn`; console-script shebangs may retain staging paths
after a release is moved.

## Git-backed publishing

Campaigns, new articles, general project pages, and media manifests are discovered from checked-in JSON and validated before Flask starts. The existing structured Scratch project system, including Escape from the Giant Pigeon, is part of the same repository rather than a parallel CMS.

See [ARCHITECTURE.md](ARCHITECTURE.md) for the schema, authoring workflow, visibility rules, validation boundaries, automatic routes, and website-only GitHub Actions deployment contract.
