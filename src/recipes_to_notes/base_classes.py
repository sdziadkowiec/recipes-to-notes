"""Base abstract classes for the recipes-to-notes package."""

from abc import abstractmethod
from langchain_core.documents.base import Document
from langchain_core.language_models.chat_models import BaseChatModel
from recipes_to_notes.schema import Recipe


class BaseScraper:
    """Abstract base class for web scraping implementations.

    This class defines the interface that all scraper implementations must follow
    to extract content from recipe websites.
    """

    @abstractmethod
    def scrape(self, url: str) -> list[Document]:
        """Scrape content from a given URL.

        Args:
            url (str): The URL of the recipe website to scrape.

        Returns:
            list[Document]: A list of Document objects containing the scraped content.
        """
        raise NotImplementedError("This method should be implemented by the subclass")


class BaseSchemaExtractionProvider:
    """Abstract base class for schema extraction providers.

    This class defines the interface for providers that supply language models
    for extracting structured recipe data from unstructured content.
    """

    @abstractmethod
    def get_model(self) -> BaseChatModel:
        """Get the language model for schema extraction.

        Returns:
            BaseChatModel: A BaseChatModel instance configured for recipe schema extraction.
        """
        raise NotImplementedError("This method should be implemented by the subclass")


class BaseNotesApp:
    """Abstract base class for notes application integrations.

    This class defines the interface that all notes app implementations must follow
    to create notes from extracted recipe data.
    """

    @abstractmethod
    def create_note(self, recipe: Recipe) -> None:
        """Create a note from a recipe in the target notes application.

        Args:
            recipe (Recipe): The Recipe object containing the extracted recipe data.
        """
        raise NotImplementedError("This method should be implemented by the subclass")
