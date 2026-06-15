"""Integration tests for AnthropicLLMAdapter (S2-6)."""

from __future__ import annotations

import json
from pathlib import Path

import httpx
from anthropic import Anthropic

from contract.fakes import InMemoryConfigurationFake
from llm_wiki.adapters.llm.anthropic import AnthropicLLMAdapter


def _anthropic_config(*, api_key: str | None = "sk-ant-test") -> InMemoryConfigurationFake:
    return InMemoryConfigurationFake(
        vault_root=Path("/vault"),
        wiki_dir=Path("/vault/wiki"),
        anthropic_api_key=api_key,
        anthropic_model="claude-3-5-sonnet-20241022",
    )


def _mock_anthropic_client() -> Anthropic:
    def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content.decode())
        assert body["model"] == "claude-3-5-sonnet-20241022"
        return httpx.Response(
            200,
            json={
                "id": "msg_test",
                "type": "message",
                "role": "assistant",
                "content": [{"type": "text", "text": "anthropic assistant reply"}],
                "model": "claude-3-5-sonnet-20241022",
                "stop_reason": "end_turn",
                "usage": {"input_tokens": 10, "output_tokens": 5},
            },
        )

    return Anthropic(
        api_key="sk-ant-test",
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    )


def anthropic_complete_round_trip_C1() -> None:
    """C1 — complete() returns text block content from SDK test transport."""
    config = _anthropic_config()
    adapter = AnthropicLLMAdapter(config, client=_mock_anthropic_client())
    assert adapter.complete("hello") == "anthropic assistant reply"


def anthropic_unavailable_without_key_C2() -> None:
    """C2 — is_available() is False when anthropic_api_key is None."""
    adapter = AnthropicLLMAdapter(
        _anthropic_config(api_key=None),
        client=_mock_anthropic_client(),
    )
    assert adapter.is_available() is False
