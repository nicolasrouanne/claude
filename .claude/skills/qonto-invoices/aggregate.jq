# Qraft — Aggregate Qonto client invoices by performance period and destination account.
#
# Args (jq --arg / --argjson) :
#   year      : "2025" — target performance year
#   window    : "2"    — months after Dec 31 to scan for late-issued invoices
#   accounts  : { "<iban>": "<account_name>", ... } — IBAN → account name map
#               Built dynamically from `get_qonto_organization` so no IBAN
#               is hard-coded in the public repo.
#
# Input  : raw JSON from Qonto MCP `get_client_invoices` (the `{result: {...}}` envelope).
# Output : plain-text report with per-account totals (HT + TTC) and an audit
#          section listing invoices whose period source is `issue_date_fallback`.
#
# Period of a single invoice is determined in this order :
#   1. `performance_date`                       → most reliable
#   2. French month found in header / items     → e.g. "Prestations janvier 2025"
#   3. fallback to `issue_date`                 → flagged for review

def iban_to_account($accounts; $iban):
  $accounts[$iban] // "Autre (\($iban))";

def fr_month_to_num($m):
  {"janvier":"01","février":"02","fevrier":"02","mars":"03","avril":"04",
   "mai":"05","juin":"06","juillet":"07","août":"08","aout":"08",
   "septembre":"09","octobre":"10","novembre":"11","décembre":"12","decembre":"12"}
  [$m | ascii_downcase];

def parse_fr_period($text):
  ($text // "")
  | [scan("(?i)(janvier|février|fevrier|mars|avril|mai|juin|juillet|août|aout|septembre|octobre|novembre|décembre|decembre)\\s+(\\d{4})")]
  | if length > 0 then "\(.[0][1])-\(fr_month_to_num(.[0][0]))-01" else null end;

def derived_period:
  if (.performance_date // "") != "" then
    {p: .performance_date, src: "performance_date"}
  else
    ([.header, .items[]?.description, .items[]?.title]
     | map(parse_fr_period(.))
     | map(select(. != null))) as $parsed
    | if ($parsed | length) > 0 then {p: $parsed[0], src: "fr_header_or_items"}
      else {p: .issue_date, src: "issue_date_fallback"}
      end
  end;

def round2: . * 100 | round / 100;

def scope_end($year; $window):
  ($year | tonumber + 1 | tostring) as $next
  | ($window | tonumber) as $w
  | "\($next)-\(if $w < 10 then "0\($w)" else "\($w)" end)-28";

($year // "2025") as $YEAR
| ($window // "2") as $WINDOW
| ($accounts // {}) as $ACCOUNTS

| .result.client_invoices
| map(
    . as $inv
    | (iban_to_account($ACCOUNTS; .payment_methods[0].iban // "")) as $account
    | (derived_period) as $dp
    | . + {
        account: $account,
        ht: ((.total_amount.value | tonumber) - (.vat_amount.value | tonumber)),
        ttc: (.total_amount.value | tonumber),
        period: $dp.p,
        period_source: $dp.src
      }
  )
| map(select(.issue_date >= "\($YEAR)-01-01" and .issue_date <= scope_end($YEAR; $WINDOW)))
| map(select(.period[0:4] == $YEAR))
| . as $invoices

| (
    "═══════════════════════════════════════════════════════",
    "Factures Qonto — prestation \($YEAR) (scope émission : jan \($YEAR) → fenêtre +\($WINDOW) mois)",
    "═══════════════════════════════════════════════════════",
    "",
    "TOTAL : \($invoices | length) factures",
    "  HT  brut       : \([$invoices[].ht] | add | round2) EUR",
    "  HT  hors annul.: \([$invoices[] | select(.status != "canceled") | .ht]  | add | round2) EUR",
    "  TTC hors annul.: \([$invoices[] | select(.status != "canceled") | .ttc] | add | round2) EUR",
    "",
    "Source de la période :",
    ($invoices | group_by(.period_source) | .[] | "  \(.[0].period_source) : \(length) factures"),
    "",
    "═══ Par compte de destination ═══════════════════════"
  ),
  (
    $invoices
    | group_by(.account)
    | .[] as $g
    | (
        "",
        "▶ \($g[0].account) — \($g | length) factures",
        "  HT  hors annul.: \([$g[] | select(.status != "canceled") | .ht]  | add | round2) EUR",
        "  TTC hors annul.: \([$g[] | select(.status != "canceled") | .ttc] | add | round2) EUR",
        "  Top clients (HT, hors annulées) :",
        (
          $g
          | map(select(.status != "canceled"))
          | group_by(.client.name)
          | map({client: .[0].client.name, count: length, ht: ([.[].ht] | add)})
          | sort_by(-.ht)
          | .[] | "    - \(.client) : \(.count) facture(s) — \(.ht | round2) EUR HT"
        )
      )
  ),
  (
    "",
    "═══ ⚠ À vérifier manuellement (period = issue_date_fallback) ═══",
    "(headers vides ou non parsables — confirmer la période réelle de prestation)",
    "",
    ($invoices
     | map(select(.period_source == "issue_date_fallback"))
     | sort_by(.issue_date)
     | if length == 0 then "  (aucune — clean)"
       else (.[] | "  [\(.account)] period=\(.period[0:7]) (émise \(.issue_date)) | \(.number) | \(.client.name) | \(.ttc) TTC | \(.status) | header=\"\(.header)\"")
       end)
  ),
  (
    "",
    "═══ Détail complet (par compte, période, n°) ═══",
    ($invoices
     | sort_by(.account, .period, .number)
     | .[]
     | "[\(.account[0:4])] perf=\(.period[0:7]) (émise \(.issue_date)) | \(.number) | \(.client.name) | \(.ht | round2) HT | \(.ttc) TTC | \(.status)")
  )
