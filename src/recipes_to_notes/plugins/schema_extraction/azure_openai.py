from langchain_openai import AzureChatOpenAI
from langchain_core.language_models.chat_models import BaseChatModel
from recipes_to_notes.base_classes import BaseSchemaExtractionProvider
import logging

class AzureOpenAI(BaseSchemaExtractionProvider):
    def __init__(self, azure_endpoint: str, api_key: str, azure_deployment: str, api_version: str):
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
        return self.model
