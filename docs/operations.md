# Webgarden operations

This is the canonical read-only operations guide for the Webgarden host. It
helps an operator identify what is running before proposing a change. Site
layout is recorded in [Architecture](architecture.md); deployment and rollback
are covered in [Deployment](deployment.md).

Commands here inspect state. They do not authorize a restart, deployment,
migration, package change, permission change, or infrastructure edit.

## Safety first

- Use low-volume checks and inspect one site at a time.
- Never print environment values, connection URLs, tokens, private keys,
  cookies, database rows, form submissions, chat messages, or raw request
  bodies.
- Treat Psyling logs, uploads, database, backups, and admin routes as private.
- Prefer status codes and narrow journal windows to complete responses or logs.
- Record the effective runtime before relying on a repository template.
- A service restart is a separate, site-specific action requiring explicit
  authorization. Never restart every Webgarden service as a diagnostic step.

## Identify the source revision

The Webgarden source checkout is `/var/www/webgarden`. The application source
of truth is `main` in `evgeny-vlasov/my-web-garden`.

```bash
git -C /var/www/webgarden status --short --branch
git -C /var/www/webgarden rev-parse HEAD
git -C /var/www/webgarden remote -v
git -C /var/www/webgarden rev-parse refs/remotes/origin/main
```

These commands compare the checkout with its locally recorded remote-tracking
branch. They do not contact GitHub, so `origin/main` may itself be stale. Do not
fetch, pull, switch branches, reset, clean, or stash merely to inspect a
production problem.

Tom Umber has a separate checkout:

```bash
git -C /home/fluffy/projects/tomumber status --short --branch
git -C /home/fluffy/projects/tomumber rev-parse HEAD
git -C /home/fluffy/projects/tomumber remote -v
git -C /home/fluffy/projects/tomumber rev-list --left-right --count HEAD...origin/main
```

During the architecture audit, that checkout was clean and three commits ahead
of its recorded GitHub branch. Those commits must not be assumed to exist in a
remote backup.

## Inspect the effective service runtime

Repository unit files are useful inputs, but systemd's effective configuration
is runtime truth. Select one unit from the inventory in
[Architecture](architecture.md):

```bash
unit=webgarden-psyling.service
systemctl show "$unit" --no-pager \
  -p Id -p LoadState -p ActiveState -p SubState -p UnitFileState \
  -p FragmentPath -p DropInPaths -p User -p Group \
  -p WorkingDirectory -p ExecStart -p EnvironmentFiles \
  -p MainPID -p ExecMainStartTimestamp -p Result
systemctl status "$unit" --no-pager
```

Other active application units are:

```text
webgarden-poolemergency.service
webgarden-laic.service
webgarden-science.service
webgarden-shkolakoda.service
tomumber.service
```

Do not use `systemctl show -p Environment`, inspect `/proc/*/environ`, or turn
on shell tracing. Tom Umber currently has sensitive configuration embedded in
its unit, so do not publish its complete unit body.

## Inspect nginx routing

Live enabled configuration under `/etc/nginx` is authoritative, not the copy in
`deploy/`.

```bash
find /etc/nginx/sites-enabled -maxdepth 1 -mindepth 1 \
  -printf '%f -> %l\n' | sort
grep -RHnE \
  '^[[:space:]]*(listen|server_name|root|alias|proxy_pass)[[:space:]]' \
  /etc/nginx/sites-enabled
```

An authorized operator can perform the read-only syntax check:

```bash
sudo /usr/sbin/nginx -t
```

The unprivileged account may be unable to read restricted certificate files;
that access error does not prove the running configuration is invalid. A syntax
check does not authorize an nginx reload or restart.

## Resolve the active School of Code release

School of Code does not run from the Webgarden checkout. Inspect all three
revision signals:

```bash
git -C /var/www/webgarden rev-parse HEAD
readlink /var/www/soccl/current
readlink -f /var/www/soccl/current
cat /var/www/soccl/current/.soccl-revision
cat /var/www/soccl/current/.soccl-built-at
systemctl show webgarden-shkolakoda.service --no-pager \
  -p WorkingDirectory -p ExecStart -p User -p Group -p MainPID \
  -p ExecMainStartTimestamp
```

