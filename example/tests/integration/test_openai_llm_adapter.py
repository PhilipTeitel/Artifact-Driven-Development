"""Integration tests for OpenAILLMAdapter (S2-6)."""

from __future__ import annotations

import json
from pathlib import Path

import httpx
from openai import OpenAI

from contract.fakes import InMemoryConfigurationFake
from llm_wiki.adapters.llm.openai import OpenAILLMAdapter


def _openai_config(*, api_key: str | None = "sk-test") -> InMemoryConfigurationFake:
    return InMemoryConfigurationFake(
        vault_root=Path("/vault"),
        wiki_dir=Path("/vault/wiki"),
        openai_api_key=api_key,
        openai_model="gpt-4o-mini",
    )


def _mock_openai_client() -> OpenAI:
    def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content.decode())
        assert body["model"] == "gpt-4o-mini"
        return httpx.Response(
            200,
            json={
                "id": "chatcmpl-test",
                "object": "chat.completion",
                "choices": [
                    {
                        "index": 0,
                        "message": {"role": "assistant", "content": "openai assistant reply"},
                        "finish_reason": "stop",
                    }
                ],
            },
        )

    return OpenAI(
        api_key="sk-test",
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    )


def openai_complete_round_trip_B1() -> None:
    """B1 — complete() returns message content from SDK test transport."""
    config = _openai_config()
    adapter = OpenAILLMAdapter(config, client=_mock_openai_client())
    assert adapter.complete("hello") == "openai assistant reply"


def openai_unavailable_without_key_B2() -> None:
    """B2 — is_available() is False when openai_api_key is None."""
    adapter = OpenAILLMAdapter(_openai_config(api_key=None), client=_mock_openai_client())
    assert adapter.is_available() is False
