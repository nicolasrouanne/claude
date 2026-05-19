---
name: qonto-invoices
description: "Analyse des factures clients Qonto par période de prestation (pas date d'émission) et compte de destination. Sortie HT/TTC, top clients, audit des cas ambigus."
title: /qonto-invoices
parent: Skills
permalink: /skills/qonto-invoices/
nav_order: 20
---

# Qonto Invoices

Bilan factures clients Qonto pour une année donnée, en raisonnant sur la **période de prestation** (et non la date d'émission), avec une vue par **compte de destination** (récupérés dynamiquement depuis l'organisation Qonto).

## Pourquoi cette skill

Le bilan annuel "factures émises en YYYY" donne un mauvais résultat car :
- Une facture émise début janvier YYYY concerne souvent décembre YYYY-1.
- Une facture émise en janvier/février YYYY+1 concerne souvent décembre YYYY.
- Certaines factures n'ont **pas** le champ `performance_date` rempli — il faut parser le mois en français (`"Prestations janvier 2025"`, `"…mai 2026"`, etc.) dans le `header` ou les `items`.

La skill applique une heuristique en cascade :

1. `performance_date` si renseigné
2. Sinon, mois français parsé dans `header` / `items[].title` / `items[].description`
3. Sinon, fallback sur `issue_date` (signalé dans la section audit)

## Script

- `aggregate.jq` (dans ce dossier) — toute la logique de filtrage et d'agrégation. Reçoit `year`, `window` (nb de mois après le 31/12 à scanner) et `accounts` (mapping IBAN → nom de compte, **construit dynamiquement** depuis l'API pour ne rien hardcoder dans le repo).

## Your Task

Quand l'utilisateur invoque `/qonto-invoices [année]` :

### 1. Récupérer le mapping IBAN → compte (dynamique)

```
mcp__qonto__get_qonto_organization
```

→ Extrais `bank_accounts[].iban` + `bank_accounts[].name`. Construis un objet JSON `{ "<iban>": "<name>", ... }`. **Ne jamais hardcoder un IBAN ni un nom de compte spécifique dans le repo.**

### 2. Récupérer toutes les factures clients

```
mcp__qonto__get_client_invoices  per_page=500  current_page=1
```

⚠ **Important** : utiliser `per_page=500` (ou un nombre ≥ `total_count`). Avec `per_page=100`, la pagination Qonto trie par DESC et la concaténation page 1 + page 2 peut produire des doublons / oublis (bug observé). Toujours vérifier `meta.total_count` vs `client_invoices | length`.

Le résultat dépasse 200k caractères → il sera sauvegardé dans un fichier temporaire (`tool-results/.../mcp-qonto-get_client_invoices-*.txt`). Récupère le chemin du fichier dans le message d'erreur, puis passe-le à jq directement.

### 3. Lancer l'agrégation

```bash
jq -r \
  --arg year "2025" \
  --arg window "2" \
  --argjson accounts "$(cat <<'EOF'
{"<iban1>":"<nom1>","<iban2>":"<nom2>"}
EOF
)" \
  -f ~/dev/claude/.claude/skills/qonto-invoices/aggregate.jq \
  <chemin-du-fichier-tool-result>
```

- Sans argument utilisateur : `year` = année en cours - 1 (cas le plus fréquent = bilan annuel).
- Si l'utilisateur dit "2024", "2025"… → `year` correspondant.
- `window=2` est le défaut raisonnable (couvre les factures émises jusqu'à fin février N+1).

### 4. Présenter le résultat

Affiche la sortie brute du script (déjà formatée), puis :

- **Mets en avant la section "À vérifier manuellement"** : factures avec `period_source = issue_date_fallback` (headers vides, placeholders non remplis, etc.). Pour chacune, propose une période corrigée basée sur le contexte (cadence client, type de prestation) et **demande confirmation à l'utilisateur** avant d'ajuster.
- Si l'utilisateur valide une exclusion, recalcule en filtrant et redonne les totaux. Pas besoin de re-fetch l'API.

### 5. Cas limites connus à signaler

| Symptôme | Cause probable | Action |
|---|---|---|
| Header vide sur une facture début janvier | Facture pour le mois précédent (donc année précédente) | Proposer d'exclure |
| Header avec `%mois%` / `%année%` littéraux | Template Qonto avec placeholder pas substitué | Signaler comme bug Qonto, déduire la période de la cadence |
| Un client apparaît avec 2 graphies (majuscules vs casse mixte) | Doublon côté Qonto | Suggérer un merge dans Qonto |
| `total_pages > 1` avec `per_page=100` | Ne pas paginer manuellement | Augmenter `per_page` à ≥ `total_count` |

## Options avancées

- **Filtrer un compte spécifique** : ajouter `| map(select(.account == "<nom>"))` dans le pipeline jq, ou faire un `select` en post.
- **Cumul HT par mois de prestation** : `group_by(.period[0:7])` au lieu de `group_by(.account)`.
- **Année partielle** : restreindre par `select(.period >= "YYYY-MM-01")` etc.

## Notes

- Le script ne traite que les factures **clients** (`get_client_invoices`). Pour les factures fournisseurs ou les notes de crédit, voir `get_supplier_invoices` / `get_credit_notes`.
- Les montants HT sont calculés comme `total_amount - vat_amount` (plus simple et exact que de sommer les `items[].subtotal`).
- L'IBAN du compte de destination est lu dans `payment_methods[0].iban` — vérifier qu'il n'y a pas de multi-IBAN par facture (à date, un seul moyen de paiement par facture).
