"""Contract tests for ConfigurationPort."""

from __future__ import annotations

import inspect
from pathlib import Path

from llm_wiki.ports.configuration import ConfigurationPort

from .conftest import _cli_configuration_adapter
from .fakes import InMemoryConfigurationFake

ADR_PROPERTIES = (
    "vault_root",
    "wiki_dir",
    "batch_mode",
    "provider_override",
    "ollama_base_url",
    "ollama_model",
    "openai_api_key",
    "openai_model",
    "anthropic_api_key",
    "anthropic_model",
)


def _run_configuration_core_contract(adapter: ConfigurationPort) -> None:
    """Shared behavioral suite for fake and CLI adapters."""
    assert isinstance(adapter, ConfigurationPort)
    assert adapter.batch_mode is True
    assert adapter.provider_override == "ollama"
    assert adapter.ollama_base_url == "http://localhost:11434"
    assert adapter.ollama_model == "llama3.2"
    assert adapter.openai_model == "gpt-4o-mini"
    assert adapter.anthropic_model == "claude-3-5-sonnet-20241022"


def configuration_properties_A1() -> None:
    """ConfigurationPort defines all ADR-002 properties."""
    for name in ADR_PROPERTIES:
        assert name in ConfigurationPort.__annotations__ or hasattr(ConfigurationPort, name)


def configuration_core_contract_A1(configuration_adapter_impl: ConfigurationPort) -> None:
    """A1 — core configuration contract runs against parametrized fake and CLI adapters."""
    _run_configuration_core_contract(configuration_adapter_impl)
    if isinstance(configuration_adapter_impl, InMemoryConfigurationFake):
        assert configuration_adapter_impl.vault_root == Path("/vault")
        assert configuration_adapter_impl.wiki_dir == Path("/vault/wiki")
    else:
        assert configuration_adapter_impl.vault_root.is_dir()
        assert configuration_adapter_impl.wiki_dir == (
            configuration_adapter_impl.vault_root / "wiki"
        ).resolve()


def configuration_contract_Y2() -> None:
    """Reference fake satisfies ConfigurationPort contract."""
    fake = InMemoryConfigurationFake(
        vault_root=Path("/vault"),
        wiki_dir=Path("/vault/wiki"),
        batch_mode=True,
        provider_override="ollama",
    )
    assert isinstance(fake, ConfigurationPort)
    assert fake.vault_root == Path("/vault")
    assert fake.wiki_dir == Path("/vault/wiki")
    assert fake.batch_mode is True
    assert fake.provider_override == "ollama"
    assert fake.ollama_base_url == "http://localhost:11434"
    assert fake.ollama_model == "llama3.2"
    assert fake.openai_model == "gpt-4o-mini"
    assert fake.anthropic_model == "claude-3-5-sonnet-20241022"

    port_source = inspect.getsource(ConfigurationPort)
    assert "os.environ" not in port_source
    assert "import os" not in port_source


def cli_adapter_passes_contract_E1(tmp_path: Path) -> None:
    """E1 — CLIConfigurationAdapter satisfies ConfigurationPort contract."""
    adapter = _cli_configuration_adapter(tmp_path)
    _run_configuration_core_contract(adapter)
    assert adapter.vault_root == (tmp_path / "vault").resolve()
    assert adapter.wiki_dir == (tmp_path / "vault" / "wiki").resolve()


def cli_adapter_passes_contract_Y4(tmp_path: Path) -> None:
    """Y4 — binding: configuration contract passes against CLI adapter."""
    cli_adapter_passes_contract_E1(tmp_path)
