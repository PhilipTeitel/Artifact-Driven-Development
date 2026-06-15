#!/usr/bin/env bash
# verify-wiki-query-command.sh — binding checks for /wiki-query (story S1-4)
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CMD="${ROOT}/.cursor/commands/wiki-query.md"
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
  for ref in "SCHEMA.md" "index.md" "log.md"; do
    if grep -qF "$ref" "$CMD"; then
      pass "A1_refs_${ref//[.\/ ]/_}"
    else
      fail "A1_refs_${ref//[.\/ ]/_}"
    fi
  done
fi

# B1_index_first_s8 — must read index.md before other wiki pages
if grep -qiE 'index\.md.*before|MUST read.*index\.md|read.*index\.md.*before|index-first' "$CMD"; then
  pass "B1_index_first_s8"
else
  fail "B1_index_first_s8"
fi
if grep -qiE 'index\.md' "$CMD" && grep -qiE 'before.*(page|wiki|other)|first' "$CMD"; then
  pass "B1_index_order"
else
  fail "B1_index_order"
fi

# B2_citations_s8 — synthesized answer with citations
if grep -qiE 'citation|citations' "$CMD" && grep -qiE 'synthesi[sz]e|answer' "$CMD"; then
  pass "B2_citations_s8"
else
  fail "B2_citations_s8"
fi
if grep -qiE 'markdown links|\[title\]\(|wiki/.*\.md' "$CMD"; then
  pass "B2_citation_format"
else
  fail "B2_citation_format"
fi

# C1_confirm_filing_s8 — explicit user confirmation before writes
if grep -qiE 'explicit.*confirm|confirm.*explicit|explicitly confirm' "$CMD" \
  && grep -qiE 'yes/no|yes.*no|ask the user|filing gate' "$CMD"; then
  pass "C1_confirm_filing_s8"
else
  fail "C1_confirm_filing_s8"
fi
if grep -qiE 'do not.*(create|modify|write|append)|until the user|before any.*write' "$CMD"; then
  pass "C1_no_write_without_confirm"
else
  fail "C1_no_write_without_confirm"
fi

# C2_decline_no_writes_s8 — decline means no wiki mutations after answer
if grep -qiE 'declin|do not confirm|does not confirm' "$CMD" \
  && grep -qiE 'no.*(mutation|write|modif)|read-only|STOP' "$CMD"; then
  pass "C2_decline_no_writes_s8"
else
  fail "C2_decline_no_writes_s8"
fi

# C3_filing_updates_s8 — on confirm: page + index + log
if grep -qiE 'create.*(page|wiki)|new wiki page' "$CMD" \
  && grep -qiE 'update.*index|index.*update' "$CMD" \
  && grep -qiE 'append.*log|log.*append' "$CMD"; then
  pass "C3_filing_updates_s8"
else
  fail "C3_filing_updates_s8"
fi

# D1_immutability_s5 — no modifications outside wiki/
if grep -qiE 'outside.*wiki|outside.*\{wiki_dir\}|only.*\{wiki_dir\}|writes only' "$CMD" \
  && grep -qiE 'must not|do not|never' "$CMD"; then
  pass "D1_immutability_s5"
else
  fail "D1_immutability_s5"
fi

# E1_log_format_s13 — query operation in log heading
if grep -qF '## [YYYY-MM-DD] query |' "$CMD" || grep -qE '## \[[0-9]{4}-[0-9]{2}-[0-9]{2}\] query \|' "$CMD"; then
  pass "E1_log_format_s13"
else
  fail "E1_log_format_s13"
fi

# F1_no_vector_rag — forbid embeddings / vector search
if grep -qiE 'embed|vector|RAG|semantic search' "$CMD" \
  && grep -qiE 'do not|must not|never|no vector|No RAG|No vector' "$CMD"; then
  pass "F1_no_vector_rag"
else
  fail "F1_no_vector_rag"
fi
if grep -qiE 'index.*page read|direct page read|index \+ direct' "$CMD"; then
  pass "F1_index_page_only"
else
  fail "F1_index_page_only"
fi

# Y1_full
if [[ $FAILURES -eq 0 ]]; then
  pass "Y1_full"
  exit 0
fi

fail "Y1_full"
echo "${FAILURES} check(s) failed."
exit 1
