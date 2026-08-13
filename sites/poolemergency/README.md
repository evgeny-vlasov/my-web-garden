# PoolEmergency

Public Flask site for `poolemergency.ca` inside Web Garden.

## Current Shape

- App path: `/var/www/webgarden/sites/poolemergency`
- Service name: `webgarden-poolemergency.service`
- Environment file: `/etc/webgarden/poolemergency.env`
- Local bind: `127.0.0.1:8003`
- Domains: `poolemergency.ca`, `www.poolemergency.ca`

Production runs directly from this shared checkout. PoolEmergency has no
canonical versioned deployer, deployed-SHA marker, or code-version rollback
tool. It also imports `shared/`, so changes there may affect Psyling. Python
changes require a separately authorized restart of this service; nginx-served
static files may change immediately. See
[Webgarden deployment](../../docs/deployment.md) and
[operations](../../docs/operations.md) before a production change.

The public routes render static templates:

- `/`
- `/services`
- `/about`
- `/contact`
- `/blog`

## Database Requirement

The current app initializes the shared Web Garden SQLAlchemy extension during app startup. Even though the public routes do not query the database, `DATABASE_URL` is required for the app to boot with the current shared app factory.

Recommended PostgreSQL names:

- Database: `poolemergency_db`
- Role: `poolemergency_user`

> The database and protected environment already exist in production. The
> commands below document initial provisioning; they are not routine setup or
> deployment steps. Database, secret, environment-file, and permission changes
> require a separately reviewed infrastructure change. Do not run them against
> production to diagnose an application problem.

Create the role and database without printing the password:

```bash
read -rsp "New PostgreSQL password for poolemergency_user: " POOLEMERGENCY_DB_PASSWORD; echo
export POOLEMERGENCY_DB_PASSWORD
python3 - <<'PY' | sudo -u postgres psql --set=ON_ERROR_STOP=1 >/dev/null
import os

password = os.environ["POOLEMERGENCY_DB_PASSWORD"].replace("'", "''")
print(f"""
DO $$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'poolemergency_user') THEN
      CREATE ROLE poolemergency_user LOGIN PASSWORD '{password}';
   ELSE
      ALTER ROLE poolemergency_user WITH LOGIN PASSWORD '{password}';
   END IF;
END
$$;
""")
PY
unset POOLEMERGENCY_DB_PASSWORD
sudo -u postgres psql -tc "SELECT 1 FROM pg_database WHERE datname = 'poolemergency_db'" | grep -q 1 || sudo -u postgres createdb --owner=poolemergency_user poolemergency_db
sudo -u postgres psql -d poolemergency_db -c "REVOKE ALL ON SCHEMA public FROM PUBLIC; GRANT USAGE, CREATE ON SCHEMA public TO poolemergency_user;"
```

Set the application environment without printing the value:

```bash
read -rsp "PostgreSQL password for poolemergency_user: " POOLEMERGENCY_DB_PASSWORD; echo
read -rsp "Flask SECRET_KEY for PoolEmergency: " POOLEMERGENCY_SECRET_KEY; echo
export POOLEMERGENCY_DB_PASSWORD POOLEMERGENCY_SECRET_KEY
sudo install -d -m 0755 /etc/webgarden
umask 077
tmp_env="$(mktemp)"
python3 - <<'PY' > "$tmp_env"
import os
from urllib.parse import quote

db_password = quote(os.environ["POOLEMERGENCY_DB_PASSWORD"], safe="")
secret_key = os.environ["POOLEMERGENCY_SECRET_KEY"]

print(f"SECRET_KEY={secret_key}")
print(f"DATABASE_URL=postgresql://poolemergency_user:{db_password}@localhost/poolemergency_db")
print("FLASK_ENV=production")
print("SITE_NAME=PoolEmergency")
print("SITE_DOMAIN=poolemergency.ca")
PY
sudo install -m 0600 -o root -g root "$tmp_env" /etc/webgarden/poolemergency.env
rm -f "$tmp_env"
unset POOLEMERGENCY_DB_PASSWORD POOLEMERGENCY_SECRET_KEY
sudo sed -n 's/^\([A-Za-z_][A-Za-z0-9_]*\)=.*/\1/p' /etc/webgarden/poolemergency.env
```

Initialize the schema:

```bash
cd /var/www/webgarden/sites/poolemergency
set -a
source /etc/webgarden/poolemergency.env
set +a
venv/bin/flask db upgrade
```

## Development runtime

Use an isolated development checkout and development configuration. Do not
create or replace a venv in the live checkout, read the protected production
environment file, weaken its permissions, or bind the production port while the
service is running.

```bash
cd /path/to/development-checkout/sites/poolemergency
python3 -m venv venv
venv/bin/pip install -r requirements.txt
set -a
source /path/to/development.env
set +a
venv/bin/python -m gunicorn --workers 2 --bind 127.0.0.1:18003 app:app
```

Smoke test:

```bash
for path in / /services /about /contact /blog; do
  curl --max-time 10 -sS -o /dev/null -w "poolemergency_local ${path} %{http_code}\n" "http://127.0.0.1:18003${path}"
done
```

## Historical initial provisioning

> The following records how the service and nginx site were initially
> installed. It is not a current deployment or rollback procedure. Do not copy
> these files over live configuration or reload services without a separately
> reviewed infrastructure change. Effective systemd and enabled live nginx
> configuration are runtime authority.

- Systemd repository copy: `../../deploy/systemd/webgarden-poolemergency.service`
- nginx repository copy: `../../deploy/nginx/poolemergency.ca`
- Checked-in backup profile: `../../webgarden-backup/sites.d/poolemergency.conf`

Install the systemd unit only after local boot succeeds:

```bash
sudo cp /var/www/webgarden/deploy/systemd/webgarden-poolemergency.service /etc/systemd/system/webgarden-poolemergency.service
sudo systemctl daemon-reload
sudo systemctl enable --now webgarden-poolemergency.service
sudo systemctl status webgarden-poolemergency.service --no-pager
```

Install nginx only after the service responds locally:

```bash
sudo cp /var/www/webgarden/deploy/nginx/poolemergency.ca /etc/nginx/sites-available/poolemergency.ca
sudo ln -s /etc/nginx/sites-available/poolemergency.ca /etc/nginx/sites-enabled/poolemergency.ca
sudo nginx -t
sudo systemctl reload nginx
```

Do not change DNS or Cloudflare until the origin is verified locally and through nginx.

After DNS is fixed and both names resolve to this server, issue the certificate:

```bash
sudo certbot --nginx -d poolemergency.ca -d www.poolemergency.ca
```

## Historical teardown (not rollback)

> **Do not run these commands to roll back code.** They disable the application
> and remove its live systemd and nginx configuration. PoolEmergency currently
> has no documented version rollback mechanism; plan one before an approved
> production change. The commands are retained only as an initial-provisioning
> removal record.

```bash
sudo systemctl disable --now webgarden-poolemergency.service
sudo rm -f /etc/systemd/system/webgarden-poolemergency.service
sudo systemctl daemon-reload
sudo rm -f /etc/nginx/sites-enabled/poolemergency.ca
sudo rm -f /etc/nginx/sites-available/poolemergency.ca
sudo nginx -t
sudo systemctl reload nginx
```
