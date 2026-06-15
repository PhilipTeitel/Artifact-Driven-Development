"""CLI integration tests via Typer CliRunner (S2-11)."""

from __future__ import annotations

import json
import os
import shutil
from pathlib import Path

import pytest
from typer.testing import CliRunner

from contract.fakes import InMemoryLLMFake
from integration.conftest import REPO_ROOT, TEMPLATES_DIR
from integration.fake_llm import canned_cli_llm
from llm_wiki.adapters.cli.main import app
from llm_wiki.adapters.storage.filesystem import INGESTED_FILENAME

runner = CliRunner()
VAULT_SEED = REPO_ROOT / "tests" / "fixtures" / "vault"


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


def _copy_vault(tmp_path: Path) -> Path:
    vault_root = tmp_path / "vault"
    shutil.copytree(VAULT_SEED, vault_root)
    return vault_root


def _vault_cli(vault: Path, *parts: str) -> list[str]:
    return ["--vault", str(vault), *parts]


def _invoke(
    args: list[str],
    *,
    input: str | None = None,
    environ: dict[str, str] | None = None,
    llm: InMemoryLLMFake | None = None,
    monkeypatch: pytest.MonkeyPatch | None = None,
) -> object:
    env = environ if environ is not None else _clean_environ()
    if llm is not None:
        assert monkeypatch is not None
        monkeypatch.setattr(
            "llm_wiki.adapters.cli.wiring.select_llm_provider",
            lambda _config: llm,
        )
    kwargs: dict = {"env": env}
    if input is not None:
        kwargs["input"] = input
    return runner.invoke(app, args, **kwargs)


def _fake_llm() -> InMemoryLLMFake:
    return canned_cli_llm()


def _init_vault(
    vault: Path,
    *,
    monkeypatch: pytest.MonkeyPatch | None = None,
    llm: InMemoryLLMFake | None = None,
) -> None:
    result = _invoke(_vault_cli(vault, "init"), monkeypatch=monkeypatch, llm=llm)
    assert result.exit_code == 0, result.output


