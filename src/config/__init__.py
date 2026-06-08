#for intializing the file 
"""
Config package - Application configuration via pydantic-settings.

Loads all settings from environment variables / .env file.
"""

from src.config.settings import settings

__all__ = ["settings"]