# No: https://domainr.com/docs/api, requires credit card
import json
import time
from datetime import datetime
from itertools import product
from pathlib import Path

import requests

import load_env

# Reference: https://developer.godaddy.com/doc/endpoint/domains#/v1/available
API_URL = 'https://api.ote-godaddy.com/v1/domains/available?domain='
env = load_env.load_env('.env.local')
API_KEY = env['API_KEY']
API_SECRET = env['API_SECRET']
API_HEADER = { 'Authorization': f'sso-key {API_KEY}:{API_SECRET}' }


def is_domain_available(domain: str) -> bool:
    print(f'is_domain_available({domain})')
    url = f'{API_URL}{domain}'
    print(f'    url={url}')
    response = requests.get(url, headers=API_HEADER)
    print(f'    response={response.text}')
    return response.json()['available']


def check_domain_and_save(file: Path, domain: str) -> bool:
    print(f'check_domain_and_save()')
    if file.exists():
        with file.open() as f:
            urls = json.load(f)
    else:
        file.touch()
        urls = {}

    is_already_checked = domain in urls
    if is_already_checked:
        print(f'    Already checked: {domain}')
    else:
        is_available = is_domain_available(domain)
        print(f'    Checked: {domain}')
        urls[domain] = {'is_available': is_available, 'checked': datetime.now().isoformat()}

    with file.open('w') as f:
        f.write(json.dumps(urls, indent=2))

    return is_already_checked


def generate_domain_names(names_path: Path, tlds_path: Path) -> list:
    print('generate_domain_names()')
    with names_path.open() as f:
        names = [ name.rstrip('\n') for name in list(f) ]
    with tlds_path.open() as f:
        tlds = [ tld.rstrip('\n') for tld in list(f) ]
    # print(f'    names={names}')
    # print(f'    tlds={tlds}')
    domains = [f'{name}.{tld}' for name in names for tld in tlds]
    # for name, tld in product(names, tlds):
    #     domains += f'{name}.{tld}'
    print(f'    domains={domains}')
    return domains


def main():
    print('main()')
    domains = generate_domain_names(Path('res/interesting-names.txt'), Path('res/interesting-top-level-domains.txt'))
    for domain in domains:
        is_already_checked = check_domain_and_save(Path('database/checked-domains.json'), domain)
        if not is_already_checked:
            time.sleep(10)


if __name__ == '__main__':
    main()
