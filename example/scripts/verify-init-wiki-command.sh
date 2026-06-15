#!/usr/bin/env bash
# verify-init-wiki-command.sh — binding checks for /init-wiki (story S1-2)
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CMD="${ROOT}/.cursor/commands/init-wiki.md"
INDEX_TMPL="${ROOT}/templates/wiki/index.md"
LOG_TMPL="${ROOT}/templates/wiki/log.md"
SCHEMA_TMPL="${ROOT}/templates/wiki/SCHEMA.md"
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
  for ref in "templates/wiki/SCHEMA.md" "templates/wiki/index.md" "templates/wiki/log.md"; do
    if grep -qF "$ref" "$CMD"; then
      pass "A1_refs_${ref##*/}"
    else
      fail "A1_refs_${ref##*/}"
    fi
  done
fi

# B1_index_template_s1
if require_file "$INDEX_TMPL" "B1_index_file"; then
  if grep -qE '^#[[:space:]]+' "$INDEX_TMPL"; then
    pass "B1_index_template_s1_heading"
  else
    fail "B1_index_template_s1_heading"
  fi
  if grep -qiE '^##[[:space:]]+Pages[[:space:]]*$' "$INDEX_TMPL"; then
    pass "B1_index_template_s1"
  else
    fail "B1_index_template_s1"
  fi
fi

# B2_log_template_s1
if require_file "$LOG_TMPL" "B2_log_file"; then
  if grep -qiE 'append-only|append only' "$LOG_TMPL"; then
    pass "B2_log_template_s1"
  else
    fail "B2_log_template_s1"
  fi
  if grep -qi 'SCHEMA' "$LOG_TMPL"; then
    pass "B2_log_refs_schema"
  else
    fail "B2_log_refs_schema"
  fi
fi

# C1_creates_layout_s1
grep_cmd 'wiki_dir|wiki/' 'C1_wiki_dir'
grep_cmd 'SCHEMA\.md' 'C1_schema'
grep_cmd 'index\.md' 'C1_index'
grep_cmd 'log\.md' 'C1_log'
if grep -qiE 'missing|only if|when missing|does not exist' "$CMD"; then
  pass "C1_creates_layout_s1"
else
  fail "C1_creates_layout_s1"
fi

# C2_idempotent_s2
if grep -qiE 'never overwrite|do not overwrite|leave its body unchanged|already exist' "$CMD"; then
  pass "C2_idempotent_s2"
else
  fail "C2_idempotent_s2"
fi

# C3_reports_summary_s2
if grep -qiE 'summary|created|skipped|already present' "$CMD"; then
  pass "C3_reports_summary_s2"
else
  fail "C3_reports_summary_s2"
fi

# D1_vault_detection_s3
grep_cmd '\.obsidian/' 'D1_obsidian'
if grep -qiE 'walk|parent' "$CMD" && grep -qiE 'SCHEMA\.md' "$CMD"; then
  pass "D1_vault_detection_s3"
else
  fail "D1_vault_detection_s3"
fi
if grep -qiE 'stop|do not create' "$CMD"; then
  pass "D1_abort_on_failure"
else
  fail "D1_abort_on_failure"
fi

# E1_immutability_s5
if grep -qiE 'outside.*wiki|outside.*\{wiki_dir\}|read-only' "$CMD" \
  && grep -qiE 'must not|do not|never' "$CMD"; then
  pass "E1_immutability_s5"
else
  fail "E1_immutability_s5"
fi

# F1_log_format_s13
if grep -qF '## [YYYY-MM-DD] init |' "$CMD" || grep -qE '## \[[0-9]{4}-[0-9]{2}-[0-9]{2}\] init \|' "$CMD"; then
  pass "F1_log_format_s13"
else
  fail "F1_log_format_s13"
fi

# Y1_command_and_templates
if [[ -f "$CMD" && -f "$INDEX_TMPL" && -f "$LOG_TMPL" && -f "$SCHEMA_TMPL" ]]; then
  pass "Y1_command_and_templates"
else
  fail "Y1_command_and_templates"
fi

# G1_smoke_fixture — simulate idempotent init on test/vault copy; daily notes unchanged
G1_smoke_fixture() {
  local fixture="${ROOT}/test/vault"
  local tmp
  tmp="$(mktemp -d)"
  trap 'rm -rf "$tmp"' RETURN

  if [[ ! -d "${fixture}/.obsidian" ]]; then
    fail "G1_smoke_fixture"
    echo "  missing ${fixture}/.obsidian"
    return 1
  fi

  cp -a "$fixture/." "$tmp/"
  hash_daily_tree() {
    local base="$1"
    find "$base/daily" -name '*.md' -type f 2>/dev/null | sort | while read -r f; do
      shasum -a 256 "$f"
    done | shasum -a 256 | awk '{print $1}'
  }
  local daily_hash_before daily_hash_after
  daily_hash_before="$(hash_daily_tree "$tmp")"
  if [[ -z "$daily_hash_before" ]]; then
    fail "G1_smoke_fixture"
    echo "  no daily/*.md in fixture"
    return 1
  fi

  local wiki="${tmp}/wiki"
  mkdir -p "$wiki"
  for pair in "SCHEMA.md:${SCHEMA_TMPL}" "index.md:${INDEX_TMPL}" "log.md:${LOG_TMPL}"; do
    local name="${pair%%:*}"
    local src="${pair#*:}"
    if [[ ! -f "$wiki/$name" ]]; then
      cp "$src" "$wiki/$name"
    fi
  done

  for f in SCHEMA.md index.md log.md; do
    if [[ ! -f "$wiki/$f" ]]; then
      fail "G1_smoke_fixture"
      echo "  missing wiki/$f after init simulation"
      return 1
    fi
  done

  daily_hash_after="$(hash_daily_tree "$tmp")"
  if [[ "$daily_hash_before" != "$daily_hash_after" ]]; then
    fail "G1_smoke_fixture"
    echo "  daily/*.md checksum changed"
    return 1
  fi

  pass "G1_smoke_fixture"
  return 0
}
G1_smoke_fixture || true

if [[ $FAILURES -eq 0 ]]; then
  pass "Z1_verifier_passes"
  exit 0
fi

fail "Z1_verifier_passes"
echo "${FAILURES} check(s) failed."
exit 1
