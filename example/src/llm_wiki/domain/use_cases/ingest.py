"""Ingest vault sources into the wiki (S6, S7, S12, S13)."""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from fnmatch import fnmatch
from pathlib import Path

from llm_wiki.domain.models import IngestResult
from llm_wiki.domain.prompts.ingest import build_ingest_prompt, parse_ingest_response
from llm_wiki.ports.configuration import ConfigurationPort
from llm_wiki.ports.interaction import UserInteractionPort
from llm_wiki.ports.llm import LLMPort
from llm_wiki.ports.schema import SchemaPort
from llm_wiki.ports.storage import WikiStoragePort

logger = logging.getLogger("llm_wiki.domain.use_cases")

_CONFIRM_MESSAGE = "Proceed with wiki writes for this ingest?"


class IngestUseCase:
    """Orchestrate interactive and batch ingest through ports only."""

    def __init__(
        self,
        *,
        storage: WikiStoragePort,
        llm: LLMPort,
        schema: SchemaPort,
        interaction: UserInteractionPort,
        config: ConfigurationPort,
    ) -> None:
        self._storage = storage
        self._llm = llm
        self._schema = schema
        self._interaction = interaction
        self._config = config

    def execute(self, path: str) -> IngestResult:
        """Ingest one source file or directory per S6/S7."""
        normalized = _normalize_path(path)
        schema = self._schema.load()
        ingested = self._storage.read_ingested()
        wiki_prefix = self._wiki_relative_prefix()

        if _is_directory_path(normalized, self._storage.list_sources()):
            if not self._config.batch_mode:
                raise ValueError(
                    f"Directory ingest requires batch_mode; got directory path {normalized!r}"
                )
            return self._batch_ingest_directory(
                normalized,
                excludes=schema.excludes,
                wiki_prefix=wiki_prefix,
                ingested=ingested,
            )

        return self._ingest_single(
            normalized,
            excludes=schema.excludes,
            wiki_prefix=wiki_prefix,
            ingested=ingested,
        )

    def _batch_ingest_directory(
        self,
        directory: str,
        *,
        excludes: tuple[str, ...],
        wiki_prefix: str,
        ingested: dict,
    ) -> IngestResult:
        logger.info("Batch ingest starting for directory %s", directory)
        processed: list[str] = []
        skipped: list[str] = []
        pages_written: list[str] = []
        log_appended = False

        candidates = _list_markdown_under(directory, self._storage.list_sources())
        for source_path in candidates:
            if _is_excluded(source_path, excludes, wiki_prefix):
                logger.debug("Skipping excluded source %s", source_path)
                skipped.append(source_path)
                continue
            if source_path in ingested.get("sources", {}):
                logger.debug("Skipping already-ingested source %s", source_path)
                skipped.append(source_path)
                continue

            result = self._ingest_single(
                source_path,
                excludes=excludes,
                wiki_prefix=wiki_prefix,
                ingested=ingested,
                require_confirm=False,
            )
            if result.processed:
                processed.extend(result.processed)
                pages_written.extend(result.pages_written)
                log_appended = log_appended or result.log_appended
                ingested = self._storage.read_ingested()

        logger.info(
            "Batch ingest complete: processed=%d skipped=%d",
            len(processed),
            len(skipped),
        )
        return IngestResult(
            processed=tuple(processed),
            skipped=tuple(skipped),
            pages_written=tuple(pages_written),
            log_appended=log_appended,
        )

    def _ingest_single(
        self,
        source_path: str,
        *,
        excludes: tuple[str, ...],
        wiki_prefix: str,
        ingested: dict,
        require_confirm: bool | None = None,
    ) -> IngestResult:
        if _is_excluded(source_path, excludes, wiki_prefix):
            logger.debug("Skipping excluded source %s", source_path)
            return IngestResult(
                processed=(), skipped=(source_path,), pages_written=(), log_appended=False
            )

        if source_path in ingested.get("sources", {}):
            logger.debug("Skipping already-ingested source %s", source_path)
            return IngestResult(
                processed=(), skipped=(source_path,), pages_written=(), log_appended=False
            )

        logger.info("Ingest starting for source %s", source_path)
        content = self._storage.read_source(source_path)
        prompt = build_ingest_prompt(source_path=source_path, content=content)
        llm_response = self._llm.complete(prompt)
        parsed = parse_ingest_response(llm_response)

        needs_confirm = (
            require_confirm if require_confirm is not None else not self._config.batch_mode
        )
        if needs_confirm:
            self._interaction.present(parsed.takeaways)
            if not self._interaction.confirm(_CONFIRM_MESSAGE):
                logger.info("Ingest declined for source %s", source_path)
                return IngestResult(processed=(), skipped=(), pages_written=(), log_appended=False)

        pages_written: list[str] = []
        for page_path, page_content in parsed.wiki_pages.items():
            self._storage.write_wiki_page(page_path, page_content)
            pages_written.append(page_path)

        if parsed.index_update:
            self._storage.write_index(parsed.index_update)

        title = _source_title(source_path)
        log_entry = _build_ingest_log_entry(title)
        self._storage.append_log(log_entry)

        updated = _update_ingested_sidecar(ingested, source_path)
        self._storage.write_ingested(updated)

        logger.info("Ingest complete for source %s pages=%d", source_path, len(pages_written))
        return IngestResult(
            processed=(source_path,),
            skipped=(),
            pages_written=tuple(pages_written),
            log_appended=True,
        )

    def _wiki_relative_prefix(self) -> str:
        return self._config.wiki_dir.relative_to(self._config.vault_root).as_posix()


def _normalize_path(path: str) -> str:
    normalized = path.replace("\\", "/")
    trailing_slash = normalized.endswith("/")
    stripped = normalized.strip("/")
    if trailing_slash and stripped:
        return f"{stripped}/"
    return stripped


def _is_directory_path(path: str, sources: list[str]) -> bool:
    if path.endswith("/"):
        return True
    prefix = f"{path}/"
    return any(source.startswith(prefix) for source in sources)


def _list_markdown_under(directory: str, sources: list[str]) -> list[str]:
    prefix = f"{directory.rstrip('/')}/"
    return sorted(
        source
        for source in sources
        if source.startswith(prefix) and source.endswith(".md")
    )


def _is_excluded(path: str, excludes: tuple[str, ...], wiki_prefix: str) -> bool:
    if path.startswith(f"{wiki_prefix}/") or path == wiki_prefix:
        return True
    for pattern in excludes:
        if _matches_exclude(path, pattern):
            return True
    return False


def _matches_exclude(path: str, pattern: str) -> bool:
    if pattern == ".*":
        return Path(path).name.startswith(".")
    if pattern.endswith("/"):
        prefix = pattern.rstrip("/")
        return path == prefix or path.startswith(f"{prefix}/")
    return fnmatch(path, pattern) or fnmatch(Path(path).name, pattern)


def _source_title(source_path: str) -> str:
    stem = Path(source_path).stem
    return stem.replace("-", " ").replace("_", " ").title()


def _build_ingest_log_entry(title: str) -> str:
    date = datetime.now(UTC).strftime("%Y-%m-%d")
    return f"## [{date}] ingest | {title}"


def _update_ingested_sidecar(ingested: dict, source_path: str) -> dict:
    sources = dict(ingested.get("sources", {}))
    timestamp = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    sources[source_path.replace("\\", "/")] = timestamp
    return {"version": ingested.get("version", 1), "sources": sources}
