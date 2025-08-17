# recipes-to-notes
Toolchain for scraping cooking recipes, structuring them using LLM-based schema extraction and saving as notes

Comes with customizable plugins, 

## Key concepts
The workflow consists of 3 steps

1. Scrape the website, ideally to markdown or other LLM-friendly format
2. Extract schema of the recipe
3. Save to note-taking app

The steps are based on custimizable plugins with minimal interface to implement:

```python
class BaseScraper:
    @abstractmethod
    def scrape(self, url: str) -> list[Document]:
        ...


class BaseSchemaExtractionProvider:
    @abstractmethod
    def get_model(self) -> BaseChatModel:
        ...


class BaseNotesApp:
    @abstractmethod
    def create_note(self, recipe: Recipe) -> None:
        ...
```

`BaseScraper` and `BaseSchemaExtractionProvider` are based on Langchain and interface via its standard base classes. `BaseNotesApp` takes a Pydantic class with the recipe as input.

## Default plugins
- Scraping: [Spider Cloud](https://spider.cloud)
- Recipe schema exctraction: [Azure OpenAI](https://python.langchain.com/api_reference/openai/chat_models/langchain_openai.chat_models.azure.AzureChatOpenAI.html#azurechatopenai)
- Notes app: [Notion](http://notion.com/)

## Getting started

### Pre-requisites
- Python
- [Astral UV](https://docs.astral.sh/uv/getting-started/installation/)

### Install
1. Git clone
2. Run `uv sync` to install packages

## How to use
1. Import and configure plugins
2. Set up secrets/credentials via environment variables or `.env` file (see [.env.template](.env.template) for what's required by default plugins).
3. Provide URL for scraping
4. Run the workflow

## Usage example
See [run.ipynb](notebooks/run.ipynb)