import logging

import httpx

from books_mcp.models import OpenLibrary

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


class OpenLibraryProvider:
    def __init__(self) -> None:
        self.base_url = "https://openlibrary.org"
        logger.info(
            f"🔧 OpenLibraryProvider initialized with base_url: {self.base_url}"
        )

    async def search_books(self, query: str) -> OpenLibrary:
        logger.info(f"📚 Starting book search for query: '{query}'")

        url = f"{self.base_url}/search.json?q={query}&format=json"
        logger.debug(f"🌐 Making request to: {url}")

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)

                # Log response status
                logger.info(
                    f"📡 API Response: {response.status_code} | Content-Length: {response.headers.get('content-length', 'unknown')}"
                )

                if response.status_code != 200:
                    logger.error(
                        f"❌ API request failed with status {response.status_code}"
                    )
                    response.raise_for_status()

                data = response.json()

                # Log useful response metrics
                num_found = data.get("num_found", 0)
                docs_count = len(data.get("docs", []))
                logger.info(
                    f"✅ Search completed: {num_found} total books found, {docs_count} returned in response"
                )

                if docs_count > 0:
                    logger.debug(
                        f"📖 First book title: '{data['docs'][0].get('title', 'N/A')}'"
                    )

                # Process response into model
                result = OpenLibrary(**data)
                logger.info(
                    f"🎯 Successfully processed {len(result.docs)} book records"
                )

                return result

        except httpx.HTTPError as e:
            logger.error(f"🚨 HTTP error occurred: {e}")
            raise
        except Exception as e:
            logger.error(f"💥 Unexpected error during book search: {e}")
            raise
