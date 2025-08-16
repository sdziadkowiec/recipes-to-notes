from abc import abstractmethod
from langchain_core.documents.base import Document
from langchain_core.language_models.chat_models import BaseChatModel
from pydantic import BaseModel, Field
from typing import Optional


class Recipe(BaseModel):
    name: str = Field(description="The name of the recipe")
    ingredients: list[str] = Field(description="The ingredients of the recipe")
    cooking_time_temperature: str = Field(description="The cooking time and temperature of the recipe")
    instructions: list[str] = Field(description="The instructions of the recipe")
    url: Optional[str] = Field(description="The URL of the recipe")
    image_url: Optional[str] = Field(description="The URL of the image of the recipe")


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
