from langchain_openai import AzureChatOpenAI
from langchain_core.language_models.chat_models import BaseChatModel
from recipes_to_notes.base_classes import BaseSchemaExtractionProvider
import logging


class AzureOpenAI(BaseSchemaExtractionProvider):
    """Azure OpenAI implementation for schema extraction.
    
    This class provides a language model interface using Azure OpenAI services
    for extracting structured recipe data from unstructured content.
    
    Attributes:
        logger (logging.Logger): Logger instance for this class.
        model (AzureChatOpenAI): The configured AzureChatOpenAI model instance.
    """

    REQUIRED_KWARGS = {"azure_endpoint", "azure_deployment", "openai_api_version", "api_key"}

    def __init__(self, **openai_kwargs) -> None:
        """Initialize the Azure OpenAI provider.
        
        Args:
            **openai_kwargs: Keyword arguments for the AzureChatOpenAI model.
                Required: azure_endpoint, azure_deployment, openai_api_version, api_key
        
        Raises:
            ValueError: If any required kwargs are missing.
        """
        self.logger = logging.getLogger(__name__)
        
        missing_kwargs = self.REQUIRED_KWARGS - openai_kwargs.keys()
        if missing_kwargs:
            raise ValueError(f"Missing required kwargs: {', '.join(sorted(missing_kwargs))}")
        
        self.logger.info(f"Initializing AzureOpenAI with endpoint: {openai_kwargs['azure_endpoint']}")
        self.logger.info(f"Using deployment: {openai_kwargs['azure_deployment']}")
        self.logger.info(f"Using API version: {openai_kwargs['openai_api_version']}")

        self.model = AzureChatOpenAI(
            **openai_kwargs
        )

    def get_model(self) -> BaseChatModel:
        """Get the configured Azure OpenAI model.
        
        Returns:
            BaseChatModel: The AzureChatOpenAI model instance configured for schema extraction.
        """
        return self.model
