"""Hermetic Ollama HTTP fixture for LLM adapter integration tests (S2-6)."""

from __future__ import annotations

import json
import threading
from collections.abc import Iterator
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any

import pytest


class _HermeticOllamaHandler(BaseHTTPRequestHandler):
    """Minimal Ollama-shaped HTTP handler for /api/tags and /api/chat."""

    chat_response: str = "assistant reply from hermetic server"
    last_chat_payload: dict[str, Any] | None = None
    installed_models: list[str] = ["llama3.2"]
    chat_status: int = 200
    chat_error: str = ""

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/api/tags":
            models = [{"name": name} for name in self.installed_models]
            self._send_json(200, {"models": models})
            return
        self.send_error(404)

    def do_POST(self) -> None:  # noqa: N802
        if self.path == "/api/chat":
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length))
            _HermeticOllamaHandler.last_chat_payload = payload
            if self.chat_status == 404:
                self._send_json(404, {"error": self.chat_error or "model not found"})
                return
            self._send_json(
                200,
                {
                    "model": payload.get("model", "llama3.2"),
                    "message": {"role": "assistant", "content": self.chat_response},
                    "done": True,
                },
            )
            return
        self.send_error(404)

    def _send_json(self, status: int, data: dict[str, Any]) -> None:
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        return


@pytest.fixture
def hermetic_ollama_server() -> Iterator[str]:
    """Start a threaded HTTP server mimicking Ollama on a random local port."""
    _HermeticOllamaHandler.last_chat_payload = None
    _HermeticOllamaHandler.installed_models = ["llama3.2"]
    _HermeticOllamaHandler.chat_status = 200
    _HermeticOllamaHandler.chat_error = ""
    server = HTTPServer(("127.0.0.1", 0), _HermeticOllamaHandler)
    host, port = server.server_address
    base_url = f"http://{host}:{port}"
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield base_url
    finally:
        server.shutdown()
        thread.join(timeout=2)
