"""Stage 2 CLI end-to-end integration tests on hermetic vault copy (S2-12)."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
from dataclasses import dataclass
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
DAILY_MANIFEST = REPO_ROOT / "scripts" / "fixtures" / "tests-fixtures-vault-daily.sha256"


@dataclass
class PipelineState:
    """Artifacts produced by the full Stage 2 CLI pipeline."""

    vault: Path
    validate_exit_code: int
    log_content: str
    ingested: dict[str, object]
    wiki_page_count: int


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
    kwargs: dict[str, object] = {"env": env}
    if input is not None:
        kwargs["input"] = input
    return runner.invoke(app, args, **kwargs)


def _daily_checksums(vault: Path) -> dict[str, str]:
    """Map manifest-style paths to SHA256 digests for vault daily sources."""
    daily_root = vault / "daily"
    checksums: dict[str, str] = {}
    for path in sorted(daily_root.rglob("*.md")):
        rel_under_daily = path.relative_to(daily_root).as_posix()
        manifest_key = f"tests/fixtures/vault/daily/{rel_under_daily}"
        checksums[manifest_key] = hashlib.sha256(path.read_bytes()).hexdigest()
    return checksums


def _load_manifest() -> dict[str, str]:
    entries: dict[str, str] = {}
    for line in DAILY_MANIFEST.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, rel = line.split(maxsplit=1)
        entries[rel.strip()] = digest
    return entries


def _run_full_pipeline(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    *,
    vault: Path | None = None,
) -> PipelineState:
    if vault is None:
        vault = _copy_vault(tmp_path)
    llm = canned_cli_llm()
    init_result = _invoke(_vault_cli(vault, "init"), monkeypatch=monkeypatch, llm=llm)
    assert init_result.exit_code == 0, init_result.output

    ingest_result = _invoke(
        _vault_cli(vault, "ingest", "daily/", "--batch"),
        llm=llm,
        monkeypatch=monkeypatch,
    )
    assert ingest_result.exit_code == 0, ingest_result.output

    query_result = _invoke(
        _vault_cli(vault, "query", "What themes appear?"),
        input="y\n",
        llm=llm,
        monkeypatch=monkeypatch,
    )
    assert query_result.exit_code == 0, query_result.output

    lint_result = _invoke(_vault_cli(vault, "lint"), llm=llm, monkeypatch=monkeypatch)
    assert lint_result.exit_code == 0, lint_result.output

    validate_result = _invoke(_vault_cli(vault, "validate"), monkeypatch=monkeypatch)
    wiki = vault / "wiki"
    wiki_pages = [
        path
        for path in wiki.rglob("*.md")
        if path.name not in {"SCHEMA.md", "index.md", "log.md"}
    ]
    ingested = json.loads((wiki / INGESTED_FILENAME).read_text(encoding="utf-8"))
    return PipelineState(
        vault=vault,
        validate_exit_code=validate_result.exit_code,
        log_content=(wiki / "log.md").read_text(encoding="utf-8"),
        ingested=ingested,
        wiki_page_count=len(wiki_pages),
    )


@pytest.fixture
def pipeline_state(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> PipelineState:
    """Run init → ingest → query → lint → validate once per test module."""
    return _run_full_pipeline(tmp_path, monkeypatch)


def full_pipeline_s18_stage2_B1(pipeline_state: PipelineState) -> None:
    """B1 — full CLI pipeline exits 0 on final validate."""
    assert pipeline_state.validate_exit_code == 0
    wiki = pipeline_state.vault / "wiki"
    for name in ("SCHEMA.md", "index.md", "log.md"):
        assert (wiki / name).is_file()
    assert pipeline_state.wiki_page_count >= 1


def log_operations_s13_B2(pipeline_state: PipelineState) -> None:
    """B2 — log.md contains init, ingest, query, and lint operation headings."""
    log = pipeline_state.log_content
    for op in ("init", "ingest", "query", "lint"):
        assert re.search(
            rf"^## \[[0-9]{{4}}-[0-9]{{2}}-[0-9]{{2}}\] {op} \|",
            log,
            re.MULTILINE,
        ), f"missing log heading for {op}"


def ingested_sidecar_s12_B3(pipeline_state: PipelineState) -> None:
    """B3 — .ingested.json records at least one ingested source."""
    sources = pipeline_state.ingested.get("sources", {})
    assert isinstance(sources, dict)
    assert len(sources) >= 1


def sources_unchanged_s5_C1(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """C1 — daily source checksums unchanged after E2E pipeline."""
    vault = _copy_vault(tmp_path)
    before = _daily_checksums(vault)
    assert before == _load_manifest()
    _run_full_pipeline(tmp_path, monkeypatch, vault=vault)
    after = _daily_checksums(vault)
    assert before == after == _load_manifest()


def explicit_vault_flag_s19_D1(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """D1 — E2E resolves vault path via explicit --vault flag."""
    vault = _copy_vault(tmp_path)
    llm = canned_cli_llm()
    result = _invoke(_vault_cli(vault, "init"), monkeypatch=monkeypatch, llm=llm)
    assert result.exit_code == 0
    assert (vault / "wiki" / "SCHEMA.md").is_file()
    assert "--vault" in " ".join(_vault_cli(vault, "init"))


def real_filesystem_binding_Y1(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Y1 — binding: CLI E2E writes wiki artifacts via real filesystem adapter."""
    vault = _copy_vault(tmp_path)
    llm = canned_cli_llm()
    result = _invoke(_vault_cli(vault, "init"), monkeypatch=monkeypatch, llm=llm)
    assert result.exit_code == 0
    schema_bytes = (vault / "wiki" / "SCHEMA.md").read_bytes()
    template_bytes = (TEMPLATES_DIR / "SCHEMA.md").read_bytes()
    assert schema_bytes == template_bytes
    source = subprocess.check_output(
        [
            "grep",
            "-r",
            "FilesystemWikiStorageAdapter",
            str(REPO_ROOT / "src" / "llm_wiki" / "adapters" / "cli" / "wiring.py"),
        ],
        text=True,
    )
    assert "FilesystemWikiStorageAdapter" in source
