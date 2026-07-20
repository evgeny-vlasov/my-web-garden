"""Schema-validated, Git-backed publication discovery for School of Code."""

from __future__ import annotations

import argparse
import copy
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

from jsonschema import Draft202012Validator, FormatChecker


SITE_ROOT = Path(__file__).resolve().parent
DEFAULT_CONTENT_ROOT = SITE_ROOT / "content"
DEFAULT_SCRATCH_ROOT = SITE_ROOT / "scratch_projects"
DEFAULT_SCHEMA_PATH = DEFAULT_CONTENT_ROOT / "schemas" / "publication.schema.json"
DEFAULT_STATIC_ROOT = SITE_ROOT / "static"
PUBLICATION_DIRECTORIES = {
    "campaigns": "campaign",
    "articles": "article",
    "projects": "project",
    "media": "media",
}
URL_PREFIXES = {
    "campaign": "/campaigns/",
    "article": "/blog/",
    "project": "/projects/",
}


class ContentValidationError(ValueError):
    """Raised when checked-in content cannot be published safely."""


def _format_path(parts):
    return ".".join(str(part) for part in parts) or "record"


def _parse_publish_at(value, source):
    if value is None:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (TypeError, ValueError) as error:
        raise ContentValidationError(f"{source}: publish_at is not a valid ISO 8601 timestamp") from error
    if parsed.tzinfo is None:
        raise ContentValidationError(f"{source}: publish_at must include a timezone")
    return parsed.astimezone(timezone.utc)


def _safe_relative_path(value, source, field):
    if not isinstance(value, str) or not value:
        raise ContentValidationError(f"{source}: {field} must be a non-empty relative path")
    if "\\" in value:
        raise ContentValidationError(f"{source}: {field} must use forward slashes")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or "." in path.parts or value.startswith("//"):
        raise ContentValidationError(f"{source}: unsafe {field} path {value!r}")
    return path


