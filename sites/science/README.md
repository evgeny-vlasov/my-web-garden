# Happy Science Calgary

This Flask project serves the Happy Science Calgary website at
`science.shkolakoda.com`.

Happy Science is the science side of the Shkolakoda family. Its main future
focus will be hands-on workshops and science labs for kids. Camps remain part
of the offering, but as a secondary or occasional format rather than the main
identity.

School of Code belongs at `https://shkolakoda.com`.

## Production

This app is live at `science.shkolakoda.com`. It runs directly from
`/var/www/webgarden/sites/science` through `webgarden-science.service` on
`127.0.0.1:8005`.

Happy Science has no canonical versioned deployer, deployed-SHA marker, or
version rollback tool. Python changes require a separately authorized restart
of this service; nginx-served static files may change immediately. See
[Webgarden deployment](../../docs/deployment.md) and
[operations](../../docs/operations.md) before making a production change.

## URL Plan

- `/` shows the Happy Science Calgary homepage.
- `/camps` shows pilot camp themes.
- `/safety` shows parent safety and trust information.
- `/contact` shows contact details and the interest list call to action.
- School of Code Calgary lives separately at `https://shkolakoda.com`.

## Local runtime

The commands below are for an isolated development environment. Do not bind to
the production port on the live host while the service is running.

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Test the production WSGI entry with Gunicorn:

```bash
venv/bin/python -m gunicorn --bind 127.0.0.1:8005 wsgi:app
```
