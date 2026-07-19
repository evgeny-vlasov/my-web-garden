# School of Code

This Flask application serves the School of Code public website at
`shkolakoda.com` and `www.shkolakoda.com`.

School of Code is a small independent Calgary school for programming, game
design, and robotics. The Computer Lab is a guided project mode inside the
school. Scratch & Game Design and Robotics are the active first programs;
Roblox Studio / Lua and AI & Smart Machines are documented as future programs.

The first public release is informational. It has no database, registration
backend, admin area, migrations, or upload storage. Contact is handled directly
through `hello@shkolakoda.com` and the published phone number.

The preserved Happy Science site is a separate application in `sites/science`
and is served at `science.shkolakoda.com`.

## Routes

- `/`
- `/programs`
- `/programs/scratch`
- `/programs/robotics`
- `/programs/roblox`
- `/programs/ai`
- `/topics/coordinates`
- `/lessons/coordinates-and-movement`
- `/projects`
- `/projects/escape-from-the-giant-pigeon`
- `/projects/grandmas-intergalactic-taxi`
- `/projects/astro-chicken-rescue`
- `/computer-lab`
- `/parents`
- `/method`
- `/contact`
- `/robots.txt`
- `/favicon.svg`

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
gunicorn --bind 127.0.0.1:8000 wsgi:app
```

Production uses the existing `webgarden-shkolakoda.service` runtime on
`127.0.0.1:8000`; nginx deployment is managed separately.
