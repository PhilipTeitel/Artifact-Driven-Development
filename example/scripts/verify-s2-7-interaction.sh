#!/usr/bin/env bash
# verify-s2-7-interaction.sh — binding checks for S2-7 terminal interaction adapter
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TERMINAL="${ROOT}/src/llm_wiki/adapters/interaction/terminal.py"
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

grep_file "$TERMINAL" 'from rich\.console import Console' 'uses_rich_console'
grep_file "$TERMINAL" 'class TerminalUserInteractionAdapter' 'adapter_class_exists'
grep_file "$TERMINAL" 'batch' 'documents_batch_delegation_s7_E1'

if grep -E 'logger\.(info|warning|error).*(input|prompt|confirm)' "$TERMINAL" >/dev/null 2>&1; then
  fail "no_user_input_info_logging"
else
  pass "no_user_input_info_logging"
fi

if [[ $FAILURES -gt 0 ]]; then
  echo "verify-s2-7-interaction: $FAILURES failure(s)"
  exit 1
fi

echo "verify-s2-7-interaction: all checks passed"
exit 0
