# Troubleshooting

Start with inspection. A restart can hide evidence, load unreviewed checkout
changes, or affect the wrong site. Do not restart nginx, PostgreSQL, or multiple
Webgarden services as a general diagnostic step.

The commands below are read-only. They do not authorize deployment, restart,
migration, permission changes, or edits to live configuration. See
[Operations](operations.md) for privacy and log-handling rules and
[Architecture](architecture.md) for the site inventory.

## Public site returns 502

A 502 usually means nginx cannot reach the configured upstream or the upstream
closed the request.

1. Record the public result without printing the response:

   ```bash
   curl --max-time 15 -sS -o /dev/null \
     -w 'status=%{http_code}\n' https://example.com/
   ```

2. Inspect the domain's enabled nginx route:

   ```bash
   grep -RHnE \
     '^[[:space:]]*(server_name|root|alias|proxy_pass)[[:space:]]' \
     /etc/nginx/sites-enabled
   ```

3. Inspect the named unit and its effective runtime:

   ```bash
   systemctl show webgarden-EXAMPLE.service --no-pager \
     -p ActiveState -p SubState -p Result -p MainPID \
     -p User -p Group -p WorkingDirectory -p ExecStart \
     -p EnvironmentFiles -p ExecMainStartTimestamp
   systemctl status webgarden-EXAMPLE.service --no-pager
   ```

4. Check listeners and the expected local route:

   ```bash
   ss -ltn
   curl --max-time 8 -sS -o /dev/null \
     -w 'status=%{http_code}\n' http://127.0.0.1:PORT/
   ```

5. Inspect a narrow journal window for that unit:

   ```bash
   journalctl -u webgarden-EXAMPLE.service \
     --since '15 minutes ago' --no-pager
   ```

Redact personal data and connection details before sharing output. Determine
whether the failure is the process, listener, permissions, or routing before
proposing a site-specific restart.

## The wrong application or stale code appears

First identify the site's runtime model in [Architecture](architecture.md).

For direct-checkout sites:

```bash
git -C /var/www/webgarden status --short --branch
git -C /var/www/webgarden rev-parse HEAD
systemctl show webgarden-EXAMPLE.service --no-pager \
  -p WorkingDirectory -p ExecStart -p MainPID -p ExecMainStartTimestamp
```

Python code remains loaded in existing workers until that site's process starts
again. Nginx-served static files may reflect checkout changes immediately. A
clean tree does not prove which revision a long-running process imported, and
there is no deployed-SHA marker for direct-checkout sites.

