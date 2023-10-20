# Constants
HOMEPAGE = 'https://github.com/Fqwe1/Ukrainian-blocklists'
LICENSE = 'https://github.com/Fqwe1/Ukrainian-blocklists/blob/main/LICENSE'


def create_blocklist(
    filename: str, name: str, source: str, domains: set
) -> None:
    domains = sorted(domains)
    path = f'blocklists/{filename}'

    with open(path, 'w', encoding='utf-8') as blocklist:
        blocklist.write(f'! Title: {name}\n')
        blocklist.write(f'! Source: {source}\n')
        blocklist.write(f'! Homepage: {HOMEPAGE}\n')
        blocklist.write(f'! License: {LICENSE}\n')
        blocklist.write(f'! Total number of filters: {len(domains)}\n')
        blocklist.write('\n'.join(domains))
        blocklist.close()
