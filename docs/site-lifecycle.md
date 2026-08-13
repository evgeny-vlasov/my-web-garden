# Site lifecycle

Webgarden does not currently have a supported command that safely provisions
and deploys any new site. The generic scripts under `deploy/` are deprecated
and do not match this host's current users, paths, ports, or runtime models.
Treat them as historical material, not a production workflow.

This guide describes the decisions that must be explicit before a small site is
added. It is intentionally a checklist, not a promise of automated setup.

## Start with the site's contract

Write down one answer for every row before creating production configuration:

| Decision | Required answer |
|---|---|
| Source | Repository and path; for the monorepo, normally `sites/<site>` on `main` |
| Domain | Canonical hostname, aliases, and DNS owner |
| Runtime | Static files, Flask/Gunicorn over loopback TCP, or a Unix socket |
| Identity | Dedicated or shared Unix user and group, chosen deliberately |
| Listener | A confirmed-unused loopback port or a private socket path |
| Python | Virtual-environment location and requirements source |
| Configuration | Protected environment-file path, or an explicit statement that none is needed |
| Persistent data | Database, migrations, uploads, ownership, privacy, and retention |
| Process | One named systemd unit and its working directory |
| Routing | One nginx server block, static aliases, TLS names, and upstream |
| Health | A harmless local check and a public check |
| Backups | Exact data and configuration included, plus how restoration is validated |
| Deployment | How a reviewed source revision becomes the running revision |
| Rollback | How code, migrations, and persistent data return to a known state |
| Ownership | Who may approve deployment, restart, migration, DNS, and infrastructure changes |

Do not assign a port by copying an old README. Compare the intended listener
with the live system first. Do not silently reuse `fluffy`; Unix-user isolation
is already incomplete and each new choice should be conscious.

## Choose a source and runtime model

The authoritative Webgarden application branch is `main` in
`evgeny-vlasov/my-web-garden`. A small site can live in the monorepo when its
ownership and dependencies fit. A separate repository must have an equally
clear source-of-truth and backup story.

Current production uses three runtime models, described in
[Architecture](architecture.md): direct shared checkout, an immutable release
for School of Code, and Tom Umber's separate mutable checkout. None is an
automatic default for a new site.

Decide how the site will be deployed before launch. There is no canonical
versioned deployment tool for Psyling, PoolEmergency, LAIC, Happy Science, or
Tom Umber that can simply be reused. School of Code's deployer is specific to
that application and must not be generalized by assumption.

## Keep application boundaries clear

- Give the site its own systemd unit, listener, venv, and nginx mapping.
- Give it its own database and configuration when it stores data.
- Use a dedicated Unix identity when justified; otherwise document the shared
  identity and its consequences.
- Avoid importing `shared/` casually. Psyling and PoolEmergency depend on it,
  so changes there can affect both production applications.
- Do not use `sites/therapist` for a new application. It is a historical Psyling
  compatibility alias that remains runtime-significant because Psyling's
  current venv contains shebangs referring to it.
- Keep uploads and other mutable data outside code replacement operations.

## Design configuration and data handling

Secrets belong in a protected production environment file, never in Git,
Markdown, command examples, tickets, or shell history. The current convention
is `/etc/webgarden/<site>.env`, root-owned and unreadable to ordinary users,
with systemd supplying it to the service. Whether a new site uses that
convention must be confirmed against the chosen service identity and startup
method.

Before introducing a database or uploads, define:

- who owns and can read them;
- which migrations are required and whether they are reversible;
- what the backup job includes;
- how a restore is tested without exposing private data;
- whether code rollback remains safe after a schema or data change.

A successful backup timer is evidence that a job ran, not evidence that these
questions are answered.

## Establish the production path

Prepare and review the application, then separately prepare production
integration. Production work requires explicit authorization and normally
includes:

1. a final source revision and clean reviewable diff;
2. site-specific tests and an import/startup check;
3. a production runtime path and fresh or deliberately managed venv;
4. protected configuration and persistent storage;
5. one systemd unit with an explicit user, group, working directory, and start
   command;
6. one nginx mapping to the exact listener and static roots;
7. low-impact local and public health checks;
8. backup coverage and a tested recovery plan;
9. a deployment procedure and rollback decision recorded in
   [Deployment](deployment.md) and the architecture inventory.

These are separate reviewable changes. Source approval does not automatically
authorize DNS, nginx, systemd, database, deployment, or service changes.

## Deployment and rollback are required decisions

For a direct-checkout runtime, document the limitations honestly:

- tracked files can change before workers are restarted;
- nginx-served static files can change immediately;
- Python code takes effect when the affected workers start again;
- the checkout has no deployed-SHA marker;
- a Git rollback does not roll back a database or uploads.

If an immutable release is chosen, define source verification, build isolation,
validation, atomic activation, retained releases, health checks, and automatic
or manual restoration of the prior target. Do not copy School of Code's path or
deployer without reviewing every application-specific assumption.

A rollback description must restore a known working version. Removing nginx or
disabling a unit is retirement or teardown, not version rollback.

## Pre-launch review

Before the site is made public, confirm:

- the site contract table is complete;
- live nginx and effective systemd configuration agree on the runtime;
- no listener, hostname, service name, database, or filesystem ownership
  collides with another site;
- the application starts under its production identity;
- local and public checks have explicit expected results;
- error handling does not disclose configuration or user data;
- backup scope is verified and a restore has been exercised where data matters;
- the deployment process records which source revision became active;
- rollback covers both code and persistent-data compatibility;
- the canonical documentation links to application-specific development notes
  instead of duplicating them.

If a required fact is unknown, leave it marked unknown and resolve it before
launch. Do not infer production values from the deprecated templates.

## After launch

Record the site once in the compact matrix in
[Architecture](architecture.md). Keep detailed development and data contracts in
the site's README. Keep operational procedures here, in
[Operations](operations.md), and in [Deployment](deployment.md), rather than
copying them into several places.

Retirement requires the same care as launch: identify DNS, certificates,
nginx, service state, databases, uploads, backups, and retained source before
anything is disabled or removed. It is a separately authorized change, not a
rollback shortcut.
