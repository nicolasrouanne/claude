#!/usr/bin/env bash
# Claude Code status line — subscription usage, the same numbers `/usage` shows.
#   session = 5-hour rolling window   (rate_limits.five_hour)
#   week    = 7-day rolling window    (rate_limits.seven_day)
# Data comes from the JSON Claude Code pipes in on stdin (v2.1+). No network,
# no external deps beyond jq.

input=$(cat)

# Fields are joined with US (\x1f), a non-whitespace separator, so `read` does
# NOT collapse empty fields (a tab would, shifting columns when a value is absent).
IFS=$'\x1f' read -r model sess_pct sess_reset week_pct week_reset ctx_pct < <(
  printf '%s' "$input" | jq -r '
    [ .model.display_name,
      (.rate_limits.five_hour.used_percentage  | if . == null then "" else round end),
      (.rate_limits.five_hour.resets_at        // ""),
      (.rate_limits.seven_day.used_percentage  | if . == null then "" else round end),
      (.rate_limits.seven_day.resets_at        // ""),
      (.context_window.used_percentage         | if . == null then "" else round end)
    ] | map(tostring) | join("\u001f")'
)

DIM=$'\033[2m'; RESET=$'\033[0m'
color() { # $1=pct -> green <50, yellow 50-79, red >=80
  if   [ "$1" -ge 80 ]; then printf '\033[31m'
  elif [ "$1" -ge 50 ]; then printf '\033[33m'
  else                       printf '\033[32m'; fi
}
bar() { # $1=pct -> 8-char filled/empty bar
  local p=$1 filled i out=''
  filled=$(( (p + 6) / 13 )); [ "$filled" -gt 8 ] && filled=8
  for ((i=0; i<8; i++)); do [ "$i" -lt "$filled" ] && out+='█' || out+='░'; done
  printf '%s' "$out"
}
when() { # $1=epoch $2=date|time -> localized reset label, lowercase meridiem
  [ -z "$1" ] && return
  if [ "$2" = date ]; then date -r "$1" '+%b %-d %-I%p'; else date -r "$1" '+%-I:%M%p'; fi \
    | sed 's/AM/am/; s/PM/pm/'
}

out="${DIM}${model}${RESET}"
if [ -n "$sess_pct" ]; then
  c=$(color "$sess_pct")
  out+="  ${DIM}session${RESET} ${c}$(bar "$sess_pct") ${sess_pct}%${RESET} ${DIM}↻$(when "$sess_reset" time)${RESET}"
fi
if [ -n "$week_pct" ]; then
  c=$(color "$week_pct")
  out+="  ${DIM}week${RESET} ${c}$(bar "$week_pct") ${week_pct}%${RESET} ${DIM}↻$(when "$week_reset" date)${RESET}"
fi
[ -n "$ctx_pct" ] && out+="  ${DIM}ctx ${ctx_pct}%${RESET}"

printf '%s' "$out"
