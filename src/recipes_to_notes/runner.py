from recipes_to_notes.base_classes import BaseScraper, BaseSchemaExtractionProvider, BaseNotesApp
from recipes_to_notes.schema_extraction import extract_schema
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.documents.base import Document
from recipes_to_notes.schema import Recipe, EnrichedRecipe
from typing import Optional
import logging
import os


class RecipeToNote:
    logger: logging.Logger
    scraper: BaseScraper
    schema_extraction_provider: BaseSchemaExtractionProvider
    model: BaseChatModel
    notes_app: BaseNotesApp
    url: Optional[str]
    documents: Optional[list[Document]]
    extracted_schema: Optional[Recipe]

    def __init__(
        self, scraper: BaseScraper, schema_extraction_provider: BaseSchemaExtractionProvider, notes_app: BaseNotesApp
    ):
        self.scraper = scraper
        self.schema_extraction_provider = schema_extraction_provider
        self.model = self.schema_extraction_provider.get_model()
        self.notes_app = notes_app

        setup_logging()
        self.logger = logging.getLogger(__name__)

    def url(self, url: str) -> None:
        self.url = url

    async def scrape(self) -> None:
        self.documents = await self.scraper.scrape(self.url)

    async def extract_schema(self) -> None:
        self.extracted_schema = await extract_schema(self.model, self.documents)

    async def create_note(self) -> None:
        enriched_recipe = EnrichedRecipe(
            **self.extracted_schema.model_dump(),
            url=self.url,
            domain=self.url.split('/')[2]
        )
        await self.notes_app.create_note(enriched_recipe)

    async def run(self) -> None:
        await self.scrape()
        await self.extract_schema()
        await self.create_note()


def setup_logging() -> None:
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
