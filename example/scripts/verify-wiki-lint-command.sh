#!/usr/bin/env bash
# verify-wiki-lint-command.sh — binding checks for /wiki-lint (story S1-5)
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CMD="${ROOT}/.cursor/commands/wiki-lint.md"
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

# B1_check_categories_s9 — all five S9 categories
for term in contradictions "stale claims" "orphan" "missing concept" "cross-ref"; do
  if grep -qiE "${term}" "$CMD"; then
    pass "B1_category_${term// /_}"
  else
    fail "B1_category_${term// /_}"
  fi
done

# B2_report_s9 — printed report with suggested fixes
if grep -qiE 'report|findings' "$CMD" && grep -qiE 'suggest' "$CMD"; then
  pass "B2_report_s9"
else
  fail "B2_report_s9"
fi
if grep -qiE 'print.*(report|chat)|human-readable' "$CMD"; then
  pass "B2_print_report"
else
  fail "B2_print_report"
fi

# C1_no_autofix_s9 — forbid applying fixes except log append
if grep -qiE 'do not.*(apply|auto|fix)|no auto|report-only|suggestions only' "$CMD"; then
  pass "C1_no_autofix_s9"
else
  fail "C1_no_autofix_s9"
fi
if grep -qiE 'append.*log\.md|log\.md.*append' "$CMD" \
  && grep -qiE 'only.*log|except.*log|log\.md.*only' "$CMD"; then
  pass "C1_log_only_write"
else
  fail "C1_log_only_write"
fi

# D1_log_format_s13 — lint operation in log heading
if grep -qF '## [YYYY-MM-DD] lint |' "$CMD" || grep -qE '## \[[0-9]{4}-[0-9]{2}-[0-9]{2}\] lint \|' "$CMD"; then
  pass "D1_log_format_s13"
else
  fail "D1_log_format_s13"
fi

# E1_immutability_s5 — no modifications outside wiki/
if grep -qiE 'outside.*wiki|outside.*\{wiki_dir\}|only.*\{wiki_dir\}|vault sources' "$CMD" \
  && grep -qiE 'must not|do not|never' "$CMD"; then
  pass "E1_immutability_s5"
else
  fail "E1_immutability_s5"
fi

# F1_reads_schema — read SCHEMA.md before linting
if grep -qiE 'read.*SCHEMA\.md|SCHEMA\.md.*before' "$CMD"; then
  pass "F1_reads_schema"
else
  fail "F1_reads_schema"
fi
if grep -qiE 'MUST read|MUST.*SCHEMA' "$CMD"; then
  pass "F1_schema_required"
else
  fail "F1_schema_required"
fi

# Y1_full
if [[ $FAILURES -eq 0 ]]; then
  pass "Y1_full"
  exit 0
fi

fail "Y1_full"
echo "${FAILURES} check(s) failed."
exit 1
