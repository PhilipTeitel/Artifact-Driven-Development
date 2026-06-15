"""Ollama LLM adapter via httpx (ADR-004 / S2-6)."""

from __future__ import annotations

import logging

import httpx

from llm_wiki.adapters.cli.configuration import DEFAULT_OLLAMA_MODEL
from llm_wiki.ports.configuration import ConfigurationPort

logger = logging.getLogger(__name__)


class OllamaLLMAdapter:
    """HTTP client for Ollama /api/chat (not the OpenAI SDK)."""

    def __init__(
        self,
        config: ConfigurationPort,
        *,
        client: httpx.Client | None = None,
    ) -> None:
        self._config = config
        self._client = client or httpx.Client(timeout=30.0)
        self._owns_client = client is None

    def _tags_url(self) -> str:
        return f"{self._config.ollama_base_url.rstrip('/')}/api/tags"

    def _list_installed_models(self) -> list[str]:
        try:
            response = self._client.get(self._tags_url())
            if response.status_code != 200:
                return []
            models = response.json().get("models") or []
            return [name for m in models if isinstance(name := m.get("name"), str)]
        except (httpx.HTTPError, ValueError, TypeError):
            return []

    def _resolve_chat_model(self) -> str:
        requested = self._config.ollama_model
        installed = self._list_installed_models()
        if requested in installed:
            return requested
        for name in installed:
            if name.split(":")[0] == requested:
                return name
        if installed and requested == DEFAULT_OLLAMA_MODEL:
            chosen = installed[0]
            logger.warning(
                "Ollama model %r not installed; using %r instead. "
                "Set OLLAMA_MODEL or run `ollama pull %s`.",
                requested,
                chosen,
                requested,
            )
            return chosen
        return requested

    def _raise_model_not_found(self, response: httpx.Response, model: str) -> None:
        installed = self._list_installed_models()
        available = ", ".join(installed) if installed else "(none)"
        detail = ""
        try:
            err = response.json().get("error", "")
            if isinstance(err, str) and err:
                detail = f" {err}."
        except ValueError:
            pass
        raise ValueError(
            f"Ollama model {model!r} not found.{detail} "
            f"Installed models: {available}. "
            f"Run `ollama pull {model}` or set OLLAMA_MODEL."
        )

    def is_available(self) -> bool:
        url = self._tags_url()
        try:
            response = self._client.get(url)
            return response.status_code == 200
        except httpx.HTTPError:
            return False

    def complete(self, prompt: str, *, system: str | None = None) -> str:
        messages: list[dict[str, str]] = []
        if system is not None:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        url = f"{self._config.ollama_base_url.rstrip('/')}/api/chat"
        model = self._resolve_chat_model()
        payload: dict[str, object] = {
            "model": model,
            "messages": messages,
            "stream": False,
        }
        logger.debug(
            "Ollama complete model=%s base_url=%s",
            model,
            self._config.ollama_base_url,
        )
        response = self._client.post(url, json=payload)
        if response.status_code == 404:
            self._raise_model_not_found(response, model)
        response.raise_for_status()
        data = response.json()
        message = data.get("message") or {}
        content = message.get("content")
        if not isinstance(content, str):
            raise ValueError("Ollama response missing message.content")
        return content

    def close(self) -> None:
        if self._owns_client:
            self._client.close()
