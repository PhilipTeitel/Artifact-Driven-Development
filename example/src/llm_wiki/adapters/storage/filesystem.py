"""Filesystem wiki storage adapter (S2-4)."""

from __future__ import annotations

import json
import logging
from fnmatch import fnmatch
from pathlib import Path

from llm_wiki.domain.models import InitResult
from llm_wiki.domain.prompts.lint import LINT_SCAN_EXCLUDES
from llm_wiki.ports.configuration import ConfigurationPort
from llm_wiki.ports.schema import SchemaPort

logger = logging.getLogger(__name__)

REQUIRED_WIKI_ARTIFACTS = ("SCHEMA.md", "index.md", "log.md")
INGESTED_FILENAME = ".ingested.json"


class WikiStorageBoundaryError(ValueError):
    """Raised when a write targets a path outside the wiki subdirectory."""


class FilesystemWikiStorageAdapter:
    """Real filesystem I/O for vault/wiki artifacts (ADR-003)."""

    def __init__(
        self,
        *,
        config: ConfigurationPort,
        schema: SchemaPort,
        templates_dir: Path | None = None,
    ) -> None:
        self._config = config
        self._schema = schema
        self._templates_dir = templates_dir or _default_templates_dir()

    def read_source(self, relative_path: str) -> str:
        path = self._vault_path(relative_path)
        return path.read_text(encoding="utf-8")

    def list_sources(self) -> list[str]:
        excludes = self._schema.load().excludes
        wiki_prefix = self._wiki_relative_prefix()
        sources: list[str] = []
        for path in sorted(self._config.vault_root.rglob("*.md")):
            rel = path.relative_to(self._config.vault_root).as_posix()
            if self._is_excluded(rel, excludes, wiki_prefix):
                continue
            sources.append(rel)
        return sources

    def read_wiki_page(self, relative_path: str) -> str:
        return self._wiki_path(relative_path).read_text(encoding="utf-8")

    def write_wiki_page(self, relative_path: str, content: str) -> None:
        path = self._wiki_path(relative_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def read_index(self) -> str:
        return self.read_wiki_page("index.md")

    def list_wiki_pages(self) -> list[str]:
        wiki_dir = self._config.wiki_dir
        if not wiki_dir.is_dir():
            return []
        pages: list[str] = []
        for path in sorted(wiki_dir.rglob("*.md")):
            rel = path.relative_to(wiki_dir).as_posix()
            if rel in LINT_SCAN_EXCLUDES:
                continue
            pages.append(rel)
        return pages

    def write_index(self, content: str) -> None:
        self.write_wiki_page("index.md", content)

    def append_log(self, entry: str) -> None:
        log_path = self._wiki_path("log.md")
        if log_path.is_file():
            prior = log_path.read_bytes()
            if prior and not prior.endswith(b"\n"):
                entry = "\n" + entry
            log_path.write_bytes(prior + entry.encode("utf-8"))
        else:
            log_path.parent.mkdir(parents=True, exist_ok=True)
            log_path.write_text(entry, encoding="utf-8")

    def read_ingested(self) -> dict:
        path = self._wiki_path(INGESTED_FILENAME)
        if not path.is_file():
            return {"version": 1, "sources": {}}
        return json.loads(path.read_text(encoding="utf-8"))

    def write_ingested(self, data: dict) -> None:
        normalized = _normalize_ingested(data)
        path = self._wiki_path(INGESTED_FILENAME)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(normalized, indent=2) + "\n", encoding="utf-8")

    def wiki_exists(self) -> bool:
        wiki_dir = self._config.wiki_dir
        if not wiki_dir.is_dir():
            return False
        return all((wiki_dir / name).is_file() for name in REQUIRED_WIKI_ARTIFACTS)

    def ensure_wiki_layout(self) -> InitResult:
        wiki_dir = self._config.wiki_dir
        wiki_dir.mkdir(parents=True, exist_ok=True)
        created: list[str] = []
        already_present: list[str] = []
        for artifact in REQUIRED_WIKI_ARTIFACTS:
            dest = wiki_dir / artifact
            if dest.is_file():
                already_present.append(artifact)
                continue
            template = self._templates_dir / artifact
            if not template.is_file():
                logger.error("Missing init template: %s", template)
                raise FileNotFoundError(f"Init template not found: {template}")
            dest.write_bytes(template.read_bytes())
            created.append(artifact)
        return InitResult(
            created=tuple(created),
            already_present=tuple(already_present),
            wiki_dir=wiki_dir,
        )

    def _vault_path(self, relative_path: str) -> Path:
        rel = Path(relative_path)
        if rel.is_absolute() or ".." in rel.parts:
            raise WikiStorageBoundaryError(
                f"Invalid vault-relative path: {relative_path!r}"
            )
        resolved = (self._config.vault_root / rel).resolve()
        vault_resolved = self._config.vault_root.resolve()
        if not resolved.is_relative_to(vault_resolved):
            raise WikiStorageBoundaryError(
                f"Path escapes vault root: {relative_path!r}"
            )
        return resolved

    def _wiki_path(self, relative_path: str) -> Path:
        rel = Path(relative_path)
        if rel.is_absolute() or ".." in rel.parts:
            raise WikiStorageBoundaryError(
                f"Wiki writes must stay inside wiki dir; rejected: {relative_path!r}"
            )
        resolved = (self._config.wiki_dir / rel).resolve()
        wiki_resolved = self._config.wiki_dir.resolve()
        if not resolved.is_relative_to(wiki_resolved):
            raise WikiStorageBoundaryError(
                f"Wiki writes must stay inside wiki dir; rejected: {relative_path!r}"
            )
        return resolved

    def _wiki_relative_prefix(self) -> str:
        return self._config.wiki_dir.relative_to(self._config.vault_root).as_posix()

    def _is_excluded(
        self,
        vault_relative: str,
        excludes: tuple[str, ...],
        wiki_prefix: str,
    ) -> bool:
        if vault_relative.startswith(f"{wiki_prefix}/") or vault_relative == wiki_prefix:
            return True
        for pattern in excludes:
            if _matches_exclude(vault_relative, pattern):
                return True
        return False


def _default_templates_dir() -> Path:
    return Path(__file__).resolve().parents[4] / "templates" / "wiki"


def _normalize_ingested(data: dict) -> dict:
    sources = data.get("sources", {})
    normalized_sources = {
        str(key).replace("\\", "/"): value for key, value in sources.items()
    }
    return {"version": data.get("version", 1), "sources": normalized_sources}


def _matches_exclude(path: str, pattern: str) -> bool:
    if pattern == ".*":
        basename = Path(path).name
        return basename.startswith(".")
    if pattern.endswith("/"):
        prefix = pattern.rstrip("/")
        return path == prefix or path.startswith(f"{prefix}/")
    return fnmatch(path, pattern) or fnmatch(Path(path).name, pattern)