For School of Code, follow
[School of Code checkout changed but production did not](#school-of-code-checkout-changed-but-production-did-not).

For Tom Umber, inspect `/home/fluffy/projects/tomumber`, not the Webgarden
checkout. During the audit it was three commits ahead of its recorded GitHub
branch.

## A service fails to start

Capture systemd's reason and the first relevant application error:

```bash
unit=webgarden-EXAMPLE.service
systemctl show "$unit" --no-pager \
  -p LoadState -p ActiveState -p SubState -p Result -p ExecMainStatus \
  -p User -p Group -p WorkingDirectory -p ExecStart -p EnvironmentFiles
systemctl status "$unit" --no-pager
journalctl -u "$unit" --since '15 minutes ago' --no-pager
```

Then compare the effective working directory and executable with what actually
exists:

```bash
namei -l /path/from/WorkingDirectory
test -x /path/to/venv/bin/python && printf 'python executable present\n'
sed -n '1p' /path/to/venv/bin/gunicorn
```

Do not repair permissions, recreate a venv, install packages, or edit a unit
while diagnosing. A venv console-script shebang can reveal an obsolete path;
School of Code deliberately starts Gunicorn with `venv/bin/python -m gunicorn`
because release venv console scripts may retain staging paths.

## Database configuration failure

Typical evidence includes an application boot error, connection refusal, or a
missing required variable. Do not print the connection URL.

```bash
systemctl status postgresql@15-main.service --no-pager
systemctl show webgarden-EXAMPLE.service --no-pager \
  -p ActiveState -p Result -p EnvironmentFiles
find /etc/webgarden -maxdepth 1 -type f \
  -printf '%M %u:%g %f\n' | sort
```

If access permits, list only key names in the one relevant file:

```bash
awk -F= '/^[A-Za-z_][A-Za-z0-9_]*=/{print $1}' \
  /etc/webgarden/EXAMPLE.env
```

If access is denied, record that fact. Never change permissions, `cat` the
file, inspect a process environment, paste a database URL into a command, or
query private rows. Database migration and credential changes require separate
plans and authorization.

## Nginx and application paths disagree

Compare live nginx with effective systemd state:

```bash
grep -nE \
  '^[[:space:]]*(listen|server_name|root|alias|proxy_pass)[[:space:]]' \
  /etc/nginx/sites-enabled/EXAMPLE
systemctl show webgarden-EXAMPLE.service --no-pager \
  -p WorkingDirectory -p ExecStart -p User -p Group
readlink -f /path/used/by/nginx
readlink -f /path/used/by/systemd
```

Repository files in `deploy/nginx/` and `deploy/systemd/` may be templates,
installation inputs, or stale artifacts. Do not edit either copy until the
conflict is understood. Live enabled nginx and effective systemd configuration
describe what the host currently runs.

For School of Code, both nginx static paths and systemd must resolve through
`/var/www/soccl/current`, not `/var/www/webgarden/sites/shkolakoda`.

## School of Code checkout changed but production did not

This is expected under its immutable-release model. Changing the checkout and
restarting systemd does not deploy the checkout; the unit continues to load the
release selected by `/var/www/soccl/current`.

```bash
git -C /var/www/webgarden rev-parse HEAD
readlink -f /var/www/soccl/current
cat /var/www/soccl/current/.soccl-revision
systemctl show webgarden-shkolakoda.service --no-pager \
  -p WorkingDirectory -p ExecStart -p ExecMainStartTimestamp
```

If a new revision is intended, stop troubleshooting and follow the one
canonical process in [Deployment](deployment.md#school-of-code). Do not point
`current` at the checkout or manually copy changed files into a release.

## School deployment health check failed

`/usr/local/bin/soccl-deploy` checks the new release after activation and is
designed to restore the previous `current` target automatically when activation
health fails.

After the deployer exits, inspect rather than improvising a repair:

```bash
readlink -f /var/www/soccl/current
cat /var/www/soccl/current/.soccl-revision
cat /var/www/soccl/current/.soccl-built-at
systemctl status webgarden-shkolakoda.service --no-pager
journalctl -u webgarden-shkolakoda.service \
  --since '30 minutes ago' --no-pager
```

Record the requested SHA, exit status, current release, service result, and
local/public status codes. Access to the protected deployment log may be
denied; record the gap instead of loosening permissions. Do not delete a failed
release, edit an immutable release, change the symlink manually, or attempt a
second deployment until the first result is understood.

## Source and runtime disagree

Use this order:

1. Identify the domain in the site matrix in
   [Architecture](architecture.md#site-inventory).
2. Inspect the live nginx upstream or document root.
3. Inspect the effective unit's user, working directory, executable, and start
   time.
4. Resolve any runtime symlink.
5. Inspect the relevant Git checkout, branch, SHA, and status.
6. For School of Code, compare `current` and `.soccl-revision`.
7. Compare local and public status codes.

Classify the result before taking action:

- **Expected release difference:** School source is newer than its active
  immutable release.
- **Loaded-process difference:** a direct-checkout worker predates a Python
  change.
- **Static-file difference:** nginx is reading changed files immediately from a
  mutable checkout.
- **Routing difference:** nginx and systemd point at different paths or
  listeners.
- **Source-of-truth gap:** the production checkout contains commits absent from
  the expected remote, as observed for Tom Umber during the audit.

Deployment, restart, rollback, and infrastructure repair are different actions.
Once the disagreement is classified, obtain authorization for the smallest
site-specific action supported by [Deployment](deployment.md).
