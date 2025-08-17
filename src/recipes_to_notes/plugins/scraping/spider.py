from langchain_community.document_loaders import SpiderLoader
from langchain_core.documents.base import Document
from recipes_to_notes.base_classes import BaseScraper
from typing import Optional
import os
import logging


class SpiderScraper(BaseScraper):
    """Web scraper implementation using the Spider API.
    
    This class provides web scraping functionality using Spider Cloud
    to extract content from recipe websites.
    
    Attributes:
        api_key (str): The Spider API key for authentication.
        params (Optional[dict]): Optional parameters for Spider API requests.
        logger (logging.Logger): Logger instance for this class.
    """
    def __init__(self, api_key: Optional[str] = os.getenv("SPIDER_API_KEY"), params: Optional[dict] = None) -> None:
        """Initialize the Spider scraper.
        
        Args:
            api_key (Optional[str]): The Spider API key. If None, will attempt to read from
                SPIDER_API_KEY environment variable.
            params (Optional[dict]): Optional dictionary of parameters to pass to Spider API.
                
        Raises:
            ValueError: If no API key is provided or found in environment.
        """
        if api_key is None:
            raise ValueError("Missing Spider API key. Provide it as an argument or set SPIDER_API_KEY in the environment variables.")

        self.api_key = api_key
        self.params = params
        self.logger = logging.getLogger(__name__)

    async def scrape(self, url: str) -> list[Document]:
        """Scrape content from a URL using the Spider API.
        
        Args:
            url (str): The URL of the website to scrape.
            
        Returns:
            list[Document]: A list of Document objects containing the scraped content.
                Returns an empty list if scraping fails.
        """
        try:
            self.logger.info(f"Scraping {url}")
            docs = await SpiderLoader(url=url, api_key=self.api_key, params=self.params).aload()
            self.logger.info(f"Scraped {len(docs)} documents from {url}")
        except Exception as e:
            self.logger.error(f"Error scraping {url}: {e}")
            return []
        return docs