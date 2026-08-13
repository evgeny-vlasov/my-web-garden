# Webgarden site inventory

This path is retained as a compatibility pointer. The canonical current site
matrix is [docs/architecture.md](docs/architecture.md), including runtime
paths, services, users, ports and sockets, environment files, data, and status.
Deployment and rollback reality are documented in
[docs/deployment.md](docs/deployment.md).

The former table in this file was a July 2026 snapshot. It incorrectly treated
the School of Code source checkout as its production runtime and made backup
coverage claims that the architecture audit could not verify. It remains
available in Git history for historical research, but must not be used as an
operations inventory.

Live enabled nginx configuration, effective systemd configuration, protected
environment-file metadata, and active release symlinks are runtime truth. Use
the read-only procedures in [docs/operations.md](docs/operations.md) to compare
them with the repository before changing a site.
