#!/usr/bin/env bash
# verify-wiki-schema-template.sh — binding checks for templates/wiki/SCHEMA.md (story S1-1)
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCHEMA="${ROOT}/templates/wiki/SCHEMA.md"
FAILURES=0

pass() { echo "PASS: $1"; }
fail() { echo "FAIL: $1"; FAILURES=$((FAILURES + 1)); }

require_file() {
  if [[ -f "$SCHEMA" && -s "$SCHEMA" ]]; then
    pass "$1"
    return 0
  fi
  fail "$1"
  return 1
}

require_heading() {
  local name="$1"
  local check="$2"
  if grep -qiE "^##[[:space:]]+${name}[[:space:]]*$" "$SCHEMA"; then
    pass "$check"
    return 0
  fi
  fail "$check"
  return 1
}

# A1_file_exists
require_file "A1_file_exists" || exit 1

# B1_layers_s4
require_heading "Layers" "B1_layers_heading"
if grep -qi "read-only" "$SCHEMA" \
  && grep -qiE "LLM-owned|LLM owned" "$SCHEMA" \
  && grep -qi "configuration" "$SCHEMA"; then
  pass "B1_layers_s4"
else
  fail "B1_layers_s4"
fi

# B2_workflows_s4
require_heading "Workflows" "B2_workflows_heading"
if grep -qiE "###[[:space:]]+Ingest" "$SCHEMA" \
  && grep -qiE "###[[:space:]]+Query" "$SCHEMA" \
  && grep -qiE "###[[:space:]]+Lint" "$SCHEMA"; then
  pass "B2_workflows_s4"
else
  fail "B2_workflows_s4"
fi

# B3_excludes_s4
require_heading "Excludes" "B3_excludes_heading"
if grep -qF '.obsidian/' "$SCHEMA" && grep -qF 'wiki/' "$SCHEMA" && grep -qF '.*' "$SCHEMA"; then
  pass "B3_excludes_s4"
else
  fail "B3_excludes_s4"
fi

# B4_index_log_s4
require_heading "Index and log" "B4_index_log_heading"
if grep -qi "index\.md" "$SCHEMA" && grep -qi "log\.md" "$SCHEMA" \
  && grep -qiE "append-only|append only" "$SCHEMA"; then
  pass "B4_index_log_s4"
else
  fail "B4_index_log_s4"
fi

# C1_log_format_s13
if grep -qF '## [YYYY-MM-DD] {operation} | {title}' "$SCHEMA"; then
  pass "C1_log_format_s13"
else
  fail "C1_log_format_s13"
fi
if grep -qiE '\`init\`' "$SCHEMA" && grep -qiE '\`ingest\`' "$SCHEMA" \
  && grep -qiE '\`query\`' "$SCHEMA" && grep -qiE '\`lint\`' "$SCHEMA"; then
  pass "C1_operations_listed"
else
  fail "C1_operations_listed"
fi
if grep -qE '^## \[[0-9]{4}-[0-9]{2}-[0-9]{2}\] (init|ingest|query|lint) \|' "$SCHEMA"; then
  pass "C1_example_line"
else
  fail "C1_example_line"
fi

# D1_markdown_links
require_heading "Conventions" "D1_conventions_heading"
if grep -qiE 'standard markdown links|\[text\]\(path\)' "$SCHEMA"; then
  pass "D1_markdown_links"
else
  fail "D1_markdown_links"
fi
if grep -qi 'wikilink' "$SCHEMA" && grep -qiE 'do not|must not|never' "$SCHEMA"; then
  pass "D1_no_wikilinks"
else
  fail "D1_no_wikilinks"
fi

# Y2_single_template_path
OTHER_SCHEMAS="$(find "$ROOT" -name 'SCHEMA.md' ! -path "$SCHEMA" ! -path '*/test/*' 2>/dev/null | wc -l | tr -d ' ')"
if [[ "$OTHER_SCHEMAS" == "0" ]]; then
  pass "Y2_single_template_path"
else
  find "$ROOT" -name 'SCHEMA.md' ! -path "$SCHEMA" 2>/dev/null || true
  fail "Y2_single_template_path"
fi

# Y1_adr003_compliance — all five sections present
Y1_OK=true
for section in Layers Workflows Excludes Conventions "Index and log"; do
  if ! grep -qiE "^##[[:space:]]+${section}[[:space:]]*$" "$SCHEMA"; then
    Y1_OK=false
  fi
done
if $Y1_OK && [[ $FAILURES -eq 0 ]]; then
  pass "Y1_adr003_compliance"
else
  fail "Y1_adr003_compliance"
fi

# Z1_verifier_passes
if [[ $FAILURES -eq 0 ]]; then
  pass "Z1_verifier_passes"
  exit 0
fi

fail "Z1_verifier_passes"
echo "${FAILURES} check(s) failed."
exit 1
