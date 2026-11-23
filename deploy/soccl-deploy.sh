#!/bin/bash
set -Eeuo pipefail

PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
export PATH
umask 022

readonly EXPECTED_ORIGIN="https://github.com/evgeny-vlasov/my-web-garden.git"
readonly REPOSITORY="/var/lib/soccl-deploy/repository.git"
readonly RELEASE_ROOT="/var/www/soccl/releases"
readonly CURRENT_LINK="/var/www/soccl/current"
readonly APP_USER="soccl-app"
readonly SERVICE="webgarden-shkolakoda.service"
readonly LOCK_FILE="/run/lock/soccl-deploy.lock"
readonly LOG_FILE="/var/log/soccl-deploy.log"
readonly LOCAL_BASE="http://127.0.0.1:8000"
readonly PUBLIC_HOSTS=(shkolakoda.com schoolofcode.ca)

STAGING_DIR=""
PREVIOUS_SHA=""
PREVIOUS_RELEASE=""
ROLLBACK_NEEDED=0
DEPLOYMENT_SUCCEEDED=0

log() {
    local message="$*"
    local timestamp
    timestamp="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    printf '%s %s\n' "$timestamp" "$message" | tee -a "$LOG_FILE"
    logger -t soccl-deploy -- "$message"
}

die() {
    log "status=failed reason=$1"
    exit 1
}

validate_release() {
    local release="$1"
    local expected_sha="$2"
    local marker
    local writable
    local link
    local target

    [[ -d "$release" && ! -L "$release" ]] ||
        die "invalid-release-directory sha=$expected_sha"
    [[ -f "$release/.soccl-revision" && ! -L "$release/.soccl-revision" ]] ||
        die "missing-release-marker sha=$expected_sha"
    marker="$(<"$release/.soccl-revision")"
    [[ "$marker" == "$expected_sha" ]] ||
        die "release-marker-mismatch expected=$expected_sha"
    [[ -d "$release/app" && -x "$release/venv/bin/python" ]] ||
        die "incomplete-release sha=$expected_sha"
    runuser -u "$APP_USER" -- env HOME=/nonexistent \
        PYTHONDONTWRITEBYTECODE=1 "$release/venv/bin/python" \
        -c "import gunicorn" ||
        die "gunicorn-import-failed sha=$expected_sha"
    [[ "$(stat -c '%U:%G' "$release")" == "root:root" ]] ||
        die "unsafe-release-owner sha=$expected_sha"
    [[ -z "$(find "$release/app" -type l -print -quit)" ]] ||
        die "application-symlink-present sha=$expected_sha"
    [[ -z "$(find "$release/app" ! -type d ! -type f -print -quit)" ]] ||
        die "application-special-file-present sha=$expected_sha"
    writable="$(find "$release" -xdev \( -type f -o -type d \) \
        -perm /022 -print -quit)"
    [[ -z "$writable" ]] ||
        die "writable-release-content sha=$expected_sha"
    while IFS= read -r -d '' link; do
        target="$(readlink -f "$link")" ||
            die "broken-release-symlink sha=$expected_sha"
        case "$target" in
            "$release"/*)
                ;;
            *)
                die "external-release-symlink sha=$expected_sha"
                ;;
        esac
    done < <(find "$release" -xdev -type l -print0)
}

current_revision() {
    local resolved
    local sha

    [[ -L "$CURRENT_LINK" ]] || die "current-release-link-missing"
    resolved="$(readlink -f "$CURRENT_LINK")"
    case "$resolved" in
        "$RELEASE_ROOT"/[0-9a-f]*)
            ;;
        *)
            die "current-release-link-outside-root"
            ;;
    esac
    sha="${resolved##*/}"
    [[ "$sha" =~ ^[0-9a-f]{40}$ &&
       "$resolved" == "$RELEASE_ROOT/$sha" ]] ||
        die "current-release-link-ambiguous"
    validate_release "$resolved" "$sha"
    printf '%s\n' "$sha"
}

