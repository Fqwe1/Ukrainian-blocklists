def create_blocklist(filename: str, domains: set) -> None:
    domains = sorted(domains)
    path = f'blocklists/{filename}'

    with open(path, 'w', encoding='utf-8') as blocklist:
        blocklist.write('\n'.join(domains))
        blocklist.close()
