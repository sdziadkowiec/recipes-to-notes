"""Internationalization constants for the recipes-to-notes package."""

from typing import Dict

NOTES_LABELS: Dict[str, Dict[str, str]] = {
    """Multilingual labels for recipe note sections.
    
    Contains translations for recipe section headers and common labels
    used when creating notes in various notes applications.
    
    Attributes:
        en (dict[str, str]): English translations for recipe labels.
        pl (dict[str, str]): Polish translations for recipe labels.
    """
    "en": {
        "ingredients": "Ingredients",
        "cooking_time_temperature": "Cooking time and temperature",
        "instructions": "Instructions",
        "hints": "Hints",
        "url": "Recipe URL",
        "domain": "Domain",
        "untitled_recipe": "Untitled Recipe",
    },
    "pl": {
        "ingredients": "Składniki",
        "cooking_time_temperature": "Czas gotowania i temperatura",
        "instructions": "Przepis",
        "hints": "Wskazówki",
        "url": "URL przepisu",
        "domain": "Strona",
        "untitled_recipe": "Przepis bez nazwy",
    }
}