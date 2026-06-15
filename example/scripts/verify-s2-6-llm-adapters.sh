#!/usr/bin/env bash
# verify-s2-6-llm-adapters.sh — binding checks for S2-6 LLM port adapters
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYPROJECT="${ROOT}/pyproject.toml"
OLLAMA="${ROOT}/src/llm_wiki/adapters/llm/ollama.py"
OPENAI="${ROOT}/src/llm_wiki/adapters/llm/openai.py"
ANTHROPIC="${ROOT}/src/llm_wiki/adapters/llm/anthropic.py"
FACTORY="${ROOT}/src/llm_wiki/adapters/llm/factory.py"
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

for dep in httpx openai anthropic; do
  grep_file "$PYPROJECT" "\"${dep}\"" "pyproject_dep_${dep}"
done

grep_file "$OLLAMA" 'import httpx' 'ollama_uses_httpx'
grep_file "$OPENAI" 'from openai import OpenAI' 'openai_sdk_import_Y2'
grep_file "$ANTHROPIC" 'from anthropic import Anthropic' 'anthropic_sdk_import_Y3'
grep_file "$FACTORY" 'def select_llm_provider' 'factory_select_llm_provider'

if grep -E 'import openai|from openai' "$OLLAMA" >/dev/null 2>&1; then
  fail "ollama_no_openai_import"
else
  pass "ollama_no_openai_import"
fi

if grep -E 'logger\.(debug|info|warning|error).*(prompt|api_key|API_KEY|secret)' \
  "$OLLAMA" "$OPENAI" "$ANTHROPIC" >/dev/null 2>&1; then
  fail "no_prompt_or_key_logging"
else
  pass "no_prompt_or_key_logging"
fi

if [[ $FAILURES -gt 0 ]]; then
  echo "verify-s2-6-llm-adapters: $FAILURES failure(s)"
  exit 1
fi

echo "verify-s2-6-llm-adapters: all checks passed"
exit 0
