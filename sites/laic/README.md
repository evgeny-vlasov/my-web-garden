# Local AI Collective

Public-facing Flask site for Local AI Collective inside Web Garden.

## Purpose

This site presents Local AI Collective as a practical initiative that helps nonprofits and local community organizations use AI in careful, affordable ways.

The old Love Sugar & Dough demo is treated as an example project only. It is not the homepage or the main product message.

## Routes

- `/`
- `/about`
- `/services`
- `/microprojects`
- `/for-nonprofits`
- `/contact`
- `/projects/love-sugar-dough`
- `/dashboard`
- `/health`

## Contact Storage

The contact form supports two storage modes:

1. PostgreSQL when `DATABASE_URL` is set.
2. Local file fallback at `instance/contact_submissions.jsonl` when `DATABASE_URL` is not set.

PostgreSQL schema is in `db/schema.sql`.

## Environment

Recommended production environment file:

- `/etc/webgarden/laic.env`

Suggested variable names:

- `SECRET_KEY`
- `DATABASE_URL`
- `CONTACT_EMAIL`
- `CONTACT_STORAGE_PATH`

Do not commit environment files or secrets.

## Local Run

```bash
cd /var/www/webgarden/sites/laic
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
gunicorn --bind 127.0.0.1:8004 app:app
```

## Deployment Artifacts

- Systemd template: `deploy/systemd/webgarden-laic.service`
- nginx config: `deploy/nginx/laic.conf`
