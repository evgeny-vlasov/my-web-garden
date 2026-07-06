#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'
umask 077

# TODO: add encrypted offsite replication once the local backup flow is stable.

readonly SCRIPT_VERSION="1.0.0"
readonly BACKUP_ROOT="${BACKUP_ROOT:-/home/fluffy/backups/webgarden}"
readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
readonly CONFIG_DIR="${CONFIG_DIR:-$SCRIPT_DIR/sites.d}"
readonly WEBGARDEN_ROOT="${WEBGARDEN_ROOT:-/var/www/webgarden}"
readonly ETC_WEBGARDEN="${ETC_WEBGARDEN:-/etc/webgarden}"
readonly SYSTEMD_UNIT_DIR="${SYSTEMD_UNIT_DIR:-/etc/systemd/system}"
readonly NGINX_AVAILABLE_DIR="${NGINX_AVAILABLE_DIR:-/etc/nginx/sites-available}"
readonly NGINX_ENABLED_DIR="${NGINX_ENABLED_DIR:-/etc/nginx/sites-enabled}"

timestamp="$(date -u +%Y%m%dT%H%M%SZ)"
backup_dir="$BACKUP_ROOT/$timestamp"
manifest_file="$backup_dir/manifest.txt"
log_file="$BACKUP_ROOT/backup.log"
lock_file="$BACKUP_ROOT/.backup.lock"
hostname_value="$(hostname -f 2>/dev/null || hostname)"

declare -a warnings=()
declare -a created_files=()
declare -a verification_lines=()
declare -a site_names=()
declare -a site_lines=()
declare -a global_lines=()
had_error=0
retention_days_global=30

warn() {
  local message="$1"
  warnings+=("$message")
  printf 'WARN: %s\n' "$message" >&2
}

note_error() {
  local message="$1"
  had_error=1
  warnings+=("ERROR: $message")
  printf 'ERROR: %s\n' "$message" >&2
}

record_created_file() {
  local path="$1"
  local size="$2"
  created_files+=("$path|$size")
}

record_verification() {
  local label="$1"
  local status="$2"
  local detail="${3:-}"
  if [[ -n "$detail" ]]; then
    verification_lines+=("$label|$status|$detail")
  else
    verification_lines+=("$label|$status|")
  fi
}

ensure_dir() {
  local dir="$1"
  mkdir -p "$dir"
  chmod 700 "$dir"
}

file_size() {
  stat -c '%s' "$1"
}

