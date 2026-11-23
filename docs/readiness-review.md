# Webgarden readiness review

Reviewed on 2026-11-22 against GitHub main at `a816bfd`.

The direction is a functional website in about 15 minutes, followed by a Bot
Army assistant in another 15. The immediate bottleneck is reproducing a launch
from reviewed source. Several working services rely on server-local changes
and manual integration.

## Review coverage

The review covered application entry points, shared Flask configuration,
authentication and chat boundaries, templates, migration histories, dependency
files, CI, deployment and backup scripts, and canonical documentation.
Read-only server checks established service paths, public routing, release
markers, backup job status, and the existing Bot Army connection.

The private publishing desk, the external social publishing timer, Bot Army,
and Tom Umber have distinct runtimes. Bot Army and Tom Umber were inspected at
their Webgarden integration boundaries. Their entire separate repositories and
private production data are outside this source review.

## Fixed in this branch

| Finding | Change |
|---|---|
| No usable supported local site creator | `tools/create_site.py` creates an independent Flask site and matching Bot Army handoff from four public brief fields. It refuses existing destinations and cleans up failed creation. |
| Framework configuration depended on the working directory and overwrote site settings | Resolve templates from `sites/<site>`, then apply explicit site settings after defaults. Reject known development signing keys in production. |
| Custom error files could return HTTP 200 | Preserve 404 and 500 status codes. |
| Image cleanup could raise another exception before paths were initialized | Initialize cleanup paths and remove partial thumbnails as well as partial originals. |
| Public chat accepted malformed requests and returned internal failure details | Use a shared loopback-only bridge with message/history/session validation, public errors, and a Psyling rate limit. Reuse the same bridge in generated sites. |
| Language switching trusted an external referrer | Restrict the redirect to the current origin. |
| LAIC's PostgreSQL schema was missing from Git | Restore the schema from the running source and add a narrow ignore exception. Test the PostgreSQL form path and local fallback. |
| Private publishing desk could schedule unapproved copy and retain approval after edits | Require approval and a complete editorial gate. Edited approved/scheduled copy returns to review and loses its schedule. |
| Publishing link validation accepted hostname prefixes and rejected the new English domain | Validate exact HTTPS hosts for both school domains. |
| Publishing desk installer expected an untracked file and left existing workers running | Remove the absent file from its inputs, include editorial instructions, and restart the named service when the installer is invoked. |
| Canonical School of Code deployer existed only on the host and checked one public domain | Track its source in `deploy/soccl-deploy.sh`, adding both-domain activation and rollback checks. |
| Retired provisioners still executed infrastructure commands | Exit immediately with a pointer to the current lifecycle and starter. |
| Backup exclusions were wrapped twice and the school profile archived its old checkout | Pass the intended tar options directly, test archive contents, and capture the active immutable release with its revision marker. |
| Backup validation could accept an empty archive set or a failed SQLite integrity result | Require at least one archive and verify the actual SQLite integrity result, including a Python fallback. Add the missing Science backup profile. |
| CI covered only the public school application | Add platform, Psyling, PoolEmergency, LAIC, private publisher, starter, shell syntax, and dependency advisory checks. |
| Dependency files pinned versions with published security advisories | Update affected runtime and development packages. Runtime image processing now requires Python 3.11+. |
| Scratch's development dependency tree also contained advisories | Override affected dependencies, pin hull.js to its upstream security-fix commit, and validate with npm 10. Run full npm audit and Scratch validation in CI. |
| Architecture omitted the English domain and supporting runtimes | Update the school language/domain inventory, private desk, generated notes, social timer, and bot connection. |

## Verification

The review uses temporary source copies and isolated test data. Application
tests ran with Python 3.11 and the updated dependencies. The test suites cover
the shared framework and generator, Psyling, PoolEmergency, LAIC, both school
languages, and the private publishing desk.

All 177 automated tests passed. In addition, a temporary PostgreSQL 15 instance
passed PoolEmergency and Psyling's full migration chains and normal contact
submissions, plus LAIC's schema initialization and normal contact submission.
Test email delivery was replaced with controlled responses.

The new regressions exercise failures at normal entry points, including an
actual generated Flask application, migrated contact submissions, malformed
chat requests, error responses, public redirects, upload processing, approval
and scheduling changes, corrupt backup data, and both-domain deployment health.

The API bridge tests use controlled bot replies. A newly generated site still
needs a real Bot Army process and a live-answer check before public launch.
Shell health tests replace network/service commands with test doubles. They
exercise the verification logic, including English-domain failure.

Dependency checks use `pip-audit` against the individual requirement files.
All eight unique Python dependency files and the full Scratch npm dependency
tree passed their advisory scans. The Scratch build, browser rendering, and
official-VM runtime validation passed with the updated lockfile. npm 10 or newer
is required for its pinned upstream hull.js override.
The CI workflow repeats these checks so newly published advisories are visible.
Upstream release information is available for
[Flask](https://flask.palletsprojects.com/en/stable/changes/),
[Pillow](https://pillow.readthedocs.io/en/stable/releasenotes/index.html), and
[Bleach](https://github.com/mozilla/bleach).

All seven live public homepages, including both school domains, returned
HTTP 200 during the review.

## Remaining launch work

| Priority | Work | Completion condition |
|---|---|---|
| First | Reconcile the shared live checkout | Preserve existing Psyling content, Science template changes, and school source edits. Apply reviewed revisions per affected site and verify newly started workers. The live shared checkout was still `328cecb` during this review. |
| First | Preserve Bot Army's actual source | Review and commit its existing OpenAI adapter, bot changes, requirements, and user-service definitions in its own repository. Its tracked HEAD was `2d61302`, with local changes supplying the working OpenAI runtime. |
| Next | Automate one site-and-bot instance | Consume the same brief, assign isolated paths/listeners, configure the bot, launch a preview, and verify a real answer. Record a source revision and per-instance state. |
| Next | Add reversible removal to that same workflow | One action disables the site's route and bot access, verifies both endpoints, and keeps recoverable source/configuration/data. Test launch, answer, removal, and restoration on one disposable instance. |
| Next | Install reviewed deployment and backup changes | Compare installed copies, install the reviewed versions, and verify both school domains and actual Science archive inclusion. |
| Next | Verify backup recovery for all persistent state | Include the private publishing database and generated notes, then perform isolated restores. The backup timer last reported success, which does not establish recovery. |
| Before reusing Keystone | Decide its future | Its admin templates are missing and its migrations predate the current shared CRM/blog model. Complete a deliberate revival or retire it after confirming ownership. |
| Separate repository | Preserve Tom Umber's source | Its checkout remains three commits ahead of its recorded upstream. Reconcile and preserve those commits in its own repository. |

## Next acceptance demonstration

Use one disposable business brief to create the website and bot handoff.
Provision its Bot Army process from reviewed source, activate one public
preview, and obtain a correct answer to a real public question. Then remove
the instance, verify both public endpoints, and restore it. Record the actual
commands and timings. That demonstration will show which remaining steps
prevent the 15-minute site and 15-minute bot target.
