"""In-memory reference fakes implementing all five ports for contract tests."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from llm_wiki.domain.models import InitResult, WikiSchema
from llm_wiki.domain.prompts.lint import LINT_SCAN_EXCLUDES

REQUIRED_WIKI_ARTIFACTS = ("SCHEMA.md", "index.md", "log.md")
DEFAULT_EXCLUDES = [".obsidian/", "wiki/", ".*"]


@dataclass
class InMemoryConfigurationFake:
    """Reference fake for ConfigurationPort."""

    vault_root: Path
    wiki_dir: Path
    batch_mode: bool = False
    provider_override: str | None = None
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"
    anthropic_api_key: str | None = None
    anthropic_model: str = "claude-3-5-sonnet-20241022"


@dataclass
class InMemoryLLMFake:
    """Reference fake for LLMPort."""

    available: bool = True
    responses: dict[str, str] = field(default_factory=dict)

    def complete(self, prompt: str, *, system: str | None = None) -> str:
        if prompt in self.responses:
            return self.responses[prompt]
        for key, response in self.responses.items():
            if key in prompt:
                return response
        prefix = f"[system:{system}] " if system else ""
        return f"{prefix}echo:{prompt}"

    def is_available(self) -> bool:
        return self.available


@dataclass
class InMemoryWikiStorageFake:
    """Reference fake for WikiStoragePort."""

    wiki_dir: Path
    sources: dict[str, str] = field(default_factory=dict)
    wiki_pages: dict[str, str] = field(default_factory=dict)
    index_content: str = ""
    log_entries: list[str] = field(default_factory=list)
    ingested: dict = field(default_factory=lambda: {"version": 1, "sources": {}})
    call_log: list[str] = field(default_factory=list)
    ingested_writes: int = 0
    _layout_initialized: bool = False

    def _record(self, method: str, detail: str = "") -> None:
        entry = f"{method}:{detail}" if detail else method
        self.call_log.append(entry)

    def read_source(self, relative_path: str) -> str:
        self._record("read_source")
        return self.sources[relative_path]

    def list_sources(self) -> list[str]:
        self._record("list_sources")
        return sorted(self.sources)

    def read_wiki_page(self, relative_path: str) -> str:
        self._record("read_wiki_page")
        if relative_path not in self.wiki_pages:
            raise KeyError(relative_path)
        return self.wiki_pages[relative_path]

    def write_wiki_page(self, relative_path: str, content: str) -> None:
        self._record("write_wiki_page", relative_path)
        self.wiki_pages[relative_path] = content

    def read_index(self) -> str:
        self._record("read_index")
        if "index.md" not in self.wiki_pages:
            raise KeyError("index.md")
        return self.wiki_pages["index.md"]

    def list_wiki_pages(self) -> list[str]:
        self._record("list_wiki_pages")
        return sorted(
            path
            for path in self.wiki_pages
            if path.endswith(".md") and path not in LINT_SCAN_EXCLUDES
        )

    def write_index(self, content: str) -> None:
        self._record("write_index")
        self.index_content = content
        self.wiki_pages["index.md"] = content

    def append_log(self, entry: str) -> None:
        self._record("append_log")
        self.log_entries.append(entry)

    def read_ingested(self) -> dict:
        self._record("read_ingested")
        return dict(self.ingested)

    def write_ingested(self, data: dict) -> None:
        self._record("write_ingested")
        self.ingested_writes += 1
        self.ingested = dict(data)

    def wiki_exists(self) -> bool:
        self._record("wiki_exists")
        return self._layout_initialized

    def ensure_wiki_layout(self) -> InitResult:
        self._record("ensure_wiki_layout")
        created: list[str] = []
        already_present: list[str] = []
        for artifact in REQUIRED_WIKI_ARTIFACTS:
            if artifact in self.wiki_pages:
                already_present.append(artifact)
            else:
                self.wiki_pages[artifact] = ""
                if artifact == "index.md":
                    self.index_content = ""
                created.append(artifact)
        self._layout_initialized = True
        return InitResult(
            created=tuple(created),
            already_present=tuple(already_present),
            wiki_dir=self.wiki_dir,
        )


@dataclass
class InMemorySchemaFake:
    """Reference fake for SchemaPort."""

    excludes: tuple[str, ...] = tuple(DEFAULT_EXCLUDES)
    raw_sections: dict[str, str] = field(default_factory=dict)

    def load(self) -> WikiSchema:
        return WikiSchema(excludes=self.excludes, raw_sections=dict(self.raw_sections))

    def default_excludes(self) -> list[str]:
        return list(DEFAULT_EXCLUDES)


@dataclass
class InMemoryInteractionFake:
    """Reference fake for UserInteractionPort."""

    confirm_responses: dict[str, bool] = field(default_factory=dict)
    prompt_responses: dict[str, str] = field(default_factory=dict)
    presented: list[str] = field(default_factory=list)
    timeline: list[str] | None = None

    def confirm(self, message: str) -> bool:
        if self.timeline is not None:
            self.timeline.append("confirm")
        return self.confirm_responses.get(message, True)

    def present(self, text: str) -> None:
        if self.timeline is not None:
            self.timeline.append("present")
        self.presented.append(text)

    def prompt(self, message: str) -> str:
        return self.prompt_responses.get(message, "")
