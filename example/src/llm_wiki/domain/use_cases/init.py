"""Initialize wiki layout idempotently (S1, S2, S13)."""

from __future__ import annotations

import logging
import re
from datetime import UTC, datetime

from llm_wiki.domain.models import InitResult
from llm_wiki.ports.configuration import ConfigurationPort
from llm_wiki.ports.interaction import UserInteractionPort
from llm_wiki.ports.storage import WikiStoragePort

logger = logging.getLogger("llm_wiki.domain.use_cases")

_INIT_LOG_HEADING = re.compile(r"^## \[\d{4}-\d{2}-\d{2}\] init \|")


class InitUseCase:
    """Orchestrate idempotent wiki layout creation and init log append.

    Log headings use UTC calendar dates: ``## [YYYY-MM-DD] init | {title}``.
    """

    def __init__(
        self,
        *,
        storage: WikiStoragePort,
        interaction: UserInteractionPort,
        config: ConfigurationPort,
    ) -> None:
        self._storage = storage
        self._interaction = interaction
        self._config = config

    def execute(self) -> InitResult:
        """Initialize wiki layout idempotently; append init log; present summary."""
        result = self._storage.ensure_wiki_layout()
        log_entry = self._build_init_log_entry()
        self._storage.append_log(log_entry)
        self._interaction.present(self._build_summary(result))
        logger.info(
            "Init complete: created=%d already_present=%d",
            len(result.created),
            len(result.already_present),
        )
        return result

    def _build_init_log_entry(self) -> str:
        date = datetime.now(UTC).strftime("%Y-%m-%d")
        wiki_name = self._config.wiki_dir.name or "wiki"
        return f"## [{date}] init | {wiki_name}"

    def _build_summary(self, result: InitResult) -> str:
        lines: list[str] = [f"Wiki directory: {result.wiki_dir}"]
        if result.created:
            lines.append(f"Created: {', '.join(result.created)}")
        if result.already_present:
            lines.append(f"Already present: {', '.join(result.already_present)}")
        return "\n".join(lines)


def init_log_heading_matches(entry: str) -> bool:
    """Return True when the first line matches ADR-003 init log heading."""
    first_line = entry.splitlines()[0] if entry else ""
    return bool(_INIT_LOG_HEADING.match(first_line))
