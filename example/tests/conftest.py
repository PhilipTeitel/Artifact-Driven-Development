"""Shared pytest fixtures for llm-wiki tests."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

pytest_plugins = ["integration.llm.conftest"]

REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return REPO_ROOT


@pytest.fixture(scope="session")
def llm_wiki_help(repo_root: Path) -> str:
    """Invoke llm-wiki --help via the Typer app module."""
    result = subprocess.run(
        [sys.executable, "-m", "llm_wiki.adapters.cli.main", "--help"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout
