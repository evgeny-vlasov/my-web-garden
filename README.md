# Webgarden

Webgarden is a small collection of independently operated Flask websites on one
VPS. It provides a practical home for site source, shared code where useful,
and the checked-in parts of nginx, systemd, publishing, and backup work.

It is not one uniform application or deployment system. Nginx terminates HTTPS
and routes each domain to a site-specific systemd-managed Gunicorn process.
Each live site generally has its own port or socket, virtual environment,
configuration, and database or file storage.

## Start here

- Coding agents: [AGENTS.md](AGENTS.md)
- Documentation and authority index: [docs/README.md](docs/README.md)
- Current architecture and site inventory: [docs/architecture.md](docs/architecture.md)
- Deployment and rollback reality: [docs/deployment.md](docs/deployment.md)
- Safe production inspection: [docs/operations.md](docs/operations.md)
- Adding a site: [docs/site-lifecycle.md](docs/site-lifecycle.md)
- Troubleshooting: [docs/troubleshooting.md](docs/troubleshooting.md)

## Source

The Webgarden application source of truth is the GitHub repository
`evgeny-vlasov/my-web-garden`, branch `main`. The working checkout on the VPS is:

```text
/var/www/webgarden
```

That checkout has two roles. It is a source/development checkout for the whole
monorepo, and it is also the direct production runtime for several sites.
Repository `HEAD` therefore does not, by itself, identify the code loaded by
every production process.

Tom Umber is outside this monorepo under `/home/fluffy/projects/tomumber`.

## Runtime models

Webgarden currently has three:

1. **Direct checkout:** Psyling, PoolEmergency, LAIC, and Happy Science run from
   `/var/www/webgarden/sites/...`.
2. **Immutable release:** School of Code runs from
   `/var/www/soccl/current/app` and is deployed with
   `/usr/local/bin/soccl-deploy`.
3. **Separate checkout:** Tom Umber runs from its own mutable checkout and Unix
   socket.

There is no supported generic command that deploys every site. The old generic
site-creation scripts under `deploy/` are retained as historical artifacts and
must not be used on the current host.

## Repository layout

```text
shared/              shared Flask modules used by some sites
sites/               site application source
tools/               application-specific production tooling
deploy/              checked-in infrastructure artifacts and historical tools
webgarden-backup/    checked-in backup implementation and site profiles
docs/                canonical current documentation
```

Psyling and PoolEmergency import `shared/`, so a shared-code change can affect
both. `sites/therapist` is a compatibility symlink still referenced by Psyling's
current virtual environment and must not be removed casually.

## Current limitation

School of Code has exact-revision deployment, validation, health checks, and
automatic rollback. The direct-checkout sites and Tom Umber do not yet have
equivalent versioned deployment and rollback tools. The documentation describes
that difference rather than hiding it.

Historical design and sprint documents remain in the repository for context.
They are not production authority unless the canonical documentation explicitly
says otherwise.
