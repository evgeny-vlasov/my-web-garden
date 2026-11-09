#!/usr/bin/env bash
set -euo pipefail

if [[ ${EUID} -ne 0 ]]; then
    echo "Run this installer with sudo." >&2
    exit 1
fi

if ! id fluffy >/dev/null 2>&1; then
    echo "The fluffy account does not exist." >&2
    exit 1
fi

source_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
app_dir=/opt/soccl
data_dir=/var/lib/soccl
env_file=/etc/soccl.env

install -d -o root -g fluffy -m 0750 "${app_dir}"
install -d -o fluffy -g fluffy -m 0750 "${data_dir}"

for item in app.py manage.py requirements.txt wsgi.py .env.example .gitignore README.md; do
    install -o root -g fluffy -m 0640 "${source_dir}/${item}" "${app_dir}/${item}"
done

install -d -o root -g fluffy -m 0750 "${app_dir}/templates" "${app_dir}/static" "${app_dir}/deploy"
find "${source_dir}/templates" -maxdepth 1 -type f -exec install -o root -g fluffy -m 0640 {} "${app_dir}/templates/" \;
find "${source_dir}/static" -maxdepth 1 -type f -exec install -o root -g fluffy -m 0640 {} "${app_dir}/static/" \;
install -o root -g fluffy -m 0640 "${source_dir}/deploy/soccl.service" "${app_dir}/deploy/soccl.service"

if [[ ! -x "${app_dir}/venv/bin/python" ]]; then
    python3 -m venv "${app_dir}/venv"
fi
"${app_dir}/venv/bin/pip" install --disable-pip-version-check --requirement "${app_dir}/requirements.txt"

if [[ ! -s "${env_file}" ]]; then
    secret=$("${app_dir}/venv/bin/python" -c 'import secrets; print(secrets.token_urlsafe(48))')
    password_hash=$("${app_dir}/venv/bin/python" "${app_dir}/manage.py" hash-password)
    umask 027
    {
        printf 'SOCCL_SECRET_KEY=%s\n' "${secret}"
        printf 'SOCCL_ADMIN_PASSWORD_HASH=%s\n' "${password_hash}"
        printf 'SOCCL_DATABASE=%s/publisher.db\n' "${data_dir}"
        printf 'SOCCL_SECURE_COOKIE=0\n'
    } > "${env_file}"
    chown root:fluffy "${env_file}"
    chmod 0640 "${env_file}"
else
    echo "Preserving existing ${env_file}."
fi

install -o root -g root -m 0644 "${app_dir}/deploy/soccl.service" /etc/systemd/system/soccl.service
systemctl daemon-reload
systemctl enable --now soccl.service

for attempt in 1 2 3 4 5; do
    if curl --max-time 5 --fail --silent http://127.0.0.1:8010/health >/dev/null; then
        echo "School of Code publishing desk is healthy on 127.0.0.1:8010."
        exit 0
    fi
    sleep 1
done

echo "The service did not pass its health check." >&2
systemctl status soccl.service --no-pager >&2 || true
exit 1
