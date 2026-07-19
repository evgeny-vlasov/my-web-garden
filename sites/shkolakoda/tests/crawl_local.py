"""Crawl all School of Code page and pilot-download routes over local HTTP."""

import sys
from pathlib import Path
from urllib.request import urlopen

SITE_ROOT = Path(__file__).resolve().parents[1]
if str(SITE_ROOT) not in sys.path:
    sys.path.insert(0, str(SITE_ROOT))

from app import public_paths
from project_library import PROJECTS


def crawl(base_url="http://127.0.0.1:8000"):
    extra_paths = [
        download["url"]
        for project in PROJECTS.values()
        for download in project.get("downloads", [])
    ]
    extra_paths.extend(
        [
            "/static/css/styles.css",
            "/static/js/scratch-project.js",
            "/static/vendor/scratchblocks/scratchblocks-3.7.1.min.js",
            "/static/projects/escape-from-the-giant-pigeon/project-sketch.svg",
        ]
    )
    results = []
    for path in [*public_paths(), *extra_paths]:
        with urlopen(f"{base_url.rstrip('/')}{path}", timeout=10) as response:
            body = response.read()
            results.append((path, response.status, len(body)))
    failures = [result for result in results if result[1] != 200 or result[2] == 0]
    if failures:
        raise RuntimeError(f"Crawl failures: {failures}")
    print(f"Crawled {len(results)} non-empty HTTP 200 responses from {base_url}.")
    return results


if __name__ == "__main__":
    crawl(sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000")
