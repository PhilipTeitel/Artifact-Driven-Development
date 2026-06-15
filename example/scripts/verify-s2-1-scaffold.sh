#!/usr/bin/env bash
# verify-s2-1-scaffold.sh — binding checks for S2-1 Python package scaffold
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYPROJECT="${ROOT}/pyproject.toml"
SRC="${ROOT}/src/llm_wiki"
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

require_dir_init() {
  local dir="$1"
  local check="$2"
  if [[ -d "$dir" && -f "${dir}/__init__.py" ]]; then
    pass "$check"
    return 0
  fi
  fail "$check"
  return 1
}

grep_pyproject() {
  local pattern="$1"
  local check="$2"
  if grep -qE "$pattern" "$PYPROJECT"; then
    pass "$check"
    return 0
  fi
  fail "$check"
  return 1
}

# A1 / Y1 — pyproject metadata
if require_file "$PYPROJECT" "pyproject_exists"; then
  grep_pyproject '^name = "llm-wiki"' 'pyproject_metadata_A1_name'
  grep_pyproject 'requires-python = ">=3\.11"' 'pyproject_metadata_A1_python'
  grep_pyproject 'build-backend = "hatchling\.build"' 'pyproject_metadata_A1_hatchling'
  grep_pyproject 'hatchling' 'package_metadata_Y1_hatchling'
  grep_pyproject 'requires-python = ">=3\.11"' 'package_metadata_Y1_python'
fi

# B1 / Y3 — hexagonal layout
HEX_DIRS=(
  "domain/models"
  "domain/use_cases"
  "ports"
  "adapters/cli"
  "adapters/llm"
  "adapters/storage"
  "adapters/schema"
  "adapters/interaction"
)
for rel in "${HEX_DIRS[@]}"; do
  require_dir_init "${SRC}/${rel}" "hexagonal_layout_B1_${rel//\//_}"
done

# B2 / Y3 — test layout
for rel in unit contract integration; do
  if [[ -d "${ROOT}/tests/${rel}" ]]; then
    pass "test_layout_B2_${rel}"
  else
    fail "test_layout_B2_${rel}"
  fi
done
require_file "${ROOT}/tests/conftest.py" "test_layout_B2_conftest"

# C1 / Y2 — console script entry point
grep_pyproject 'llm-wiki = "llm_wiki\.adapters\.cli\.main:app"' 'console_script_C1'
grep_pyproject 'llm-wiki = "llm_wiki\.adapters\.cli\.main:app"' 'entry_point_Y2'

# Y4 — runtime dependencies
for dep in 'typer' 'httpx' 'openai' 'anthropic' 'rich'; do
  if grep -qi "$dep" "$PYPROJECT"; then
    pass "runtime_deps_Y4_${dep}"
  else
    fail "runtime_deps_Y4_${dep}"
  fi
done

# Y3 — directory tree completeness
require_file "${SRC}/__init__.py" "directory_tree_Y3_package_init"
require_file "${SRC}/adapters/cli/main.py" "directory_tree_Y3_cli_main"

if [[ $FAILURES -gt 0 ]]; then
  echo "verify-s2-1-scaffold: $FAILURES failure(s)"
  exit 1
fi

echo "verify-s2-1-scaffold: all checks passed"
exit 0