append_manifest_block() {
  local title="$1"
  shift
  {
    printf '%s\n' "$title"
    if (($# == 0)); then
      printf '  (none)\n'
    else
      local item
      for item in "$@"; do
        printf '  - %s\n' "$item"
      done
    fi
    printf '\n'
  } >> "$manifest_file"
}

archive_directory() {
  local source_dir="$1"
  local dest_file="$2"
  shift 2
  local -a exclude_args=()
  local pattern
  for pattern in "$@"; do
    exclude_args+=(--exclude="$pattern")
  done

  tar -C "$source_dir" "${exclude_args[@]}" -czf "$dest_file" .
}

archive_paths() {
  local dest_file="$1"
  shift
  local -a existing_paths=()
  local -a rel_paths=()
  local path
  for path in "$@"; do
    if [[ -e "$path" ]]; then
      existing_paths+=("$path")
      rel_paths+=("${path#/}")
    else
      warn "missing optional path: $path"
    fi
  done

  if ((${#existing_paths[@]} == 0)); then
    return 1
  fi

  tar -C / -czf "$dest_file" "${rel_paths[@]}"
}

backup_file_or_dir_tar() {
  local source_path="$1"
  local dest_file="$2"
  local source_root source_name
  source_root="$(dirname "$source_path")"
  source_name="$(basename "$source_path")"
  tar -C "$source_root" -czf "$dest_file" "$source_name"
}

resolve_database_url_from_env_file() {
  local env_file="$1"
  local var_name="$2"

  bash -c '
    set -euo pipefail
    env_file="$1"
    var_name="$2"
    set -a
    # shellcheck disable=SC1090
    source "$env_file"
    set +a

    value="${!var_name-}"
    if [[ -n "$value" ]]; then
      printf "%s" "$value"
      exit 0
    fi

    if [[ -n "${PGDATABASE-}" || -n "${PGUSER-}" || -n "${PGPASSWORD-}" || -n "${PGHOST-}" || -n "${PGPORT-}" ]]; then
      url="postgresql://"
      if [[ -n "${PGUSER-}" ]]; then
        url+="$PGUSER"
        if [[ -n "${PGPASSWORD-}" ]]; then
          url+=":${PGPASSWORD}"
        fi
        url+="@"
      elif [[ -n "${PGPASSWORD-}" ]]; then
        url+=":${PGPASSWORD}@"
      fi
      if [[ -n "${PGHOST-}" ]]; then
        url+="$PGHOST"
      else
        url+="localhost"
      fi
      if [[ -n "${PGPORT-}" ]]; then
        url+=":${PGPORT}"
      fi
      if [[ -n "${PGDATABASE-}" ]]; then
        url+="/$PGDATABASE"
      fi
      printf "%s" "$url"
    fi
  ' _ "$env_file" "$var_name"
}

resolve_database_url_from_service() {
  local service_name="$1"
  local unit_file="$SYSTEMD_UNIT_DIR/$service_name"
  local key="${2:-DATABASE_URL}"
  local line value

  [[ -r "$unit_file" ]] || return 1

  line="$(grep -E "^[[:space:]]*Environment=.*${key}=" "$unit_file" | head -n1 || true)"
  [[ -n "$line" ]] || return 1

  value="${line#*${key}=}"
  value="${value%\"}"
  value="${value#\"}"
  printf '%s' "$value"
}

resolve_database_url() {
  local env_file="$1"
  local service_name="$2"
  local var_name="$3"
  local value=""

  if [[ -n "${DATABASE_URL_VALUE:-}" ]]; then
    printf '%s' "$DATABASE_URL_VALUE"
    return 0
  fi

  if [[ -n "$env_file" && -r "$env_file" ]]; then
    value="$(resolve_database_url_from_env_file "$env_file" "$var_name" || true)"
    if [[ -n "$value" ]]; then
      printf '%s' "$value"
      return 0
    fi
  fi

  if [[ -n "$service_name" ]]; then
    value="$(resolve_database_url_from_service "$service_name" "$var_name" || true)"
    if [[ -n "$value" ]]; then
      printf '%s' "$value"
      return 0
    fi
  fi

  return 1
}

apply_postgres_url_env() {
  local db_url="$1"

  eval "$(
    python3 - "$db_url" <<'PY'
import shlex
import sys
from urllib.parse import urlparse, unquote

url = sys.argv[1]
parsed = urlparse(url)

user = unquote(parsed.username or "")
password = unquote(parsed.password or "")
host = parsed.hostname or "localhost"
port = str(parsed.port or "")
dbname = parsed.path.lstrip("/")

if user:
    print(f"PGUSER={shlex.quote(user)}")
if password:
    print(f"PGPASSWORD={shlex.quote(password)}")
print(f"PGHOST={shlex.quote(host)}")
if port:
    print(f"PGPORT={shlex.quote(port)}")
if dbname:
    print(f"PGDATABASE={shlex.quote(dbname)}")
PY
  )"
}

verify_custom_dump() {
  local dump_file="$1"
  if pg_restore --list "$dump_file" >/dev/null 2>&1; then
    record_verification "$(basename "$dump_file")" "ok" "pg_restore --list"
    return 0
  fi
  record_verification "$(basename "$dump_file")" "failed" "pg_restore --list"
  return 1
}

verify_tarball() {
  local archive_file="$1"
  if tar -tzf "$archive_file" >/dev/null 2>&1; then
    record_verification "$(basename "$archive_file")" "ok" "tar -tzf"
    return 0
  fi
  record_verification "$(basename "$archive_file")" "failed" "tar -tzf"
  return 1
}

backup_postgres() {
  local site_name="$1"
  local env_file="$2"
  local service_name="$3"
  local var_name="$4"
  local dest_file="$5"
  local db_url=""

  db_url="$(resolve_database_url "$env_file" "$service_name" "$var_name" || true)"

  if [[ -z "$db_url" ]]; then
    note_error "postgres url not found for $site_name"
    return 1
  fi

  if (
    set -euo pipefail
    PGCONNECT_TIMEOUT=10 pg_dump --format=custom --file="$dest_file" --no-password --dbname="$db_url" >/dev/null 2>&1
  ); then
    local size
    size="$(file_size "$dest_file")"
    record_created_file "$dest_file" "$size"
    if verify_custom_dump "$dest_file"; then
      return 0
    fi
    note_error "verification failed for postgres dump: $dest_file"
    return 1
  fi

  note_error "pg_dump failed for $site_name"
  return 1
}

backup_sqlite() {
  local site_name="$1"
  local source_file="$2"
  local dest_file="$3"
  local sqlite_bin=""

  if [[ ! -e "$source_file" ]]; then
    warn "missing sqlite path for $site_name: $source_file"
    return 0
  fi

  sqlite_bin="$(command -v sqlite3 2>/dev/null || true)"
  if [[ -n "$sqlite_bin" ]]; then
    if "$sqlite_bin" "$source_file" ".backup '$dest_file'" >/dev/null 2>&1; then
      :
    else
      note_error "sqlite3 backup failed for $site_name: $source_file"
      return 1
    fi
  else
    warn "sqlite3 not available; falling back to copy for $site_name: $source_file"
    if ! cp -p "$source_file" "$dest_file"; then
      note_error "sqlite copy failed for $site_name: $source_file"
      return 1
    fi
  fi

  if [[ ! -s "$dest_file" ]]; then
    note_error "sqlite backup is empty for $site_name: $dest_file"
    return 1
  fi

  record_created_file "$dest_file" "$(file_size "$dest_file")"
  if [[ -n "$sqlite_bin" ]]; then
    if "$sqlite_bin" "$dest_file" 'PRAGMA quick_check;' >/dev/null 2>&1; then
      record_verification "$(basename "$dest_file")" "ok" "sqlite quick_check"
      return 0
    fi
    note_error "sqlite quick_check failed for $site_name: $dest_file"
    return 1
  fi

  record_verification "$(basename "$dest_file")" "warn" "copied file only; sqlite3 unavailable"
  return 0
}

backup_upload_paths() {
  local site_name="$1"
  local app_path="$2"
  local uploads_spec="$3"
  local dest_dir="$4"
  local upload_path
  local rel_path
  local -a upload_paths=()

  [[ -n "$uploads_spec" ]] || return 0
  IFS=' ' read -r -a upload_paths <<< "$uploads_spec"

  ensure_dir "$dest_dir"
  for upload_path in "${upload_paths[@]}"; do
    if [[ ! -e "$upload_path" ]]; then
      warn "$site_name upload path missing: $upload_path"
      continue
    fi

    rel_path="$(basename "$upload_path")"
    if [[ "$upload_path" == "$app_path/"* ]]; then
      rel_path="${upload_path#"$app_path"/}"
    fi

    local dest_file="$dest_dir/${rel_path//\//_}.tar.gz"
    if backup_file_or_dir_tar "$upload_path" "$dest_file"; then
      record_created_file "$dest_file" "$(file_size "$dest_file")"
      if verify_tarball "$dest_file"; then
        :
      else
        note_error "verification failed for upload archive: $dest_file"
      fi
    else
      note_error "failed to archive upload path for $site_name: $upload_path"
    fi
  done
}

backup_app_source() {
  local site_name="$1"
  local app_path="$2"
  local dest_file="$3"
  local uploads_spec="$4"
  local sqlite_paths_spec="${5:-}"
  local -a exclude_args=(
    --exclude-vcs
    --exclude='./venv'
    --exclude='./venv/*'
    --exclude='./.venv'
    --exclude='./.venv/*'
    --exclude='./__pycache__'
    --exclude='./__pycache__/*'
    --exclude='*/__pycache__'
    --exclude='*/__pycache__/*'
    --exclude='*.pyc'
    --exclude='*.pyo'
    --exclude='./node_modules'
    --exclude='./node_modules/*'
    --exclude='*/node_modules'
    --exclude='*/node_modules/*'
    --exclude='./.pytest_cache'
    --exclude='./.pytest_cache/*'
    --exclude='*/.pytest_cache'
    --exclude='*/.pytest_cache/*'
    --exclude='./.mypy_cache'
    --exclude='./.mypy_cache/*'
    --exclude='*/.mypy_cache'
    --exclude='*/.mypy_cache/*'
    --exclude='./logs'
    --exclude='./logs/*'
    --exclude='*/logs'
    --exclude='*/logs/*'
    --exclude='./backup'
    --exclude='./backup/*'
    --exclude='*/backup'
    --exclude='*/backup/*'
    --exclude='./backups'
    --exclude='./backups/*'
    --exclude='*/backups'
    --exclude='*/backups/*'
    --exclude='./tmp'
    --exclude='./tmp/*'
    --exclude='*/tmp'
    --exclude='*/tmp/*'
  )
  local upload_path rel_path
  local -a upload_paths=()
  IFS=' ' read -r -a upload_paths <<< "$uploads_spec"
  for upload_path in "${upload_paths[@]}"; do
    if [[ -n "$upload_path" && -d "$upload_path" && "$upload_path" == "$app_path/"* ]]; then
      rel_path="${upload_path#"$app_path"/}"
      exclude_args+=(--exclude="./$rel_path" --exclude="./$rel_path/*")
    fi
  done

  local sqlite_path
  local -a sqlite_paths=()
  IFS=' ' read -r -a sqlite_paths <<< "$sqlite_paths_spec"
  for sqlite_path in "${sqlite_paths[@]}"; do
    if [[ -n "$sqlite_path" && -e "$sqlite_path" && "$sqlite_path" == "$app_path/"* ]]; then
      rel_path="${sqlite_path#"$app_path"/}"
      exclude_args+=(--exclude="./$rel_path")
      if [[ "$rel_path" == *.sqlite ]]; then
        exclude_args+=(--exclude="./$rel_path-wal" --exclude="./$rel_path-shm")
      fi
    fi
  done

  if archive_directory "$app_path" "$dest_file" "${exclude_args[@]}"; then
    record_created_file "$dest_file" "$(file_size "$dest_file")"
    if verify_tarball "$dest_file"; then
      return 0
    fi
    note_error "verification failed for app archive: $dest_file"
    return 1
  fi

  note_error "failed to archive app path for $site_name: $app_path"
  return 1
}

backup_global_assets() {
  local backup_dir="$1"
  local global_dir="$backup_dir/global"
  ensure_dir "$global_dir"

  local docs_archive="$global_dir/webgarden-docs-and-git.tar.gz"
  local config_archive="$global_dir/webgarden-system-config.tar.gz"
  local -a repo_items=()
  local item

  if [[ -d "$WEBGARDEN_ROOT" ]]; then
    while IFS= read -r item; do
      repo_items+=("$item")
    done < <(
      find "$WEBGARDEN_ROOT" -maxdepth 1 -mindepth 1 \
        \( -type f -name '*.md' -o -type f -name '*.txt' -o -type d -name '.git' -o -type d -name 'deploy' -o -type d -name 'webgarden-backup' \) \
        -printf '%f\n' | sort
    )
    if ((${#repo_items[@]} > 0)); then
      if tar -C "$WEBGARDEN_ROOT" -czf "$docs_archive" "${repo_items[@]}"; then
        record_created_file "$docs_archive" "$(file_size "$docs_archive")"
        verify_tarball "$docs_archive" || note_error "verification failed for $docs_archive"
      else
        note_error "failed to create webgarden docs archive"
      fi
    else
      warn "no top-level webgarden docs or git metadata found"
    fi
  else
    note_error "missing webgarden root: $WEBGARDEN_ROOT"
  fi

  local -a config_paths=(
    "$ETC_WEBGARDEN"
    "$NGINX_AVAILABLE_DIR/psyling.com"
    "$NGINX_AVAILABLE_DIR/shkolakoda.com"
    "$NGINX_AVAILABLE_DIR/tomumber.com"
    "$NGINX_ENABLED_DIR/psyling.com"
    "$NGINX_ENABLED_DIR/shkolakoda.com"
    "$NGINX_ENABLED_DIR/tomumber.com"
    "$SYSTEMD_UNIT_DIR/webgarden-psyling.service"
    "$SYSTEMD_UNIT_DIR/webgarden-shkolakoda.service"
    "$SYSTEMD_UNIT_DIR/tomumber.service"
  )

  local -a existing_config_paths=()
  local -a config_items=()
  for item in "${config_paths[@]}"; do
    if [[ -e "$item" ]]; then
      existing_config_paths+=("$item")
      config_items+=("${item#/}")
    else
      warn "missing global config path: $item"
    fi
  done

  if ((${#existing_config_paths[@]} > 0)); then
    if tar -C / -czf "$config_archive" "${config_items[@]}"; then
      record_created_file "$config_archive" "$(file_size "$config_archive")"
      verify_tarball "$config_archive" || note_error "verification failed for $config_archive"
    else
      note_error "failed to create system config archive"
    fi
  fi
}

backup_site() {
  local conf_file="$1"
  local SITE_NAME="" APP_PATH="" ENV_FILE="" SERVICE_NAME="" DB_TYPE="auto" DATABASE_URL_VAR="DATABASE_URL" DATABASE_URL_VALUE="" SQLITE_PATHS="" BACKUP_UPLOADS="no" UPLOAD_PATHS="" RETENTION_DAYS="30"

  # shellcheck disable=SC1090
  source "$conf_file"

  DB_TYPE="${DB_TYPE,,}"
  BACKUP_UPLOADS="${BACKUP_UPLOADS,,}"
  RETENTION_DAYS="${RETENTION_DAYS:-30}"
  DATABASE_URL_VAR="${DATABASE_URL_VAR:-DATABASE_URL}"
  if [[ "$RETENTION_DAYS" =~ ^[0-9]+$ ]] && (( RETENTION_DAYS > retention_days_global )); then
    retention_days_global="$RETENTION_DAYS"
  fi

  if [[ -z "$SITE_NAME" || -z "$APP_PATH" ]]; then
    note_error "invalid site config: $conf_file"
    return 0
  fi

  local site_dir="$backup_dir/sites/$SITE_NAME"
  local uploads_dir="$site_dir/uploads"
  local db_dir="$site_dir/db"
  local sqlite_dir="$site_dir/sqlite"
  ensure_dir "$site_dir"
  ensure_dir "$uploads_dir"
  ensure_dir "$db_dir"
  ensure_dir "$sqlite_dir"

  local app_archive="$site_dir/${SITE_NAME}-app.tar.gz"
  local db_archive="$db_dir/${SITE_NAME}-postgres.custom"
  local app_status="not-requested"
  local sqlite_status="not-requested"
  local postgres_status="not-requested"
  local site_notes=()

  if [[ ! -d "$APP_PATH" ]]; then
    note_error "missing app path for $SITE_NAME: $APP_PATH"
    site_names+=("$SITE_NAME")
    site_lines+=("$SITE_NAME|error|missing app path")
    return 0
  fi

  if backup_app_source "$SITE_NAME" "$APP_PATH" "$app_archive" "$UPLOAD_PATHS" "$SQLITE_PATHS"; then
    app_status="ok"
  else
    app_status="failed"
  fi

  if [[ "${BACKUP_UPLOADS}" == "yes" && -n "${UPLOAD_PATHS:-}" ]]; then
    backup_upload_paths "$SITE_NAME" "$APP_PATH" "$UPLOAD_PATHS" "$uploads_dir"
  fi

  case "$DB_TYPE" in
    postgres)
      if backup_postgres "$SITE_NAME" "${ENV_FILE:-}" "${SERVICE_NAME:-}" "$DATABASE_URL_VAR" "$db_archive"; then
        postgres_status="ok"
      else
        postgres_status="failed"
      fi
      ;;
    sqlite)
      local sqlite_path
      local -a sqlite_paths=()
      IFS=' ' read -r -a sqlite_paths <<< "$SQLITE_PATHS"
      for sqlite_path in "${sqlite_paths[@]}"; do
        if [[ -z "$sqlite_path" ]]; then
          continue
        fi
        local sqlite_name sqlite_dest
        sqlite_name="$(basename "$sqlite_path")"
        sqlite_dest="$sqlite_dir/$sqlite_name.backup"
        if backup_sqlite "$SITE_NAME" "$sqlite_path" "$sqlite_dest"; then
          :
        else
          sqlite_status="failed"
        fi
      done
      if [[ "$sqlite_status" != "failed" ]]; then
        sqlite_status="ok"
      fi
      ;;
    none)
      postgres_status="none"
      ;;
    auto)
      if [[ -n "${SQLITE_PATHS:-}" ]]; then
        local sqlite_path
        local -a sqlite_paths=()
        IFS=' ' read -r -a sqlite_paths <<< "$SQLITE_PATHS"
        for sqlite_path in "${sqlite_paths[@]}"; do
          if [[ -z "$sqlite_path" ]]; then
            continue
          fi
          local sqlite_name sqlite_dest
          sqlite_name="$(basename "$sqlite_path")"
          sqlite_dest="$sqlite_dir/$sqlite_name.backup"
          if backup_sqlite "$SITE_NAME" "$sqlite_path" "$sqlite_dest"; then
            :
          else
            sqlite_status="failed"
          fi
        done
        if [[ "$sqlite_status" != "failed" ]]; then
          sqlite_status="ok"
        fi
      fi
      if [[ -n "${ENV_FILE:-}" || -n "${SERVICE_NAME:-}" ]]; then
        if backup_postgres "$SITE_NAME" "${ENV_FILE:-}" "${SERVICE_NAME:-}" "$DATABASE_URL_VAR" "$db_archive"; then
          postgres_status="ok"
        else
          postgres_status="failed"
        fi
      fi
      ;;
    *)
      warn "unknown DB_TYPE for $SITE_NAME: $DB_TYPE"
      postgres_status="unknown"
      ;;
  esac

  if [[ -n "$RETENTION_DAYS" ]]; then
    site_notes+=("retention_days=$RETENTION_DAYS")
  fi
  if [[ -s "$app_archive" ]]; then
    site_notes+=("app=$(basename "$app_archive"):$(file_size "$app_archive")")
  fi
  if [[ -s "$db_archive" ]]; then
    site_notes+=("db=$(basename "$db_archive"):$(file_size "$db_archive")")
  fi
  if [[ "$sqlite_status" == "ok" ]]; then
    while IFS= read -r sqlite_dest; do
      [[ -n "$sqlite_dest" ]] || continue
      site_notes+=("sqlite=$(basename "$sqlite_dest"):$(file_size "$sqlite_dest")")
    done < <(find "$sqlite_dir" -maxdepth 1 -type f -name '*.backup' -print | sort)
  fi

  site_names+=("$SITE_NAME")

  if [[ "$app_status" == "failed" || "$postgres_status" == "failed" || "$sqlite_status" == "failed" ]]; then
    site_lines+=("$SITE_NAME|error|app=$app_status postgres=$postgres_status sqlite=$sqlite_status")
  else
    site_lines+=("$SITE_NAME|ok|app=$app_status postgres=$postgres_status sqlite=$sqlite_status")
  fi
  if ((${#site_notes[@]} > 0)); then
    global_lines+=("$SITE_NAME:${site_notes[*]}")
  fi
}

prune_old_backups() {
  local retention_days="${1:-30}"
  local dir
  while IFS= read -r dir; do
    [[ -d "$dir" ]] || continue
    if [[ "$(basename "$dir")" == latest ]]; then
      continue
    fi
    rm -rf -- "$dir"
  done < <(
    find "$BACKUP_ROOT" -maxdepth 1 -mindepth 1 -type d -regextype posix-extended \
      -regex ".*/[0-9]{8}T[0-9]{6}Z" -mtime +"$retention_days" -print
  )
}

write_manifest() {
  {
    printf 'timestamp=%s\n' "$timestamp"
    printf 'hostname=%s\n' "$hostname_value"
    printf 'script_version=%s\n' "$SCRIPT_VERSION"
    printf 'backup_root=%s\n' "$BACKUP_ROOT"
    printf 'backup_dir=%s\n' "$backup_dir"
    printf 'status=%s\n' "$([[ $had_error -eq 0 ]] && printf success || printf partial)"
    printf 'sites=%s\n\n' "$(printf '%s ' "${site_names[@]:-}" | sed 's/ $//')"
  } > "$manifest_file"

  append_manifest_block "Created files:" "${created_files[@]}"
  append_manifest_block "Verification:" "${verification_lines[@]}"
  append_manifest_block "Sites:" "${site_lines[@]}"
  append_manifest_block "Warnings:" "${warnings[@]}"
  append_manifest_block "Global notes:" "${global_lines[@]}"
}

main() {
  if [[ ! -d "$CONFIG_DIR" ]]; then
    note_error "missing site config directory: $CONFIG_DIR"
    exit 1
  fi

  ensure_dir "$BACKUP_ROOT"
  exec 9>"$lock_file"
  if ! flock -n 9; then
    note_error "another backup is already running"
    exit 1
  fi

  ensure_dir "$backup_dir"

  shopt -s nullglob
  local -a config_files=("$CONFIG_DIR"/*.conf)
  shopt -u nullglob

  if ((${#config_files[@]} == 0)); then
    note_error "no site configs found in $CONFIG_DIR"
    exit 1
  fi

  local conf_file
  for conf_file in "${config_files[@]}"; do
    backup_site "$conf_file"
  done

  backup_global_assets "$backup_dir"
  write_manifest
  printf '%s backup_dir=%s status=%s warnings=%d\n' "$timestamp" "$backup_dir" "$([[ $had_error -eq 0 ]] && printf success || printf partial)" "${#warnings[@]}" >> "$log_file"

  if [[ $had_error -eq 0 ]]; then
    ln -sfn "$backup_dir" "$BACKUP_ROOT/latest"
    prune_old_backups "$retention_days_global"
    printf '%s latest=%s\n' "$timestamp" "$backup_dir" >> "$log_file"
  else
    printf '%s latest=unchanged\n' "$timestamp" >> "$log_file"
  fi

  if [[ $had_error -ne 0 ]]; then
    exit 1
  fi
}

main "$@"
