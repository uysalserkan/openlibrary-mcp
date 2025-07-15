import logging
from fastapi import FastAPI, HTTPException, Request
import uvicorn
import time

from books_mcp.providers import OpenLibraryProvider

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

app = FastAPI(
    title="Books MCP FastAPI Server",
    description="Search for books using OpenLibrary API",
    version="0.1.0"
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests"""
    start_time = time.time()
    
    logger.info(f"🌐 {request.method} {request.url.path} - Query: {dict(request.query_params)}")
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    logger.info(f"📊 Response: {response.status_code} | Time: {process_time:.3f}s")
    
    return response

@app.get("/search")
async def search_books(query: str):
    """Search for books using OpenLibrary API"""
    logger.info(f"🔍 FastAPI endpoint called: /search with query='{query}'")
    
    if not query.strip():
        logger.warning("⚠️  Empty search query provided")
        raise HTTPException(status_code=400, detail="Query parameter cannot be empty")
    
    try:
        provider = OpenLibraryProvider()
        result = await provider.search_books(query)
        
        logger.info(f"✅ FastAPI search completed successfully: {result.num_found} books found")
        
        # Log response summary
        response_summary = {
            "num_found": result.num_found,
            "docs_returned": len(result.docs),
            "query": result.q
        }
        logger.debug(f"📈 Response summary: {response_summary}")
        
        return result
        
    except Exception as e:
        logger.error(f"❌ FastAPI search failed: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    logger.debug("💚 Health check requested")
    return {"status": "healthy", "service": "books-mcp"}

@app.get("/")
async def root():
    """Root endpoint with API information"""
    logger.debug("📋 Root endpoint accessed")
    return {
        "message": "Books MCP FastAPI Server",
        "version": "0.1.0",
        "endpoints": ["/search", "/health", "/docs"]
    }

if __name__ == "__main__":
    logger.info("🚀 Starting FastAPI server...")
    logger.info("📡 Server will be available at: http://0.0.0.0:8000")
    logger.info("📚 API documentation at: http://0.0.0.0:8000/docs")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
