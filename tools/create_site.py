"""Create a standalone Flask site and Bot Army handoff from one public brief."""

import argparse
import json
from pathlib import Path
import re
import shutil
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]


def validate_brief(brief):
    if not isinstance(brief, dict):
        raise ValueError('The brief must be a JSON object')
    for field, limit in {'slug': 48, 'name': 120, 'summary': 2000, 'contact': 500}.items():
        value = brief.get(field)
        if not isinstance(value, str) or not value.strip() or len(value) > limit:
            raise ValueError(f'{field} must contain 1 to {limit} characters')
        brief[field] = value.strip()
    if not re.fullmatch(r'[a-z][a-z0-9]*(?:-[a-z0-9]+)*', brief['slug']):
        raise ValueError('slug must use lowercase letters, numbers, and single hyphens')
    contact = brief['contact']
    link = urlsplit(contact)
    if link.scheme == 'https' and link.hostname and not link.username and not link.password:
        brief['contact_url'] = contact
    elif re.fullmatch(r'[^\s@<>:]+@[^\s@<>:]+\.[^\s@<>:]+', contact):
        brief['contact_url'] = 'mailto:' + contact
    else:
        raise ValueError('contact must be an email address or HTTPS URL')
    return {key: brief[key] for key in ('slug', 'name', 'summary', 'contact', 'contact_url')}


def create_site(brief, sites_dir):
    brief = validate_brief(brief)
    sites_dir = Path(sites_dir).resolve()
    sites_dir.mkdir(parents=True, exist_ok=True)
    target = sites_dir / brief['slug']
    # Exclusive creation refuses existing paths, including concurrent requests.
    target.mkdir()
    try:
        shutil.copytree(
            ROOT / 'tools' / 'site_template', target, dirs_exist_ok=True,
            ignore=shutil.ignore_patterns('__pycache__', '*.pyc'),
        )
        shutil.copy2(ROOT / 'shared' / 'chat_proxy.py', target / 'bot_proxy.py')
        (target / 'site.json').write_text(
            json.dumps(brief, ensure_ascii=False, indent=2) + '\n', encoding='utf-8',
        )
        handoff = {
            'site_id': brief['slug'],
            'name': brief['name'],
            'public_knowledge': brief['summary'],
            'contact': brief['contact'],
            'instructions': (
                'Answer using only the supplied public knowledge. Say when a fact is unknown '
                'and refer visitors to the contact. Never invent prices or availability.'
            ),
            'request': {
                'method': 'POST', 'path': '/api/chat',
                'json': {'message': 'What do you offer?', 'session_id': 'launch-check'},
            },
            'response': {'response': 'A nonempty answer based on the public knowledge'},
        }
        (target / 'bot-handoff.json').write_text(
            json.dumps(handoff, ensure_ascii=False, indent=2) + '\n', encoding='utf-8',
        )
    except Exception:
        shutil.rmtree(target)
        raise
    return target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('brief', type=Path)
    parser.add_argument('--sites-dir', type=Path, default=ROOT / 'sites')
    args = parser.parse_args()
    try:
        brief = json.loads(args.brief.read_text(encoding='utf-8'))
        target = create_site(brief, args.sites_dir)
    except (OSError, ValueError) as error:
        parser.exit(1, f'{error}\n')
    print(f'Created {target}')
    print('Follow the generated README to run the site and connect its bot.')


if __name__ == '__main__':
    main()
