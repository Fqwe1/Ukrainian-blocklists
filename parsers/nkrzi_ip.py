import asyncio
import logging

from bs4 import BeautifulSoup
from utils import create_blocklist, make_async_request

# Constants
URL = "https://uablocklist.com/blocklist/blocked-sites-nkrzi"
OUTPUT_FILE = "nkrzi_ip.txt"
TITLE = "НКРЗІ IP Blocklist"
SOURCE = "https://uablocklist.com/"

# Variables
filters = set()
semaphore = asyncio.Semaphore(10)  # Limit concurrent requests


async def fetch_ips(page: int) -> None:
    """Fetch IPs from the specified page.

    Args:
        page: Page number.
    """
    logging.debug(f"Current page: {page}")

    async with semaphore:
        # Make a GET request
        response = (
            await make_async_request(URL, params={"page": page})
            if page != 1
            else await make_async_request(URL)
        )
        soup = BeautifulSoup(response, "lxml")

        # Get domains from an HTML page
        table = soup.find("tbody")
        table_rows = table.find_all("tr")  # type: ignore

        for row in table_rows:
            if data := row.find_all("td")[3].get_text(strip=True):
                if "," in data:  # Multiple IP addresses
                    for ip in data.split(", "):
                        logging.debug(f"{ip} is added to blocklist")
                        filters.add(ip)
                else:  # One IP address
                    logging.debug(f"{data} is added to blocklist")
                    filters.add(data)


async def create_nkrzi_ip_blocklist() -> None:
    """Parse IPs from the website and create a blocklist from them."""
    logging.info(TITLE)

    # Get and parse HTML
    response = await make_async_request(URL)
    soup = BeautifulSoup(response, "lxml")

    # Get the total number of pages
    max_pages = int(
        soup.find_all("li", class_="page-item")[-2].get_text(strip=True)
    )
    logging.info(f"Number of pages: {max_pages}")

    # Iterate through pages and get their HTML
    tasks = [fetch_ips(page) for page in range(1, max_pages + 1)]
    await asyncio.gather(*tasks)

    # Create a blocklist
    create_blocklist(OUTPUT_FILE, TITLE, SOURCE, filters)  # type: ignore


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(create_nkrzi_ip_blocklist())
