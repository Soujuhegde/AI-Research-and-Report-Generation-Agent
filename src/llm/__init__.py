#initializing the file 
"""
LLM package - Sarvam AI client and utilities.

Components:
    - sarvam_client: OpenAI-compatible Sarvam AI wrapper
    - get_llm: Factory function for configured LLM instances
"""

from src.llm.sarvam_client import get_llm, SarvamChatModel, sarvam_client

__all__ = [
    "get_llm",
    "SarvamChatModel",
    "sarvam_client",
]