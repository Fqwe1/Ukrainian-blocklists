import logging
import os
from typing import Any, Dict, List

import httpx

# Constants
HOMEPAGE = "https://github.com/Fqwe1/Ukrainian-blocklists"
LICENSE = "https://github.com/Fqwe1/Ukrainian-blocklists/blob/main/LICENSE"

# Variables
http_client = httpx.Client(http2=True)
async_http_client = httpx.AsyncClient(http2=True)


def make_request(
    url: str,
    headers: Dict[Any, Any] | None = None,
    params: Dict[Any, Any] | None = None,
    timeout: int | None = None,
    is_json: bool = False,
) -> Any | str:
    """Make a GET request to the specified URL.

    Args:
        url: URL for the request.
        headers (optional): HTTP headers.
        params (optional): Query parameters.
        timeout (optional): The timeout configuration.
        is_json (optional): Parsing as JSON. Defaults to False.

    Returns:
        Response (JSON or string)
    """
    # Make a GET request
    response = http_client.get(
        url,
        headers=headers,
        params=params,
        timeout=timeout,
    )

    # Catch errors
    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as error:
        logging.error(error)

    # Return response
    return response.json() if is_json else response.text


async def make_async_request(
    url: str,
    headers: Dict[Any, Any] | None = None,
    params: Dict[Any, Any] | None = None,
    timeout: int | None = None,
    is_json: bool = False,
) -> Any | str:
    """Make an asynchronous GET request to the specified URL.

    Args:
        url: URL for the request.
        headers (optional): HTTP headers.
        params (optional): Query parameters.
        timeout (optional): The timeout configuration.
        is_json (optional): Parsing as JSON. Defaults to False.

    Returns:
        Response (JSON or string)
    """
    # Make a GET request
    response = await async_http_client.get(
        url,
        headers=headers,
        params=params,
        timeout=timeout,
    )

    # Catch errors
    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as error:
        logging.error(error)

    # Return response
    return await response.json() if is_json else response.text


def create_blocklist(
    filename: str, title: str, source: str, filters: List[str]
) -> None:
    """Create a blocklist.

    Args:
        filename: Filename.
        title: Name of the blocklist.
        source: Source of the blocklist.
        filters: List of domains or IP addresses.
    """
    path = os.path.join("blocklists", filename)  # File saving path
    filters = sorted(filters)  # Sort filters
    num_of_filters = len(filters)  # Number of filters

    # Save the file
    try:
        logging.info(f"Create the {title}: {path}")
        with open(path, "w", encoding="utf-8") as blocklist:
            blocklist.write(
                f"! Title: {title}\n"
                f"! Source: {source}\n"
                f"! Homepage: {HOMEPAGE}\n"
                f"! License: {LICENSE}\n"
                f"! Total number of filters: {num_of_filters}\n"
            )
            blocklist.write("\n".join(filters))
    except Exception as error:
        logging.error(error)
