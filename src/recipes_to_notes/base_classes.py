from abc import abstractmethod
from langchain_core.documents.base import Document
from langchain_core.language_models.chat_models import BaseChatModel
from recipes_to_notes.schema import Recipe


class BaseScraper:
    @abstractmethod
    def scrape(self, url: str) -> list[Document]:
        raise NotImplementedError("This method should be implemented by the subclass")


class BaseSchemaExtractionProvider:
    @abstractmethod
    def get_model(self) -> BaseChatModel:
        raise NotImplementedError("This method should be implemented by the subclass")


class BaseNotesApp:
    @abstractmethod
    def create_note(self, recipe: Recipe) -> None:
        raise NotImplementedError("This method should be implemented by the subclass")
