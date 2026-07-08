# Web Garden Site Inventory

Canonical production inventory for the OVH VPS `happys`.

Last reviewed: 2026-07-08. This file records deployment ownership and recovery
requirements; it does not contain credentials or private application data.

## Sites

| Domain | Status | Routing | nginx config | Service | Application path | Database | Environment | Repository / remote | Backup needs | Notes / risk |
|---|---|---|---|---|---|---|---|---|---|---|
| `psyling.com`, `www.psyling.com` | Live, production-sensitive | nginx proxies HTTPS traffic to `127.0.0.1:5001`; Cloudflare may be involved for some records | `/etc/nginx/sites-available/psyling.com` -> enabled | `webgarden-psyling.service` | `/var/www/webgarden/sites/psyling` (compatibility symlink: `/var/www/webgarden/sites/therapist`) | PostgreSQL `therapist_db` | `/etc/webgarden/psyling.env` | `/var/www/webgarden`; `git@github.com:evgeny-vlasov/my-web-garden.git` | PostgreSQL custom dump, source, migrations, protected env, nginx/systemd, uploads, and restore-test validation | Contains private CRM, client, activity, and chat data. Do not expose database rows, raw logs, env contents, or upload contents. |
| `shkolakoda.com`, `www.shkolakoda.com`, `science.shkolakoda.com` | Live | nginx proxies HTTPS traffic to `127.0.0.1:8000`; HTTP unknown/default fallback redirects to `https://shkolakoda.com/` | `/etc/nginx/sites-available/shkolakoda.com` and `/etc/nginx/sites-available/default-shkolakoda.conf` -> enabled | `webgarden-shkolakoda.service` | `/var/www/webgarden/sites/shkolakoda` | None | No application env file identified; service supplies venv `PATH` | `/var/www/webgarden`; `git@github.com:evgeny-vlasov/my-web-garden.git` | Source plus nginx/systemd/default fallback artifacts through Web Garden backups | Small static Flask site. Keep `daycamp` references as legacy only if encountered in old configs/docs. |
| `laic.ca`, `www.laic.ca` | Live | nginx proxies HTTPS traffic to `127.0.0.1:8004` | `/etc/nginx/sites-available/laic.ca` -> enabled | `webgarden-laic.service` | `/var/www/webgarden/sites/laic` | PostgreSQL `laic_db` | `/etc/webgarden/laic.env` | `/var/www/webgarden`; `git@github.com:evgeny-vlasov/my-web-garden.git` | Source, protected env, nginx/systemd, and PostgreSQL contact submissions through Web Garden backups | Public Local AI Collective site. Older Love Sugar & Dough demo routes are example/archive content only. |
| `poolemergency.ca`, `www.poolemergency.ca` | Live | nginx proxies HTTPS traffic to `127.0.0.1:8003` | `/etc/nginx/sites-available/poolemergency.ca` -> enabled | `webgarden-poolemergency.service` | `/var/www/webgarden/sites/poolemergency` | PostgreSQL `poolemergency_db` | `/etc/webgarden/poolemergency.env` | `/var/www/webgarden`; `git@github.com:evgeny-vlasov/my-web-garden.git` | Source, protected env, nginx/systemd, PostgreSQL contact submissions, and uploads if present | Small PVC/vinyl pool liner repair site. Do not publish the internal email address. |
| `tomumber.com`, `www.tomumber.com` | Live | nginx proxies HTTPS traffic to Unix socket `/run/tomumber/tomumber.sock` | `/etc/nginx/sites-available/tomumber.com` -> enabled | `tomumber.service` | `/home/fluffy/projects/tomumber` | PostgreSQL `tomumber`; legacy `/home/fluffy/projects/tomumber/instance/tomumber.sqlite` | Connection currently embedded in systemd; proposed `/etc/webgarden/tomumber.env` | `git@github.com:evgeny-vlasov/tomumber.git` | PostgreSQL custom dump, uploads, repository, protected service config, and legacy SQLite preservation | Move the connection setting out of the unit and rotate its credential in a separately approved change. No database migration/version table currently identified. |
| `poolemergency.com`, `www.poolemergency.com` | External/parked | Afternic nameservers and external parking addresses | None | None | None | None | None | None | None until ownership and intended use are confirmed | Not the local poolemergency application. |
| `keystonehardscapes.ca` | Dormant/not deployed | Domain reportedly inactive or unavailable | None | None | `/var/www/webgarden/sites/keystone` | None found | None found | Included in Web Garden repository | Repository coverage is sufficient while dormant; preserve any separately supplied assets | Source includes an Alembic migration but has no venv, dedicated requirements, nginx, service, env, or live database. Do not deploy unless the domain/product is revived. |
| SugarDough / Love Sugar & Dough | Standalone source missing; demo content only | No standalone live site identified | None | None | No standalone application source found in Web Garden; LAIC has archived demo/example routes | None | None | None identified | None until source or ownership is recovered | Treat any LAIC SugarDough material as portfolio/demo content, not an active product. |

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
