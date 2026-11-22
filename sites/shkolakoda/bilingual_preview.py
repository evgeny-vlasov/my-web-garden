"""Opt-in, noindex language preview. Production activation is a later step."""
import os
from urllib.parse import urlencode

from flask import abort, g, request

from russian_preview import PAGES

HOST_LANGUAGES = {
    'schoolofcode.ca': 'en', 'www.schoolofcode.ca': 'en',
    'shkolakoda.com': 'ru', 'www.shkolakoda.com': 'ru',
}
LOCAL_HOSTS = {'localhost', '127.0.0.1'}
LANGUAGE_ORIGINS = {'en': 'https://schoolofcode.ca', 'ru': 'https://shkolakoda.com'}


def current_origin(for_host=False):
    key = 'site_locale' if for_host else 'preview_locale'
    return LANGUAGE_ORIGINS[g.get(key, 'en')]


def preview_url(path, language=None):
    language = language or g.preview_locale
    if language not in ('en', 'ru'):
        raise ValueError('Unsupported preview language')
    if request.host.split(':')[0] in LOCAL_HOSTS:
        return path + ('&' if '?' in path else '?') + urlencode({'preview_lang': language})
    return LANGUAGE_ORIGINS[language] + path


def register_preview(app):
    app.config['BILINGUAL_PREVIEW'] = os.environ.get('BILINGUAL_PREVIEW') == '1'
    app.config['LANGUAGE_CUTOVER'] = os.environ.get('SOCCL_LANGUAGE_CUTOVER') == '1'

    @app.before_request
    def select_preview_language():
        g.preview_locale = 'en'
        g.preview_fallback = False
        if not (app.config['BILINGUAL_PREVIEW'] or app.config['LANGUAGE_CUTOVER']):
            return
        host = request.host.split(':')[0].lower()
        if host not in HOST_LANGUAGES and host not in LOCAL_HOSTS:
            abort(404)
        language = HOST_LANGUAGES.get(host, 'en')
        if host in LOCAL_HOSTS and app.config['BILINGUAL_PREVIEW']:
            language = request.args.get('preview_lang', 'en')
            if language not in ('en', 'ru'):
                abort(400)
        g.site_locale = language
        g.preview_fallback = language == 'ru' and request.path not in PAGES
        g.preview_locale = 'en' if g.preview_fallback else language

    @app.after_request
    def preview_headers(response):
        if app.config['BILINGUAL_PREVIEW']:
            response.headers['X-Robots-Tag'] = 'noindex, nofollow'
            response.headers['Cache-Control'] = 'no-store'
        if app.config['BILINGUAL_PREVIEW'] or app.config['LANGUAGE_CUTOVER']:
            response.headers['Content-Language'] = g.get('preview_locale', 'en')
        return response

    @app.context_processor
    def preview_context():
        enabled = app.config['BILINGUAL_PREVIEW']
        cutover = app.config['LANGUAGE_CUTOVER'] and not enabled
        locale = g.get('preview_locale', 'en')
        return {
            'preview_enabled': enabled,
            'language_switch_enabled': enabled or cutover,
            'language_alternates': LANGUAGE_ORIGINS if cutover and request.path in PAGES
                                   and not request.path.startswith('/workbench') else {},
            'preview_locale': locale,
            'preview_fallback': g.get('preview_fallback', False),
            'preview_has_russian': request.path in PAGES,
            'preview_url': preview_url,
            'preview_page': PAGES.get(request.path),
            'preview_has_translation': lambda path: path in PAGES,
            'preview_switch_url': preview_url(request.path, 'en' if locale == 'ru' else 'ru') if enabled and request.path in PAGES else None,
        }

    @app.url_defaults
    def preserve_local_preview_language(endpoint, values):
        if (app.config['BILINGUAL_PREVIEW'] and request.host.split(':')[0] in LOCAL_HOSTS
                and endpoint not in ('static', 'favicon_svg') and 'preview_lang' not in values):
            values['preview_lang'] = g.get('preview_locale', 'en')


def select_template(app, original):
    if g.get('preview_locale') == 'ru':
        return 'preview/russian_page.html'
    return original
