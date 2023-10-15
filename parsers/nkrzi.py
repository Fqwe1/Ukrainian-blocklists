import asyncio

import aiohttp
from bs4 import BeautifulSoup

from create import create_blocklist

# Constants
URL = 'https://uablocklist.com/blocklist/blocked-sites-nkrzi'
OUTPUT_FILE = 'nkrzi.txt'


async def fetch_data(session: aiohttp.ClientSession, page: int) -> str:
    params = {'page': page}
    async with session.get(URL, params=params) as response:
        response.raise_for_status()
        return await response.text()


async def get_blocklist() -> None:
    domains = set()

    async with aiohttp.ClientSession() as session:
        html = await fetch_data(session, 1)
        soup = BeautifulSoup(html, 'lxml')

        # Fetch the total number of pages
        max_pages = int(
            soup.find('ul', class_='pagination')
            .find_all('li')[-2]
            .a.get('href')
            .split('=')[1]
        )

        tasks = []

        # Iterate through pages to fetch domains
        for page in range(1, max_pages + 1):
            tasks.append(fetch_data(session, page))

        # Fetch HTML for all pages concurrently
        html_pages = await asyncio.gather(*tasks)

        for html in html_pages:
            soup = BeautifulSoup(html, 'lxml')
            table = soup.find('tbody')
            domains_on_page = table.find_all('a')

            for domain in domains_on_page:
                domain = domain.get_text(strip=True)
                domain = f'||{domain}^'
                domains.add(domain)

    create_blocklist(OUTPUT_FILE, domains)


if __name__ == '__main__':
    asyncio.run(get_blocklist())
