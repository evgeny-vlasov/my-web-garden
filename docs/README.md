# Webgarden documentation

This directory describes Webgarden as it runs today. Start here instead of
inferring production from old templates, sprint reports, or setup scripts.

## Canonical documents

- [Architecture](architecture.md) — request flow, runtime models, isolation,
  persistent data, and the one complete site matrix.
- [Deployment](deployment.md) — how each existing site is or is not deployed,
  School of Code's immutable release path, discovery, and rollback reality.
- [Operations](operations.md) — safe read-only inspection, status checks,
  backup status, and source-versus-runtime drift diagnosis.
- [Site lifecycle](site-lifecycle.md) — the current manual process for planning
  and adding a site safely.
- [Troubleshooting](troubleshooting.md) — symptom-led production diagnosis.

The root [AGENTS.md](../AGENTS.md) is the short mandatory entry point for coding
agents. The root [README](../README.md) is the human overview.

## Authority hierarchy

When sources conflict, use this order:

1. The running process, resolved release symlink, and effective systemd unit
   establish what application code is active.
2. Enabled `/etc/nginx` configuration establishes public routing and direct
   static-file paths.
3. Protected environment files and the production data stores establish runtime
   configuration and data. Inspect names and metadata only unless access to
   values is explicitly authorized.
4. The relevant Git repository and branch establish reviewed application source.
5. The documents in this directory explain how to connect those facts.
6. Checked-in nginx/systemd files are installation bases or reference artifacts
   unless a comparison proves they match live configuration.
7. Historical reports and deprecated provisioners explain prior work but are
   not runbooks.

Live runtime truth can differ from checkout `HEAD`. In particular, School of
Code runs from `/var/www/soccl/current`, not from its source directory in the
working checkout.

## Document classes

- **Canonical runbooks:** the files in this directory.
- **Application documentation:** site READMEs, publication contracts, Scratch
  tooling notes, route documentation, and data-model notes. These describe an
  application, not necessarily its live deployment.
- **Live configuration:** effective systemd units, enabled nginx sites,
  environment files, processes, listeners, and active release links. These are
  runtime evidence and may require privileged read access.
- **Historical material:** the old root architecture narrative, sprint reports,
  implementation summaries, and deprecated deployment guides. Keep them for
  context, but follow their pointer to current documentation before acting.

## Safety rule

Inspect before changing. If live state cannot be read, record the gap rather
than guessing from a repository template or changing permissions. Never expose
secret values or private application data in diagnostic output.
