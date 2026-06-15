#!/usr/bin/env bash
# verify-s2-5-configuration.sh — binding checks for S2-5 CLI configuration adapter
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG="${ROOT}/src/llm_wiki/adapters/cli/configuration.py"
VAULT_WALK="${ROOT}/src/llm_wiki/adapters/cli/vault_walk.py"
ERRORS="${ROOT}/src/llm_wiki/adapters/cli/errors.py"
FAILURES=0

pass() { echo "PASS: $1"; }
fail() { echo "FAIL: $1"; FAILURES=$((FAILURES + 1)); }

require_file() {
  local path="$1"
  local check="$2"
  if [[ -f "$path" ]]; then
    pass "$check"
    return 0
  fi
  fail "$check"
  return 1
}

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

adapter_modules_exist() {
  require_file "$CONFIG" "configuration_adapter_module_Y1"
  require_file "$VAULT_WALK" "vault_walk_module_Y1"
  require_file "$ERRORS" "configuration_errors_module"
  grep_file "$CONFIG" 'class CLIConfigurationAdapter' 'cli_configuration_adapter_class'
  grep_file "$CONFIG" 'def build_cli_configuration' 'build_cli_configuration_factory'
  grep_file "$VAULT_WALK" 'def walk_up_to_vault' 'walk_up_to_vault_function'
  grep_file "$ERRORS" 'class VaultNotFoundError' 'vault_not_found_error'
}

adapter_modules_exist

env_names_match_adr004_Y3() {
  local vars=(
    LLM_WIKI_DIR
    LLM_WIKI_PROVIDER
    OLLAMA_BASE_URL
    OLLAMA_MODEL
    OPENAI_API_KEY
    OPENAI_MODEL
    ANTHROPIC_API_KEY
    ANTHROPIC_MODEL
  )
  for var in "${vars[@]}"; do
    grep_file "$CONFIG" "$var" "env_var_${var}"
  done
}

env_names_match_adr004_Y3

grep_file "$CONFIG" '@dataclass\(frozen=True\)' 'immutable_configuration_adapter'
grep_file "$VAULT_WALK" '\.obsidian' 'obsidian_marker_check'
grep_file "$VAULT_WALK" 'SCHEMA\.md' 'schema_marker_check'

if grep -E 'logger\.(debug|info|warning|error).*(api_key|API_KEY|secret)' "$CONFIG" >/dev/null 2>&1; then
  fail "no_api_key_logging_Y8"
else
  pass "no_api_key_logging_Y8"
fi

if [[ $FAILURES -gt 0 ]]; then
  echo "verify-s2-5-configuration: $FAILURES failure(s)"
  exit 1
fi

echo "verify-s2-5-configuration: all checks passed (adapter_modules_exist, env_names_match_adr004_Y3)"
exit 0
