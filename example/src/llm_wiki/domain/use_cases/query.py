"""Answer questions from wiki content with optional filing (S8, S13)."""

from __future__ import annotations

import logging
import re
from datetime import UTC, datetime

from llm_wiki.domain.models import QueryResult
from llm_wiki.domain.prompts.query import (
    build_query_prompt,
    parse_query_response,
    select_pages_from_index,
)
from llm_wiki.ports.configuration import ConfigurationPort
from llm_wiki.ports.interaction import UserInteractionPort
from llm_wiki.ports.llm import LLMPort
from llm_wiki.ports.storage import WikiStoragePort

logger = logging.getLogger("llm_wiki.domain.use_cases")

_CONFIRM_MESSAGE = "File this answer as a new wiki page?"


class QueryUseCase:
    """Orchestrate index-first query and optional answer filing through ports only."""

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

    def execute(self, question: str) -> QueryResult:
        """Answer a question from wiki pages; file on explicit confirm."""
        logger.info("Query starting")
        index_content = self._storage.read_index()
        selected_pages = select_pages_from_index(index_content, question)

        page_contents: dict[str, str] = {}
        for page_path in selected_pages:
            page_contents[page_path] = self._storage.read_wiki_page(page_path)

        logger.debug("Query read %d wiki pages", len(page_contents))

        if not page_contents:
            answer = (
                "The wiki index lists no pages to search. "
                f"Wiki path: {self._config.wiki_dir.as_posix()}"
            )
            self._interaction.present(answer)
            logger.info("Query complete: no pages to search; filed=False")
            return QueryResult(answer=answer, citations=(), filed=False, filed_page=None)

        prompt = build_query_prompt(
            question=question,
            index_content=index_content,
            page_contents=page_contents,
        )
        llm_response = self._llm.complete(prompt)
        parsed = parse_query_response(llm_response, pages_read=set(page_contents))

        self._interaction.present(parsed.answer)
        if not self._interaction.confirm(_CONFIRM_MESSAGE):
            logger.info("Query complete: filing declined")
            return QueryResult(
                answer=parsed.answer,
                citations=parsed.citations,
                filed=False,
                filed_page=None,
            )

        filed_page = _file_answer_page(
            storage=self._storage,
            question=question,
            answer=parsed.answer,
            index_content=index_content,
        )
        logger.info("Query complete: filed=True page=%s", filed_page)
        return QueryResult(
            answer=parsed.answer,
            citations=parsed.citations,
            filed=True,
            filed_page=filed_page,
        )


def _file_answer_page(
    *,
    storage: WikiStoragePort,
    question: str,
    answer: str,
    index_content: str,
) -> str:
    title = _query_title(question)
    page_path = _query_page_path(question)
    storage.write_wiki_page(page_path, answer)
    storage.write_index(_append_index_link(index_content, title=title, page_path=page_path))
    storage.append_log(_build_query_log_entry(title))
    return page_path


def _query_title(question: str) -> str:
    cleaned = question.strip().rstrip("?")
    if not cleaned:
        return "Query answer"
    return cleaned[:80]


def _query_page_path(question: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", question.lower()).strip("-")[:60]
    if not slug:
        slug = "query-answer"
    date = datetime.now(UTC).strftime("%Y-%m-%d")
    return f"queries/{date}-{slug}.md"


def _append_index_link(index_content: str, *, title: str, page_path: str) -> str:
    link_line = f"- [{title}]({page_path})"
    if index_content.strip():
        return f"{index_content.rstrip()}\n{link_line}\n"
    return f"{link_line}\n"


def _build_query_log_entry(title: str) -> str:
    date = datetime.now(UTC).strftime("%Y-%m-%d")
    return f"## [{date}] query | {title}"
