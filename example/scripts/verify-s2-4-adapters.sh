#!/usr/bin/env bash
# verify-s2-4-adapters.sh — binding checks for S2-4 filesystem/schema adapters
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STORAGE="${ROOT}/src/llm_wiki/adapters/storage/filesystem.py"
SCHEMA="${ROOT}/src/llm_wiki/adapters/schema/markdown.py"
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
  require_file "$STORAGE" "filesystem_adapter_module_Y1"
  require_file "$SCHEMA" "markdown_schema_adapter_module_Y1"
  grep_file "$STORAGE" 'class FilesystemWikiStorageAdapter' 'filesystem_adapter_class'
  grep_file "$SCHEMA" 'class MarkdownSchemaAdapter' 'markdown_schema_adapter_class'
  grep_file "$STORAGE" 'def ensure_wiki_layout' 'filesystem_ensure_wiki_layout'
  grep_file "$SCHEMA" 'def load' 'markdown_schema_load'
}

adapter_modules_exist

# Writes must stay inside wiki_dir — no direct vault-root writes in adapter methods
if grep -E 'vault_root.*write|write_text\(.*vault_root' "$STORAGE" >/dev/null 2>&1; then
  fail "no_vault_root_writes_Y4"
else
  pass "no_vault_root_writes_Y4"
fi

grep_file "$STORAGE" '_wiki_path' 'wiki_path_guard_Y4'
grep_file "$STORAGE" 'WikiStorageBoundaryError' 'boundary_error_Y4'
grep_file "$STORAGE" '\.ingested\.json' 'ingested_sidecar_Y5'
grep_file "$SCHEMA" 'default_excludes' 'schema_default_excludes_Y6'
grep_file "$SCHEMA" 'parse_excludes_from_schema' 'schema_excludes_parser_Y6'

if [[ $FAILURES -gt 0 ]]; then
  echo "verify-s2-4-adapters: $FAILURES failure(s)"
  exit 1
fi

echo "verify-s2-4-adapters: all checks passed (adapter_modules_exist)"
exit 0
