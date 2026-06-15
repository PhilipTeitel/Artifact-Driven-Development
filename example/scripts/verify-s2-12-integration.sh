#!/usr/bin/env bash
# verify-s2-12-integration.sh — binding checks for S2-12 port contracts and CLI E2E
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TRACE_DOC="${ROOT}/docs/features/S2-12-scenario-traceability.md"
FAILURES=0

pass() { echo "PASS: $1"; }
fail() { echo "FAIL: $1"; FAILURES=$((FAILURES + 1)); }

five_ports_contract_A2() {
  local ports=(
    test_storage_port_contract.py
    test_schema_port_contract.py
    test_configuration_port_contract.py
    test_llm_port_contract.py
    test_interaction_port_contract.py
  )
  for port in "${ports[@]}"; do
    if [[ -f "${ROOT}/tests/contract/${port}" ]] \
      && grep -q 'core_contract_A1' "${ROOT}/tests/contract/${port}"; then
      pass "five_ports_contract_${port}"
    else
      fail "five_ports_contract_${port}"
    fi
  done
  if [[ -f "${ROOT}/tests/contract/conftest.py" ]] \
    && grep -q 'storage_adapter_impl' "${ROOT}/tests/contract/conftest.py" \
    && grep -q 'schema_adapter_impl' "${ROOT}/tests/contract/conftest.py" \
    && grep -q 'configuration_adapter_impl' "${ROOT}/tests/contract/conftest.py" \
    && grep -q 'llm_adapter_impl' "${ROOT}/tests/contract/conftest.py" \
    && grep -q 'interaction_adapter_impl' "${ROOT}/tests/contract/conftest.py"; then
    pass "five_ports_contract_conftest"
  else
    fail "five_ports_contract_conftest"
  fi
}

traceability_doc_E1() {
  if [[ ! -f "$TRACE_DOC" ]]; then
    fail "traceability_doc_exists_E1"
    return 0
  fi
  pass "traceability_doc_exists_E1"
  for sn in S1 S2 S3 S4 S5 S6 S7 S8 S9 S10 S11 S12 S13 S16 S19; do
    if grep -q "| ${sn} |" "$TRACE_DOC"; then
      pass "traceability_sn_${sn}_E1"
    else
      fail "traceability_sn_${sn}_E1"
    fi
  done
}

import_boundary_smoke() {
  if python3 -m pytest "${ROOT}/tests/unit/test_import_boundaries.py::domain_ports_no_adapters_F1" -q >/dev/null 2>&1; then
    pass "import_boundary_F1"
  else
    fail "import_boundary_F1"
  fi
}

contract_parametrize_smoke() {
  if python3 -m pytest "${ROOT}/tests/contract/conftest.py::parametrize_adapters_A1" -q >/dev/null 2>&1; then
    pass "contract_parametrize_A1"
  else
    fail "contract_parametrize_A1"
  fi
}

cli_e2e_smoke() {
  if python3 -m pytest "${ROOT}/tests/integration/test_cli_e2e.py" -q >/dev/null 2>&1; then
    pass "cli_e2e_pytest"
  else
    fail "cli_e2e_pytest"
  fi
}

five_ports_contract_A2
traceability_doc_E1
import_boundary_smoke
contract_parametrize_smoke
cli_e2e_smoke

if [[ $FAILURES -gt 0 ]]; then
  echo "verify-s2-12-integration: $FAILURES failure(s)"
  exit 1
fi

echo "verify-s2-12-integration: all checks passed"
exit 0
