from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
import sys
from loguru import logger
from fetch_book import get_book_text

# Initialize loguru for the main application
logger.remove()
logger.configure(handlers=[{"sink": sys.stderr, "level": "INFO"}])

mcp = FastMCP("book-fetcher")

@mcp.tool()
async def get_book_from_title_author(title: str, author: str) -> str:
    """
    Fetches a book from the title and author
    Args:
        title: Title of the book
        author: Author of the book"
    """
    logger.info(f"Downloading {title} | by {author}")
    book_text = await get_book_text(title, author)
    return book_text

if __name__ == "__main__":
    mcp.run(transport='stdio')