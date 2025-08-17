from recipes_to_notes.base_classes import BaseNotesApp
from recipes_to_notes.schema import EnrichedRecipe
import os
from typing import Optional
import logging
from notion_client import AsyncClient, Client

class NotionNotesApp(BaseNotesApp):

    database_id: str
    database_name: str
    client: Client
    async_client: AsyncClient

    def __init__(self, database_name: str, notion_token: Optional[str] = os.getenv('NOTION_TOKEN')) -> None:
        self.logger = logging.getLogger(__name__)
        if notion_token is None or notion_token == '':
            raise ValueError("NOTION_TOKEN is not set")
        self.client = Client(auth=notion_token)
        self.async_client = AsyncClient(auth=notion_token)

        self.database_name = database_name

        database_id_query = self.client.search(query=self.database_name, filter={"property": "object", "value": "database"})
        if len(database_id_query['results']) == 0:
            raise ValueError(f"Database with name {self.database_name} not found")
        self.database_id = database_id_query['results'][0]['id']

    async def _check_page_exists(self, page_name: str) -> str | None:
        """Check if a page with the given name already exists in the database.
        
        Returns:
            str: Page ID if page exists, None if it doesn't exist
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
        """Prepare the page properties for Notion page creation/update."""
        properties = {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": recipe.name or "Untitled Recipe"
                        }
                    }
                ]
            }
        }
        
        # Add Recipe URL if provided
        if recipe.url:
            properties["Recipe URL"] = {
                "url": recipe.url
            }
        
        return properties

    def _prepare_page_cover(self, recipe: EnrichedRecipe) -> dict | None:
        """Prepare the cover image for Notion page."""
        if recipe.image_url:
            return {
                "type": "external",
                "external": {
                    "url": recipe.image_url
                }
            }
        return None

    def _prepare_page_content(self, recipe: EnrichedRecipe) -> list:
        """Prepare the content blocks for Notion page."""
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
                                    "content": "Ingredients"
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
                                    "content": "Cooking Time & Temperature"
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
                                    "content": "Instructions"
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
                                    "content": "Hints"
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
        """Create a new page in Notion."""
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
        """Update an existing page in Notion."""
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

    async def create_note(self, recipe: EnrichedRecipe):
        """Create or update a note in Notion using the provided EnrichedRecipe schema (upsert)."""
        
        # Check if a page with the same name already exists
        page_name = recipe.name or "Untitled Recipe"
        existing_page_id = await self._check_page_exists(page_name)
        
        if existing_page_id:
            # Update existing page
            self.logger.info(f"Updating existing page '{page_name}' with ID: {existing_page_id}")
            return await self._update_page(existing_page_id, recipe)
        else:
            # Create new page
            self.logger.info(f"Creating new page '{page_name}'")
            return await self._create_page(recipe)