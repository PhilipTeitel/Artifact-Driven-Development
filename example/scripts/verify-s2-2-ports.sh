#!/usr/bin/env bash
# verify-s2-2-ports.sh — binding checks for S2-2 port protocols and domain models
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PORTS="${ROOT}/src/llm_wiki/ports"
MODELS="${ROOT}/src/llm_wiki/domain/models"
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

PORT_MODULES=(
  configuration.py
  llm.py
  storage.py
  schema.py
  interaction.py
)

for mod in "${PORT_MODULES[@]}"; do
  require_file "${PORTS}/${mod}" "port_module_Y1_${mod%.py}"
done

require_file "${PORTS}/__init__.py" "ports_init_Y1"
require_file "${MODELS}/init_result.py" "model_init_result_Y1"
require_file "${MODELS}/validation.py" "model_validation_Y1"
require_file "${MODELS}/wiki_schema.py" "model_wiki_schema_Y1"

# ADR-002 method and property names
grep_file "${PORTS}/configuration.py" 'vault_root' 'configuration_property_vault_root'
grep_file "${PORTS}/configuration.py" 'wiki_dir' 'configuration_property_wiki_dir'
grep_file "${PORTS}/configuration.py" 'batch_mode' 'configuration_property_batch_mode'
grep_file "${PORTS}/configuration.py" 'provider_override' 'configuration_property_provider_override'
grep_file "${PORTS}/configuration.py" 'ollama_base_url' 'configuration_property_ollama_base_url'
grep_file "${PORTS}/configuration.py" 'ollama_model' 'configuration_property_ollama_model'
grep_file "${PORTS}/configuration.py" 'openai_api_key' 'configuration_property_openai_api_key'
grep_file "${PORTS}/configuration.py" 'openai_model' 'configuration_property_openai_model'
grep_file "${PORTS}/configuration.py" 'anthropic_api_key' 'configuration_property_anthropic_api_key'
grep_file "${PORTS}/configuration.py" 'anthropic_model' 'configuration_property_anthropic_model'

grep_file "${PORTS}/llm.py" 'def complete' 'llm_method_complete'
grep_file "${PORTS}/llm.py" 'def is_available' 'llm_method_is_available'

for method in read_source list_sources read_wiki_page write_wiki_page read_index write_index \
  append_log read_ingested write_ingested wiki_exists ensure_wiki_layout; do
  grep_file "${PORTS}/storage.py" "def ${method}" "storage_method_${method}"
done

grep_file "${PORTS}/schema.py" 'def load' 'schema_method_load'
grep_file "${PORTS}/schema.py" 'def default_excludes' 'schema_method_default_excludes'

for method in confirm present prompt; do
  grep_file "${PORTS}/interaction.py" "def ${method}" "interaction_method_${method}"
done

grep_file "${MODELS}/init_result.py" 'class InitResult' 'domain_model_InitResult'
grep_file "${MODELS}/validation.py" 'class ValidationIssue' 'domain_model_ValidationIssue'
grep_file "${MODELS}/validation.py" 'class ValidationResult' 'domain_model_ValidationResult'
grep_file "${MODELS}/wiki_schema.py" 'class WikiSchema' 'domain_model_WikiSchema'
grep_file "${MODELS}/wiki_schema.py" 'class IngestedSidecar' 'domain_model_IngestedSidecar'

if [[ $FAILURES -gt 0 ]]; then
  echo "verify-s2-2-ports: $FAILURES failure(s)"
  exit 1
fi

echo "verify-s2-2-ports: all checks passed (port_modules_Y1)"
exit 0
