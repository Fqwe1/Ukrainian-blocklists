import requests

from create import create_blocklist

# Constants
URL = 'https://www.ema.com.ua/wp-json/api/blacklist-query'
PARAMS = {'count': '100000'}
OUTPUT_FILE = 'ema.txt'
NAME = 'EMA Blocklist'
SOURCE = 'https://www.ema.com.ua/'
WHITELIST = {'sites.google.com', 'play.google.com'}


def get_blocklist() -> None:
    response = requests.get(URL, params=PARAMS, timeout=30)
    response.raise_for_status()
    json_data = response.json()

    domains = set()

    # Iterate through data and fetch domains
    for data in json_data['data']:
        url = data['url']
        # From https://example.com/page
        # to example.com/page
        try:
            url = url.split('//')[1]
        except IndexError:
            pass

        if url:
            if '/' in url:
                url = url.split('/')[0]
            elif '@' in url:  # Telegram usernames
                continue

            # From www.example.com
            # to example.com
            if url.startswith('www.'):
                url = url.replace('www.', '')

            url = url.strip()
            url = f'||{url}^'
            domains.add(url)

    # Remove whitelisted domains
    domains.difference_update(f'||{site}^' for site in WHITELIST)

    create_blocklist(OUTPUT_FILE, NAME, SOURCE, domains)


if __name__ == '__main__':
    get_blocklist()