The resolved release directory and `.soccl-revision` should name the same full
SHA. A different checkout SHA is source-versus-production drift, not proof of a
broken deployment. See [Deployment](deployment.md#school-of-code).

## Inspect listeners and health

List loopback TCP listeners without exposing response bodies:

```bash
ss -ltn
```

Expected application endpoints are documented in
[Architecture](architecture.md). Check a single local route with a short
timeout:

```bash
curl --max-time 8 -sS -o /dev/null \
  -w 'status=%{http_code}\n' http://127.0.0.1:5001/
```

Use the applicable port: Psyling `5001`, School of Code `8000`, PoolEmergency
`8003`, LAIC `8004`, or Happy Science `8005`. Tom Umber uses a Unix socket; its
public route is the simpler non-invasive check.

Public status checks:

```bash
for url in \
  https://psyling.com/ \
  https://poolemergency.ca/ \
  https://laic.ca/ \
  https://shkolakoda.com/ \
  https://science.shkolakoda.com/ \
  https://tomumber.com/
do
  curl --max-time 15 -sS -o /dev/null \
    -w "$url status=%{http_code}\n" "$url"
done
```

Do not submit production forms or exercise private or token-bearing routes as a
health check. LAIC exposes `/health`; most other sites do not have a dedicated
health endpoint.

## Read logs without leaking private data

Use a narrow time range for the affected unit:

```bash
journalctl -u webgarden-psyling.service \
  --since '15 minutes ago' --no-pager
```

Before sharing output, remove personal data, query strings, tokens, connection
details, and user-provided content. Avoid broad nginx access-log dumps because
request paths can contain identifiers. A Gunicorn worker exit can be normal
during a deliberate graceful reload; correlate it with the master process and
timestamp.

## Inspect environment-file metadata safely

List filenames and permissions only:

```bash
find /etc/webgarden -maxdepth 1 -type f \
  -printf '%M %u:%g %f\n' | sort
```

If access allows and key names are needed, print names only for one known file:

```bash
awk -F= '/^[A-Za-z_][A-Za-z0-9_]*=/{print $1}' \
  /etc/webgarden/psyling.env
```

If access is denied, record the gap. Never work around it by changing
permissions. Do not use `cat`, `env`, `printenv`, process-environment dumps, or
commands that echo complete assignment lines.

## Detect source-versus-production drift

First identify the runtime model in [Architecture](architecture.md).

### Direct shared-checkout sites

For Psyling, PoolEmergency, LAIC, or Happy Science:

1. Inspect Git status and the checkout SHA.
2. Inspect the unit's `WorkingDirectory`, `ExecStart`, and worker start time.
3. Inspect the last commit affecting the site. Include `shared/` for Psyling and
   PoolEmergency:

   ```bash
   git -C /var/www/webgarden log -1 --format='%H %cI %s' \
     -- sites/psyling shared
   ```

4. Confirm nginx routes to the expected port and path.
5. Compare a local status-code check with the public result.

A clean checkout does not reveal what a long-running Python worker imported.
Python changes load when that site's workers start again; nginx-served static
files can change immediately. There is no deployed-SHA marker for these sites.

### School of Code

Compare checkout SHA, resolved `current` target, revision marker, effective
working directory, and public content. The active marker and symlink—not
checkout HEAD—identify production.

### Tom Umber

Inspect its separate Git status and SHA, the effective `tomumber.service`
working directory, socket, process start time, and public status. Its long-term
source of truth remains unresolved.

## Check backup job status

```bash
systemctl status webgarden-backup.timer --no-pager
systemctl status webgarden-backup.service --no-pager
systemctl list-timers webgarden-backup.timer --all --no-pager
journalctl -u webgarden-backup.service --since '7 days ago' --no-pager
```

At the audit, the daily timer existed and its last observed run succeeded. That
only shows that the job exited successfully. It does not prove that every
intended path was archived, that an archive is complete, or that restoration
works. Science coverage appears inconsistent between documentation and the
checked-in backup profiles. Installed backup tooling is protected and could not
be compared with the repository copies.

Do not inspect archive contents, database dumps, or protected manifests without
specific authorization and a privacy-safe plan.

## Before proposing a change

Record:

1. the site's runtime model and source path;
2. checkout and, where present, deployed revision;
3. effective service user, working directory, command, and start time;
4. live nginx route and listener;
5. local and public status;
6. persistent data and migration implications;
7. the site's actual deployment and rollback capabilities.

If any item is unknown, stop and investigate. Do not fill the gap with a
repository template or a command copied from another site.
