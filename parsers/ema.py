import logging

from utils import create_blocklist, make_request

# Constants
URL = "https://www.ema.com.ua/wp-json/api/blacklist-query"
PARAMS = {"count": "-1"}
OUTPUT_FILE = "ema.txt"
TITLE = "EMA Blocklist"
SOURCE = "https://www.ema.com.ua/"
WHITELIST = ["sites.google.com", "play.google.com"]


def extract_domain(url: str) -> str:
    """Extract domain from URL.

    Args:
        url: URL.

    Returns:
        Extracted domain
    """
    logging.debug(f"Extract domain from this URL: {url}")

    # From https://www.example.com/page/1
    # to www.example.com/page/1
    if url.startswith("http://") or url.startswith("https://"):
        url = url.split("://")[1]

    # From www.example.com/page/1
    # to www.example.com
    if "/" in url:
        url = url.split("/")[0]

    # From www.example.com
    # to example.com
    if url.startswith("www."):
        url = url.replace("www.", "", 1)

    logging.debug(f"Extracted domain: {url}")

    return url.strip()


def create_ema_blocklist() -> None:
    """Parse domains from the website and create a blocklist from them."""
    logging.info(TITLE)

    filters = set()

    # Get JSON data
    json = make_request(URL, params=PARAMS, timeout=20, is_json=True)

    # Iterate through data and fetch domains
    for data in json["data"]:  # type: ignore
        url = data["url"]  # type: ignore

        # Extract domain from the url
        if url and not url.startswith("@"):
            domain = extract_domain(url)

            # Skip domains from the whitelist
            if domain in WHITELIST:
                logging.debug(f"{url} is skipped!")
                continue

            logging.debug(f"{domain} is added to blocklist")
            filters.add(f"||{domain}^")

    # Create a blocklist
    create_blocklist(OUTPUT_FILE, TITLE, SOURCE, filters)  # type: ignore


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    create_ema_blocklist()
