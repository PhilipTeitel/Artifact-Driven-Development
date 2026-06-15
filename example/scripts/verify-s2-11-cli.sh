#!/usr/bin/env bash
# verify-s2-11-cli.sh — binding checks for S2-11 Typer composition root
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MAIN="${ROOT}/src/llm_wiki/adapters/cli/main.py"
WIRING="${ROOT}/src/llm_wiki/adapters/cli/wiring.py"
FAILURES=0

pass() { echo "PASS: $1"; }
fail() { echo "FAIL: $1"; FAILURES=$((FAILURES + 1)); }

grep_file() {
  local path="$1"
  local pattern="$2"
  local check="$3"
  if grep -qE "$pattern" "$path"; then
    pass "$check"
    return 0
  fi
  fail "$check"
  return 1
}

handlers_delegate_to_use_cases_A1() {
  for use_case in InitUseCase ValidateUseCase IngestUseCase QueryUseCase LintUseCase; do
    grep_file "$MAIN" "$use_case" "imports_${use_case}"
  done
  grep_file "$MAIN" '\.execute\(' 'handlers_call_execute'
}

no_stub_message_A2() {
  if grep -q '_STUB_MESSAGE' "$MAIN"; then
    fail "no_stub_message_A2"
  else
    pass "no_stub_message_A2"
  fi
}

single_wiring_point_A3() {
  grep_file "$WIRING" 'def build_context' 'build_context_in_wiring'
  grep_file "$MAIN" 'build_context' 'main_uses_build_context'
  if grep -qE 'FilesystemWikiStorageAdapter|select_llm_provider' "$MAIN"; then
    fail "adapters_not_in_main_A3"
  else
    pass "adapters_not_in_main_A3"
  fi
}

config_via_adapter_s19_Y1() {
  if grep -qE 'os\.environ' "$MAIN" && ! grep -qE 'LLM_WIKI_LOG' "$MAIN"; then
    fail "no_os_environ_in_handlers_Y1"
  elif grep -qE 'os\.environ\.get\("LLM_WIKI_LOG"' "$MAIN"; then
    pass "logging_env_only_Y1"
  else
    pass "no_os_environ_in_handlers_Y1"
  fi
  grep_file "$MAIN" 'build_context' 'config_via_build_context_Y1'
}

uses_provider_factory_s11_Y3() {
  grep_file "$WIRING" 'select_llm_provider' 'wiring_calls_select_llm_provider_Y3'
}

handlers_delegate_to_use_cases_A1
no_stub_message_A2
single_wiring_point_A3
config_via_adapter_s19_Y1
uses_provider_factory_s11_Y3

if [[ $FAILURES -gt 0 ]]; then
  echo "verify-s2-11-cli: $FAILURES failure(s)"
  exit 1
fi

echo "verify-s2-11-cli: all checks passed"
exit 0
