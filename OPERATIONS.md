# Webgarden operations

This path is retained as a compatibility pointer. The canonical current
read-only runbook is [docs/operations.md](docs/operations.md). Use
[docs/deployment.md](docs/deployment.md) for site-specific deployment and
rollback, and [docs/troubleshooting.md](docs/troubleshooting.md) for
symptom-led diagnosis.

The previous root runbook remains available in Git history. It contained useful
privacy guidance, but its inventory and School of Code runtime assumptions no
longer described the whole host. Keeping a second operational procedure here
would make future drift more likely.

Core safety rules still apply:

- Never print environment values, secrets, database rows, private messages, or
  complete connection URLs.
- Inspect effective live configuration before relying on repository copies.
- Prefer narrow, read-only checks before proposing a change.
- A deployment, migration, service restart, nginx reload, or infrastructure
  edit requires separate explicit authorization.
- Never restart every Webgarden service as a diagnostic step.
