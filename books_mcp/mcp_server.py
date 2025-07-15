import logging
import sys

from fastmcp import FastMCP

from books_mcp.models import OpenLibrary
from books_mcp.providers import OpenLibraryProvider

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

app = FastMCP(
    name="OpenLibrary",
    version="0.1.0",
)


@app.tool()
async def search_books(query: str) -> OpenLibrary:
    """Search for books using OpenLibrary API"""
    logger.info(f"🔍 MCP tool called: search_books with query='{query}'")

    try:
        provider = OpenLibraryProvider()
        result = await provider.search_books(query)

        logger.info(
            f"✅ MCP search_books completed successfully: {result.num_found} books found"
        )
        return result

    except Exception as e:
        logger.error(f"❌ MCP search_books failed: {e}")
        raise


def main() -> None:
    logger.info("🚀 Starting MCP server...")
    logger.info("📡 Server will be available at: http://127.0.0.1:8000")
    logger.info("🔧 Transport: SSE (Server-Sent Events)")

    try:
        app.run(transport="sse", host="127.0.0.1", port=8000)
    except KeyboardInterrupt:
        logger.info("⏹️  Server stopped by user")
    except Exception as e:
        logger.error(f"💥 Server error: {e}")
        print(f"💥 Server error: {e}", file=sys.stderr)
        raise


if __name__ == "__main__":
    main()
