# Web Garden Housekeeping Plan

Planning document only. Every item below requires a separately reviewed and
approved implementation step. Do not combine source-control repair, credential
rotation, backup installation, deployment, and DNS changes into one operation.

## Urgent

### 1. Establish application-level backups

- Back up PostgreSQL `therapist_db` and `tomumber` nightly with custom-format
  `pg_dump` archives and validate each archive with `pg_restore --list`.
- Encrypt backups before sending them off the VPS. OVH provider snapshots remain
  a second layer, not the application-level restore mechanism.
- Include protected environment files, repositories, migrations, nginx site
  definitions, systemd units, and non-reproducible uploads.
- Treat psyling CRM/chat backups as private data with restricted access and an
  explicit retention/deletion policy.
- Preserve Tomumber’s legacy SQLite file once, separately from the live
  PostgreSQL backup.
- Suggested retention: 7 daily, 5 weekly, 12 monthly, subject to privacy review.
- Alert when the latest successful offsite backup is older than 26 hours.
- Perform and document an isolated restore test at least quarterly.
- Select and approve an encrypted offsite tool/target. Restic, Borg, Rclone, and
  rsync are not currently installed.

### 2. Protect shkolakoda source

Do not clean or reset the live directory in place.

1. Capture a read-only inventory and verified archive/copy of the entire current
   source tree before changing Git metadata.
2. Identify which current files are actual source and which are venv, caches,
   bytecode, or generated artifacts.
3. Build a clean candidate repository in a separate staging directory.
4. Add a `.gitignore` that excludes `venv`, caches, bytecode, local environments,
   logs, and generated files.
5. Commit only reviewed source, templates, static assets, requirements, and safe
   deployment documentation.
6. Create a private remote and verify clone/rebuild in an isolated directory.
7. Compare the staged app with production before considering any switch.
8. Do not move the live path or restart `webgarden-shkolakoda.service` during
   source-control cleanup unless separately approved.

### 3. Resolve accidental `/home/fluffy/.git`

Do not delete `/home/fluffy/.git` yet.

1. Record whether it contains commits, branches, remotes, stashes, or unique
   objects not present elsewhere.
2. Create a restricted backup of the `.git` metadata only.
3. Verify that no intended project relies on the home-level repository.
4. Review nested repositories and ensure their metadata is independent.
5. With explicit approval, remove only the accidental home-level `.git`
   directory—not home files or nested project repositories.
6. Re-run repository discovery and confirm no sensitive home content is tracked.

## Next

### 4. Standardize Tomumber environment handling

1. Back up the current unit definition and PostgreSQL database.
2. Create `/etc/webgarden/tomumber.env`, owned by the appropriate operator and
   mode `600`, containing the required variable names and values.
3. Update `tomumber.service` to use `EnvironmentFile=` and remove the embedded
   connection setting.
4. Rotate the database credential because it has been stored in unit text.
5. Use a least-privilege database role and verify access before reload.
6. Run `systemd-analyze verify`, daemon-reload, and service reload/restart only in
   an approved maintenance step with rollback commands.
7. Verify Tomumber HTTP health, uploads, login behavior, and safe row counts.

### 5. Repair poolemergency routing/origin

1. Confirm that `poolemergency.ca` is the intended production domain and that
   the current Cloudflare zone is under control.
2. Inspect Cloudflare DNS/origin settings without changing them; identify the
   origin responsible for HTTP 530.
3. Decide whether the application should be restored elsewhere or deployed on
   `happys`.
4. Complete and review the source: requirements, configuration, environment,
   database needs, templates, error handling, and privacy boundaries.
5. Build and test in isolation with a non-public host binding.
6. Add backup coverage before production data is accepted.
7. Add systemd and nginx only after application approval; validate TLS locally.
8. Change Cloudflare origin/DNS last, with a rollback target and low TTL plan.
9. Keep `poolemergency.com` separate unless ownership and intended use are
   confirmed; it currently appears parked at Afternic.

### 6. Restore laic.ca from GitHub

1. Obtain the exact repository URL, owner, access method, and production branch.
   No public LAIC repository was found under the known GitHub account.
2. Determine what is missing from Git: database, user uploads, generated assets,
   environment settings, mail configuration, and deployment definitions.
3. Recover any available exports/backups from the dead server or provider.
4. Review the code and dependency versions offline before running it.
5. Create a dedicated path, venv, least-privilege database, protected env file,
   systemd service, and backup policy.
6. Restore and test on an isolated local binding; validate content and security.
7. Add nginx and obtain TLS only after application verification.
8. Repoint DNS away from the dead address last. Document the prior records and
   rollback plan before the change.

### 7. Psyling operational follow-up

- Investigate the logged missing `email_validator` dependency in a scoped change.
- Do not expose CRM/chat records while reproducing the issue.
- Keep migration/backup verification mandatory for future CRM changes.

## Later

- Standardize application manifests, service names, environment paths, health
  checks, and deployment templates without moving live apps prematurely.
- Add monitoring for site status, systemd state, certificate expiry, backup age,
  disk usage, PostgreSQL health, and restore-test age.
- Decide whether Tomumber should adopt a formal migration system.
- Review upload-directory permissions and retention per application.
- Review the orphaned Plantfriend venv and retain or remove it in a separate,
  backed-up housekeeping step.
- Create a Sites dashboard/portfolio only after inventory and backups are stable.
- Create a separate documented backup policy for `/opt/bedrock` game worlds.

## Low Priority

### Keystone

The source remains in the Web Garden repository, but the intended domain is no
longer registered and there is no runtime deployment. Keep it dormant. Do not
create a service, database, nginx configuration, certificate, or backup job
beyond repository coverage unless the project/domain is explicitly revived.

## Approval Gates

Separate approval is required before any of the following:

- deleting or moving files or Git metadata;
- installing backup software;
- creating credentials, databases, users, services, or environment files;
- changing systemd/nginx/Cloudflare/DNS;
- restarting or reloading services;
- running migrations or restoring production data.
