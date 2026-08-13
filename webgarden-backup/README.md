# Web Garden Backups

> **Checked-in implementation, not proof of installed coverage.** A daily
> backup timer was active and its last observed run succeeded on 2026-08-13,
> but the protected installed tooling and archives could not be compared with
> this repository copy. A successful job does not prove archive completeness or
> restoration. Science coverage appears inconsistent with the checked-in site
> profiles. See [operations](../docs/operations.md#check-backup-job-status).

This checked-in backup job is designed to archive site source, selected uploads,
PostgreSQL or SQLite data, nginx/systemd configuration, and `/etc/webgarden`.

The global system config archive is expected to include the active nginx
available/enabled files for Psyling, Shkolakoda, Tom Umber, LAIC,
PoolEmergency, and the Shkolakoda default fallback, plus the active Web Garden
systemd units and timer.

## Privileges

Run `backup-webgarden.sh` as root. Environment files in `/etc/webgarden` are
intentionally root-owned `0600`, and the backup archive must preserve those
protected files without loosening permissions.

The systemd unit in `deploy/systemd/webgarden-backup.service` intentionally does
not set `User=` or `Group=`, so systemd runs the oneshot job as root.

## Protected Output

Backups are written under `/home/fluffy/backups/webgarden` by default. The script
uses `umask 077`, creates backup directories with mode `0700`, and writes logs,
manifests, archives, and dumps with mode `0600` where applicable.

## Success Marker

Each timestamped backup has a `manifest.txt` with `status=success` or
`status=partial`.

The `latest` symlink is updated only after a successful backup. Failed or partial
backups leave `latest` unchanged. `restore-test-webgarden.sh` scans timestamped
backup directories newest-first and validates only the newest backup whose
manifest says `status=success`.

The restore-test script validates archive structure; it does not perform or
prove a working restoration.

## Installation record

The commands below mutate protected production paths and services. They are not
a routine operations procedure and require a separately reviewed infrastructure
change with explicit authorization. Compare the protected installed version
with this repository copy before replacing anything.

```bash
sudo install -d -m 700 -o root -g root /home/fluffy/webgarden-backup
sudo install -d -m 700 -o root -g root /home/fluffy/webgarden-backup/sites.d
sudo install -m 700 -o root -g root /var/www/webgarden/webgarden-backup/backup-webgarden.sh /home/fluffy/webgarden-backup/backup-webgarden.sh
sudo install -m 700 -o root -g root /var/www/webgarden/webgarden-backup/restore-test-webgarden.sh /home/fluffy/webgarden-backup/restore-test-webgarden.sh
for conf in /var/www/webgarden/webgarden-backup/sites.d/*.conf; do
  sudo install -m 600 -o root -g root "$conf" "/home/fluffy/webgarden-backup/sites.d/$(basename "$conf")"
done
sudo cp /var/www/webgarden/deploy/systemd/webgarden-backup.service /etc/systemd/system/webgarden-backup.service
sudo systemctl daemon-reload
sudo systemctl restart webgarden-backup.service
```
