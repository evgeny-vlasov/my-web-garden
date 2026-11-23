# Start a Webgarden site

Use Python 3.11 or newer in an isolated source checkout.
Copy [the example brief](../tools/site-brief.example.json) and edit its
`slug`, `name`, `summary`, and `contact` fields with public information.

```bash
python tools/create_site.py /path/to/brief.json
cd sites/YOUR_SLUG
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m flask --app app run --host 127.0.0.1 --port 18080
```

On Windows use `.venv/Scripts/python`. Open `http://127.0.0.1:18080`
and check `/health`.

The generated README explains how to use `bot-handoff.json` and connect
a site-specific Bot Army endpoint. Public activation needs the domain, TLS,
service, listener, revision, and recovery steps in
[the site lifecycle](../docs/site-lifecycle.md). Prepare reversible removal
alongside launch.

For existing production sites use [the deployment guide](../docs/deployment.md).
The remaining launch automation is tracked in
[the readiness review](../docs/readiness-review.md).
