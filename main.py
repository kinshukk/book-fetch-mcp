from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
import sys
from loguru import logger

# Initialize loguru for the main application
logger.remove()
logger.configure(handlers=[{"sink": sys.stderr, "level": "INFO"}])

mcp = FastMCP("book-fetcher")
