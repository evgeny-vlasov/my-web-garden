#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

readonly BACKUP_ROOT="${BACKUP_ROOT:-/home/fluffy/backups/webgarden}"
readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
readonly DEFAULT_BACKUP_DIR="$BACKUP_ROOT/latest"

log() {
  printf '%s\n' "$*"
}

die() {
  printf 'ERROR: %s\n' "$1" >&2
  exit 1
}

require_root() {
  if [[ "${EUID:-$(id -u)}" -ne 0 ]]; then
    die "restore-test-webgarden.sh must run as root to read protected backup archives"
  fi
}

backup_status() {
  local backup_dir="$1"
  local manifest="$backup_dir/manifest.txt"
  [[ -f "$manifest" ]] || return 1
  awk -F= '$1 == "status" { print $2; exit }' "$manifest"
}

is_successful_backup() {
  local backup_dir="$1"
  [[ -d "$backup_dir" ]] || return 1
  [[ "$(backup_status "$backup_dir" 2>/dev/null || true)" == "success" ]]
}

latest_backup_dir() {
  local candidate=""

  while IFS= read -r candidate; do
    [[ -n "$candidate" ]] || continue
    if is_successful_backup "$candidate"; then
      printf '%s' "$candidate"
      return 0
    fi
  done < <(
    find "$BACKUP_ROOT" -maxdepth 1 -mindepth 1 -type d -regextype posix-extended \
      -regex '.*/[0-9]{8}T[0-9]{6}Z' | sort -r
  )

  if [[ -L "$DEFAULT_BACKUP_DIR" || -d "$DEFAULT_BACKUP_DIR" ]]; then
    candidate="$(readlink -f "$DEFAULT_BACKUP_DIR" 2>/dev/null || true)"
    if [[ -n "$candidate" ]] && is_successful_backup "$candidate"; then
      printf '%s' "$candidate"
      return 0
    fi
  fi

  return 1
}

verify_tarball() {
  local archive_file="$1"
  tar -tzf "$archive_file" >/dev/null
}

verify_dump() {
  local dump_file="$1"
  pg_restore --list "$dump_file" >/dev/null
}

verify_sqlite_copy() {
  local db_file="$1"
  if command -v sqlite3 >/dev/null 2>&1; then
    sqlite3 "$db_file" 'PRAGMA quick_check;' >/dev/null
  else
    [[ -s "$db_file" ]]
  fi
}

main() {
  require_root

  local backup_dir
  backup_dir="$(latest_backup_dir || true)"
  [[ -n "$backup_dir" ]] || die "no successful backup directory found under $BACKUP_ROOT"

  log "restore-test: backup_dir=$backup_dir"
  log "restore-test: validation-only mode; no production data will be modified"
  log "restore-test: limitation=postgres archives are checked with pg_restore --list instead of full scratch-database restore"

  [[ -f "$backup_dir/manifest.txt" ]] || die "missing manifest.txt in $backup_dir"
  [[ -s "$backup_dir/manifest.txt" ]] || die "empty manifest.txt in $backup_dir"

  local verified_count=0
  local archive
  while IFS= read -r archive; do
    [[ -n "$archive" ]] || continue
    case "$archive" in
      *.tar.gz)
        verify_tarball "$archive" || die "tar validation failed: $archive"
        verified_count=$((verified_count + 1))
        ;;
      *.custom|*.dump)
        verify_dump "$archive" || die "postgres validation failed: $archive"
        verified_count=$((verified_count + 1))
        ;;
      *.backup|*.sqlite)
        verify_sqlite_copy "$archive" || die "sqlite validation failed: $archive"
        verified_count=$((verified_count + 1))
        ;;
      *)
        :
        ;;
    esac
  done < <(find "$backup_dir" -type f | sort)

  log "restore-test: verified_files=$verified_count"
  log "restore-test: result=passed"
}

main "$@"
