import unittest
from html.parser import HTMLParser
from urllib.parse import parse_qs, urlsplit

from app import app, public_paths
from russian_preview import PAGES
from russian_coordinates import TOPIC, LESSON, PIGEON, TAXI, CHICKEN
from project_library import PROJECTS
from pathlib import Path


class Links(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.items = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.items.append(dict(attrs))


class BilingualPreviewTests(unittest.TestCase):
    def setUp(self):
        self.previous = app.config['BILINGUAL_PREVIEW']
        self.previous_cutover = app.config['LANGUAGE_CUTOVER']
        app.config['BILINGUAL_PREVIEW'] = True
        self.client = app.test_client()

    def tearDown(self):
        app.config['BILINGUAL_PREVIEW'] = self.previous
        app.config['LANGUAGE_CUTOVER'] = self.previous_cutover

    def test_translated_pages_in_both_languages_and_no_seo_cutover(self):
        self.assertFalse(set(public_paths()) - PAGES.keys())
        for path, copy in PAGES.items():
            for host, lang in [('schoolofcode.ca', 'en'), ('shkolakoda.com', 'ru'),
                               ('www.schoolofcode.ca', 'en'), ('www.shkolakoda.com', 'ru')]:
                with self.subTest(path=path, host=host):
                    response = self.client.get(path, base_url='https://' + host)
                    if path.startswith('/workbench') and lang == 'en':
                        self.assertEqual(response.status_code, 302)
                        self.assertEqual(response.headers['Location'], copy['original_url'])
                        continue
                    html = response.get_data(as_text=True)
                    self.assertEqual(response.status_code, 200)
                    self.assertIn('<html lang="' + lang + '">', html)
                    self.assertEqual(response.headers['Content-Language'], lang)
                    self.assertEqual(response.headers['X-Robots-Tag'], 'noindex, nofollow')
                    self.assertEqual(response.headers['Cache-Control'], 'no-store')
                    self.assertIn('rel="canonical" href="https://shkolakoda.com' + path + '"', html)
                    self.assertNotIn('hreflang=', html)
                    if path in ('/', '/programs', '/programs/scratch', '/programs/robotics', '/parents'):
                        self.assertNotIn('active now', html.lower())
                    if lang == 'ru':
                        self.assertIn(copy['heading'], html)
                        self.assertNotIn('Skip to content', html)

    def test_local_switch_keeps_the_page_and_stays_in_preview(self):
        for path in PAGES:
            response = self.client.get(path + '?preview_lang=ru')
            links = Links(response.get_data(as_text=True)).items
            english = next(a['href'] for a in links if a.get('lang') == 'en')
            if path.startswith('/workbench'):
                self.assertEqual(english, PAGES[path]['original_url'])
                continue
            self.assertEqual(urlsplit(english).path, path)
            self.assertEqual(parse_qs(urlsplit(english).query), {'preview_lang': ['en']})
            for a in links:
                href = a.get('href', '')
                if href.startswith('/') and urlsplit(href).path in PAGES:
                    self.assertIn('preview_lang=', href)
            self.assertIn('<html lang="en">', self.client.get(english).get_data(as_text=True))

    def test_domain_switch_uses_explicit_hosts_and_matching_path(self):
        html = self.client.get('/programs/robotics', base_url='https://shkolakoda.com').get_data(as_text=True)
        self.assertIn('href="https://schoolofcode.ca/programs/robotics" lang="en"', html)
        html = self.client.get('/parents', base_url='https://schoolofcode.ca').get_data(as_text=True)
        self.assertIn('href="https://shkolakoda.com/parents" lang="ru"', html)

    def test_untranslated_material_is_explicitly_english(self):
        response = self.client.get('/campaigns', base_url='https://shkolakoda.com')
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('<html lang="en">', html)
        self.assertIn('This page is available in English.', html)
        self.assertNotIn('lang="ru" aria-current=', html)
        self.assertEqual(response.headers['Content-Language'], 'en')

    def test_invalid_host_or_language_does_not_select_content(self):
        self.assertEqual(self.client.get('/', base_url='https://attacker.example').status_code, 404)
        self.assertEqual(self.client.get('/?preview_lang=de').status_code, 400)
        # Query overrides work only on the local preview, not on named domains.
        html = self.client.get('/?preview_lang=en', base_url='https://shkolakoda.com').get_data(as_text=True)
        self.assertIn('<html lang="ru">', html)

    def test_disabled_preview_leaves_domain_behavior_and_indexability_alone(self):
        app.config['BILINGUAL_PREVIEW'] = False
        response = self.client.get('/?preview_lang=ru', base_url='https://shkolakoda.com')
        html = response.get_data(as_text=True)
        self.assertIn('<html lang="en">', html)
        self.assertNotIn('X-Robots-Tag', response.headers)
        self.assertNotIn('preview-toolbar', html)
        self.assertNotIn('noindex, nofollow', html)

    def test_cutover_canonicals_alternates_and_sitemaps_match_each_domain(self):
        app.config.update(BILINGUAL_PREVIEW=False, LANGUAGE_CUTOVER=True)
        for host, lang in [('schoolofcode.ca', 'en'), ('shkolakoda.com', 'ru')]:
            base = 'https://' + host
            response = self.client.get('/topics/coordinates', base_url=base)
            html = response.get_data(as_text=True)
            self.assertIn(f'<html lang="{lang}">', html)
            self.assertIn(f'rel="canonical" href="{base}/topics/coordinates"', html)
            self.assertIn('hreflang="en-CA" href="https://schoolofcode.ca/topics/coordinates"', html)
            self.assertIn('hreflang="ru-CA" href="https://shkolakoda.com/topics/coordinates"', html)
            self.assertNotIn('X-Robots-Tag', response.headers)
            sitemap = self.client.get('/sitemap.xml', base_url=base).get_data(as_text=True)
            self.assertIn(f'<loc>{base}/topics/coordinates</loc>', sitemap)
            self.assertEqual('/workbench/' in sitemap, lang == 'ru')
            robots = self.client.get('/robots.txt', base_url=base).get_data(as_text=True)
            self.assertIn(f'Sitemap: {base}/sitemap.xml', robots)

    def test_coordinates_path_links_stay_in_russian(self):
        sequence = {TOPIC, LESSON, PIGEON, TAXI, CHICKEN}
        for path in sequence:
            html = self.client.get(path + '?preview_lang=ru').get_data(as_text=True)
            destinations = set()
            for link in Links(html).items:
                url = urlsplit(link.get('href', ''))
                if url.path in sequence:
                    # English language-switch link is the one intentional exception.
                    if link.get('lang') != 'en':
                        self.assertEqual(parse_qs(url.query).get('preview_lang'), ['ru'])
                        destinations.add(url.path)
            self.assertTrue(sequence - {path} <= destinations, path)

    def test_home_and_scratch_promote_available_translations(self):
        for path in ['/', '/programs/scratch']:
            html = self.client.get(path + '?preview_lang=ru').get_data(as_text=True)
            links = Links(html).items
            matching = [a['href'] for a in links if urlsplit(a.get('href', '')).path == PIGEON]
            self.assertTrue(matching)
            self.assertTrue(all(parse_qs(urlsplit(href).query).get('preview_lang') == ['ru'] for href in matching))

    def test_pigeon_scripts_and_system_anchors_match_working_original(self):
        class Scripts(HTMLParser):
            def __init__(self, html):
                super().__init__()
                self.active = None
                self.scripts = {}
                self.ids = []
                self.feed(html)
            def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                if 'id' in attrs:
                    self.ids.append(attrs['id'])
                if tag == 'pre' and 'data-script-id' in attrs:
                    self.active = attrs['data-script-id']
                    self.scripts[self.active] = ''
            def handle_data(self, data):
                if self.active is not None:
                    self.scripts[self.active] += data
            def handle_endtag(self, tag):
                if tag == 'pre':
                    self.active = None
        project = PROJECTS['escape-from-the-giant-pigeon']
        html = self.client.get(PIGEON + '?preview_lang=ru').get_data(as_text=True)
        parsed = Scripts(html)
        expected = {script['id']: script['source'] for system in project['code_sections'] for script in system['scripts']}
        self.assertEqual(parsed.scripts, expected)
        self.assertEqual(len(parsed.ids), len(set(parsed.ids)))
        for system in project['code_sections']:
            self.assertIn(system['anchor'], parsed.ids)
        self.assertIn('x = -218/218', html)
        self.assertIn('x = -190, y = -110', html)

    def test_downloads_remain_original_files_and_reject_unknown_names(self):
        project = PROJECTS['escape-from-the-giant-pigeon']
        for download in project['downloads']:
            response = self.client.get(download['url'] + '?preview_lang=ru')
            expected = Path(app.static_folder) / 'projects' / project['slug'] / download['filename']
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, expected.read_bytes())
            self.assertIn('attachment', response.headers['Content-Disposition'])
            response.close()
        self.assertEqual(self.client.get(PIGEON + '/downloads/not-a-project.sb3').status_code, 404)
