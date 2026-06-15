"""Integration tests for CLIConfigurationAdapter."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from llm_wiki.adapters.cli.configuration import (
    CLIFlags,
    build_cli_configuration,
)
from llm_wiki.adapters.cli.errors import VaultNotFoundError


def _clean_environ() -> dict[str, str]:
    keys = (
        "LLM_WIKI_DIR",
        "LLM_WIKI_PROVIDER",
        "OLLAMA_BASE_URL",
        "OLLAMA_MODEL",
        "OPENAI_API_KEY",
        "OPENAI_MODEL",
        "ANTHROPIC_API_KEY",
        "ANTHROPIC_MODEL",
    )
    return {k: v for k, v in os.environ.items() if k not in keys}


def _make_obsidian_vault(root: Path) -> Path:
    (root / ".obsidian").mkdir(parents=True)
    return root


def walkup_finds_obsidian_A1(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A1 — walk-up finds ancestor with .obsidian/."""
    vault = _make_obsidian_vault(tmp_path / "vault")
    nested = vault / "daily" / "2026"
    nested.mkdir(parents=True)
    monkeypatch.chdir(nested)
    config = build_cli_configuration(environ=_clean_environ(), start_path=nested)
    assert config.vault_root == vault.resolve()
    assert config.wiki_dir == (vault / "wiki").resolve()


def walkup_finds_schema_A2(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A2 — walk-up finds vault via wiki/SCHEMA.md without .obsidian/."""
    vault = tmp_path / "vault"
    wiki = vault / "wiki"
    wiki.mkdir(parents=True)
    (wiki / "SCHEMA.md").write_text("# schema\n", encoding="utf-8")
    nested = vault / "notes" / "deep"
    nested.mkdir(parents=True)
    monkeypatch.chdir(nested)
    config = build_cli_configuration(environ=_clean_environ(), start_path=nested)
    assert config.vault_root == vault.resolve()


def explicit_vault_flag_A3(tmp_path: Path) -> None:
    """A3 — explicit --vault path used when valid."""
    vault = _make_obsidian_vault(tmp_path / "explicit-vault")
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    config = build_cli_configuration(
        flags=CLIFlags(vault=str(vault)),
        environ=_clean_environ(),
        start_path=elsewhere,
    )
    assert config.vault_root == vault.resolve()


def rejects_invalid_vault_s3_B1(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """B1 — no marker raises VaultNotFoundError with --vault guidance."""
    orphan = tmp_path / "nowhere" / "deep"
    orphan.mkdir(parents=True)
    monkeypatch.chdir(orphan)
    with pytest.raises(VaultNotFoundError) as exc_info:
        build_cli_configuration(environ=_clean_environ(), start_path=orphan)
    message = str(exc_info.value).lower()
    assert "--vault" in message
    assert "workspace" in message or "open" in message


def no_partial_wiki_on_error_s3_B2(tmp_path: Path) -> None:
    """B2 — invalid --vault raises without creating wiki files."""
    invalid = tmp_path / "not-a-vault"
    invalid.mkdir()
    before = list(tmp_path.rglob("*"))
    with pytest.raises(VaultNotFoundError):
        build_cli_configuration(
            flags=CLIFlags(vault=str(invalid)),
            environ=_clean_environ(),
            start_path=tmp_path,
        )
    after = list(tmp_path.rglob("*"))
    assert before == after
    assert not (invalid / "wiki").exists()
    assert not (invalid / "SCHEMA.md").exists()


def default_models_adr004_C1(tmp_path: Path) -> None:
    """C1 — ADR-004 defaults when env unset."""
    vault = _make_obsidian_vault(tmp_path / "vault")
    config = build_cli_configuration(
        flags=CLIFlags(vault=str(vault)),
        environ=_clean_environ(),
    )
    assert config.ollama_base_url == "http://localhost:11434"
    assert config.ollama_model == "llama3.2"
    assert config.openai_model == "gpt-4o-mini"
    assert config.anthropic_model == "claude-3-5-sonnet-20241022"


def reads_api_keys_C2(tmp_path: Path) -> None:
    """C2 — API keys read from OPENAI_API_KEY and ANTHROPIC_API_KEY."""
    vault = _make_obsidian_vault(tmp_path / "vault")
    environ = _clean_environ()
    environ["OPENAI_API_KEY"] = "sk-openai-test"
    environ["ANTHROPIC_API_KEY"] = "sk-ant-test"
    config = build_cli_configuration(
        flags=CLIFlags(vault=str(vault)),
        environ=environ,
    )
    assert config.openai_api_key == "sk-openai-test"
    assert config.anthropic_api_key == "sk-ant-test"


def flag_overrides_wiki_dir_s19_D1(tmp_path: Path) -> None:
    """D1 — --wiki-dir flag overrides LLM_WIKI_DIR env."""
    vault = _make_obsidian_vault(tmp_path / "vault")
    environ = _clean_environ()
    environ["LLM_WIKI_DIR"] = "notes"
    config = build_cli_configuration(
        flags=CLIFlags(vault=str(vault), wiki_dir="wiki"),
        environ=environ,
    )
    assert config.wiki_dir == (vault / "wiki").resolve()


def flag_overrides_provider_s19_D2(tmp_path: Path) -> None:
    """D2 — --provider flag overrides LLM_WIKI_PROVIDER env."""
    vault = _make_obsidian_vault(tmp_path / "vault")
    environ = _clean_environ()
    environ["LLM_WIKI_PROVIDER"] = "openai"
    config = build_cli_configuration(
        flags=CLIFlags(vault=str(vault), provider="ollama"),
        environ=environ,
    )
    assert config.provider_override == "ollama"


def batch_flag_sets_mode_D3(tmp_path: Path) -> None:
    """D3 — --batch sets batch_mode True."""
    vault = _make_obsidian_vault(tmp_path / "vault")
    config = build_cli_configuration(
        flags=CLIFlags(vault=str(vault), batch=True),
        environ=_clean_environ(),
    )
    assert config.batch_mode is True


def real_walkup_binding_Y1(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Y1 — walk-up uses real filesystem markers, not mocked Path.exists."""
    vault = _make_obsidian_vault(tmp_path / "real-vault")
    nested = vault / "projects" / "app"
    nested.mkdir(parents=True)
    monkeypatch.chdir(nested)
    config = build_cli_configuration(environ=_clean_environ(), start_path=nested)
    assert config.vault_root.is_dir()
    assert (config.vault_root / ".obsidian").is_dir()


def override_rule_binding_s19_Y2(tmp_path: Path) -> None:
    """Y2 — binding: CLI flags override env for wiki dir and provider."""
    vault = _make_obsidian_vault(tmp_path / "vault")
    environ = _clean_environ()
    environ["LLM_WIKI_DIR"] = "env-wiki"
    environ["LLM_WIKI_PROVIDER"] = "anthropic"
    config = build_cli_configuration(
        flags=CLIFlags(vault=str(vault), wiki_dir="flag-wiki", provider="openai"),
        environ=environ,
    )
    assert config.wiki_dir == (vault / "flag-wiki").resolve()
    assert config.provider_override == "openai"
