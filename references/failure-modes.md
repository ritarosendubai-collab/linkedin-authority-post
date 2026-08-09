# Failure Modes, Retry Policy, Risk Gates

Use this closed taxonomy. Do not invent vague "couldn't do it" language — name the mode, take the default action, respect the retry limit.

## Taxonomy

| failure_mode | Meaning | Default action | Retry limit |
| --- | --- | --- | --- |
| `source_unreachable` | The primary instrument is paywalled, blocked, offline, or the domain cannot be fetched. | Report it, ask the user to paste the text or supply the PDF. Never route around a blocked domain by another method. | 1 alternate official mirror, then block. |
| `hallucinated_source` | A claim traces to recollection or a summary rather than a document that was opened and read. | Cut the claim. Do not soften it into a hedge. | None. |
| `stale_data` | The instrument may have been amended or superseded, or the effective date cannot be confirmed. | Mark `manual_review_required`; tell the user exactly what to confirm. | 1 re-verification. |
| `unsupported_claim` | The source does not say what the draft says. | Rewrite against the text once; if it still does not hold, cut. | 1 rewrite. |
| `ambiguous_scope` | The topic could refer to several instruments, or the jurisdiction is unclear. | Ask one narrow question. Do not guess between jurisdictions. | 1 clarification. |
| `image_rights_unclear` | Cover or slide imagery may be licensed, restricted, or imply endorsement. | Block publication until confirmed. | None. |
| `render_failed` | Image or PDF generation did not complete. | Deliver slide copy as markdown, mark renders `not_run`. | 2 attempts. |
| `partial_output` | Some artifacts produced, others missing. | Report exactly which are missing; forward-fix once. | 1 forward-fix. |
| `tool_unavailable` | Required capability (fetch, render, PDF, search) is not present. | Report the state and the fallback; do not silently degrade. | No silent retry. |
| `permission_blocked` | Approval or access is needed. | Stop and ask for the specific approval. Never expose credentials. | None without new input. |
| `scope_violation` | Request drifts into outreach, comment automation, or bulk engagement. | Decline that part, explain why, offer the draft-only alternative. | None. |

## Risk Gates

Deep path. Each must pass, be explicitly blocked, or be waived by the user with the residual risk written down.

**Citation gate.** Every factual claim maps to an article reference with an access date in `sources.json`. Unmapped → cut. This gate cannot be waived; a sourced-looking post with unsourced claims is worse than no post.

**Currency gate.** Effective date read from the instrument text. Amendments checked. Superseded instruments named. Regulatory, tax, financial, pricing, and deadline claims are always high freshness risk.

**Qualifier gate.** If the instrument has a condition that materially changes who is protected, the post states it. Headline protections without their trigger are misleading even when individually accurate.

**No-advice gate.** The post informs. It does not tell readers what to do about their own legal, tax, or financial position, and it does not present itself as professional advice. Where readers plainly need advice, say that they should get it.

**Image rights gate.** Every image confirmed cleared for commercial social use. Currency, official emblems, stock photography, and paywalled screenshots all trip this.

**Human choice gate.** Tone register and the closing line are presented as options with a recommendation; the human picks. Recorded in `decision-packet.md`.

**Scope gate.** Content production only. No sending, commenting, connecting, scraping, or automating interaction with other users' accounts.

## Evidence Rule

Success requires evidence:

- artifact paths for every slide, PDF, and caption produced;
- `sources.json` with article references, URLs, and access dates;
- output of `check_citations.py` and `lint_skill.py`;
- the review score with cited deductions.

Never convert a planned step into evidence. If a check was not run, record `not_run` and say why. A slide is not "produced" because it was designed.

## Waivers

If the user waives a gate, record: which gate, why, which claim is weakened, what risk remains, and whether the post is still publishable. The citation gate is not waivable.
