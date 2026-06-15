"""Typer CLI composition root wiring domain use cases (ADR-005)."""

from __future__ import annotations

import logging
import os
from collections.abc import Callable
from pathlib import Path
from typing import Annotated

import typer

from llm_wiki.adapters.cli.configuration import CLIFlags
from llm_wiki.adapters.cli.errors import ConfigurationError, VaultNotFoundError
from llm_wiki.adapters.cli.wiring import AppContext, WiringOverrides, build_context
from llm_wiki.adapters.llm.errors import ProviderUnavailableError
from llm_wiki.domain.use_cases import (
    IngestUseCase,
    InitUseCase,
    LintUseCase,
    QueryUseCase,
    ValidateUseCase,
)

logger = logging.getLogger("llm_wiki.adapters.cli")

if os.environ.get("LLM_WIKI_LOG", "").upper() == "DEBUG":
    logging.basicConfig(level=logging.DEBUG)

app = typer.Typer(
    name="llm-wiki",
    help="LLM-maintained wiki CLI for Obsidian vaults (Stage 2 scaffold).",
    no_args_is_help=True,
)


@app.callback()
def main(
    ctx: typer.Context,
    vault: Annotated[
        str | None,
        typer.Option("--vault", help="Path to Obsidian vault root."),
    ] = None,
    wiki_dir: Annotated[
        str | None,
        typer.Option("--wiki-dir", help="Wiki subdirectory name under vault."),
    ] = None,
    provider: Annotated[
        str | None,
        typer.Option("--provider", help="LLM provider: ollama, openai, or anthropic."),
    ] = None,
) -> None:
    """Global options resolved via CLIConfigurationAdapter."""
    ctx.ensure_object(dict)
    ctx.obj["cli_flags"] = CLIFlags(vault=vault, wiki_dir=wiki_dir, provider=provider)
    logger.debug(
        "CLI invoked with vault=%r wiki_dir=%r provider=%r",
        vault,
        wiki_dir,
        provider,
    )


def _flags_from_ctx(ctx: typer.Context, *, batch: bool = False) -> CLIFlags:
    base: CLIFlags = ctx.obj.get("cli_flags", CLIFlags())
    return CLIFlags(
        vault=base.vault,
        wiki_dir=base.wiki_dir,
        provider=base.provider,
        batch=batch,
    )


def _run_command(
    ctx: typer.Context,
    command_name: str,
    handler: Callable[[AppContext], int],
    *,
    batch: bool = False,
    require_llm: bool = False,
    overrides: WiringOverrides | None = None,
) -> None:
    """Build context, invoke handler, map outcomes to Typer exit codes."""
    try:
        context = build_context(
            flags=_flags_from_ctx(ctx, batch=batch),
            start_path=Path.cwd(),
            overrides=overrides,
            require_llm=require_llm,
        )
    except VaultNotFoundError as exc:
        typer.echo(str(exc), err=True)
        logger.info("%s failed: vault not found", command_name)
        raise typer.Exit(code=1) from exc
    except ConfigurationError as exc:
        typer.echo(str(exc), err=True)
        logger.info("%s failed: configuration error", command_name)
        raise typer.Exit(code=1) from exc
    except ProviderUnavailableError as exc:
        typer.echo(str(exc), err=True)
        logger.info("%s failed: no LLM provider", command_name)
        raise typer.Exit(code=1) from exc

    try:
        exit_code = handler(context)
    except ProviderUnavailableError as exc:
        typer.echo(str(exc), err=True)
        logger.info("%s failed: no LLM provider", command_name)
        raise typer.Exit(code=1) from exc
    except ValueError as exc:
        typer.echo(str(exc), err=True)
        logger.info("%s failed: %s", command_name, exc)
        raise typer.Exit(code=1) from exc

    if exit_code == 0:
        logger.info("%s complete", command_name)
    else:
        logger.info("%s failed exit=%d", command_name, exit_code)
    raise typer.Exit(code=exit_code)


@app.command()
def init(ctx: typer.Context) -> None:
    """Initialize wiki layout in the vault."""

    def handler(context: AppContext) -> int:
        use_case = InitUseCase(
            storage=context.storage,
            interaction=context.interaction,
            config=context.config,
        )
        use_case.execute()
        return 0

    _run_command(ctx, "init", handler)


@app.command()
def validate(ctx: typer.Context) -> None:
    """Validate vault/wiki structure."""

    def handler(context: AppContext) -> int:
        use_case = ValidateUseCase(
            storage=context.storage,
            schema=context.schema,
            config=context.config,
        )
        result = use_case.execute()
        if not result.valid:
            for issue in result.issues:
                typer.echo(issue.message, err=True)
            return 1
        typer.echo("Wiki validation passed.")
        return 0

    _run_command(ctx, "validate", handler)


@app.command()
def ingest(
    ctx: typer.Context,
    path: Annotated[str, typer.Argument(help="Source file or directory to ingest.")],
    batch: Annotated[
        bool,
        typer.Option("--batch", help="Non-interactive ingest mode."),
    ] = False,
) -> None:
    """Ingest source markdown into the wiki."""
    logger.debug("ingest path=%r batch=%s", path, batch)

    def handler(context: AppContext) -> int:
        if context.llm is None:
            raise ProviderUnavailableError()
        use_case = IngestUseCase(
            storage=context.storage,
            llm=context.llm,
            schema=context.schema,
            interaction=context.interaction,
            config=context.config,
        )
        use_case.execute(path)
        return 0

    _run_command(ctx, "ingest", handler, batch=batch, require_llm=True)


@app.command()
def query(
    ctx: typer.Context,
    text: Annotated[list[str], typer.Argument(help="Question text.")],
) -> None:
    """Query the wiki with a natural-language question."""
    question = " ".join(text)
    logger.debug("query text=%r", question)

    def handler(context: AppContext) -> int:
        if context.llm is None:
            raise ProviderUnavailableError()
        use_case = QueryUseCase(
            storage=context.storage,
            llm=context.llm,
            interaction=context.interaction,
            config=context.config,
        )
        use_case.execute(question)
        return 0

    _run_command(ctx, "query", handler, require_llm=True)


@app.command()
def lint(ctx: typer.Context) -> None:
    """Report wiki health issues."""

    def handler(context: AppContext) -> int:
        if context.llm is None:
            raise ProviderUnavailableError()
        use_case = LintUseCase(
            storage=context.storage,
            llm=context.llm,
            interaction=context.interaction,
            config=context.config,
        )
        use_case.execute()
        return 0

    _run_command(ctx, "lint", handler, require_llm=True)


if __name__ == "__main__":
    app()
