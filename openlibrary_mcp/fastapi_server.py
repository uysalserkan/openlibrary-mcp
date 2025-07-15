import logging
import time
from collections.abc import Awaitable, Callable
from typing import Any

import uvicorn
from fastapi import FastAPI, HTTPException, Request, Response

from openlibrary_mcp.providers import OpenLibraryProvider

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

app = FastAPI(
    title="Books MCP FastAPI Server",
    description="Search for books using OpenLibrary API",
    version="0.1.1",
)


@app.middleware("http")
async def log_requests(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    """Log all incoming requests"""
    start_time = time.time()

    logger.info(
        f"🌐 {request.method} {request.url.path} - Query: {dict(request.query_params)}"
    )

    response = await call_next(request)

    process_time = time.time() - start_time
    logger.info(f"📊 Response: {response.status_code} | Time: {process_time:.3f}s")

    return response


@app.get("/search")
async def search_books(query: str) -> Any:
    """Search for books using OpenLibrary API"""
    logger.info(f"🔍 FastAPI endpoint called: /search with query='{query}'")

    if not query.strip():
        logger.warning("⚠️  Empty search query provided")
        raise HTTPException(status_code=400, detail="Query parameter cannot be empty")

    try:
        provider = OpenLibraryProvider()
        result = await provider.search_books(query)

        logger.info(
            f"✅ FastAPI search completed successfully: {result.num_found} books found"
        )

        # Log response summary
        response_summary = {
            "num_found": result.num_found,
            "docs_returned": len(result.docs),
            "query": result.q,
        }
        logger.debug(f"📈 Response summary: {response_summary}")

        # Convert to dict for proper JSON serialization
        return result.model_dump()

    except Exception as e:
        logger.error(f"❌ FastAPI search failed: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}") from e


@app.get("/search_author_with_book_name")
async def search_author_with_book_name(query: str) -> Any:
    """Search for author using OpenLibrary API"""
    logger.info(
        f"🔍 FastAPI endpoint called: /search_author_with_book_name with query='{query}'"
    )

    if not query.strip():
        logger.warning("⚠️  Empty search query provided")
        raise HTTPException(status_code=400, detail="Query parameter cannot be empty")

    try:
        provider = OpenLibraryProvider()
        result = await provider.search_author_with_book_name(query)

        logger.info(f"✅ FastAPI author search completed successfully: {result.name}")

        return result.model_dump()

    except Exception as e:
        logger.error(f"❌ FastAPI author search failed: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}") from e


@app.get("/search_author")
async def search_author(query: str) -> Any:
    """Search for author using OpenLibrary API"""
    logger.info(f"🔍 FastAPI endpoint called: /search_author with query='{query}'")

    if not query.strip():
        logger.warning("⚠️  Empty search query provided")
        raise HTTPException(status_code=400, detail="Query parameter cannot be empty")

    try:
        provider = OpenLibraryProvider()
        result = await provider.search_author(query)

        logger.info(f"✅ FastAPI author search completed successfully: {result.name}")

        return result.model_dump()

    except Exception as e:
        logger.error(f"❌ FastAPI author search failed: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}") from e


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint"""
    logger.debug("💚 Health check requested")
    return {"status": "healthy", "service": "openlibrary-mcp"}


@app.get("/")
async def root() -> dict[str, Any]:
    """Root endpoint with API information"""
    logger.debug("📋 Root endpoint accessed")
    return {
        "message": "Books MCP FastAPI Server",
        "version": "0.1.1",
        "endpoints": [
            "/search",
            "/search_author_with_book_name",
            "/search_author",
            "/health",
            "/docs",
        ],
    }


if __name__ == "__main__":
    logger.info("🚀 Starting FastAPI server...")
    logger.info("📡 Server will be available at: http://localhost:8000")
    logger.info("📚 API documentation at: http://localhost:8000/docs")

    uvicorn.run(app, host="localhost", port=8000)
