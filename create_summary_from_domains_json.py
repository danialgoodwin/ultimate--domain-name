import json
import logging
from pathlib import Path

import file_utils


def create_summary_from_domains_json(domains_as_json):
    logging.info('create_summary_from_domains_json()')
    all_domains = []
    available_domains = []
    for domain_key in domains_as_json:
        all_domains.append(domain_key)
        if domains_as_json[domain_key]['is_available']:
            available_domains.append(domain_key)
    file_utils.write('output/all_domains.txt', '\n'.join(all_domains))
    file_utils.write('output/available_domains.txt', '\n'.join(available_domains))
    print(f'len(all_domains)={len(all_domains)}')
    print(f'len(available_domains)={len(available_domains)}')


def main():
    logging.info('main()')
    with Path('database/checked-domains.json').open() as f:
        domains_as_json = json.load(f)
    create_summary_from_domains_json(domains_as_json)


if __name__ == '__main__':
    main()
