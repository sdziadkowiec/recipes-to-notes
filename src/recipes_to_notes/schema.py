from pydantic import BaseModel, Field
from typing import Optional, List


class Recipe(BaseModel):
    """Cooking recipe extracted from a website.
    
    This model represents the structured data extracted from recipe websites,
    containing all the essential information needed to recreate a recipe.
    
    Attributes:
        name (Optional[str]): The exact title/name of the recipe as it appears on the website.
        ingredients (Optional[List[str]]): List of ingredients with quantities and measurements.
        cooking_time_temperature (Optional[str]): Cooking time, temperature, or timing information.
        instructions (Optional[List[str]]): Step-by-step cooking instructions.
        hints (Optional[str]): Additional tips or suggestions for the recipe.
        image_url (Optional[str]): URL of the main recipe image if available.
    """
    name: Optional[str] = Field(
        default=None,
        description="The exact title/name of the recipe as it appears on the website. Do not modify or guess."
    )
    ingredients: Optional[List[str]] = Field(
        default=None,
        description="List of ingredients exactly as written on the website, including quantities and measurements. Each ingredient should be a separate list item. Do not modify the text or format."
    )
    cooking_time_temperature: Optional[str] = Field(
        default=None,
        description="Cooking time, baking temperature, or any time/temperature information as stated on the website. Combine cooking and time information into a single string if multiple values are provided. Isolate from other instructions."
    )
    instructions: Optional[List[str]] = Field(
        default=None,
        description="Step-by-step cooking instructions exactly as written on the website. Each step should be a separate list item. Preserve the original wording and formatting."
    )
    hints: Optional[str] = Field(
        default=None,
        description="Additional instructions and/or on top of the the main instructions."
    )
    image_url: Optional[str] = Field(
        default=None,
        description="URL of the main recipe image if explicitly provided. Only include if a clear image URL is present in the content."
    )


class EnrichedRecipe(Recipe):
    """Cooking recipe with additional metadata.
    
    This model extends the base Recipe with additional information about
    the source website, used for creating enriched notes.
    
    Attributes:
        url (str): The URL of the recipe website.
        domain (str): The domain of the recipe website.
    """
    url: str = Field(
        description="The URL of the recipe website."
    )
    domain: str = Field(
        description="The domain of the recipe website."
    )
    