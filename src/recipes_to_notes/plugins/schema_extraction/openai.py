from langchain_openai import ChatOpenAI
from langchain_core.language_models.chat_models import BaseChatModel
from recipes_to_notes.base_classes import BaseSchemaExtractionProvider
import logging


class OpenAI(BaseSchemaExtractionProvider):
    """OpenAI implementation for schema extraction.
    
    This class provides a language model interface using OpenAI services
    for extracting structured recipe data from unstructured content.
    
    Attributes:
        logger (logging.Logger): Logger instance for this class.
        model (ChatOpenAI): The configured ChatOpenAI model instance.
    """

    def __init__(self, api_key: str, model: str) -> None:
        """Initialize the OpenAI provider.
        
        Args:
            api_key (str): The API key for authenticating with OpenAI.
            model (str): The model to use for schema extraction.
        """
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Initializing OpenAI with model: {model}")

        self.model = ChatOpenAI(
            api_key=api_key,
            model=model,
            temperature=0,
        )

    def get_model(self) -> BaseChatModel:
        """Get the configured OpenAI model.
        
        Returns:
            BaseChatModel: The ChatOpenAI model instance configured for schema extraction.
        """
        return self.model
