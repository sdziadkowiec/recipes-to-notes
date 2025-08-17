from recipes_to_notes.base_classes import BaseScraper, BaseSchemaExtractionProvider, BaseNotesApp
from recipes_to_notes.schema_extraction import extract_schema
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.documents.base import Document
from recipes_to_notes.schema import Recipe, EnrichedRecipe
from typing import Optional
import logging
import os


class RecipeToNote:
    """Main orchestration class for converting recipes to notes.
    
    This class coordinates the entire pipeline from scraping recipe websites
    to creating structured notes in a target notes application.
    
    Attributes:
        logger (logging.Logger): Logger instance for this class.
        scraper (BaseScraper): The web scraper implementation to use.
        schema_extraction_provider (BaseSchemaExtractionProvider): The schema extraction provider.
        model (BaseChatModel): The language model for schema extraction.
        notes_app (BaseNotesApp): The notes application integration.
        _url (Optional[str]): The current recipe URL being processed.
        documents (Optional[list[Document]]): The scraped documents from the current URL.
        extracted_schema (Optional[Recipe]): The extracted recipe schema.
    """
    logger: logging.Logger
    scraper: BaseScraper
    schema_extraction_provider: BaseSchemaExtractionProvider
    model: BaseChatModel
    notes_app: BaseNotesApp
    _url: Optional[str]
    documents: Optional[list[Document]]
    extracted_schema: Optional[Recipe]

    def __init__(
        self, scraper: BaseScraper, schema_extraction_provider: BaseSchemaExtractionProvider, notes_app: BaseNotesApp
    ) -> None:
        """Initialize the RecipeToNote orchestrator.
        
        Args:
            scraper (BaseScraper): The web scraper implementation to use for content extraction.
            schema_extraction_provider (BaseSchemaExtractionProvider): The provider for language model access.
            notes_app (BaseNotesApp): The notes application integration for creating notes.
        """
        self.scraper = scraper
        self.schema_extraction_provider = schema_extraction_provider
        self.model = self.schema_extraction_provider.get_model()
        self.notes_app = notes_app

        setup_logging()
        self.logger = logging.getLogger(__name__)

    def url(self, url: str) -> None:
        """Set the URL of the recipe to process.
        
        Args:
            url (str): The URL of the recipe website to scrape and convert.
        """
        self._url = url

    async def scrape(self) -> None:
        """Scrape content from the configured URL.
        
        Uses the configured scraper to extract content from the recipe website.
        The scraped documents are stored in the instance for later processing.
        """
        self.documents = await self.scraper.scrape(self._url)

    async def extract_schema(self) -> None:
        """Extract structured recipe data from scraped documents.
        
        Uses the configured language model to parse the scraped content
        and extract structured recipe information.
        """
        self.extracted_schema = await extract_schema(self.model, self.documents)

    async def create_note(self) -> None:
        """Create a note from the extracted recipe data.
        
        Enriches the extracted recipe with URL metadata and creates
        a note in the configured notes application.
        """
        enriched_recipe = EnrichedRecipe(
            **self.extracted_schema.model_dump(),
            url=self._url,
            domain=self._url.split('/')[2]
        )
        await self.notes_app.create_note(enriched_recipe)

    async def run(self) -> None:
        """Execute the complete recipe-to-note conversion pipeline.
        
        Runs the full pipeline: scraping, schema extraction, and note creation.
        The URL must be set using the url() method before calling this method.
        """
        await self.scrape()
        await self.extract_schema()
        await self.create_note()


def setup_logging() -> None:
    """Configure logging for the application.
    
    Sets up logging with a consistent format and configurable log level.
    The log level can be controlled via the LOG_LEVEL environment variable.
    If not set or invalid, defaults to INFO level.
    """
    if os.getenv("LOG_LEVEL") is not None:
        try:
            log_level = getattr(logging, os.getenv("LOG_LEVEL"))
        except AttributeError:
            log_level = logging.INFO
    else:
        log_level = logging.INFO
    # Set up logging on root logger level
    logging.basicConfig(level=log_level)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    # Remove all handlers
    if root_logger.hasHandlers():
        root_logger.handlers.clear()
    root_logger.addHandler(handler)
