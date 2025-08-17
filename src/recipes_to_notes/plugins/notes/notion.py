from recipes_to_notes.base_classes import BaseNotesApp
from recipes_to_notes.schema import EnrichedRecipe
import os
from typing import Optional
import logging
from notion_client import AsyncClient, Client
from recipes_to_notes.i18n import NOTES_LABELS


class NotionNotesApp(BaseNotesApp):
    """Notion notes application integration.
    
    This class provides functionality to create and update recipe notes
    in a Notion database, with support for multiple languages.
    
    Attributes:
        database_id (str): The ID of the target Notion database.
        database_name (str): The name of the target Notion database.
        client (Client): Synchronous Notion client for database queries.
        async_client (AsyncClient): Asynchronous Notion client for page operations.
        language (str): Language code for internationalized labels.
        logger (logging.Logger): Logger instance for this class.
    """

    database_id: str
    database_name: str
    client: Client
    async_client: AsyncClient

    def __init__(self, database_name: str, notion_token: Optional[str] = os.getenv('NOTION_TOKEN'), language: Optional[str] = "en") -> None:
        """Initialize the Notion notes app integration.
        
        Args:
            database_name (str): The name of the target Notion database.
            notion_token (Optional[str]): The Notion API token. If None, will attempt to read
                from NOTION_TOKEN environment variable.
            language (Optional[str]): Language code for internationalized labels. Defaults to "en".
                
        Raises:
            ValueError: If no Notion token is provided or the specified database
                is not found.
        """
        self.logger = logging.getLogger(__name__)
        if notion_token is None or notion_token == '':
            raise ValueError("NOTION_TOKEN is not set")
        self.client = Client(auth=notion_token)
        self.async_client = AsyncClient(auth=notion_token)

        self.database_name = database_name
        self.language = language
        database_id_query = self.client.search(query=self.database_name, filter={"property": "object", "value": "database"})
        if len(database_id_query['results']) == 0:
            raise ValueError(f"Database with name {self.database_name} not found")
        self.database_id = database_id_query['results'][0]['id']

    async def _check_page_exists(self, page_name: str) -> Optional[str]:
        """Check if a page with the given name already exists in the database.
        
        Args:
            page_name (str): The name of the page to search for.
            
        Returns:
            Optional[str]: The page ID if a page with the given name exists, None otherwise.
        """
        try:
            # Query the database for pages with the same name
            query_result = await self.async_client.databases.query(
                database_id=self.database_id,
                filter={
                    "property": "Name",
                    "title": {
                        "equals": page_name
                    }
                }
            )
            
            # Return page ID if any pages were found, None otherwise
            if len(query_result['results']) > 0:
                return query_result['results'][0]['id']
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to check if page exists: {str(e)}")
            # In case of error, assume page doesn't exist to avoid blocking creation
            return None

    def _prepare_page_properties(self, recipe: EnrichedRecipe) -> dict:
        """Prepare the page properties for Notion page creation/update.
        
        Args:
            recipe (EnrichedRecipe): The enriched recipe data to convert to Notion properties.
            
        Returns:
            dict: A dictionary of Notion page properties.
        """
        properties = {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": recipe.name or NOTES_LABELS[self.language]["untitled_recipe"]
                        }
                    }
                ]
            }
        }
        
        # Add Recipe URL if provided
        if recipe.url:
            properties[NOTES_LABELS[self.language]["url"]] = {
                "url": recipe.url
            }

        # Add Domain if provided
        if recipe.domain:
            properties[NOTES_LABELS[self.language]["domain"]] = {
                "select": {
                    "name": recipe.domain
                }
            }
        
        return properties

    def _prepare_page_cover(self, recipe: EnrichedRecipe) -> Optional[dict]:
        """Prepare the cover image for Notion page.
        
        Args:
            recipe (EnrichedRecipe): The enriched recipe data containing the image URL.
            
        Returns:
            Optional[dict]: A dictionary with cover image configuration, or None if no image URL.
        """
        if recipe.image_url:
            return {
                "type": "external",
                "external": {
                    "url": recipe.image_url
                }
            }
        return None

    def _prepare_page_content(self, recipe: EnrichedRecipe) -> list[dict]:
        """Prepare the content blocks for Notion page.
        
        Args:
            recipe (EnrichedRecipe): The enriched recipe data to convert to Notion blocks.
            
        Returns:
            list[dict]: A list of Notion block objects representing the recipe content.
        """
        children = []
        
        # Add Ingredients section
        if recipe.ingredients:
            children.extend([
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": NOTES_LABELS[self.language]["ingredients"]
                                }
                            }
                        ]
                    }
                }
            ])
            
            # Add each ingredient as a bullet point
            for ingredient in recipe.ingredients:
                children.append({
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": ingredient
                                }
                            }
                        ]
                    }
                })
        
        # Add Cooking Time & Temperature section
        if recipe.cooking_time_temperature:
            children.extend([
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": NOTES_LABELS[self.language]["cooking_time_temperature"]
                                }
                            }
                        ]
                    }
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": recipe.cooking_time_temperature
                                }
                            }
                        ]
                    }
                }
            ])
        
        # Add Instructions section
        if recipe.instructions:
            children.extend([
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": NOTES_LABELS[self.language]["instructions"]
                                }
                            }
                        ]
                    }
                }
            ])
            
            # Add each instruction as a numbered list item
            for i, instruction in enumerate(recipe.instructions, 1):
                children.append({
                    "object": "block",
                    "type": "numbered_list_item",
                    "numbered_list_item": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": instruction
                                }
                            }
                        ]
                    }
                })
        
        # Add Hints section
        if recipe.hints:
            children.extend([
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": NOTES_LABELS[self.language]["hints"]
                                }
                            }
                        ]
                    }
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": recipe.hints
                                }
                            }
                        ]
                    }
                }
            ])
        
        return children

    async def _create_page(self, recipe: EnrichedRecipe) -> dict:
        """Create a new page in Notion.
        
        Args:
            recipe (EnrichedRecipe): The enriched recipe data to create a page for.
            
        Returns:
            dict: The created Notion page object.
            
        Raises:
            Exception: If page creation fails.
        """
        properties = self._prepare_page_properties(recipe)
        cover = self._prepare_page_cover(recipe)
        children = self._prepare_page_content(recipe)
        
        try:
            new_page = await self.async_client.pages.create(
                parent={"database_id": self.database_id},
                properties=properties,
                cover=cover,
                children=children
            )
            
            self.logger.info(f"Successfully created Notion page: {new_page['id']}")
            return new_page
            
        except Exception as e:
            self.logger.error(f"Failed to create Notion page: {str(e)}")
            raise

    async def _update_page(self, page_id: str, recipe: EnrichedRecipe) -> dict:
        """Update an existing page in Notion.
        
        Args:
            page_id (str): The ID of the existing page to update.
            recipe (EnrichedRecipe): The enriched recipe data to update the page with.
            
        Returns:
            dict: The updated Notion page object.
            
        Raises:
            Exception: If page update fails.
        """
        properties = self._prepare_page_properties(recipe)
        cover = self._prepare_page_cover(recipe)
        
        try:
            # Update page properties and cover
            updated_page = await self.async_client.pages.update(
                page_id=page_id,
                properties=properties,
                cover=cover
            )
            
            # Get existing page content to clear it
            existing_blocks = await self.async_client.blocks.children.list(block_id=page_id)
            
            # Delete existing content blocks
            for block in existing_blocks['results']:
                await self.async_client.blocks.delete(block_id=block['id'])
            
            # Add new content
            children = self._prepare_page_content(recipe)
            if children:
                await self.async_client.blocks.children.append(
                    block_id=page_id,
                    children=children
                )
            
            self.logger.info(f"Successfully updated Notion page: {page_id}")
            return updated_page
            
        except Exception as e:
            self.logger.error(f"Failed to update Notion page: {str(e)}")
            raise

    async def create_note(self, recipe: EnrichedRecipe) -> dict:
        """Create or update a note in Notion using the provided EnrichedRecipe schema (upsert).
        
        This method implements an upsert operation - it will update an existing page
        if one with the same name exists, otherwise it will create a new page.
        
        Args:
            recipe (EnrichedRecipe): The enriched recipe data to create or update a note for.
            
        Returns:
            dict: The created or updated Notion page object.
        """
        
        # Check if a page with the same name already exists
        page_name = recipe.name or NOTES_LABELS[self.language]["untitled_recipe"]
        existing_page_id = await self._check_page_exists(page_name)
        
        if existing_page_id:
            # Update existing page
            self.logger.info(f"Updating existing page '{page_name}' with ID: {existing_page_id}")
            return await self._update_page(existing_page_id, recipe)
        else:
            # Create new page
            self.logger.info(f"Creating new page '{page_name}'")
            return await self._create_page(recipe)