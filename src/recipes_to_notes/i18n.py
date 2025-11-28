"""Internationalization constants for the recipes-to-notes package."""

from typing import Dict

NOTES_LABELS: Dict[str, Dict[str, str]] = {
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

STREAM_MESSAGES: Dict[str, Dict[str, str]] = {
    "en": {
        "scraping": "Scraping website...",
        "schema_extraction": "Extracting schema...",
        "note_creation": "Creating note...",
        "completed": "Note created successfully",
        "failed": "Failed",
    },
    "pl": {
        "scraping": "Scrapowanie strony...",
        "schema_extraction": "Ekstrakcja schemy...",
        "note_creation": "Tworzenie notatki...",
        "completed": "Notatka utworzona pomyślnie",
        "failed": "Błąd",
    }
}
