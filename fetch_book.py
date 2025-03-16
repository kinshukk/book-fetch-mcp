from typing import Any
from libgen_api import LibgenSearch
import requests
import sys
from loguru import logger

searcher = LibgenSearch()

def get_book_title_author(title: str, author: str) -> Any:
    logger.info(f"Downloading {title} | by {author}")
    title_filter = {"Extension": "pdf"}
    results = searcher.search_title_filtered(
                    title,
                    title_filter,
                    exact_match=False
    )
    logger.debug(f"results: {results}")

    if len(results) == 0:
        return f"No results for {title}\n"
    else:
        logger.debug(str(results))

    # using infura as it has the best uptime
    # you can probably maintain a preference list for this as well
    # usually these are available: ['GET', 'IPFS.io', 'Infura', 'Cloudflare']
    download_links = searcher.resolve_download_links(results[0])
    sources = list(download_links.keys())
    logger.info(f"Found {len(sources)} sources: {sources}")
    logger.info(f"Using {sources[0]}")
    download_link = download_links[sources[0]]
    logger.info(f"download link: {download_link}\nDownloading...")

    response = requests.get(download_link)
    logger.info(f"length of book: {len(response.content)}")

if __name__ == "__main__":
    # Initialize loguru when run as standalone script
    logger.remove()
    logger.configure(handlers=[{"sink": sys.stderr, "level": "INFO"}])
    logger.info("Running fetch_book.py as standalone script")
        
    get_book_title_author("The Art of War", "Sun Tzu")
