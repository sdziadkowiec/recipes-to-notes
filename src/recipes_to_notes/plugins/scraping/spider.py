from langchain_community.document_loaders import SpiderLoader
from langchain_core.documents.base import Document
from recipes_to_notes.base_classes import BaseScraper
from typing import Optional
import os
import logging

class SpiderScraper(BaseScraper):
    def __init__(self, api_key: Optional[str] = os.getenv("SPIDER_API_KEY"), params: Optional[dict] = None):
        if api_key is None:
            raise ValueError("Missing Spider API key. Provide it as an argument or set SPIDER_API_KEY in the environment variables.")

        self.api_key = api_key
        self.params = params
        self.logger = logging.getLogger(__name__)

    async def scrape(self, url: str) -> list[Document]:
        try:
            docs = await SpiderLoader(url=url, api_key=self.api_key, params=self.params).aload()
            self.logger.debug(f"Scraped {len(docs)} documents from {url}")
        except Exception as e:
            self.logger.error(f"Error scraping {url}: {e}")
            return []
        return docs