def invalid_vault_exits_s3_B1(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """B1 — subcommand outside vault without --vault exits non-zero with guidance."""
    orphan = tmp_path / "nowhere" / "deep"
    orphan.mkdir(parents=True)
    monkeypatch.chdir(orphan)
    result = _invoke(["validate"])
    assert result.exit_code == 1
    assert "--vault" in result.output.lower() or "--vault" in result.output


def no_partial_wiki_s3_B2(tmp_path: Path) -> None:
    """B2 — invalid vault attempt does not create wiki artifacts."""
    invalid = tmp_path / "not-a-vault"
    invalid.mkdir()
    before = {p for p in tmp_path.rglob("*")}
    result = _invoke(_vault_cli(invalid, "init"))
    assert result.exit_code == 1
    after = {p for p in tmp_path.rglob("*")}
    assert before == after
    assert not (invalid / "wiki").exists()


def validate_success_s10_C1(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """C1 — validate on initialized hermetic vault exits 0."""
    vault = _copy_vault(tmp_path)
    _init_vault(vault, monkeypatch=monkeypatch)
    result = _invoke(_vault_cli(vault, "validate"), monkeypatch=monkeypatch)
    assert result.exit_code == 0


def validate_failure_s10_C2(tmp_path: Path) -> None:
    """C2 — validate on vault without wiki exits 1."""
    vault = _copy_vault(tmp_path)
    result = _invoke(_vault_cli(vault, "validate"))
    assert result.exit_code == 1


def init_creates_layout_s1_D1(tmp_path: Path) -> None:
    """D1 — init creates SCHEMA, index, log in temp vault."""
    vault = _copy_vault(tmp_path)
    result = _invoke(_vault_cli(vault, "init"))
    assert result.exit_code == 0
    wiki = vault / "wiki"
    for name in ("SCHEMA.md", "index.md", "log.md"):
        assert (wiki / name).is_file()


def init_idempotent_s2_D2(tmp_path: Path) -> None:
    """D2 — second init is idempotent (exit 0; content unchanged)."""
    vault = _copy_vault(tmp_path)
    _init_vault(vault)
    layout_files = ("SCHEMA.md", "index.md")
    before = {
        name: (vault / "wiki" / name).read_bytes()
        for name in layout_files
    }
    result = _invoke(_vault_cli(vault, "init"))
    assert result.exit_code == 0
    after = {
        name: (vault / "wiki" / name).read_bytes()
        for name in layout_files
    }
    assert before == after


def ingest_batch_smoke_s7_E1(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """E1 — batch ingest writes .ingested.json entry."""
    vault = _copy_vault(tmp_path)
    llm = _fake_llm()
    _init_vault(vault, monkeypatch=monkeypatch, llm=llm)
    result = _invoke(
        _vault_cli(vault, "ingest", "daily/", "--batch"),
        llm=llm,
        monkeypatch=monkeypatch,
    )
    assert result.exit_code == 0
    ingested_path = vault / "wiki" / INGESTED_FILENAME
    assert ingested_path.is_file()
    data = json.loads(ingested_path.read_text(encoding="utf-8"))
    assert "daily/sample.md" in data.get("sources", {})


def query_smoke_s8_E2(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """E2 — query presents answer on stdout."""
    vault = _copy_vault(tmp_path)
    llm = _fake_llm()
    _init_vault(vault, monkeypatch=monkeypatch, llm=llm)
    _invoke(
        _vault_cli(vault, "ingest", "daily/sample.md", "--batch"),
        llm=llm,
        monkeypatch=monkeypatch,
    )
    result = _invoke(
        _vault_cli(vault, "query", "What themes appear?"),
        input="n\n",
        llm=llm,
        monkeypatch=monkeypatch,
    )
    assert result.exit_code == 0
    assert "Themes include" in result.output


def lint_smoke_s9_E3(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """E3 — lint appends log line without modifying wiki pages."""
    vault = _copy_vault(tmp_path)
    llm = _fake_llm()
    _init_vault(vault, monkeypatch=monkeypatch, llm=llm)
    _invoke(
        _vault_cli(vault, "ingest", "daily/sample.md", "--batch"),
        llm=llm,
        monkeypatch=monkeypatch,
    )
    page_paths = [
        path
        for path in (vault / "wiki").rglob("*.md")
        if path.name not in {INGESTED_FILENAME, "log.md"}
    ]
    before = {path: path.read_text(encoding="utf-8") for path in page_paths}
    result = _invoke(_vault_cli(vault, "lint"), llm=llm, monkeypatch=monkeypatch)
    assert result.exit_code == 0
    after = {path: path.read_text(encoding="utf-8") for path in page_paths}
    assert before == after
    log_content = (vault / "wiki" / "log.md").read_text(encoding="utf-8")
    assert "lint |" in log_content


def no_provider_error_s11_F1(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """F1 — no LLM provider exits 1 with clear error."""
    vault = _copy_vault(tmp_path)
    _init_vault(vault)

    def raise_unavailable(_config):
        from llm_wiki.adapters.llm.errors import ProviderUnavailableError

        raise ProviderUnavailableError("No LLM provider available for test.")

    monkeypatch.setattr(
        "llm_wiki.adapters.cli.wiring.select_llm_provider",
        raise_unavailable,
    )
    result = runner.invoke(
        app,
        _vault_cli(vault, "ingest", "daily/sample.md", "--batch"),
        env=_clean_environ(),
    )
    assert result.exit_code == 1
    assert "provider" in result.output.lower()


def test_init_works_without_provider(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Init does not require an LLM provider (S11 applies only to LLM commands)."""
    vault = _copy_vault(tmp_path)

    def raise_unavailable(_config):
        from llm_wiki.adapters.llm.errors import ProviderUnavailableError

        raise ProviderUnavailableError("No LLM provider available for test.")

    monkeypatch.setattr(
        "llm_wiki.adapters.cli.wiring.select_llm_provider",
        raise_unavailable,
    )
    result = _invoke(_vault_cli(vault, "init"))
    assert result.exit_code == 0


def real_storage_binding_Y2(tmp_path: Path) -> None:
    """Y2 — CLI uses real filesystem storage (templates on disk)."""
    vault = _copy_vault(tmp_path)
    result = _invoke(_vault_cli(vault, "init"))
    assert result.exit_code == 0
    schema_bytes = (vault / "wiki" / "SCHEMA.md").read_bytes()
    template_bytes = (TEMPLATES_DIR / "SCHEMA.md").read_bytes()
    assert schema_bytes == template_bytes
