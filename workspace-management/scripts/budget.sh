#!/usr/bin/env bash
# Report the workspace's spend today against its daily budget.
#
# The first line is the state, for scripts and for agents that must check the
# budget before starting work:
#   budget: below        below the pace (the budget times the share of the day gone)
#   budget: above        above the pace, below the budget
#   budget: at           at or past the budget
#   budget: unknown      some of today's usage has no price, or a usage source failed,
#                        so the spend is not known
#   budget: unset        no budget: the workspace has no manager, or its task has
#                        no "Daily budget" row
#   budget: unavailable  usage or the manager task could not be read, such as
#                        during a takeover that was cut short (exit 1)
# The lines after it give the figures. Spend is in USD at list price across all
# providers, as `t3c usage summary` prices it, and days are in UTC.
#
# Environment:
#   MANAGER_BOARD  the workspace board (default: /tasks)
set -uo pipefail
# shellcheck source=manager-lib.sh source-path=SCRIPTDIR
source "$(dirname "${BASH_SOURCE[0]}")/manager-lib.sh"

BOARD=${MANAGER_BOARD:-/tasks}
# Wait out a takeover under way, so a half-made roll is not read as no budget.
if [ -d "$BOARD" ]; then manager_lock "$BOARD" 2>/dev/null || true; fi
TODAY=$(date -u +%F)
WEEK=$(date -u -d '6 days ago' +%F)
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

if ! t3c --json usage summary --since-day "$WEEK" --until-day "$TODAY" --time-zone Etc/UTC >"$TMP/usage.json" 2>"$TMP/usage.err" ||
  ! jq -e '.data.buckets | type == "array"' "$TMP/usage.json" >/dev/null 2>&1; then
  echo "budget: unavailable"
  echo "t3c usage summary failed: $(head -c 300 "$TMP/usage.err")"
  exit 1
fi

budget=""
reason=""
rc=0
body=$(manager_body "$BOARD" 2>"$TMP/body.err") || rc=$?
if [ "$rc" -eq 0 ] && ! standing_state <<<"$body" >/dev/null; then
  echo "no ## Log heading outside a code block in the manager task" >"$TMP/body.err"
  rc=1
fi
if [ "$rc" -eq 0 ]; then
  budget=$(standing_state <<<"$body" | section Budget | sed -nE 's/^\| *Daily budget[^|]*\| *\$?([0-9]+(\.[0-9]+)?) *\|.*/\1/p' | head -1)
  [ -n "$budget" ] || reason="the manager task's Budget section has no Daily budget row with a number"
elif [ "$rc" -ne 2 ]; then
  # A manager exists but its task cannot be read: not knowing the budget is not
  # having none.
  echo "budget: unavailable"
  echo "the manager task cannot be read: $(cat "$TMP/body.err")"
  exit 1
else
  reason=$(cat "$TMP/body.err")
fi

jq -r --arg today "$TODAY" --arg budget "$budget" --arg reason "$reason" \
  --argjson elapsed "$(($(date -u +%s) % 86400))" '
  def usd: . * 100 | round / 100;
  .data.buckets as $b
  | ($b | map(select(.day == $today))) as $t
  | ($t | map(.costUsd // 0) | add // 0) as $spent
  | ($t | map((.unpricedTokens // 0) + (.unpricedRecords // 0)) | add // 0) as $unpriced
  | ([.data.sources[]? | select(.status | IN("ok", "missing") | not)
      | "\(.fingerprint.provider // "?") \(.status)\(if .message then ": \(.message)" else "" end)"]) as $failed
  | ($b | map(select(.day != $today)) | group_by(.day) | map(map(.costUsd // 0) | add)) as $days
  | (if $budget == "" then null else ($budget | tonumber) end) as $bud
  | (if $bud == null then null else $bud * $elapsed / 86400 end) as $pace
  | "budget: " + (
      if $bud == null then "unset"
      elif $spent >= $bud then "at"
      elif $unpriced > 0 or ($failed | length) > 0 then "unknown"
      elif $spent > $pace then "above"
      else "below" end),
    "today so far: $\($spent | usd) (" + ($t | group_by(.provider) | map("\(.[0].provider) $\(map(.costUsd // 0) | add | usd)") | join(", ")) + ")",
    (if ($failed | length) > 0 then "usage sources failed: \($failed | join("; "))" else empty end),
    (if $unpriced > 0 then "unpriced today: \($t | map(.unpricedTokens // 0) | add) tokens in \($t | map(.unpricedRecords // 0) | add) records" else empty end),
    "previous 6 days: average $\(if ($days | length) > 0 then ($days | add / length | usd) else 0 end) a day",
    "day elapsed: \($elapsed * 100 / 86400 | round)%",
    (if $bud == null then "daily budget: none (\($reason))"
     else "daily budget: $\($bud), pace now: $\($pace | usd)" end)' "$TMP/usage.json"
