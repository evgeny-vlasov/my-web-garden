# School of Code Git-backed publishing

## Purpose

School of Code Computer Lab publications are reviewed as ordinary Git changes. A valid content file becomes available to the Flask application automatically; adding a campaign, article, or general project does not require a route or template change.

This foundation extends the existing structured Scratch architecture. It does not replace `curriculum.py`, `project_library.py`, or `blog_content.py`. The production Escape from the Giant Pigeon record remains the rich Scratch pilot and is now validated and indexed by the same publication repository used for new content.

## Repository layout

```text
sites/shkolakoda/
├── content/
│   ├── campaigns/       # campaign publication JSON
│   ├── articles/        # new blog article JSON
│   ├── projects/        # general project page JSON
│   ├── media/           # manifests for files below static/
│   └── schemas/
│       └── publication.schema.json
├── scratch_projects/    # rich Scratch project JSON, discovered as project content
├── publishing.py        # discovery, validation, visibility, and URL resolution
├── static/              # immutable website media and project downloads
└── templates/
    ├── publication.html # shared campaign/article/project renderer
    └── campaigns.html   # automatically populated campaign index
```

`publishing.CONTENT` is built when the application imports. Invalid checked-in content stops application startup and CI instead of producing a partial or silently broken publication.

## Common publication contract

Every record carries these fields:

- `schema_version`: currently `1`;
- `kind`: `campaign`, `article`, `project`, or `media`;
- `id`: stable, globally unique machine identity; do not change it after links use it;
- `slug`: lowercase URL identity, unique within its kind;
- `title` and `summary`;
- `status`: `draft`, `scheduled`, `published`, or `archived`;
- `publish_at`: timezone-aware ISO 8601 timestamp or `null` where allowed;
- `topics` and `categories`;
- `seo.title`, `seo.description`, and optional canonical/no-index fields;
- `internal_links`: labels plus stable target IDs, never hand-built content URLs;
- `image`: a media ID and page-specific alt text, or `null`;
- `related.lessons`, `related.projects`, and `related.articles`;
- `campaign_id`: a stable campaign ID or `null`.

Articles add `author` and `body`. General projects add `project` display metadata and `body`. Campaigns add `body` and may add a `call_to_action`. Media records add `path`, `media_type`, `alt`, and `credit`. The JSON Schema is the authoritative field and length contract.

The Scratch pilot has the same common envelope plus its existing downloads, art slots, code sections, and script model. `scratch_content.py` adapts that validated record back into the established project template shape.

## Discovery and rendering

At startup, `ContentRepository.load()` discovers every JSON file below the four `content/` publication directories and every top-level JSON file in `scratch_projects/`. Directory and `kind` must agree.

Public URLs are derived from kind and slug:

| Kind | URL |
| --- | --- |
| campaign | `/campaigns/<slug>` |
| article | `/blog/<slug>` |
| project | `/projects/<slug>` |
| media | `/static/<path>` |

The established blog and project routes look in their Python libraries first, preserving all existing behavior. If no legacy record matches, they look up a currently public Git-backed record and use `publication.html`. Indexes and the sitemap query the repository at request time, so a scheduled record can become public without a code or template edit.

## Visibility rules

- `draft` and `archived` records are never public.
- `scheduled` records become public when `publish_at` is reached.
- `published` records are public when `publish_at` is `null` or has been reached. A future timestamp prevents accidental early visibility.
- Media can be physically present in `static/` while every page referencing it remains private.

The sample at `content/campaigns/sample-scratch-build-week.json` is intentionally `draft`. It validates in CI but returns 404 at its campaign URL and is absent from indexes and the sitemap.

## Validation boundaries

CI and application startup reject:

- JSON Schema errors or a kind/directory mismatch;
- duplicate stable IDs or duplicate slugs within a kind;
- invalid or timezone-free publication timestamps;
- missing media manifests, missing static files, or missing Scratch downloads/art;
- internal link or campaign IDs that do not exist;
- related lesson, project, or article slugs that do not exist;
- unsafe absolute, parent-traversal, backslash, symlink, and canonical paths;
- new article/project slugs that collide with established Python content;
- public records that link to draft or archived targets.

Run the same checks locally:

```bash
cd sites/shkolakoda
venv/bin/python -m publishing --check
venv/bin/python -m unittest discover -s tests -v
```

## Authoring workflow

1. Copy a record of the intended kind and assign a new stable ID and slug.
2. Add media beneath `static/`, then add its manifest beneath `content/media/`.
3. Use stable IDs for `image`, `campaign_id`, calls to action, and internal links.
4. Keep the record `draft` while editing and review the Git diff.
5. Set `scheduled` with a timezone-aware timestamp, or `published` with an eligible timestamp, only in the review that should make it public.
6. Open a pull request. `soccl-ci.yml` validates every PR targeting `main`.

Changing a slug changes its URL and should be treated as a redirect/migration task. Changing a stable ID breaks ID-based relationships and should be avoided after publication.

## Website deployment and recovery

`.github/workflows/soccl-deploy.yml` runs only for pushes to `main` affecting `sites/shkolakoda` (or the workflow itself), and by manual `workflow_dispatch`. It validates the selected revision before entering the protected `soccl-production` environment. A repository-wide concurrency group allows only one SoCCL deployment at a time and does not cancel an in-progress deployment.

The production environment must provide these secrets:

- `SOCCL_DEPLOY_HOST`;
- `SOCCL_DEPLOY_USER`;
- `SOCCL_DEPLOY_SSH_KEY`;
- `SOCCL_DEPLOY_KNOWN_HOSTS`.

The deployment account is expected to expose a narrowly scoped server-side command:

```text
/usr/local/bin/soccl-deploy <verified-git-commit>
```

That command is an infrastructure concern and is not created or changed by this content foundation. A failed deployment can be retried from Actions with `workflow_dispatch` and an explicit known-good commit, tag, or branch. Environment protection can require a reviewer before the SSH request runs.

## Social publishing boundary

The deploy workflow updates the website only. It has no Meta, X, Telegram, webhook, or social-network credentials and performs no social post creation. Channel-specific publishing should use separate workflows, credentials, approvals, idempotency records, and failure recovery so a website publication never implies a social announcement.
