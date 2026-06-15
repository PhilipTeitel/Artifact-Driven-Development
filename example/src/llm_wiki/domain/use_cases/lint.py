"""Health-check wiki pages with report-only lint (S9, S13)."""

from __future__ import annotations

import logging
from datetime import UTC, datetime

from llm_wiki.domain.models.lint_result import LintResult
from llm_wiki.domain.prompts.lint import (
    build_lint_prompt,
    build_lint_report,
    extract_lint_summary,
    lint_log_title,
    parse_lint_response,
)
from llm_wiki.ports.configuration import ConfigurationPort
from llm_wiki.ports.interaction import UserInteractionPort
from llm_wiki.ports.llm import LLMPort
from llm_wiki.ports.storage import WikiStoragePort

logger = logging.getLogger("llm_wiki.domain.use_cases")


class LintUseCase:
    """Orchestrate wiki lint through ports only; suggest fixes without auto-apply."""

    def __init__(
        self,
        *,
        storage: WikiStoragePort,
        llm: LLMPort,
        interaction: UserInteractionPort,
        config: ConfigurationPort,
    ) -> None:
        self._storage = storage
        self._llm = llm
        self._interaction = interaction
        self._config = config

    def execute(self) -> LintResult:
        """Scan wiki pages, present a report, and append a lint log entry."""
        logger.info("Lint starting")
        index_content = self._storage.read_index()
        page_paths = self._storage.list_wiki_pages()

        page_contents: dict[str, str] = {}
        for page_path in page_paths:
            page_contents[page_path] = self._storage.read_wiki_page(page_path)

        logger.debug("Lint read %d wiki pages", len(page_contents))

        if not page_contents:
            report = (
                "# Lint Report\n\n"
                "## Summary\n"
                "No pages to lint.\n\n"
                "## Findings\n"
                f"No wiki pages found under {self._config.wiki_dir.as_posix()}.\n"
            )
            self._interaction.present(report)
            self._storage.append_log(_build_lint_log_entry("no pages to lint"))
            logger.info("Lint complete: 0 pages, 0 findings")
            return LintResult(findings=(), report=report, log_appended=True)

        prompt = build_lint_prompt(index_content=index_content, page_contents=page_contents)
        llm_response = self._llm.complete(prompt)
        findings = parse_lint_response(llm_response)
        report = build_lint_report(findings, summary=extract_lint_summary(llm_response))

        self._interaction.present(report)
        self._storage.append_log(_build_lint_log_entry(lint_log_title(findings)))
        logger.info("Lint complete: %d findings", len(findings))
        return LintResult(findings=findings, report=report, log_appended=True)


def _build_lint_log_entry(title: str) -> str:
    date = datetime.now(UTC).strftime("%Y-%m-%d")
    return f"## [{date}] lint | {title}"
