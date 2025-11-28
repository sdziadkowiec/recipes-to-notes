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

    REQUIRED_KWARGS = {"api_key", "model"}

    def __init__(self, **openai_kwargs) -> None:
        """Initialize the OpenAI provider.
        
        Args:
            **openai_kwargs: Keyword arguments for the ChatOpenAI model.
                Required: api_key, model

        Raises:
            ValueError: If any required kwargs are missing.
        """
        missing_kwargs = self.REQUIRED_KWARGS - openai_kwargs.keys()
        if missing_kwargs:
            raise ValueError(f"Missing required kwargs: {', '.join(sorted(missing_kwargs))}")
        
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Initializing OpenAI with model: {openai_kwargs['model']}")

        self.model = ChatOpenAI(
            **openai_kwargs
        )

    def get_model(self) -> BaseChatModel:
        """Get the configured OpenAI model.
        
        Returns:
            BaseChatModel: The ChatOpenAI model instance configured for schema extraction.
        """
        return self.model
