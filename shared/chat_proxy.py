"""Same-origin bridge to a site-specific Bot Army process."""

from urllib.parse import urlsplit

from flask import jsonify, request
import requests


def validate_bot_url(url):
    parsed = urlsplit(url)
    if (
        parsed.scheme != 'http'
        or parsed.hostname not in {'localhost', '127.0.0.1', '::1'}
        or parsed.username
        or parsed.password
        or parsed.query
        or parsed.fragment
        or parsed.path != '/api/chat'
    ):
        raise ValueError('BOT_CHAT_URL must be a loopback HTTP /api/chat URL')
    return url


def forward_chat(url):
    if not url:
        return jsonify(error='Chat is awaiting configuration'), 503
    validate_bot_url(url)
    if request.content_length and request.content_length > 65536:
        return jsonify(error='Chat request is too large'), 413
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error='Send a JSON object'), 400
    message = data.get('message')
    if not isinstance(message, str) or not message.strip() or len(message) > 1000:
        return jsonify(error='Message must contain 1 to 1000 characters'), 400
    payload = {'message': message.strip()}
    session_id = data.get('session_id')
    if session_id is not None:
        if not isinstance(session_id, str) or not 1 <= len(session_id) <= 128:
            return jsonify(error='Invalid chat session'), 400
        payload['session_id'] = session_id
    history = data.get('conversation_history', [])
    if not isinstance(history, list) or len(history) > 10:
        return jsonify(error='Invalid conversation history'), 400
    for turn in history:
        if (
            not isinstance(turn, dict)
            or turn.get('role') not in ('user', 'assistant')
            or not isinstance(turn.get('content'), str)
            or not 1 <= len(turn['content']) <= 1000
        ):
            return jsonify(error='Invalid conversation history'), 400
    payload['conversation_history'] = history
    try:
        upstream = requests.post(
            url, json=payload, timeout=(3, 30), allow_redirects=False,
        )
        if upstream.status_code == 429:
            return jsonify(error='Chat is busy. Please try again shortly'), 429
        upstream.raise_for_status()
        result = upstream.json()
        if not isinstance(result, dict) or not isinstance(result.get('response'), str):
            return jsonify(error='Bot service returned an invalid reply'), 502
        if not result['response'].strip():
            return jsonify(error='Bot service returned an empty reply'), 502
        return jsonify(response=result['response'], status='success')
    except (requests.RequestException, ValueError):
        return jsonify(error='Bot service temporarily unavailable'), 503
