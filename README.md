# Book Fetch MCP
Talk to any published book in the world right inside claude (or your other MCP clients).

## Feature list
- [x] write mcp tool, test basic version
- [x] if book too long, maintain in MCP cache, and paginate through it
- [ ] use gemini 1.5 for asking questions from book, feed that response to claude (due to GINORMOUS context length)
- [ ] spawn mini-RAG engine inside the server, ingestion, chunking, reranking. maintained through to end of app lifecycle
- [ ] integrate scihub as well. FREE THE WORLD'S KNOWLEDGEEE

## Setup
- make sure you have uv installed
- install deps. `cd book-fetch && `
- add this to your `claude_desktop_config.json`
```json
{
  "mcpServers": {
    "book-fetcher": {
        "command": "uv",
        "args": [
        "--directory",
        "<PATH_TO_PARENT_DIR>/libgen-mcp",
        "run",
        "main.py"
        ]
    }
  }
}
```