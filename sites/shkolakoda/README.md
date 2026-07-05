# Happy Science Calgary

This Flask project serves the Happy Science Calgary website.

## Intended Deployment

This app is intended for `science.shkolakoda.com`.

## URL Plan

- `/` shows the Happy Science Calgary homepage.
- `/camps` shows pilot camp themes.
- `/safety` shows parent safety and trust information.
- `/contact` shows contact details and the interest list call to action.
- The separate School of Code Calgary app will live at `https://shkolakoda.com`.

## Debian VPS Deployment Notes

In production, this app will run on `127.0.0.1:8001`.

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
gunicorn --bind 127.0.0.1:8001 wsgi:app
```

Nginx reverse proxy configuration will be handled separately.

Systemd service configuration will be handled separately.
