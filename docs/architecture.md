# Webgarden architecture

Last verified against the running VPS: 2026-08-13.

Webgarden is a small collection of Flask websites hosted on one VPS. Its
authoritative application repository is
[`evgeny-vlasov/my-web-garden`](https://github.com/evgeny-vlasov/my-web-garden),
branch `main`; the primary checkout is `/var/www/webgarden`.

It is not one uniform runtime. Some sites run directly from that checkout,
School of Code runs from an immutable release, and Tom Umber has a separate
checkout. Repository `HEAD` therefore does not, by itself, identify the code a
site is serving.

## Request flow

```text
public HTTPS request
  -> nginx terminates TLS and selects the domain
  -> nginx proxies to a loopback TCP port or Unix socket
  -> a site-specific systemd unit manages Gunicorn
  -> Gunicorn imports the site's Flask application from its runtime directory
  -> the application may use PostgreSQL, uploads, or file-backed content
```

Live files under `/etc/nginx` and effective systemd properties are runtime
truth. Checked-in nginx and systemd files may be templates, installation
sources, or historical copies; compare them with the live system before using
them. See [Operations](operations.md) for safe inspection commands.

## Three runtime models

### 1. Direct shared-checkout runtime

Psyling, PoolEmergency, LAIC, and Happy Science run from directories below
`/var/www/webgarden/sites`. The checkout is both their development/source tree
and their production runtime.

This model is mutable. Nginx-served static files can change as soon as files in
the checkout change. Python changes are normally loaded only when the affected
worker is restarted. There is no deployed-SHA marker, so a clean Git tree does
not prove which revision a long-running worker imported.

### 2. Immutable release runtime

School of Code runs from `/var/www/soccl/current/app`, where `current` is a
symlink to `/var/www/soccl/releases/<full-git-sha>`. It has a release-local
virtual environment and revision markers. The monorepo checkout is its source,
not its production runtime. Its deployment process is documented once in
[Deployment](deployment.md#school-of-code).

### 3. Separate mutable checkout

Tom Umber runs from `/home/fluffy/projects/tomumber`, a repository outside the
Webgarden monorepo. During the audit its deployed checkout was clean but three
commits ahead of its GitHub `main`. Those commits must not be assumed to be
backed up; its long-term source of truth remains unresolved.

## Isolation and shared dependencies

Each live site has a distinct nginx mapping, systemd unit, local port or socket,
and virtual environment. Sites with application configuration generally have a
separate protected environment file or unit configuration. Database-backed
sites use site-specific databases.

This is useful process isolation, not complete security isolation. Psyling,
PoolEmergency, LAIC, Happy Science, and Tom Umber currently run as `fluffy`;
School of Code uses the dedicated `soccl-app` user. Several services can
therefore read or modify files owned by the same account.

Psyling and PoolEmergency both import `shared/`. A change there can affect both
sites and must be reviewed and validated in both contexts.

`sites/therapist` is a historical symlink to Psyling, but it is still
runtime-significant: Psyling's current virtual-environment console scripts have
shebangs that reference that path. Do not remove the alias until the Psyling
environment has been rebuilt from its canonical path and verified. The old
therapist service is disabled and must not be enabled; it would conflict with
Psyling's port.

## Site inventory

Environment-file values were not inspected during the audit. Database names
below are recorded only where documentation or a safe live check established
them.

| Site/domain | Source | Production runtime and venv | Unit and identity | Live nginx / upstream | Environment | Persistent data / status |
|---|---|---|---|---|---|---|
| Psyling — `psyling.com`, `www` | `sites/psyling` and `shared/` | `/var/www/webgarden/sites/psyling`; `sites/psyling/venv` | `webgarden-psyling.service`; `fluffy:fluffy` | Enabled `psyling.com` config → `127.0.0.1:5001` | Required `/etc/webgarden/psyling.env` | PostgreSQL `therapist_db`; private CRM/chat/contact data; upload location depends on protected configuration. Live. |
| PoolEmergency — `poolemergency.ca`, `www` | `sites/poolemergency` and `shared/` | `/var/www/webgarden/sites/poolemergency`; `sites/poolemergency/venv` | `webgarden-poolemergency.service`; `fluffy:fluffy` | Enabled `poolemergency.ca` config → `127.0.0.1:8003` | Required `/etc/webgarden/poolemergency.env` | PostgreSQL required; documented database `poolemergency_db`; uploads may exist. Live. |
| LAIC — `laic.ca`, `www` | `sites/laic` | `/var/www/webgarden/sites/laic`; `sites/laic/venv` | `webgarden-laic.service`; `fluffy:www-data` | Enabled `laic.ca` config → `127.0.0.1:8004` | Optional `/etc/webgarden/laic.env` | Live `/health` reported PostgreSQL; documentation names `laic_db`; an ignored local fallback area also exists. Live. |
| Happy Science — `science.shkolakoda.com` | `sites/science` | `/var/www/webgarden/sites/science`; `sites/science/venv` | `webgarden-science.service`; `fluffy:www-data` | Enabled `science.shkolakoda.com` config → `127.0.0.1:8005` | None identified | No database or application data store identified. Live. |
| School of Code — `shkolakoda.com`, `www` | `sites/shkolakoda` on monorepo `main` | `/var/www/soccl/current/app`; `/var/www/soccl/current/venv` | `webgarden-shkolakoda.service`; `soccl-app:www-data` | Enabled `shkolakoda.com` and default configs → `127.0.0.1:8000`; static root also follows `current` | None identified | File-backed public content in an immutable release. Live. |
| Keystone — `keystonehardscapes.ca` | `sites/keystone` and `shared/` | None | None | No enabled config or upstream | None found | Source only; no live database, venv, service, or nginx mapping found. Dormant. |
| Therapist compatibility alias | `sites/therapist -> psyling` | No independent application; affects current Psyling venv shebangs | Historical `webgarden-therapist.service` is disabled | No independent config/upstream; old service would collide with `5001` | Legacy env file exists but is not the Psyling authority | Historical but runtime-significant compatibility path; do not remove or enable casually. |
| Tom Umber — `tomumber.com`, `www` | Separate `/home/fluffy/projects/tomumber` repository | Same mutable checkout; `/home/fluffy/projects/tomumber/venv` | `tomumber.service`; `fluffy:www-data` | Enabled `tomumber.com` config → `/run/tomumber/tomumber.sock` | Database connection currently embedded in the protected unit, not a standard Webgarden env file | PostgreSQL `tomumber`, uploads, and a preserved legacy SQLite file. Live; source-of-truth gap remains. |

`poolemergency.com` is externally parked and is not the local PoolEmergency
application. SugarDough material is archived LAIC demonstration content, not a
separate runtime. Plantfriend is an incomplete local artifact, not a deployed
site.

## Configuration and data boundaries

- Live nginx configuration is under `/etc/nginx`; enabled site links determine
  active routing.
- Effective systemd configuration, including drop-ins, determines the runtime
  user, working directory, command, and environment sources.
- Protected application configuration is under `/etc/webgarden` where used.
  Never print complete values or connection URLs.
- School of Code's active release is the resolved `/var/www/soccl/current`
  target plus its `.soccl-revision` marker.
- PostgreSQL databases, uploads, and instance directories are persistent data;
  they are not interchangeable with application source or a code release.

A daily backup timer exists and its last observed run succeeded. That fact does
not establish archive completeness or restore validity. Science coverage is
inconsistent between documentation and checked-in backup profiles, and the
installed protected backup tooling could not be compared with the repository
copies.

## What is deliberately not unified

There is no supported command that deploys every Webgarden site. The generic
scripts under `deploy/` are deprecated on the current host. School of Code has
a mature release transaction; the direct-checkout sites and Tom Umber do not.
That difference should remain visible until replacement tooling, validation,
and rollback behavior are explicitly designed and approved.
