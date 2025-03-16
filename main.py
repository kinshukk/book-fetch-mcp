from typing import Any, Dict, Optional, Tuple
import httpx
from mcp.server.fastmcp import FastMCP
import sys
from loguru import logger
from fetch_book import get_book_text

# Initialize loguru for the main application
logger.remove()
logger.configure(handlers=[{"sink": sys.stderr, "level": "INFO"}])

mcp = FastMCP("book-fetcher")

# Book cache to store downloaded books
# Structure: {(title, author): book_text}
BOOK_CACHE: Dict[Tuple[str, str], str] = {}

@mcp.tool()
async def get_book_from_title_author(
    title: str, 
    author: str, 
    start_index: Optional[int] = 0, 
    end_index: Optional[int] = None
) -> Dict[str, Any]:
    """
    Fetches a book from the title and author
    Args:
        title: Title of the book
        author: Author of the book
        start_index: Starting character index (default: 0)
        end_index: Ending character index (default: start_index + 95000)
    
    Returns:
        Dict containing book text slice and metadata
    """
    # Default end_index if not provided
    # claude has 200K tokens context length
    # 10K english characters give ~3K tokens
    # claude desktop truncates at 100K characters so we'll take 95K, to include the remaining JSON as well
    if end_index is None:
        end_index = start_index + 95000
    
    # Validate indices
    if start_index < 0:
        raise ValueError("start_index must be non-negative")
    if end_index <= start_index:
        raise ValueError("end_index must be greater than start_index")
    
    # Check cache for book
    cache_key = (title.lower(), author.lower())
    if cache_key not in BOOK_CACHE:
        logger.info(f"Book not in cache. Downloading {title} | by {author}")
        book_text = await get_book_text(title, author)
        BOOK_CACHE[cache_key] = book_text
    else:
        logger.info(f"Found book in cache: {title} | by {author}")
    
    # Get the full text
    full_text = BOOK_CACHE[cache_key]
    total_length = len(full_text)
    
    # Adjust end_index if it exceeds total length
    end_index = min(end_index, total_length)
    
    # Get the requested slice
    text_slice = full_text[start_index:end_index]
    
    # Prepare response with metadata
    return {
        "text": text_slice,
        "metadata": {
            "title": title,
            "author": author,
            "total_length": total_length,
            "start_index": start_index,
            "end_index": end_index,
            "slice_length": len(text_slice),
            "has_more": end_index < total_length
        }
    }

if __name__ == "__main__":
    mcp.run(transport='stdio')