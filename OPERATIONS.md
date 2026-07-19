# Web Garden Operations

Safe operating notes for the OVH VPS `happys`. Commands in this document are
diagnostic unless explicitly labelled otherwise. Obtain approval before any
restart, reload, migration, package installation, DNS change, or file mutation.

## Privacy Boundary

Psyling stores private contact submissions, client records, administrative
activities, follow-up tasks, and private chat messages. Treat its database,
environment, backups, logs, and admin pages as sensitive.

Never print or paste:

- environment-file values or complete connection URLs;
- passwords, hashes, secret keys, private keys, invite tokens, or API keys;
- contact/chat message bodies, names, email addresses, or phone numbers;
- database dumps or raw request bodies.

## Site Health

Use one low-volume request and report only the status code:

```bash
curl --max-time 15 -sS -o /dev/null -w '%{http_code}\n' https://psyling.com/
curl --max-time 15 -sS -o /dev/null -w '%{http_code}\n' https://tomumber.com/
curl --max-time 15 -sS -o /dev/null -w '%{http_code}\n' https://shkolakoda.com/
curl --max-time 15 -sS -o /dev/null -w '%{http_code}\n' https://science.shkolakoda.com/
```

Expected healthy result: `200`. Do not submit forms or test private room links
against production. Check both the canonical domain and aliases only when a DNS
or certificate problem is suspected.

## Service Health

```bash
systemctl --failed --no-pager
systemctl status webgarden-psyling.service --no-pager
systemctl status tomumber.service --no-pager
systemctl status webgarden-shkolakoda.service --no-pager
systemctl status webgarden-science.service --no-pager
systemctl status postgresql@15-main.service --no-pager
```

These commands do not authorize a restart. Record the active state, main PID,
worker count, and start time before proposing runtime changes.

## nginx Checks

Inventory enabled mappings without displaying certificate private keys:

```bash
find /etc/nginx/sites-enabled -maxdepth 1 -mindepth 1 -printf '%f -> %l\n'
grep -RhnE '^[[:space:]]*(server_name|root|proxy_pass|listen|access_log|error_log)' \
  /etc/nginx/sites-enabled
```

An authorized operator can run the read-only syntax test:

```bash
sudo /usr/sbin/nginx -t
```

Do not run `reload` or `restart` as part of a check. The unprivileged account
cannot complete `nginx -t` because Let’s Encrypt certificates are restricted;
that permission error alone does not mean the active configuration is invalid.

Shkolakoda and Science must keep matching IPv4 and IPv6 listeners on their
named nginx server blocks:

```nginx
listen 80;
listen [::]:80;
listen 443 ssl;
listen [::]:443 ssl;
```

On 2026-07-09, `https://shkolakoda.com` was presenting the LAIC certificate on
IPv6 because the Shkolakoda HTTPS block had `listen 443 ssl` but no
`listen [::]:443 ssl`. Adding the IPv6 HTTP and HTTPS listen lines fixed
`shkolakoda.com`, `www.shkolakoda.com`, and `science.shkolakoda.com`.

Current intended split:

- `sites/shkolakoda` -> School of Code on `127.0.0.1:8000`.
- `sites/science` -> Happy Science on `127.0.0.1:8005`.

## Safe Log Inspection

Prefer narrow time windows, counts, and error signatures:

```bash
journalctl -u webgarden-psyling.service --since '15 minutes ago' --no-pager
journalctl -u tomumber.service --since '15 minutes ago' --no-pager
journalctl -u webgarden-shkolakoda.service --since '15 minutes ago' --no-pager
```

Before sharing output, redact URLs, query strings, addresses, identifiers, and
all private content. Avoid dumping nginx access logs: paths can contain sensitive
tokens or user-provided data. Gunicorn may label normal worker termination during
a graceful reload as `ERROR`; correlate it with the master’s HUP/reload event.

## Environment Inspection

List variable names only:

```bash
awk -F= '/^[A-Za-z_][A-Za-z0-9_]*=/{print $1}' /etc/webgarden/psyling.env
```

Do not use `cat`, `env`, `printenv`, `systemctl show -p Environment`, process
environment dumps, shell tracing, or commands that echo connection URLs.

Current protected application environment:

- psyling: `/etc/webgarden/psyling.env`
- tomumber: environment-file standardization pending
- shkolakoda: no application environment file identified
- science: no application environment file identified

## Database Checks

Use application-specific credentials and read-only SQL. Safe checks include:

- current database name and migration revision;
- schema/table names;
- aggregate row counts;
- dump archive listing and checksum validation.

Never select private columns or run broad `SELECT *`. Do not place a connection
URL directly in a command, service report, or ticket.

Psyling migration directory:

```text
/var/www/webgarden/sites/psyling/migrations
```

## Git Checks

```bash
git -C /var/www/webgarden status --short --branch
git -C /home/fluffy/projects/tomumber status --short --branch
```

Do not run destructive Git operations on production. Daycamp and `/home/fluffy`
require special cleanup plans in `TODO_WEBGARDEN.md`; ordinary reset/clean
commands are unsafe there.

## Change Checklist

Before an approved production change:

1. Confirm the site mapping in `SITES.md`.
2. Confirm a current, validated database/file backup.
3. Capture safe pre-change counts and service status.
4. Review the exact diff and migration rollback.
5. Apply one scoped change.
6. Reload only the affected service when authorized.
7. Verify public health, protected-route behavior, counts, and recent logs.
8. Record the commit, migration, backup path, verification, and rollback.
