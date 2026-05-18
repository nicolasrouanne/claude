# Writing Style

Nicolas's voice across written communication. The **voice** (tone, structure, posture) is the same everywhere; only the **formatting** changes per channel.

## Universal voice

Apply these to every drafted message (Slack, email, Notion, PR description, status update).

- **Open with a narrative frame, not a headline.** Combine the topic AND your feeling about it in the first sentence. "j'ai bien avancé sur X qui est en fait une belle pelote de laine 🧵" tells the reader it was harder than expected without complaining. Avoid clinical openings like "PR ready for review".
- **Share reasoning, not just conclusions.** When you made a choice, name the alternative and assume the opinion: "j'ai choisi X parce que [raison], il y'avait d'autres solutions". Open to debate without inviting it.
- **Narrate the journey.** Show before/after: "Ca fait pas mal de choses, mais maintenant le plan est propre." Don't just describe the current state — make the effort visible.
- **End vulnerable, not triumphant.** Surface the unglamorous workaround or remaining risk instead of hiding it. "Peut-être qu'il va nous falloir un autre refresh manuel 😅". Builds trust.
- **Direct first sentence, no preamble.** Skip "Je me permets de...", "Je vous écris pour...", "I wanted to reach out about...". Get to the point.
- **French parlé but precise.** "Du coup", "y'avait", "ça fait pas mal" are fine in casual contexts. Casual ≠ sloppy — proper nouns stay correctly capitalized (Cloudflare, Terraform, DNS, GitHub).
- **Short and warm closings.** "Merci !", "Belle journée,", "À bientôt,". Never "Cordialement" or "Veuillez agréer".
- **Émoji rare et sémantique.** 🧵 for entanglement, 😅 for self-deprecation, "!" for friendly emphasis. Never decorative.
- **Length matches medium.** Slack status update: 4-6 short paragraphs. Slack DM: 1-2 lines. Email: 2-5 sentences max.

## Channel-specific formatting

### Slack

Use the full Slack formatting palette — don't default to plain text.

| Element | Usage |
|---|---|
| `` `code` `` | Technical identifiers: tool names, file paths, commands, domains. Ex: `` `terraform` ``, `` `app.episto.fr` ``, `` `terraform plan/apply` ``. |
| `*italic*` | Product/proper nouns once in context: *Cloudflare*, *sub-issue GitHub*. |
| `**bold**` | Key state or action words: **à review**, **C'est ce qui activera le certificat SSL**. |
| `> quote` | Final tentative/self-deprecating aside. Sets it apart visually as "thinking out loud". |
| Native bullets | Parallel-action lists. Format: `[action] -> issue #NNNN` or `-> pr #NNNN`. |
| Plain `#NNNN` | GitHub refs. Slack auto-unfurls same-org links — no markdown links needed. |

**Typical structure for a multi-track status update:**

1. Opening paragraph with narrative frame + emotional signal (1-2 sentences)
2. Reasoning paragraph explaining the high-level choice (1-2 sentences)
3. Macro context line ("la macro issue est #NNNN") then bullets decomposing the work
4. Wrap paragraph with before/after framing ("maintenant le plan est propre")
5. Quote-block aside with humble caveat or remaining risk

### Email

More formal than Slack. Vouvoiement simple, no emoji in body.

- **Greeting**: "Bonjour," or "Bonsoir," (standalone). "Bonjour/Bonsoir [Prénom]" or "Mme/M. [Nom]" only when Nicolas knows the person.
- **Body**: Direct, to the point in the first sentence. The universal-voice principles still apply.
- **Closing**: Short and warm — "Merci !", "Belle journée,", "Merci et bonne journée,", "À bientôt,".
- **Sign-off**: Just "Nicolas" (first name only). Gmail appends the signature automatically — never inline contact info.
- **Tone**: Natural, warm, concise. Vouvoiement simple. Uses "!" for friendly emphasis.
- **Length**: 2-5 sentences max. Numbered lists for multiple questions.
- **Never**: "Veuillez agréer", "Cordialement", "Je me permets de...", "N'hésitez pas à me contacter", long preambles.

### Notion / long-form docs

Covers blog posts (external) and technical write-ups (internal) alike — same register. The universal-voice principles still apply; what follows is the long-form layer on top.

**The shape that works:**

- **Short opener, no preamble.** For change/migration posts, a two-line `Avant : … / Après : …` followed by a single line pointing to the macro issue or PR is enough. For other posts, one or two short paragraphs stating the goal. No "Dans cet article…", no "Format : 10 minutes…".
- **Plain numbered sections** (`## 1. …`, `## 2. …`). Each section ends with relevant refs on a single trailing line: `→ #1212, PR #1208.`
- **At least one real code block per section** — HCL, YAML, bash, kubectl/curl verification, etc. Snippets from the actual code/PRs/scripts, not paraphrased examples.
- **Inline doc links throughout** — provider docs, CLI repos, RFC pages, internal Slite docs. A consolidated "Tous les liens" / "All links" section at the end is fine but doesn't replace inline links.
- **Honest tail section** (`## Ce qui reste` / `## What's still pending`) listing limitations and open items. No triumphant wrap-up after it.

**Avoid in long-form:**

- Clickbait titles or "X will change everything" framings.
- Opening `🎯` pitch callouts or closing `💬` punchline callouts — they read as overwritten.
- Grandiose constructions: "L'équation, c'est :", "C'est ce qui ferme la boucle", "déterministe et autonome", "tuer le rituel", "Si X demande Y, elle est incomplète".
- Acte 1 / Acte 2 / Acte 3 structure. Two existing TBMAs use it, but it doesn't generalize — copying it lands as theatrical.
- Long preambles, multi-paragraph framing, restated stakes.
- Tool comparison tables unless the comparison itself is the point of the article.
- Buzzwords: "game-changer", "revolutionize", "leverage", "unlock".

The universal voice (direct first sentence, share reasoning, vulnerable closing, semantic emoji) still applies — just without the Slack-style narrative arc.

### GitHub PR descriptions, issues, and comments

- **Use plain URLs**, not markdown links, for permalinks to the same repository. GitHub auto-unfurls same-repo links — markdown format like `[text](url)` creates unwanted code previews. Just paste the URL directly.
- PR descriptions: universal voice + concise summary + test plan checklist.

## How to apply

When drafting any message, produce a draft that already has this voice — don't wait for a correction. Match the medium: terse DMs stay terse, formal external messages get formal treatment (ask first if unsure). Default to this style for: Slack team broadcasts, async status updates, informal team messages, internal Notion updates, professional emails.