verify_repository() {
    local origin
    local resolved

    [[ -d "$REPOSITORY" ]] || die "deployment-repository-missing"
    [[ "$(git --git-dir="$REPOSITORY" rev-parse --is-bare-repository)" == "true" ]] ||
        die "deployment-repository-not-bare"
    [[ "$(stat -c '%U:%G' "$REPOSITORY")" == "root:root" ]] ||
        die "deployment-repository-owner-unsafe"
    [[ -z "$(find "$REPOSITORY" -maxdepth 0 -perm /022 -print)" ]] ||
        die "deployment-repository-writable-by-non-root"
    origin="$(git --git-dir="$REPOSITORY" remote get-url origin)"
    [[ "$origin" == "$EXPECTED_ORIGIN" ]] ||
        die "deployment-origin-mismatch"
    [[ ! -f "$REPOSITORY/objects/info/alternates" ]] ||
        die "deployment-repository-alternates-present"
    [[ "$(git --git-dir="$REPOSITORY" config --bool --get transfer.fsckObjects)" == \
       "true" ]] || die "deployment-transfer-fsck-disabled"
    [[ "$(git --git-dir="$REPOSITORY" config --bool --get fetch.fsckObjects)" == \
       "true" ]] || die "deployment-fetch-fsck-disabled"

    log "status=fetching revision=$REVISION"
    GIT_TERMINAL_PROMPT=0 git --git-dir="$REPOSITORY" \
        fetch --force --prune --no-tags origin \
        "+refs/heads/main:refs/remotes/origin/main"

    git --git-dir="$REPOSITORY" cat-file -e "${REVISION}^{commit}" ||
        die "requested-object-not-a-commit revision=$REVISION"
    resolved="$(git --git-dir="$REPOSITORY" rev-parse --verify "${REVISION}^{commit}")"
    [[ "$resolved" == "$REVISION" ]] ||
        die "requested-revision-mismatch revision=$REVISION"
    git --git-dir="$REPOSITORY" merge-base --is-ancestor \
        "$REVISION" refs/remotes/origin/main ||
        die "requested-revision-not-on-main revision=$REVISION"
    git --git-dir="$REPOSITORY" cat-file -e \
        "$REVISION:sites/shkolakoda/requirements.txt" ||
        die "requested-revision-missing-soccl revision=$REVISION"
    git --git-dir="$REPOSITORY" fsck --strict --no-dangling "$REVISION"
}

run_release_checks() {
    local release="$1"
    local sha="$2"

    log "status=validating revision=$sha"
    (
        cd "$release/app"
        runuser -u "$APP_USER" -- env \
            HOME=/nonexistent PYTHONDONTWRITEBYTECODE=1 \
            "$release/venv/bin/python" -m publishing --check
        runuser -u "$APP_USER" -- env \
            HOME=/nonexistent PYTHONDONTWRITEBYTECODE=1 \
            "$release/venv/bin/python" -m unittest discover -s tests -v
    )
}

build_release() {
    local sha="$1"
    local release="$RELEASE_ROOT/$sha"
    local unexpected

    if [[ -e "$release" ]]; then
        validate_release "$release" "$sha"
        run_release_checks "$release" "$sha"
        return
    fi

    STAGING_DIR="$(mktemp -d "$RELEASE_ROOT/.staging-${sha}.XXXXXX")"
    chmod 0755 "$STAGING_DIR"
    install -d -m 0755 "$STAGING_DIR/app"
    log "status=building revision=$sha"
    git --git-dir="$REPOSITORY" archive --format=tar "$sha" sites/shkolakoda |
        tar -x -C "$STAGING_DIR/app" --strip-components=2

    unexpected="$(find "$STAGING_DIR/app" -type l -print -quit)"
    [[ -z "$unexpected" ]] || die "application-symlink-refused revision=$sha"
    unexpected="$(find "$STAGING_DIR/app" ! -type d ! -type f -print -quit)"
    [[ -z "$unexpected" ]] ||
        die "application-special-file-refused revision=$sha"

    install -d -m 0755 -o "$APP_USER" -g "$APP_USER" "$STAGING_DIR/venv"
    runuser -u "$APP_USER" -- env HOME=/nonexistent \
        python3 -m venv --copies "$STAGING_DIR/venv"
    runuser -u "$APP_USER" -- env HOME=/nonexistent \
        "$STAGING_DIR/venv/bin/python" -m pip install \
        --disable-pip-version-check --no-input \
        --no-cache-dir \
        --requirement "$STAGING_DIR/app/requirements.txt"

    chown -R root:root "$STAGING_DIR"
    chmod -R a-s "$STAGING_DIR"
    chmod -R go-w "$STAGING_DIR"
    run_release_checks "$STAGING_DIR" "$sha"
    printf '%s\n' "$sha" > "$STAGING_DIR/.soccl-revision"
    date -u +%Y-%m-%dT%H:%M:%SZ > "$STAGING_DIR/.soccl-built-at"
    chmod 0444 "$STAGING_DIR/.soccl-revision" "$STAGING_DIR/.soccl-built-at"
    mv "$STAGING_DIR" "$release"
    STAGING_DIR=""
    validate_release "$release" "$sha"
}

atomic_link() {
    local release="$1"
    local temporary="${CURRENT_LINK}.new.$$"

    case "$release" in
        "$RELEASE_ROOT"/[0-9a-f]*)
            ;;
        *)
            die "activation-target-outside-release-root"
            ;;
    esac
    rm -f -- "$temporary"
    ln -s "$release" "$temporary"
    mv -Tf "$temporary" "$CURRENT_LINK"
}

request_code() {
    local scope="$1"
    local path="$2"
    local host="${3:-shkolakoda.com}"
    local code

    if [[ "$scope" == "local" ]]; then
        code="$(curl --silent --show-error --output /dev/null \
            --connect-timeout 3 --max-time 12 \
            --header "Host: $host" \
            --write-out '%{http_code}' "${LOCAL_BASE}${path}")" || return 1
    else
        code="$(curl --silent --show-error --output /dev/null \
            --connect-timeout 5 --max-time 15 \
            --write-out '%{http_code}' "https://${host}${path}")" || return 1
    fi
    printf '%s\n' "$code"
}

