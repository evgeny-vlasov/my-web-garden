# Working in Webgarden

Webgarden is a small VPS hosting several independent Flask sites. Nginx
terminates HTTPS and sends each domain to a site-specific systemd service.
Sites normally have their own Gunicorn process, port or socket, virtual
environment, configuration, and data, but several services share the Unix user
`fluffy`.

The application source of truth is `evgeny-vlasov/my-web-garden`, branch
`main`. The working checkout is `/var/www/webgarden`. It is both a development
checkout and the live runtime for some sites, so inspect it carefully. Checkout
`HEAD` is not proof of the revision running in production.

## Runtime models

- Direct shared checkout: Psyling, PoolEmergency, LAIC, and Happy Science run
  from `/var/www/webgarden/sites/...`.
- Immutable release: School of Code runs from `/var/www/soccl/current/app`.
  Its canonical server deployer is `/usr/local/bin/soccl-deploy`.
- Separate checkout: Tom Umber runs from `/home/fluffy/projects/tomumber`.

Read [the documentation index](docs/README.md) before changing a site. The
canonical architecture, deployment, operations, lifecycle, and troubleshooting
documents live under `docs/`.

## Boundaries

- Identify the domain, source path, live working directory, systemd unit,
  port or socket, venv, environment file, data, deployment mechanism, and
  rollback mechanism before proposing a change.
- Discover and use site-specific deployment tooling. There is no general
  supported `deploy any Webgarden site` command.
- Changes under `shared/` can affect Psyling and PoolEmergency.
- `sites/therapist` is historical but still needed by Psyling's current venv
  shebangs. Do not remove or replace it casually.
- Changing `sites/shkolakoda` and restarting systemd does not deploy School of
  Code; its service loads the release selected by `/var/www/soccl/current`.
- Never print environment values, connection URLs, credentials, private data,
  tokens, cookies, or complete process environments.
- Do not casually change live nginx, systemd, certificates, environment files,
  databases, migrations, service identities, venvs, release directories, or
  the School of Code `current` symlink.
- Do not run deprecated `deploy/new_site.sh` or `deploy/setup_site.sh` on the
  current host.
- Never use a broad restart. Any restart must name one reviewed service.

Commit, push, PR creation or modification, merge, deployment, service restart,
database change, and infrastructure change each require explicit authorization.
Authorization for one does not imply authorization for another.

## Essential read-only checks

```bash
git status --short --branch
git rev-parse HEAD
git remote -v

systemctl show UNIT \
  -p ActiveState -p SubState -p User -p Group \
  -p WorkingDirectory -p ExecStart -p EnvironmentFiles

grep -nE 'server_name|proxy_pass|root|alias' \
  /etc/nginx/sites-enabled/SITE

readlink -f /var/www/soccl/current
cat /var/www/soccl/current/.soccl-revision

curl --max-time 15 -sS -o /dev/null -w '%{http_code}\n' URL
```

Access denial is evidence to record, not permission to weaken protections.
Prefer inspection before restart, and live configuration over repository
templates when the two disagree.
