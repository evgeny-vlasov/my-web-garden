"""Standalone Webgarden starter. Public content lives in site.json."""

import json
import os
from pathlib import Path

from flask import Flask, jsonify, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from bot_proxy import forward_chat, validate_bot_url


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 65536
app.config['BOT_CHAT_URL'] = os.environ.get('BOT_CHAT_URL', '')
if app.config['BOT_CHAT_URL']:
    validate_bot_url(app.config['BOT_CHAT_URL'])
content = json.loads((Path(__file__).parent / 'site.json').read_text(encoding='utf-8'))
limiter = Limiter(get_remote_address, app=app, storage_uri='memory://')


@app.get('/')
def home():
    return render_template('index.html', site=content, chat_enabled=bool(app.config['BOT_CHAT_URL']))


@app.get('/health')
def health():
    return jsonify(status='ok', site=content['slug'], chat_configured=bool(app.config['BOT_CHAT_URL']))


@app.post('/api/chat')
@limiter.limit('10 per minute')
def chat():
    return forward_chat(app.config['BOT_CHAT_URL'])
