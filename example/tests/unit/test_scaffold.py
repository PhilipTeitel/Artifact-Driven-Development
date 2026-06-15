"""Smoke tests for S2-1 Python package scaffold."""

from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path

from typer.testing import CliRunner

import llm_wiki
import llm_wiki.adapters.cli.main

REPO_ROOT = Path(__file__).resolve().parents[2]
CLI_MAIN = REPO_ROOT / "src" / "llm_wiki" / "adapters" / "cli" / "main.py"
runner = CliRunner()


def test_editable_install_imports_A2() -> None:
    """Editable install exposes the llm_wiki package."""
    assert llm_wiki.__version__ == "0.1.0"
    assert hasattr(llm_wiki.adapters.cli.main, "app")


def test_help_lists_subcommands_C2() -> None:
    """Typer help lists all stub subcommands."""
    result = runner.invoke(llm_wiki.adapters.cli.main.app, ["--help"])
    assert result.exit_code == 0, result.stdout
    help_text = result.stdout.lower()
    for name in ("init", "validate", "ingest", "query", "lint"):
        assert name in help_text, f"missing subcommand {name!r} in help"


def test_stub_handlers_no_domain_imports_C3() -> None:
    """Stub CLI module does not import domain use cases or concrete adapters."""
    source = CLI_MAIN.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported_modules: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_modules.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_modules.append(node.module)

    forbidden_prefixes = (
        "llm_wiki.domain",
        "llm_wiki.adapters.llm",
        "llm_wiki.adapters.storage",
        "llm_wiki.adapters.schema",
        "llm_wiki.adapters.interaction",
    )
    for module in imported_modules:
        for prefix in forbidden_prefixes:
            assert not module.startswith(prefix), f"unexpected import: {module}"


def test_pytest_runs_D1() -> None:
    """Pytest discovers this module (harness smoke)."""
    assert Path(__file__).name == "test_scaffold.py"


def test_ruff_clean_D2() -> None:
    """Ruff passes on src/ and tests/."""
    result = subprocess.run(
        [sys.executable, "-m", "ruff", "check", "src", "tests"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
