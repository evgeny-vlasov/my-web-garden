# Local AI Collective

Public-facing Flask site for Local AI Collective inside Web Garden.

## Production status

LAIC is live from this shared checkout through `webgarden-laic.service` on
`127.0.0.1:8004`. The service runs as `fluffy:www-data` and may load the
protected `/etc/webgarden/laic.env` file.

LAIC has no canonical versioned deployer, deployed-SHA marker, or code-version
rollback tool. Python changes require a separately authorized restart of this
service; nginx-served static files may change immediately. See
[Webgarden deployment](../../docs/deployment.md) and
[operations](../../docs/operations.md) before a production change.

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

## PostgreSQL Setup

> Production already uses PostgreSQL. The commands below describe initial
> provisioning; they are not routine setup, deployment, or repair steps.
> Database, environment-file, secret, schema, and permission changes require a
> separate review and explicit authorization.

Recommended names:

- Database: `laic_db`
- Role: `laic_user`

Create the role and database without printing the password:

```bash
read -rsp "New PostgreSQL password for laic_user: " LAIC_DB_PASSWORD; echo
sudo -u postgres psql <<SQL
DO \$\$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'laic_user') THEN
      CREATE ROLE laic_user LOGIN PASSWORD '${LAIC_DB_PASSWORD}';
   ELSE
      ALTER ROLE laic_user WITH LOGIN PASSWORD '${LAIC_DB_PASSWORD}';
   END IF;
END
\$\$;
SQL
unset LAIC_DB_PASSWORD
sudo -u postgres psql -tc "SELECT 1 FROM pg_database WHERE datname = 'laic_db'" | grep -q 1 || sudo -u postgres createdb --owner=laic_user laic_db
sudo -u postgres psql -d laic_db -c "REVOKE ALL ON SCHEMA public FROM PUBLIC; GRANT USAGE, CREATE ON SCHEMA public TO laic_user;"
```

Set the application environment without printing the value:

```bash
read -rsp "PostgreSQL password for laic_user: " LAIC_DB_PASSWORD; echo
sudo install -d -m 0755 /etc/webgarden
sudo touch /etc/webgarden/laic.env
sudo chmod 0600 /etc/webgarden/laic.env
sudo chown root:root /etc/webgarden/laic.env
{
  sudo grep -v "^DATABASE_URL=" /etc/webgarden/laic.env 2>/dev/null || true
  printf "%s\n" "DATABASE_URL=postgresql://laic_user:${LAIC_DB_PASSWORD}@localhost/laic_db"
} | sudo tee /etc/webgarden/laic.env.tmp >/dev/null
sudo chmod 0600 /etc/webgarden/laic.env.tmp
sudo chown root:root /etc/webgarden/laic.env.tmp
sudo mv /etc/webgarden/laic.env.tmp /etc/webgarden/laic.env
unset LAIC_DB_PASSWORD
```

Initialize the LAIC schema:

```bash
cd /var/www/webgarden/sites/laic
set -a
source /etc/webgarden/laic.env
set +a
venv/bin/python - <<'PY'
from app import app
from database import ensure_schema
ensure_schema(app.config["DATABASE_URL"])
print("LAIC schema initialized.")
PY
```

Safe verification commands:

```bash
sudo -u postgres psql -d laic_db -XAt -c "SELECT current_database(); SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_name='contact_submissions';"
curl --max-time 10 -sS -o /dev/null -w 'laic_local=%{http_code}\n' http://127.0.0.1:8004/contact
```

## Development runtime

Use an isolated development checkout and development configuration. Do not
replace the venv in the live checkout, source the protected production
environment, or bind the production port while its service is running.

```bash
cd /path/to/development-checkout/sites/laic
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
venv/bin/python -m gunicorn --bind 127.0.0.1:18004 app:app
```

## Repository infrastructure artifacts

These files are installation/reference inputs, not proof of the effective live
configuration and not a deployment procedure. Compare them with enabled nginx
and effective systemd state using the central operations guide.

- Systemd repository copy: `../../deploy/systemd/webgarden-laic.service`
- nginx repository copy: `../../deploy/nginx/laic.conf`
