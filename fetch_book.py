from typing import Any
from libgen_api import LibgenSearch
import requests
import sys

searcher = LibgenSearch()

def get_book_title_author(title: str, author: str) -> Any:
    print(f"Downloading {title} | by {author}")
    title_filter = {"Extension": "pdf"}
    results = searcher.search_title_filtered(
                    title,
                    title_filter,
                    exact_match=False
    )
    print(f"results: {results}")

    if len(results) == 0:
        return f"No results for {title}\n"
    else:
        print(results)

    # using infura as it has the best uptime
    # you can probably maintain a preference list for this as well
    # usually these are available: ['GET', 'IPFS.io', 'Infura', 'Cloudflare']
    download_links = searcher.resolve_download_links(results[0])
    sources = list(download_links.keys())
    print(f"Found {len(sources)} sources: {sources}")
    print(f"Using {sources[0]}")
    download_link = download_links[sources[0]]
    print(f"download link: {download_link}\nDownloading...")

    response = requests.get(download_link)
    print(f"length of book: {len(response.content)}")

def get_book_title(title: str) -> Any:
    print(f"Downloading {title}")
    results = searcher.search_title(title)
    print(f"results: {results}")

    if len(results) == 0:
        return f"No results for {title}\n"
    else:
        print(results)

    # using infura as it has the best uptime
    # you can probably maintain a preference list for this as well
    # usually these are available: ['GET', 'IPFS.io', 'Infura', 'Cloudflare']
    download_links = searcher.resolve_download_links(results[0])
    sources = list(download_links.keys())
    print(f"Found {len(sources)} sources: {sources}")
    print(f"Using {sources[0]}")
    download_link = download_links[sources[0]]
    print(f"download link: {download_link}\nDownloading...")

    response = requests.get(download_link)
    print(f"length of book: {len(response.content)}")

if __name__ == "__main__":
    get_book_title_author(sys.argv[1], sys.argv[2])