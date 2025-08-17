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

    def __init__(self, azure_endpoint: str, api_key: str, azure_deployment: str, api_version: str) -> None:
        """Initialize the Azure OpenAI provider.
        
        Args:
            azure_endpoint (str): The Azure OpenAI endpoint URL.
            api_key (str): The API key for authenticating with Azure OpenAI.
            azure_deployment (str): The name of the Azure OpenAI deployment to use.
            api_version (str): The API version to use for requests.
        """
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Initializing AzureOpenAI with endpoint: {azure_endpoint}")
        self.logger.info(f"Using deployment: {azure_deployment}")
        self.logger.info(f"Using API version: {api_version}")

        self.model = AzureChatOpenAI(
            azure_endpoint=azure_endpoint,
            api_key=api_key,
            azure_deployment=azure_deployment,
            openai_api_version=api_version,
            temperature=0,
        )

    def get_model(self) -> BaseChatModel:
        """Get the configured Azure OpenAI model.
        
        Returns:
            BaseChatModel: The AzureChatOpenAI model instance configured for schema extraction.
        """
        return self.model
