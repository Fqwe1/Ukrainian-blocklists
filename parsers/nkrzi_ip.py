import asyncio

import aiohttp
from bs4 import BeautifulSoup

from create import create_blocklist

# Constants
URL = 'https://uablocklist.com/blocklist/blocked-sites-nkrzi'
OUTPUT_FILE = 'nkrzi_ip.txt'
NAME = 'НКРЗІ IP Blocklist'
SOURCE = 'https://uablocklist.com/'


async def fetch_data(session: aiohttp.ClientSession, page: int) -> str:
    params = {'page': page}
    async with session.get(URL, params=params) as response:
        response.raise_for_status()
        return await response.text()


async def get_blocklist() -> None:
    ips = set()

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

        # Iterate through pages to fetch IPs
        for page in range(1, max_pages + 1):
            tasks.append(fetch_data(session, page))

        # Fetch HTML for all pages concurrently
        html_pages = await asyncio.gather(*tasks)

        for html in html_pages:
            soup = BeautifulSoup(html, 'lxml')
            table = soup.find('tbody')
            table_rows = table.find_all('tr')

            for table_row in table_rows:
                table_data = table_row.find_all('td')[3]

                # Check if the table data is empty
                if table_data:
                    table_data = table_data.get_text(strip=True)
                    if ',' in table_data:
                        ip_list = table_data.split(', ')
                        for ip in ip_list:
                            ips.add(ip)
                    else:
                        ips.add(table_data)

    create_blocklist(OUTPUT_FILE, NAME, SOURCE, ips)


if __name__ == '__main__':
    asyncio.run(get_blocklist())
