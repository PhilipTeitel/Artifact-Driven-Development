#!/usr/bin/env bash
# verify-wiki-ingest-command.sh — binding checks for /wiki-ingest (story S1-3)
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CMD="${ROOT}/.cursor/commands/wiki-ingest.md"
FIXTURE="${ROOT}/test/fixtures/ingested-v1.json"
FAILURES=0

pass() { echo "PASS: $1"; }
fail() { echo "FAIL: $1"; FAILURES=$((FAILURES + 1)); }

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

grep_cmd() {
  local pattern="$1"
  local check="$2"
  if grep -qiE "$pattern" "$CMD"; then
    pass "$check"
    return 0
  fi
  fail "$check"
  return 1
}

# A1_command_exists
if require_file "$CMD" "A1_command_exists"; then
  for ref in "SCHEMA.md" "Excludes" ".ingested.json" "index.md" "log.md"; do
    if grep -qF "$ref" "$CMD"; then
      pass "A1_refs_${ref//[.\/ ]/_}"
    else
      fail "A1_refs_${ref//[.\/ ]/_}"
    fi
  done
fi

# B1_interactive_s6 — read → review → write
if grep -qiE 'read.*review|review.*write|read → review → write' "$CMD" \
  || (grep -qiE '\*\*Read\*\*|read-only' "$CMD" && grep -qiE 'review|confirm|takeaways' "$CMD" && grep -qiE 'write|update' "$CMD"); then
  pass "B1_interactive_s6"
else
  fail "B1_interactive_s6"
fi
if grep -qiE 'proceed without review|waive' "$CMD"; then
  pass "B1_review_waiver"
else
  fail "B1_review_waiver"
fi

# B2_index_log_s6
grep_cmd 'index\.md' 'B2_index'
grep_cmd 'log\.md' 'B2_log'
if grep -qiE 'update.*index|index.*update' "$CMD" && grep -qiE 'append.*log|log.*append' "$CMD"; then
  pass "B2_index_log_s6"
else
  fail "B2_index_log_s6"
fi

# C1_batch_s7
if grep -qiE 'batch|--batch' "$CMD" && grep -qiE 'sequential|without interactive|no.*prompt|between files' "$CMD"; then
  pass "C1_batch_s7"
else
  fail "C1_batch_s7"
fi

# C2_skips_s7
if grep -qiE 'Excludes|exclude' "$CMD" && grep -qiE '\.ingested\.json|already ingested|sources' "$CMD"; then
  pass "C2_skips_s7"
else
  fail "C2_skips_s7"
fi

# D1_ingested_json_s12
grep_cmd '"version"[[:space:]]*:[[:space:]]*1|"version": 1' 'D1_version'
grep_cmd '"sources"' 'D1_sources'
if grep -qiE 'vault-relative|forward slash|forward slashes' "$CMD"; then
  pass "D1_ingested_json_s12"
else
  fail "D1_ingested_json_s12"
fi
if require_file "$FIXTURE" "D1_fixture_optional"; then
  if grep -q '"version": 1' "$FIXTURE" && grep -q '"sources"' "$FIXTURE"; then
    pass "D1_fixture_shape"
  else
    fail "D1_fixture_shape"
  fi
fi

# D2_source_immutable_s12
if grep -qiE 'never modify|do not modify|read-only|immutable' "$CMD" \
  && grep -qiE 'source' "$CMD"; then
  pass "D2_source_immutable_s12"
else
  fail "D2_source_immutable_s12"
fi

# E1_immutability_s5
if grep -qiE 'outside.*wiki|outside.*\{wiki_dir\}|only.*\{wiki_dir\}|writes only' "$CMD" \
  && grep -qiE 'must not|do not|never' "$CMD"; then
  pass "E1_immutability_s5"
else
  fail "E1_immutability_s5"
fi

# F1_log_format_s13
if grep -qF '## [YYYY-MM-DD] ingest |' "$CMD" || grep -qE '## \[[0-9]{4}-[0-9]{2}-[0-9]{2}\] ingest \|' "$CMD"; then
  pass "F1_log_format_s13"
else
  fail "F1_log_format_s13"
fi

# G1_markdown_links
if grep -qiE 'standard markdown links|\[text\]\(path\)' "$CMD" \
  && grep -qiE 'wikilink|no `\[\[`|never.*\[\[' "$CMD"; then
  pass "G1_markdown_links"
else
  fail "G1_markdown_links"
fi

# Y1_full
if [[ $FAILURES -eq 0 ]]; then
  pass "Y1_full"
  exit 0
fi

fail "Y1_full"
echo "${FAILURES} check(s) failed."
exit 1
