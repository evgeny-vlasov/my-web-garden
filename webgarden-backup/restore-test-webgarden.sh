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

latest_backup_dir() {
  local candidate=""
  if [[ -L "$DEFAULT_BACKUP_DIR" || -d "$DEFAULT_BACKUP_DIR" ]]; then
    candidate="$(readlink -f "$DEFAULT_BACKUP_DIR" 2>/dev/null || true)"
    if [[ -n "$candidate" && -d "$candidate" ]]; then
      printf '%s' "$candidate"
      return 0
    fi
  fi

  candidate="$(find "$BACKUP_ROOT" -maxdepth 1 -mindepth 1 -type d -regextype posix-extended -regex '.*/[0-9]{8}T[0-9]{6}Z' | sort | tail -n1 || true)"
  [[ -n "$candidate" ]] || return 1
  printf '%s' "$candidate"
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
  local backup_dir
  backup_dir="$(latest_backup_dir || true)"
  [[ -n "$backup_dir" ]] || die "no backup directory found under $BACKUP_ROOT"

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
