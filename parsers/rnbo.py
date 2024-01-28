import asyncio
import logging

from bs4 import BeautifulSoup
from utils import create_blocklist, make_async_request

# Constants
URL = "https://uablocklist.com/blocklist/blocked-sites-rnbo"
OUTPUT_FILE = "rnbo.txt"
TITLE = "РНБО Blocklist"
SOURCE = "https://uablocklist.com/"

# Variables
filters = set()
semaphore = asyncio.Semaphore(10)  # Limit concurrent requests


async def fetch_domains(page: int) -> None:
    """Fetch domains from the specified page.

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
        domains_on_page = table.find_all("a")  # type: ignore

        for domain in domains_on_page:
            if domain := domain.get_text(strip=True):
                logging.debug(f"{domain} is added to blocklist")
                filters.add(f"||{domain}^")


async def create_rnbo_blocklist() -> None:
    """Parse domains from the website and create a blocklist from them."""
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
    tasks = [fetch_domains(page) for page in range(1, max_pages + 1)]
    await asyncio.gather(*tasks)

    # Create a blocklist
    create_blocklist(OUTPUT_FILE, TITLE, SOURCE, filters)  # type: ignore


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(create_rnbo_blocklist())
