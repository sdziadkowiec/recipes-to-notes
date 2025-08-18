# recipes-to-notes
Toolchain for scraping cooking recipes, structuring them using LLM-based schema extraction and saving as notes

Comes with customizable plugins framework for integrating with different scrapers, LLMs, notes apps. Default stack:

- Scraping: [Spider Cloud](https://spider.cloud)
- Recipe schema extraction: [OpenAI](https://python.langchain.com/api_reference/openai/chat_models/langchain_openai.chat_models.base.ChatOpenAI.html) and [Azure OpenAI](https://python.langchain.com/api_reference/openai/chat_models/langchain_openai.chat_models.azure.AzureChatOpenAI.html#azurechatopenai)
- Notes app: [Notion](http://notion.com/)

## How to use?

```python
from recipes_to_notes import RecipeToNote
from recipes_to_notes.plugins.scraping.spider import SpiderScraper
from recipes_to_notes.plugins.schema_extraction.openai import OpenAI
from recipes_to_notes.plugins.notes.notion import NotionNotesApp
import os
import asyncio

url = "<YOUR-RECIPE-URL-GOES-HERE>"

spider_api_key = os.getenv("SPIDER_API_KEY")
openai_config = {
    "api_key": os.getenv("OPENAI_API_KEY"),
    "model": os.getenv("OPENAI_MODEL")
}
notion_config = {
    "database_name": "Recipes",
    "notion_token": os.getenv("NOTION_TOKEN"),
    "language": "en"
}

runner = RecipeToNote(
    scraper=SpiderScraper(api_key=spider_api_key),
    schema_extraction_provider=OpenAI(**openai_config),
    notes_app=NotionNotesApp(**notion_config),
)

runner.url(url)
asyncio.run(runner.run())
```
For a more comprehensive example, see [notebooks/run.ipynb](notebooks/run.ipynb)

All functions that implement the workflow are async, so they should be used with `asyncio.run()` or `await`.

## Installing
### Pre-requisites
- Credentials for plugins 😊
- [Astral UV](https://docs.astral.sh/uv/getting-started/installation/)

### Install
1. Git clone
2. Run `uv sync` to install packages

### Setup and run
1. Import and configure plugins
2. Set up secrets/credentials via environment variables or `.env` file (see [.env.template](.env.template) for what's required by default plugins).
3. Provide URL for scraping
4. Run the workflow


# Setting up Notion
1. Create a database for your recipes

2. Add the following properties to the database you created:
   - `Recipe URL` for English or `URL przepisu` for Polish, type URL
   - `Domain` for English or `Strona` for Polish, type Select
   
   Feel free to customize the database and add more properties to your liking

3. Go to https://www.notion.so/profile/integrations , log in and create new integration. Associate it with workspace your database is in, and set type to Internal.
4. Open the integration settings, go to Access tab and grant it access to the database you created in step 1.

5. Go back to Configuration tab and copy the token ("Internal Integration Secret")

6. Set the token as environment variable `NOTION_TOKEN`


# Plugins development
The workflow consists of 3 steps:

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

## Schema

`Recipe` schema is defined as follows:

- `name (Optional[str])`: The exact title/name of the recipe as it appears on the website.
- `ingredients (Optional[List[str]])`: List of ingredients with quantities and measurements.
- `cooking_time_temperature (Optional[str])`: Cooking time, temperature, or timing information.
- `instructions (Optional[List[str]])`: Step-by-step cooking instructions.
- `hints (Optional[str])`: Additional tips or suggestions for the recipe.
- `image_url (Optional[str])`: URL of the main recipe image if available.

Before passing to notes app, the schema is enriched by 2 additional attributes included in `EnrichedRecipe` schema:
- `url: str`: URL of the recipe
- `domain: str`: Domain name of the recipe's site


## Packaging

Run `uv build` to create a wheel.

# Internationalization
Names of properties and recipe section headings in Notion plugin are language-specific.
By default, English and Polish locale are provided, but other languages can be easily added by modifying [i18n.py](src/recipes_to_notes/i18n.py) file