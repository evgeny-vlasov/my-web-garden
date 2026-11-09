# School of Code publishing desk

Private publishing operations for School of Code. The first release provides a
password-protected queue, Facebook and Instagram copy editing, review and
approval states, Calgary-time scheduling, channel status, and an audit trail.
It deliberately has no social credentials or delivery adapter yet.

The queue also records the approved editorial gate: every package needs a real
reason to exist and one editorial sentence. It distinguishes routine social
content from factual social content and full website articles, records
green/amber/red approval level, and assigns the intended Facebook rhythm. See
[EDITORIAL.md](EDITORIAL.md) for the canonical cadence and review policy.

## Runtime boundary

- Linux identity: `fluffy` for version one
- Application: `/opt/soccl`
- Persistent database: `/var/lib/soccl/publisher.db`
- Protected configuration: `/etc/soccl.env`
- Loopback listener: `127.0.0.1:8010`
- Unit: `soccl.service`

This service is separate from the immutable public School of Code runtime at
`/var/www/soccl/current`. It must not alter that release, its symlink, its
systemd unit, or any other Webgarden application.

## Initial private access

Version one has no public nginx route. Reach it through an SSH tunnel:

```bash
ssh -L 8010:127.0.0.1:8010 fluffy@SERVER
```

Then open `http://127.0.0.1:8010`. Keep that SSH session open while using the
dashboard.

## Installation outline

After extracting the release archive, run the installer. It prompts for the
dashboard password without placing that password in shell history.

```bash
sudo bash install.sh
```

The installer copies the application to `/opt/soccl`, preserves an existing
`/etc/soccl.env`, installs dependencies, starts only `soccl.service`, and checks
the private health endpoint. It does not modify nginx or another site.

## Verification

```bash
systemctl show soccl.service -p ActiveState -p SubState -p User -p Group -p WorkingDirectory -p ExecStart -p EnvironmentFiles
curl --max-time 10 -sS -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8010/health
journalctl -u soccl.service --since '10 minutes ago' --no-pager
```

Expected health response status is `200`. Do not expose port 8010 publicly.

## Local development and tests

```bash
python3 -m venv venv
venv/bin/pip install -r requirements.txt
SOCCL_SECRET_KEY=development-only \
SOCCL_ADMIN_PASSWORD_HASH='replace-with-a-test-hash' \
SOCCL_DATABASE=/tmp/soccl-dev.db \
venv/bin/flask --app app run --port 8010

venv/bin/python -m unittest discover -s tests -v
```
