"""Load rich Scratch project records without creating a second curriculum system."""

import json
from pathlib import Path


CONTENT_ROOT = Path(__file__).with_name("scratch_projects")


def load_scratch_project(filename):
    """Return one checked-in Scratch pilot record and its script lookup."""
    record = json.loads((CONTENT_ROOT / filename).read_text(encoding="utf-8"))
    scripts = record.pop("scripts")
    scripts_by_id = {script["id"]: script for script in scripts}
    if len(scripts_by_id) != len(scripts):
        raise ValueError(f"Duplicate Scratch script id in {filename}")
    for section in record["code_sections"]:
        section["scripts"] = [scripts_by_id[script_id] for script_id in section.pop("script_ids")]
    record["scratch_scripts"] = scripts
    return record
