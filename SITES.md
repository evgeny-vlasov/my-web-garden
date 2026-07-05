# Web Garden Site Inventory

Canonical production inventory for the OVH VPS `happys`.

Last reviewed: 2026-07-05. This file records deployment ownership and recovery
requirements; it does not contain credentials or private application data.

## Sites

| Domain | Status | Routing | nginx config | Service | Application path | Database | Environment | Repository / remote | Backup needs | Notes / risk |
|---|---|---|---|---|---|---|---|---|---|---|
| `psyling.com`, `www.psyling.com` | Healthy, production-sensitive | Cloudflare is involved for at least the `www` route; apex reaches this VPS | `/etc/nginx/sites-available/psyling.com` → enabled | `webgarden-therapist.service` | `/var/www/webgarden/sites/therapist` | PostgreSQL `therapist_db` | `/etc/webgarden/therapist.env` | `/var/www/webgarden`; `git@github.com:evgeny-vlasov/my-web-garden.git` | Nightly encrypted PostgreSQL dump; repository, migrations, protected environment, and upload backup; regular restore test | Contains private CRM, client, activity, and chat data. Do not expose database rows or raw logs. nginx access logging is disabled. |
| `tomumber.com`, `www.tomumber.com` | Healthy | DNS reaches this VPS directly | `/etc/nginx/sites-available/tomumber.com` → enabled | `tomumber.service` | `/home/fluffy/projects/tomumber` | PostgreSQL `tomumber`; legacy `/home/fluffy/projects/tomumber/instance/tomumber.sqlite` | Connection currently embedded in systemd; proposed `/etc/webgarden/tomumber.env` | `git@github.com:evgeny-vlasov/tomumber.git` | Nightly encrypted PostgreSQL dump; uploads, repository, protected environment, and one-time preservation of legacy SQLite | Move the connection setting out of the unit and rotate its credential in a separately approved change. No database migration/version table currently exists. |
| `shkolakoda.com`, `www.shkolakoda.com`, `science.shkolakoda.com` | Healthy | DNS reaches this VPS directly; all three names serve the same app | `/etc/nginx/sites-available/daycamp` → enabled | `daycamp.service` | `/home/fluffy/projects/daycamp` | None found | No application env file found; service supplies venv `PATH` | Local unsafe/unborn repository; no remote found | Preserve source immediately, then establish a clean private repository; back up nginx and systemd definitions | Production source control is unsafe: venv/generated files are staged or tracked and there is no reliable commit history. Do not clean it in place without a verified copy. |
| `poolemergency.ca`, `www.poolemergency.ca` | Broken, not deployed here | Cloudflare; HTTP 530 indicates an unresolved/unreachable origin | None | None | Undeployed scaffold at `/var/www/webgarden/sites/poolemergency` | None found | None found | Included in Web Garden repository | Back up source through Web Garden; after deployment add DB/uploads/env and restore testing as applicable | Confirm intended origin before changing Cloudflare. Local source has no dedicated venv or requirements file. |
| `poolemergency.com`, `www.poolemergency.com` | External/parked | Afternic nameservers and external parking addresses | None | None | None | None | None | None | None until ownership and intended use are confirmed | Not the local poolemergency application. |
| `laic.ca`, `www.laic.ca` | Broken/external; restoration required | Resolves to the dead former server address, not this VPS | None | None | None | None known | None | Exact GitHub repository/branch still required; no public LAIC repository found under the known owner | After source recovery: code, content/assets, DB, uploads, protected env, deployment config, and restore test | Do not repoint DNS until an isolated restoration is reviewed and tested. GitHub may not contain database, uploads, or secrets. |
| `keystonehardscapes.ca` | Missing/not deployed; low priority | Domain currently has no DNS records and is reportedly no longer registered | None | None | `/var/www/webgarden/sites/keystone` | None found | None found | Included in Web Garden repository | Repository coverage is sufficient while dormant; preserve any separately supplied assets | Source includes an Alembic migration but has no venv, dedicated requirements, nginx, service, env, or live database. Do not deploy unless the domain/product is revived. |

## Other Local Project Artifacts

| Path | Classification | Action |
|---|---|---|
| `/home/fluffy/projects/plantfriend` | Orphaned/incomplete: venv only | Do not treat as a deployable site. Review later before retaining or removing. |
| `/var/www/html` | nginx package/default document directory | Not an active site in the current enabled-site inventory. |
| `/opt/bedrock` | Separate non-Web-Garden game-server workload | Maintain a separate backup and operations policy; do not mix private web-app backups with game-world retention. |

## Canonical Mapping Rules

1. Every production domain must map to exactly one nginx configuration, service,
   application directory, environment file, database (if any), repository, and
   backup policy in this document.
2. Credentials belong in protected environment files, never in this inventory,
   Git, systemd command text, or shell history.
3. A source directory is not considered deployed unless nginx, systemd, runtime,
   environment, and health-check ownership are all documented.
4. Update this file in the same reviewed change that adds, moves, retires, or
   restores a site.