class ContentRepository:
    """Discover, validate, index, and expose publication records."""

    def __init__(self, records, static_root, sources):
        self.static_root = Path(static_root).resolve()
        self._records = tuple(records)
        self._sources = dict(sources)
        self._by_id = {record["id"]: record for record in records}
        self._by_kind_slug = {(record["kind"], record["slug"]): record for record in records}

    @classmethod
    def load(
        cls,
        content_root=DEFAULT_CONTENT_ROOT,
        scratch_root=DEFAULT_SCRATCH_ROOT,
        schema_path=DEFAULT_SCHEMA_PATH,
        static_root=DEFAULT_STATIC_ROOT,
    ):
        content_root = Path(content_root).resolve()
        scratch_root = Path(scratch_root).resolve() if scratch_root else None
        schema_path = Path(schema_path).resolve()
        static_root = Path(static_root).resolve()
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        discovered = []

        for directory, expected_kind in PUBLICATION_DIRECTORIES.items():
            root = content_root / directory
            if not root.exists():
                continue
            for path in sorted(root.rglob("*.json")):
                cls._assert_discovery_path(path, root)
                discovered.append((path, expected_kind))

        if scratch_root and scratch_root.exists():
            for path in sorted(scratch_root.glob("*.json")):
                cls._assert_discovery_path(path, scratch_root)
                discovered.append((path, "project"))

        records = []
        sources = {}
        validation_errors = []
        for path, expected_kind in discovered:
            try:
                record = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as error:
                validation_errors.append(f"{path}: invalid JSON: {error}")
                continue
            errors = sorted(validator.iter_errors(record), key=lambda item: list(item.absolute_path))
            if errors:
                for error in errors:
                    validation_errors.append(f"{path}: {_format_path(error.absolute_path)}: {error.message}")
                continue
            if record["kind"] != expected_kind:
                validation_errors.append(
                    f"{path}: kind {record['kind']!r} does not match the {path.parent.name!r} content directory"
                )
                continue
            records.append(record)
            sources[id(record)] = path

        if validation_errors:
            raise ContentValidationError("\n".join(validation_errors))

        repository = cls(records, static_root, sources)
        repository._validate_index()
        repository._validate_paths_and_links()
        return repository

    @staticmethod
    def _assert_discovery_path(path, root):
        resolved = path.resolve()
        try:
            resolved.relative_to(root.resolve())
        except ValueError as error:
            raise ContentValidationError(f"Unsafe content path escapes {root}: {path}") from error
        if path.is_symlink():
            raise ContentValidationError(f"Content files may not be symlinks: {path}")

    def _source(self, record):
        return self._sources.get(id(record), Path("<memory>"))

    def _validate_index(self):
        ids = defaultdict(list)
        slugs = defaultdict(list)
        for record in self._records:
            ids[record["id"]].append(self._source(record))
            slugs[(record["kind"], record["slug"])].append(self._source(record))
            _parse_publish_at(record["publish_at"], self._source(record))
        errors = []
        for stable_id, paths in ids.items():
            if len(paths) > 1:
                errors.append(f"Duplicate content id {stable_id!r}: {', '.join(map(str, paths))}")
        for (kind, slug), paths in slugs.items():
            if len(paths) > 1:
                errors.append(f"Duplicate {kind} slug {slug!r}: {', '.join(map(str, paths))}")
        if errors:
            raise ContentValidationError("\n".join(errors))

    def _validate_paths_and_links(self):
        errors = []
        for record in self._records:
            source = self._source(record)
            if record["kind"] == "media":
                try:
                    media_path = _safe_relative_path(record["path"], source, "media")
                    candidate = (self.static_root / Path(*media_path.parts)).resolve()
                    candidate.relative_to(self.static_root)
                    if not candidate.is_file():
                        errors.append(f"{source}: missing media file {record['path']!r}")
                except (ContentValidationError, ValueError) as error:
                    errors.append(str(error))

            canonical = record["seo"].get("canonical_path")
            if canonical:
                try:
                    _safe_relative_path(canonical.lstrip("/"), source, "canonical")
                except ContentValidationError as error:
                    errors.append(str(error))
                expected = self.url_for(record)
                if record["kind"] != "media" and canonical != expected:
                    errors.append(f"{source}: canonical_path must match the publication URL {expected!r}")

            image = record.get("image")
            if image:
                media = self._by_id.get(image["media_id"])
                if media is None or media["kind"] != "media":
                    errors.append(f"{source}: missing media id {image['media_id']!r}")

            campaign_id = record.get("campaign_id")
            if campaign_id:
                campaign = self._by_id.get(campaign_id)
                if campaign is None or campaign["kind"] != "campaign":
                    errors.append(f"{source}: invalid campaign id {campaign_id!r}")

            links = list(record.get("internal_links", []))
            if record.get("call_to_action"):
                links.append(record["call_to_action"])
            for link in links:
                target = self._by_id.get(link["target_id"])
                if target is None:
                    errors.append(f"{source}: invalid internal link target {link['target_id']!r}")
                elif record["status"] in {"published", "scheduled"} and target["status"] in {"draft", "archived"}:
                    errors.append(f"{source}: public content cannot link to non-public target {target['id']!r}")

            if record.get("scratch_pilot"):
                project_root = self.static_root / "projects" / record["slug"]
                for download in record.get("downloads", []):
                    try:
                        filename = _safe_relative_path(download["filename"], source, "download")
                        if len(filename.parts) != 1:
                            raise ContentValidationError(f"{source}: download filename must not contain directories")
                        if not (project_root / filename.name).is_file():
                            errors.append(f"{source}: missing project download {filename.name!r}")
                    except ContentValidationError as error:
                        errors.append(str(error))
                for slot in record.get("art_slots", {}).values():
                    try:
                        asset = _safe_relative_path(slot["src"], source, "art asset")
                        if not (self.static_root / Path(*asset.parts)).is_file():
                            errors.append(f"{source}: missing project art asset {slot['src']!r}")
                    except ContentValidationError as error:
                        errors.append(str(error))

        if errors:
            raise ContentValidationError("\n".join(errors))

    def validate_route_compatibility(self, legacy_projects=(), legacy_articles=(), legacy_lessons=()):
        """Validate references that live in the established Python curriculum."""
        errors = []
        legacy_projects = set(legacy_projects)
        legacy_articles = set(legacy_articles)
        legacy_lessons = set(legacy_lessons)
        for record in self._records:
            source = self._source(record)
            if record["kind"] == "project" and record["slug"] in legacy_projects and not record.get("scratch_pilot"):
                errors.append(f"{source}: project slug conflicts with an existing route: {record['slug']!r}")
            if record["kind"] == "article" and record["slug"] in legacy_articles:
                errors.append(f"{source}: article slug conflicts with an existing route: {record['slug']!r}")
            related = record.get("related", {})
            catalogs = {
                "lessons": legacy_lessons,
                "projects": legacy_projects | {item["slug"] for item in self._records if item["kind"] == "project"},
                "articles": legacy_articles | {item["slug"] for item in self._records if item["kind"] == "article"},
            }
            for relation, slugs in related.items():
                for slug in slugs:
                    if slug not in catalogs[relation]:
                        errors.append(f"{source}: invalid related {relation[:-1]} {slug!r}")
        if errors:
            raise ContentValidationError("\n".join(errors))

    def all(self, kind=None):
        records = self._records if kind is None else (record for record in self._records if record["kind"] == kind)
        return [copy.deepcopy(record) for record in records]

    def by_id(self, stable_id):
        record = self._by_id.get(stable_id)
        return copy.deepcopy(record) if record else None

    def by_slug(self, kind, slug):
        record = self._by_kind_slug.get((kind, slug))
        return copy.deepcopy(record) if record else None

    def public(self, kind=None, now=None):
        now = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
        records = [record for record in self._records if kind is None or record["kind"] == kind]
        visible = [record for record in records if self.is_public(record, now)]
        visible.sort(key=lambda record: (_parse_publish_at(record["publish_at"], self._source(record)) or datetime.min.replace(tzinfo=timezone.utc), record["title"]), reverse=True)
        return [copy.deepcopy(record) for record in visible]

    def public_by_slug(self, kind, slug, now=None):
        record = self._by_kind_slug.get((kind, slug))
        if record is None or not self.is_public(record, now):
            return None
        return copy.deepcopy(record)

    def is_public(self, record, now=None):
        now = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
        if record["status"] not in {"published", "scheduled"}:
            return False
        publish_at = _parse_publish_at(record["publish_at"], self._source(record))
        return publish_at is None or publish_at <= now

    def url_for(self, record):
        if record["kind"] == "media":
            return f"/static/{record['path']}"
        return f"{URL_PREFIXES[record['kind']]}{record['slug']}"

    def present(self, record):
        """Return a template-safe record with resolved internal URLs."""
        presented = copy.deepcopy(record)
        presented["url"] = self.url_for(record)
        image = presented.get("image")
        if image:
            media = self._by_id[image["media_id"]]
            image["url"] = self.url_for(media)
        for link in presented.get("internal_links", []):
            target = self._by_id[link["target_id"]]
            link["url"] = self.url_for(target)
        if presented.get("call_to_action"):
            target = self._by_id[presented["call_to_action"]["target_id"]]
            presented["call_to_action"]["url"] = self.url_for(target)
        return presented

    def source_record(self, filename):
        """Return a defensive copy of a discovered Scratch project by filename."""
        for record in self._records:
            if self._source(record).name == filename and record.get("scratch_pilot"):
                return copy.deepcopy(record)
        raise ContentValidationError(f"Scratch publication was not discovered: {filename}")


CONTENT = ContentRepository.load()


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate School of Code Git-backed content")
    parser.add_argument("--check", action="store_true", help="validate all discovered publications")
    parser.parse_args(argv)
    print(f"Validated {len(CONTENT.all())} publication records.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
