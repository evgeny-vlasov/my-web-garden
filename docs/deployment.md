# Deployment

Webgarden does not currently have a general `deploy any site` command. Discover
the site's actual runtime first, then use its established path. Deployment,
service restart, database migration, and infrastructure changes are separate
operations and each requires explicit authorization.

The full source/runtime inventory is in [Architecture](architecture.md#site-inventory).
Safe status and drift checks are in [Operations](operations.md).

## Deployment decision table

| Site | Runtime model | Canonical deployment mechanism | Rollback reality |
|---|---|---|---|
| School of Code | Immutable release | `/usr/local/bin/soccl-deploy <40-character-main-SHA>` | Automatic restoration of the previously active release if activation health checks fail; old releases are retained. |
| Psyling | Direct Webgarden checkout | No canonical versioned deployer found | No deployed-SHA rollback. Restore code deliberately and account separately for database migrations and uploads. |
| PoolEmergency | Direct Webgarden checkout | No canonical versioned deployer found | No deployed-SHA rollback. Its README's old “rollback” procedure is service/nginx teardown, not version rollback. |
| LAIC | Direct Webgarden checkout | No canonical versioned deployer found | No deployed-SHA rollback found; database state requires separate planning. |
| Happy Science | Direct Webgarden checkout | No canonical versioned deployer found | No deployed-SHA rollback found. |
| Tom Umber | Separate mutable checkout | No canonical versioned deployer found | No deployed-SHA rollback found; production was three commits ahead of GitHub during the audit. |
| Keystone | Dormant | None; do not deploy without a newly reviewed production plan | None. |
| Therapist compatibility alias | Not an independent site | None; do not deploy or enable the historical service | Preserve the alias until Psyling's venv is rebuilt and verified. |

The deprecated `deploy/new_site.sh`, `deploy/setup_site.sh`, templates, and
`deploy/webgarden-ctl.sh` are not a supported production deployment path.
`webgarden-ctl.sh` is a limited historical service wrapper, not a deployer.

## Mandatory discovery before any deployment

Do this before proposing a change. These commands are read-only.

1. Identify the repository, branch, revision, remotes, and local changes:

   ```bash
   git -C /var/www/webgarden status --short --branch
   git -C /var/www/webgarden rev-parse HEAD
   git -C /var/www/webgarden remote -v
   ```

   For Tom Umber, inspect `/home/fluffy/projects/tomumber` instead.

2. Resolve the effective service runtime rather than trusting a checked-in unit:

   ```bash
   systemctl show SERVICE --no-pager \
     -p LoadState -p ActiveState -p FragmentPath -p DropInPaths \
     -p User -p Group -p WorkingDirectory -p ExecStart -p EnvironmentFiles
   ```

3. Resolve nginx routing from the enabled live configuration:

   ```bash
   find /etc/nginx/sites-enabled -maxdepth 1 -mindepth 1 \
     -printf '%f -> %l\n'
   grep -RhnE '^[[:space:]]*(server_name|root|alias|proxy_pass|listen)[[:space:]]' \
     /etc/nginx/sites-enabled
   ```

4. Identify the affected venv, database, uploads, migrations, shared code, health
   route, backup requirements, and rollback limit. List environment variable
   names only when necessary; never print values.

5. Confirm the exact authorization scope: source change, deployment, migration,
   service restart, and infrastructure change are not interchangeable approvals.

6. Record pre-change service state and a low-volume local/public health result.
   Do not restart a service merely to find out whether it is healthy.

## School of Code

School of Code has the platform's only canonical immutable-release deployer:

```text
/usr/local/bin/soccl-deploy
```

Production runs as `soccl-app` from `/var/www/soccl/current/app` through
`webgarden-shkolakoda.service` on `127.0.0.1:8000`. The `current` symlink selects
one directory under `/var/www/soccl/releases/<full-git-sha>`.

The deployer accepts exactly one full 40-character commit SHA and requires root.
For an authorized deployment, its server-side invocation is:

```bash
sudo /usr/local/bin/soccl-deploy FULL_40_CHARACTER_SHA
```

The deployer performs one release transaction:

1. It takes an exclusive deployment lock and fetches `main` into the protected
   bare repository at `/var/lib/soccl-deploy/repository.git`.
2. It verifies that the requested object is the exact supplied commit, belongs
   to the fetched current `main`, contains the School requirements file, and
   passes Git object checks.
3. It archives only `sites/shkolakoda` into a staging directory below
   `/var/www/soccl/releases`; it does not deploy from the mutable checkout.
4. It rejects application symlinks and special files, creates a fresh venv,
   installs `requirements.txt`, and runs build checks as `soccl-app` where
   appropriate.
5. It runs `python -m publishing --check` and full unit-test discovery. At the
   audit revision this was 52 tests; treat the live test count as authoritative
   if the suite changes.
6. It writes `.soccl-revision` and `.soccl-built-at`, applies the established
   root-owned read-only release permissions, and moves the completed staging
   tree to `/var/www/soccl/releases/<sha>`.
7. It atomically replaces `/var/www/soccl/current` using a temporary symlink.
8. It restarts only `webgarden-shkolakoda.service` and checks local and public
   routes, expected 404 behavior, and representative static assets.
9. If activation health fails, it atomically restores the previous `current`
   target, restarts the same service, checks rollback health, and reports the
   failed deployment. It does not delete old releases.

It does not modify nginx, certificates, Science, another systemd unit, or the
working checkout.

> Changing `/var/www/webgarden/sites/shkolakoda` and restarting systemd does not
> deploy new School of Code code. The service continues to load the release
> selected by `/var/www/soccl/current`.

To identify what is active, compare the resolved symlink and its marker:

```bash
readlink -f /var/www/soccl/current
cat /var/www/soccl/current/.soccl-revision
```

Invoke Gunicorn from a release as `venv/bin/python -m gunicorn`. Console-script
shebangs created in the staging venv can retain the staging path after the
release directory is moved.

Old releases provide rollback material, but do not improvise a manual symlink
change. The verified rollback behavior is the automatic path inside
`soccl-deploy`; any separate manual rollback requires its own reviewed and
authorized procedure.

## Direct-checkout sites

Psyling, PoolEmergency, LAIC, and Happy Science execute from the shared
`/var/www/webgarden` checkout. They do not have a comparable versioned deployer
or rollback transaction.

Operational consequences:

- Editing the checkout changes production files, but that alone is not a
  complete, verified deployment.
- Nginx-served static files may change immediately.
- Python changes normally take effect only after the affected service is
  restarted.
- A clean checkout does not prove which code a long-running worker loaded.
- There is no active-release symlink or deployed-SHA marker.
- A service restart must name only the affected site and be separately
  authorized. Never use a broad Webgarden restart.
- A Git rollback does not roll back database migrations, uploads, queued work,
  or other persistent state.
- Psyling and PoolEmergency both depend on `shared/`; changes there require
  validation for both sites.

No deployment command is documented here because no canonical one was found.
Until one exists, each proposed production change must state the exact source
revision, affected paths, validations, site-specific restart, health checks,
and rollback limits before authorization.

## Tom Umber

Tom Umber is outside the Webgarden monorepo. Its source and runtime are the same
mutable checkout at `/home/fluffy/projects/tomumber`; `tomumber.service` serves
it through `/run/tomumber/tomumber.sock`.

During the audit the deployed checkout was clean but three commits ahead of its
GitHub `main`. This does not establish that those commits are safely backed up,
and it leaves the long-term source of truth unresolved. There is no verified
canonical deployment or code-version rollback command. Resolve repository
authority and preservation before treating GitHub or the VPS checkout as a
deployment source.

## Rollback and data

Only School of Code has an automatic code-release rollback. For every other
site, “put the old files back” is incomplete when a change also affects a
database, uploads, environment configuration, or nginx/systemd state.

A daily backup timer exists and its last observed run succeeded. This does not
prove that a given site was included, that an archive is complete, or that a
restore works. Science coverage is inconsistent between current documentation
and checked-in backup profiles, and the protected installed tooling could not
be compared with the repository copies. Treat backup and restore validation as
explicit pre-deployment questions, not assumptions.
