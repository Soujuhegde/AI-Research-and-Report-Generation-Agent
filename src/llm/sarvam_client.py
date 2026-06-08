"""
Sarvam AI Client - Uses OpenAI-compatible API interface.
Sarvam AI provides an OpenAI-compatible endpoint.
"""
from openai import OpenAI
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import (
    AIMessage, HumanMessage, SystemMessage, BaseMessage
)
from langchain_core.outputs import ChatResult, ChatGeneration
from typing import List, Optional, Any, Iterator
from pydantic import Field
import json

from src.config.settings import settings
from src.utils.logger import app_logger


# Raw Sarvam client for direct use
sarvam_client = OpenAI(
    api_key=settings.sarvam_api_key,
    base_url=settings.sarvam_api_base_url,
)


class SarvamChatModel(BaseChatModel):
    """
    LangChain-compatible wrapper for Sarvam AI API.
    Uses OpenAI-compatible interface provided by Sarvam.
    """

    model_name: str = Field(default=settings.sarvam_model)
    temperature: float = Field(default=0.7)
    max_tokens: int = Field(default=2048)
    api_key: str = Field(default=settings.sarvam_api_key)
    api_base: str = Field(default=settings.sarvam_api_base_url)

    class Config:
        arbitrary_types_allowed = True

    @property
    def _llm_type(self) -> str:
        return "sarvam"

    def _get_client(self) -> OpenAI:
        return OpenAI(
            api_key=self.api_key,
            base_url=self.api_base,
        )

    def _convert_messages(self, messages: List[BaseMessage]) -> List[dict]:
        converted = []
        for msg in messages:
            if isinstance(msg, SystemMessage):
                converted.append({"role": "system", "content": msg.content})
            elif isinstance(msg, HumanMessage):
                converted.append({"role": "user", "content": msg.content})
            elif isinstance(msg, AIMessage):
                converted.append({"role": "assistant", "content": msg.content})
        return converted

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> ChatResult:
        client = self._get_client()
        converted = self._convert_messages(messages)

        app_logger.debug(f"Calling Sarvam API with model: {self.model_name}")

        try:
            response = client.chat.completions.create(
                model=self.model_name,
                messages=converted,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                stop=stop,
            )

            content = response.choices[0].message.content
            if content is None:
                content = ""
            ai_message = AIMessage(content=content)
            generation = ChatGeneration(message=ai_message)
            return ChatResult(generations=[generation])

        except Exception as e:
            app_logger.error(f"Sarvam API error: {e}")
            raise

    def _stream(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> Iterator[ChatGeneration]:
        client = self._get_client()
        converted = self._convert_messages(messages)

        try:
            stream = client.chat.completions.create(
                model=self.model_name,
                messages=converted,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                stream=True,
                stop=stop,
            )

            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield ChatGeneration(
                        message=AIMessage(content=chunk.choices[0].delta.content)
                    )
        except Exception as e:
            app_logger.error(f"Sarvam streaming error: {e}")
            raise

    @property
    def _identifying_params(self) -> dict:
        return {"model_name": self.model_name}


def get_llm(temperature: float = 0.7, max_tokens: int = 2048) -> SarvamChatModel:
    """Factory function to get configured LLM."""
    return SarvamChatModel(
        temperature=temperature,
        max_tokens=max_tokens,
    )