check_expected() {
    local scope="$1"
    local path="$2"
    local expected="$3"
    local code

    code="$(request_code "$scope" "$path" "${4:-shkolakoda.com}")" || return 1
    [[ "$code" == "$expected" ]]
}

target_health_once() {
    local scope
    local host

    systemctl is-active --quiet "$SERVICE" || return 1
    for host in "${PUBLIC_HOSTS[@]}"; do
      for scope in local public; do
        check_expected "$scope" "/" 200 "$host" || return 1
        check_expected "$scope" "/projects" 200 "$host" || return 1
        check_expected "$scope" "/blog" 200 "$host" || return 1
        check_expected "$scope" "/campaigns" 200 "$host" || return 1
        check_expected "$scope" "/campaigns/sample-scratch-build-week" 404 "$host" ||
            return 1
        check_expected "$scope" \
            "/static/brand/logos/wordmark-horizontal.svg" 200 "$host" || return 1
        check_expected "$scope" \
            "/static/brand/mascot/robot-avatar-96.png" 200 "$host" || return 1
      done
    done
}

rollback_health_once() {
    local scope
    local host

    systemctl is-active --quiet "$SERVICE" || return 1
    for host in "${PUBLIC_HOSTS[@]}"; do
      for scope in local public; do
        check_expected "$scope" "/" 200 "$host" || return 1
        check_expected "$scope" "/projects" 200 "$host" || return 1
        check_expected "$scope" "/blog" 200 "$host" || return 1
      done
    done
}

wait_for_health() {
    local mode="$1"
    local attempt

    for attempt in 1 2 3 4 5 6; do
        if [[ "$mode" == "target" ]]; then
            target_health_once && return 0
        else
            rollback_health_once && return 0
        fi
        sleep 2
    done
    return 1
}

perform_rollback() {
    local rollback_result="failed"

    ROLLBACK_NEEDED=0
    log "status=rolling-back attempted=$REVISION previous=$PREVIOUS_SHA"
    atomic_link "$PREVIOUS_RELEASE"
    if systemctl restart "$SERVICE" && wait_for_health rollback; then
        rollback_result="healthy"
    fi
    log "status=rolled-back attempted=$REVISION previous=$PREVIOUS_SHA result=$rollback_result"
    [[ "$rollback_result" == "healthy" ]]
}

on_exit() {
    local result=$?
    local rollback_result=0

    trap - EXIT INT TERM HUP
    if [[ -n "$STAGING_DIR" ]]; then
        case "$STAGING_DIR" in
            "$RELEASE_ROOT"/.staging-*)
                rm -rf -- "$STAGING_DIR"
                ;;
        esac
    fi
    if [[ "$ROLLBACK_NEEDED" -eq 1 && "$DEPLOYMENT_SUCCEEDED" -eq 0 ]]; then
        set +e
        perform_rollback
        rollback_result=$?
        set -e
        [[ "$result" -ne 0 ]] || result=1
        [[ "$rollback_result" -eq 0 ]] || result=2
    fi
    exit "$result"
}

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
trap on_exit EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
trap 'exit 129' HUP

[[ "$EUID" -eq 0 ]] || die "root-required"
[[ "$#" -eq 1 ]] || die "expected-one-full-commit-sha"
REVISION="$1"
readonly REVISION
[[ "$REVISION" =~ ^[0-9a-f]{40}$ ]] ||
    die "invalid-commit-sha"

exec 9>"$LOCK_FILE"
flock -n 9 || die "deployment-already-running"

[[ -d "$RELEASE_ROOT" && ! -L "$RELEASE_ROOT" ]] ||
    die "release-root-missing-or-unsafe"
[[ "$(stat -c '%U:%G' "$RELEASE_ROOT")" == "root:root" ]] ||
    die "release-root-owner-unsafe"
[[ -z "$(find "$RELEASE_ROOT" -maxdepth 0 -perm /022 -print)" ]] ||
    die "release-root-writable-by-non-root"
[[ "$(systemctl show "$SERVICE" -p WorkingDirectory --value)" == \
   "/var/www/soccl/current/app" ]] ||
    die "service-working-directory-not-release-managed"
[[ "$(systemctl show "$SERVICE" -p ExecStart --value)" == \
   *"/var/www/soccl/current/venv/bin/python -m gunicorn"* ]] ||
    die "service-executable-not-release-managed"

PREVIOUS_SHA="$(current_revision)"
PREVIOUS_RELEASE="$RELEASE_ROOT/$PREVIOUS_SHA"
log "status=started requested=$REVISION previous=$PREVIOUS_SHA"

verify_repository
build_release "$REVISION"
validate_release "$RELEASE_ROOT/$REVISION" "$REVISION"

atomic_link "$RELEASE_ROOT/$REVISION"
ROLLBACK_NEEDED=1
log "status=activated requested=$REVISION previous=$PREVIOUS_SHA"
systemctl restart "$SERVICE"
wait_for_health target ||
    die "target-health-verification-failed revision=$REVISION"

DEPLOYMENT_SUCCEEDED=1
ROLLBACK_NEEDED=0
log "status=deployed revision=$REVISION previous=$PREVIOUS_SHA service=$SERVICE"
fi
