from langchain_openai import AzureChatOpenAI
from langchain_core.language_models.chat_models import BaseChatModel
from recipes_to_notes.base_classes import BaseSchemaExtractionProvider


class AzureOpenAI(BaseSchemaExtractionProvider):
    def __init__(self, azure_endpoint: str, api_key: str, azure_deployment: str, api_version: str):
        self.model = AzureChatOpenAI(
            azure_endpoint=azure_endpoint,
            api_key=api_key,
            azure_deployment=azure_deployment,
            api_version=api_version,
            temperature=0,
        )

    def get_model(self) -> BaseChatModel:
        return self.model
