#!/usr/bin/env bash
# verify-stage1-e2e.sh — Stage 1 E2E post-conditions on test/vault/wiki/ (story S1-6)
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VAULT_FIXTURE="${VAULT_FIXTURE:-${ROOT}/test/vault}"
WIKI="${VAULT_FIXTURE}/wiki"
DAILY="${VAULT_FIXTURE}/daily"
EVIDENCE="${ROOT}/docs/features/S1-6-acceptance-evidence.md"
DAILY_MANIFEST="${ROOT}/scripts/fixtures/test-vault-daily.sha256"
FAILURES=0

pass() { echo "PASS: $1"; }
fail() { echo "FAIL: $1"; FAILURES=$((FAILURES + 1)); }

require_dir() {
  local path="$1"
  local check="$2"
  if [[ -d "$path" ]]; then
    pass "$check"
    return 0
  fi
  fail "$check"
  return 1
}

require_file() {
  local path="$1"
  local check="$2"
  if [[ -f "$path" && -s "$path" ]]; then
    pass "$check"
    return 0
  fi
  fail "$check"
  return 1
}

# A1_evidence_doc_exists
A1_evidence_doc_exists() {
  if require_file "$EVIDENCE" "A1_evidence_doc_exists"; then
    for section in Environment "Commands executed" Observations "Verifier output" Sign-off; do
      if grep -qF "$section" "$EVIDENCE"; then
        pass "A1_section_${section// /_}"
      else
        fail "A1_section_${section// /_}"
      fi
    done
  fi
}

# B1_core_artifacts_s18
B1_core_artifacts_s18() {
  require_dir "$WIKI" "B1_wiki_dir" || return 0
  for f in SCHEMA.md index.md log.md; do
    require_file "${WIKI}/${f}" "B1_${f%.md}_s18"
  done
}

# B2_wiki_page_s18
B2_wiki_page_s18() {
  local count
  count="$(find "$WIKI" -name '*.md' -type f \
    ! -name 'SCHEMA.md' ! -name 'index.md' ! -name 'log.md' 2>/dev/null | wc -l | tr -d ' ')"
  if [[ "${count:-0}" -ge 1 ]]; then
    pass "B2_wiki_page_s18"
  else
    fail "B2_wiki_page_s18"
    echo "  expected at least one wiki page besides SCHEMA, index, log"
  fi
}

# B3_ingested_json_s12
B3_ingested_json_s12() {
  local sidecar="${WIKI}/.ingested.json"
  if ! require_file "$sidecar" "B3_ingested_file"; then
    return 0
  fi
  if python3 -c "
import json, sys
p = sys.argv[1]
with open(p) as f:
    d = json.load(f)
assert d.get('version') == 1, 'version must be 1'
sources = d.get('sources') or {}
assert len(sources) >= 1, 'sources must have at least one entry'
" "$sidecar" 2>/dev/null; then
    pass "B3_ingested_json_s12"
  else
    fail "B3_ingested_json_s12"
  fi
}

# B4_log_operations_s13_s18
B4_log_operations_s13_s18() {
  local log="${WIKI}/log.md"
  if ! require_file "$log" "B4_log_file"; then
    return 0
  fi
  for op in init ingest query lint; do
    if grep -qE "^## \[[0-9]{4}-[0-9]{2}-[0-9]{2}\] ${op} \|" "$log"; then
      pass "B4_log_${op}_s13_s18"
    else
      fail "B4_log_${op}_s13_s18"
    fi
  done
}

# C1_sources_unchanged_s5
C1_sources_unchanged_s5() {
  if [[ ! -d "$DAILY" ]]; then
    fail "C1_sources_unchanged_s5"
    echo "  missing ${DAILY}"
    return 0
  fi
  if [[ ! -f "$DAILY_MANIFEST" ]]; then
    fail "C1_sources_unchanged_s5"
    echo "  missing manifest ${DAILY_MANIFEST}"
    return 0
  fi
  local tmp current
  tmp="$(mktemp)"
  (cd "$ROOT" && find test/vault/daily -name '*.md' -type f | sort | while read -r f; do
    shasum -a 256 "$f"
  done > "$tmp")
  if diff -q "$DAILY_MANIFEST" "$tmp" >/dev/null 2>&1; then
    pass "C1_sources_unchanged_s5"
  else
    fail "C1_sources_unchanged_s5"
    echo "  daily/*.md checksums differ from ${DAILY_MANIFEST}"
    diff "$DAILY_MANIFEST" "$tmp" | head -20 || true
  fi
  rm -f "$tmp"
}

# D1_all_command_verifiers
D1_all_command_verifiers() {
  local script name
  for name in verify-wiki-schema-template verify-init-wiki-command verify-wiki-ingest-command verify-wiki-query-command verify-wiki-lint-command; do
    script="${ROOT}/scripts/${name}.sh"
    if [[ ! -x "$script" ]]; then
      if [[ -f "$script" ]]; then
        chmod +x "$script" 2>/dev/null || true
      fi
    fi
    if bash "$script" >/dev/null 2>&1; then
      pass "D1_${name}"
    else
      fail "D1_${name}"
    fi
  done
}

# E1_no_stage2
E1_no_stage2() {
  if require_file "$EVIDENCE" "E1_evidence_present"; then
    if grep -qiE 'Stage 2 CLI was not used|no Python CLI|no stage 2' "$EVIDENCE"; then
      pass "E1_no_stage2_doc"
    else
      fail "E1_no_stage2_doc"
    fi
    if grep -qiE 'pyproject|pip install|llm-wiki' "$EVIDENCE" \
      && ! grep -qiE 'not (used|required|invoked)|was not used|no Python CLI' "$EVIDENCE"; then
      fail "E1_no_stage2_install"
    else
      pass "E1_no_stage2_install"
    fi
  fi
}

# Y2 evidence QA PASS
Y2_evidence_qa_pass() {
  if require_file "$EVIDENCE" "Y2_evidence_file"; then
    if grep -qF 'QA result: PASS' "$EVIDENCE"; then
      pass "Y2_qa_result_pass"
    else
      fail "Y2_qa_result_pass"
    fi
  fi
}

A1_evidence_doc_exists
B1_core_artifacts_s18
B2_wiki_page_s18
B3_ingested_json_s12
B4_log_operations_s13_s18
C1_sources_unchanged_s5
D1_all_command_verifiers
E1_no_stage2
Y2_evidence_qa_pass

# Y1_full
if [[ $FAILURES -eq 0 ]]; then
  pass "Y1_full"
  exit 0
fi

fail "Y1_full"
echo "${FAILURES} check(s) failed."
exit 1
