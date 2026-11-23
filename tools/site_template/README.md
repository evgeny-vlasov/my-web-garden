# Run this site

Public content is in `site.json`. Both this site and `bot-handoff.json` were
created from the same brief. Customize the content and template before launch.
Keep the public facts in both JSON files aligned when editing them.

Use Python 3.11 or newer. From this site's directory, create an isolated
environment and start locally.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m flask --app app run --host 127.0.0.1 --port 18080
```

On Windows use `.venv/Scripts/python` in place of `.venv/bin/python`.
Check `/` and `/health`. The starter uses contact links and has no database.

## Connect Bot Army

Give `bot-handoff.json` to Bot Army. It describes public knowledge, contact
details, and the request/response contract. Bot Army currently needs a separately
configured bot process, listener, credentials, and optional database/RAG setup.
The handoff file is a specification for that setup.

Once the bot's loopback listener is assigned, set `BOT_CHAT_URL` in the site's
service environment and start the application with Gunicorn. For example,
`BOT_CHAT_URL=http://127.0.0.1:18081/api/chat`. The URL must point to this site's
bot. Keep provider credentials in the bot process's protected configuration.

The page displays its chat form when the URL is configured. Both the existing
Psyling bot and this starter use POST `/api/chat` with `message`, an optional
`session_id`, and optional `conversation_history`. A successful reply contains
a nonempty `response` string.

Test with a real public question and check the answer against `site.json`.
The bridge validates inputs, limits requests, and hides backend failure details.
The default limit is per process and uses the direct peer address. A production
proxy needs reviewed client-IP handling and a shared limiter store when scaling.

## Public launch and removal

Choose the domain, service identity, listener, venv, configuration, health
checks, and rollback using Webgarden's `docs/site-lifecycle.md`. Serve the app
with Gunicorn behind nginx and TLS. Use the site's working directory for
`python -m gunicorn --bind 127.0.0.1:ASSIGNED_PORT app:app`.

For removal, disable this site's public routing and bot access together,
verify both endpoints, and retain the source and bot configuration for recovery.
Record the site's actual activation and removal commands before launch.
