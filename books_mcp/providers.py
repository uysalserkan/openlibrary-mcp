import logging

import httpx

from books_mcp.models import AuthorDetails, AuthorWorks, OpenLibrary

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

    async def search_author_with_book_name(self, query: str) -> AuthorDetails:
        logger.info(f"📚 Starting author search for query: '{query}'")

        url = "{url}/authors/{author_id}.json"
        logger.debug(f"🌐 Making request to: {url}")

        try:
            async with httpx.AsyncClient() as client:
                book_response = await self.search_books(query=query)
                logger.info(
                    f"🎯 Successfully processed {len(book_response.docs)} book records"
                )
                logger.info(f"🆔 Author ID: {book_response.docs[0].author_key}")
                author_id = book_response.docs[0].author_key
                url = url.format(url=self.base_url, author_id=author_id)
                logger.debug(f"🌐 Making request to: {url}")

                response = await client.get(url)
                logger.info(
                    f"📡 API Response: {response.status_code} | Content-Length: {response.headers.get('content-length', 'unknown')}"
                )

                if response.status_code != 200:
                    logger.error(
                        f"❌ API request failed with status {response.status_code}"
                    )
                    response.raise_for_status()

                data = response.json()
                logger.info(f"🎯 Successfully processed {len(data)} author records")

                author_details = AuthorDetails(**data)
                author_works = await self.search_author_works(author_id=author_id)
                author_details.add_author_works(author_works)
                logger.info(
                    f"🎯 Successfully processed {len(author_details.works)} author works"
                )

                return author_details

        except httpx.HTTPError as e:
            logger.error(f"🚨 HTTP error occurred: {e}")
            raise
        except Exception as e:
            logger.error(f"💥 Unexpected error during author search: {e}")
            raise

    async def search_author(self, query: str) -> AuthorDetails:
        """Search for author using OpenLibrary API"""
        logger.info(f"📚 Starting author search for query: '{query}'")

        url = f"{self.base_url}/search/authors.json?q={query}"
        logger.debug(f"🌐 Making request to: {url}")

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                logger.info(
                    f"📡 API Response: {response.status_code} | Content-Length: {response.headers.get('content-length', 'unknown')}"
                )

                if response.status_code != 200:
                    logger.error(
                        f"❌ API request failed with status {response.status_code}"
                    )
                    response.raise_for_status()

                data = response.json()["docs"][0]
                logger.info(f"🎯 Successfully processed {len(data)} author records")

                author_details = AuthorDetails(**data)
                author_works = await self.search_author_works(
                    author_id=author_details.key
                )
                author_details.add_author_works(author_works)
                logger.info(
                    f"🎯 Successfully processed {len(author_details.works)} author works"
                )

                return author_details

        except httpx.HTTPError as e:
            logger.error(f"🚨 HTTP error occurred: {e}")
            raise
        except Exception as e:
            logger.error(f"💥 Unexpected error during author search: {e}")
            raise

    async def search_author_works(self, author_id: str) -> list[AuthorWorks]:
        """Search for author works using OpenLibrary API"""
        logger.info(f"📚 Starting author works search for author ID: '{author_id}'")

        url = f"{self.base_url}/authors/{author_id}/works.json"
        logger.debug(f"🌐 Making request to: {url}")

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                logger.info(
                    f"📡 API Response: {response.status_code} | Content-Length: {response.headers.get('content-length', 'unknown')}"
                )

                if response.status_code != 200:
                    logger.error(
                        f"❌ API request failed with status {response.status_code}"
                    )
                    response.raise_for_status()

                data = response.json()["entries"]
                logger.info(f"🎯 Successfully processed {len(data)} author works")

                return [AuthorWorks(**work) for work in data]

        except httpx.HTTPError as e:
            logger.error(f"🚨 HTTP error occurred: {e}")
            raise
        except Exception as e:
            logger.error(f"💥 Unexpected error during author works search: {e}")
            raise
