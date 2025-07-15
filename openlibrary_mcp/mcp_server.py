import logging
import sys

from fastmcp import FastMCP

from openlibrary_mcp.models import AuthorDetails, OpenLibrary
from openlibrary_mcp.providers import OpenLibraryProvider

# Configure logging for Claude Desktop (stderr only)
logger = logging.getLogger(__name__)
logging.basicConfig(
    stream=sys.stderr,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

app = FastMCP(
    name="openlibrary-mcp",
    version="0.1.1",
)


@app.tool()
async def search_books(query: str) -> OpenLibrary:
    """
    Search for books using the OpenLibrary API.

    Args:
        query: Search query for books (e.g., "python programming", "tolkien", "1984")

    Returns:
        OpenLibrary response containing search results with book details

    Examples:
        - search_books("python programming")
        - search_books("lord of the rings tolkien")
        - search_books("george orwell 1984")
    """
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


@app.tool()
async def search_author_with_book_name(query: str) -> AuthorDetails:
    """
    Search for author with book name using the OpenLibrary API.
    """
    logger.info(
        f"🔍 MCP tool called: search_author_with_book_name with query='{query}'"
    )

    try:
        provider = OpenLibraryProvider()
        result = await provider.search_author_with_book_name(query)

        logger.info(
            f"✅ MCP search_author_with_book_name completed successfully: {result.name}"
        )
        return result
    except Exception as e:
        logger.error(f"❌ MCP search_author_with_book_name failed: {e}")
        raise


@app.tool()
async def search_author(query: str) -> AuthorDetails:
    """
    Search for author using the OpenLibrary API.
    """
    logger.info(f"🔍 MCP tool called: search_author with query='{query}'")

    try:
        provider = OpenLibraryProvider()
        result = await provider.search_author(query)

        logger.info(f"✅ MCP search_author completed successfully: {result.name}")
        return result
    except Exception as e:
        logger.error(f"❌ MCP search_author failed: {e}")
        raise


def main() -> None:
    """Main function to run the MCP server for Claude Desktop integration."""
    logger.info("🚀 Starting Books MCP server for Claude Desktop...")
    logger.info("🔧 Using stdio transport for Claude Desktop integration")

    try:
        # FastMCP will automatically use stdio transport which is what Claude Desktop expects
        app.run()
    except KeyboardInterrupt:
        logger.info("⏹️  Server stopped by user")
    except Exception as e:
        logger.error(f"💥 Server error: {e}")
        print(f"💥 Server error: {e}", file=sys.stderr)
        raise


if __name__ == "__main__":
    main()
