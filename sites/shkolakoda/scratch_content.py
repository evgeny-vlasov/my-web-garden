"""Adapt rich Scratch records from the shared publishing repository."""

from publishing import CONTENT


def load_scratch_project(filename):
    """Return one checked-in Scratch pilot record and its script lookup."""
    record = CONTENT.source_record(filename)
    record["publication_status"] = record.pop("status")
    record["status"] = record.pop("project_status")
    record["meta_description"] = record["seo"]["description"]
    scripts = record.pop("scripts")
    scripts_by_id = {script["id"]: script for script in scripts}
    if len(scripts_by_id) != len(scripts):
        raise ValueError(f"Duplicate Scratch script id in {filename}")
    for section in record["code_sections"]:
        section["scripts"] = [scripts_by_id[script_id] for script_id in section.pop("script_ids")]
    record["scratch_scripts"] = scripts
    return record
