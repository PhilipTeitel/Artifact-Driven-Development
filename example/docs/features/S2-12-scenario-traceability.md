# S2-12 Scenario traceability — Stage 2 REQ-001 evidence

Maps in-scope Gherkin scenarios from [REQ-001](REQ-001-llm-wiki-cli.md) to executable Stage 2 test and verify-script evidence.

**Story:** [S2-12-port-contract-and-cli-integration-tests.md](S2-12-port-contract-and-cli-integration-tests.md)

## In-scope scenarios

| Sn | Scenario summary | Evidence | Notes |
|----|------------------|----------|-------|
| S1 | Init creates wiki layout | `tests/integration/test_cli_e2e.py::full_pipeline_s18_stage2_B1` | ADR-003 artifacts |
| S2 | Init is idempotent | `tests/integration/test_cli_commands.py::init_idempotent_s2_D2` | S2-11 smoke |
| S3 | Vault walk-up / explicit path | `tests/integration/test_cli_e2e.py::explicit_vault_flag_s19_D1` | `--vault` flag |
| S4 | SCHEMA excludes defaults | `tests/contract/test_schema_port_contract.py::schema_core_contract_A1` | parametrized |
| S5 | Source immutability | `tests/integration/test_cli_e2e.py::sources_unchanged_s5_C1` | SHA256 manifest |
| S6 | Interactive ingest confirm | `tests/contract/test_interaction_port_contract.py::interaction_core_contract_A1` | terminal adapter |
| S7 | Batch ingest directory | `tests/integration/test_cli_e2e.py::full_pipeline_s18_stage2_B1` | `ingest --batch` |
| S8 | Query presents answer | `tests/integration/test_cli_e2e.py::full_pipeline_s18_stage2_B1` | decline filing (`n`) |
| S9 | Lint report-only | `tests/integration/test_cli_e2e.py::full_pipeline_s18_stage2_B1` | lint in pipeline |
| S10 | Validate vault structure | `tests/integration/test_cli_e2e.py::full_pipeline_s18_stage2_B1` | final `validate` |
| S11 | LLM provider selection | `tests/contract/test_llm_port_contract.py::llm_core_contract_A1` | hermetic Ollama |
| S12 | `.ingested.json` sidecar | `tests/integration/test_cli_e2e.py::ingested_sidecar_s12_B3` | ≥1 source key |
| S13 | Log operation headings | `tests/integration/test_cli_e2e.py::log_operations_s13_B2` | init/ingest/query/lint |
| S16 | Hexagonal import boundaries | `tests/unit/test_import_boundaries.py::domain_ports_no_adapters_F1` | domain + ports |
| S19 | Configuration via adapter | `tests/contract/test_configuration_port_contract.py::configuration_core_contract_A1` | CLI adapter |

## Binding verify script

| Check | Script function | Covers |
|-------|-----------------|--------|
| Five port contract parametrization | `scripts/verify-s2-12-integration.sh::five_ports_contract_A2` | A2 |
| Traceability doc rows | `scripts/verify-s2-12-integration.sh::traceability_doc_E1` | E1, S15 |
| Offline CI gate | `bash scripts/verify-s2-12-integration.sh` | Y3, Y7 |

## Out of scope (documented)

| Sn | Reason |
|----|--------|
| S14 | Stage 1 Cursor commands — [S1-6](S1-6-stage1-e2e-acceptance.md) |
| S17 | Future Obsidian plugin |
| S18 | Stage 1 daily-driver gate — Stage 2 E2E is parallel evidence |
