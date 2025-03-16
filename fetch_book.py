from typing import Any
from libgen_api import LibgenSearch
import requests
import sys
from loguru import logger
import io
from typing import Union
import PyPDF2

searcher = LibgenSearch()

from concurrent.futures import ProcessPoolExecutor
import time

def extract_page_text(page: Any) -> str:
    """Extract text from a single PDF page"""
    return page.extract_text() + "\n"

async def get_text_from_pdf(pdf_str: Union[str, bytes]) -> str:
    """
    Extract text from PDF content.
    
    Args:
        pdf_str: Raw PDF content as bytes or string
        
    Returns:
        Extracted text as string
    """
    try:
        # Ensure we have bytes
        if isinstance(pdf_str, str):
            pdf_bytes = pdf_str.encode('utf-8')
        else:
            pdf_bytes = pdf_str
        
        # Create a file-like object
        pdf_file = io.BytesIO(pdf_bytes)
        
        try:
            # Create PDF reader
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            # Extract text from all pages in parallel
            start_time = time.time()
            logger.info("Starting PDF text extraction...")
            
            with ProcessPoolExecutor() as executor:
                try:
                    # Map the extract_page_text function across all pages
                    text_chunks = list(executor.map(extract_page_text, pdf_reader.pages))
                except Exception as e:
                    logger.error(f"Error during parallel text extraction: {str(e)}")
                    raise
            
            # Combine all text chunks
            text = "".join(text_chunks)
            
            end_time = time.time()
            duration = end_time - start_time
            logger.info(f"PDF text extraction completed in {duration:.2f} seconds. Total length: {len(text)}")
            
            return text
            
        except PyPDF2.PdfReadError as e:
            logger.error(f"Error reading PDF: {str(e)}")
            raise
            
    except Exception as e:
        logger.error(f"Error processing PDF content: {str(e)}")
        raise


async def get_book_text(title: str, author: str) -> Any:
    try:
        logger.info(f"Downloading {title} | by {author}")
        title_filter = {"Extension": "pdf"}
        try:
            results = searcher.search_title_filtered(
                        title,
                        title_filter,
                        exact_match=False
            )
            logger.debug(f"results: {results}")
        except Exception as e:
            logger.error(f"Error searching for book: {str(e)}")
            raise

        if len(results) == 0:
            logger.warning(f"No results found for {title} | {author}")
            return f"No results for {title} | {author} . Maybe there's a typo?\n"
        else:
            logger.debug(str(results))

        try:
            # using infura as it has the best uptime
            # you can probably maintain a preference list for this as well
            # usually these are available: ['GET', 'IPFS.io', 'Infura', 'Cloudflare']
            download_links = searcher.resolve_download_links(results[0])
            sources = list(download_links.keys())
            logger.info(f"Found {len(sources)} sources: {sources}")
            
            if not sources:
                logger.error("No download sources available")
                raise ValueError("No download sources available")
                
            logger.info(f"Using {sources[0]}")
            download_link = download_links[sources[0]]
            logger.info(f"download link: {download_link}\nDownloading...")

            try:
                response = requests.get(download_link)
                response.raise_for_status()  # Raises an HTTPError for bad responses
                logger.info(f"length of book: {len(response.content)}")
            except requests.exceptions.RequestException as e:
                logger.error(f"Error downloading book: {str(e)}")
                raise

            try:
                book_text = await get_text_from_pdf(response.content)
                logger.info(f"length of book text: {len(book_text)}")
                return book_text
            except Exception as e:
                logger.error(f"Error extracting text from PDF: {str(e)}")
                raise

        except Exception as e:
            logger.error(f"Error resolving download links: {str(e)}")
            raise

    except Exception as e:
        logger.error(f"Error in get_book_text: {str(e)}")
        raise


if __name__ == "__main__":
    logger.remove()
    logger.configure(handlers=[{"sink": sys.stderr, "level": "INFO"}])
    logger.info("Running fetch_book.py as standalone script")
    
    import asyncio
    asyncio.run(get_book_title_author("The Art of War", "Sun Tzu"))
    logger.info("Done")