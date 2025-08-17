from recipes_to_notes.schema import Recipe
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.documents.base import Document
from langchain_core.prompts import ChatPromptTemplate
from typing import Optional
import logging

SYSTEM_PROMPT: str = """
You are a precise recipe extraction assistant. Your task is to extract cooking recipe information from scraped website content and return it in the specified structured format.

CRITICAL EXTRACTION RULES:
1. IGNORE ALL BOILERPLATE: Skip navigation menus, headers, footers, advertisements, social media links, related articles, comments, author bios, and any non-recipe content.

2. EXTRACT LITERALLY: Copy recipe information exactly as written. Do not:
   - Rephrase or rewrite instructions
   - Convert measurements or units
   - Standardize formatting
   - Correct grammar or spelling
   - Add missing information

3. NO GUESSING: If information is not explicitly provided in the content:
   - Leave the field as null/empty
   - Do not infer or estimate values
   - Do not use placeholder text
   - Do not combine partial information to create complete entries

4. FOCUS ON RECIPE CONTENT ONLY: Look for:
   - Recipe title/name (usually in headings)
   - Ingredient lists (with exact quantities and descriptions)
   - Step-by-step cooking instructions
   - Cooking times, temperatures
   - Suggestions and/or hints
   - Recipe images (actual URLs, not placeholders)

5. PRESERVE ORIGINAL FORMAT: 
   - Keep ingredients as separate list items exactly as listed
   - Maintain instruction steps as separate items
   - Preserve original wording and punctuation
   - Include quantities, measurements, and descriptive details as written

6. QUALITY CHECKS:
   - Ensure extracted content is actually recipe-related
   - Verify ingredient lists contain real ingredients, not navigation items
   - Confirm instructions are cooking steps, not website instructions
   - Only include image URLs that are actual recipe photos

Extract only what is clearly present and recipe-specific. When in doubt, omit the information rather than guess.
"""

async def extract_schema(model: BaseChatModel, documents: list[Document]) -> Optional[Recipe]:
    """Extract structured recipe data from unstructured document content.
    
    Uses a language model to parse scraped website content and extract
    recipe information into a structured Recipe object.
    
    Args:
        model (BaseChatModel): The language model to use for extraction.
        documents (list[Document]): List containing exactly one Document with scraped content.
        
    Returns:
        Optional[Recipe]: A Recipe object with extracted data, or None if extraction fails.
        
    Raises:
        ValueError: If no documents are provided or more than one document is provided.
    """
    logger = logging.getLogger(__name__)
    if len(documents) == 0:
        raise ValueError("No documents provided")
    elif len(documents) > 1:
        raise ValueError("Multiple documents provided, expected exactly one")

    document = documents[0].page_content
    
    extraction_model = model.with_structured_output(schema=Recipe, method="json_schema")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("user", "{document}"),
    ])
    
    chain = prompt | extraction_model
    
    try:
        logger.info(f"Extracting schema from {documents[0].metadata['original_url']}")
        recipe = await chain.ainvoke({"document": document})
        logger.info(f"Extracted schema from {documents[0].metadata['original_url']}")
        return recipe
    except Exception as e:
        logger.error(f"Error extracting schema from {documents[0].metadata['original_url']}: {e}")
        return None