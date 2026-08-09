---
name: linkedin-authority-post
description: Turn a regulation, policy change, market rule, or industry development into a sourced LinkedIn carousel and caption for a professional B2B audience. Use when the user wants to build a LinkedIn post or carousel from a primary source, needs slide copy with article-level citations, wants a caption written for reach, needs the tone calibrated for a specific regional market, or asks whether a topic is worth posting about and who it would reach. Tuned for UAE/Gulf B2B but portable. Do not use for outreach messaging, comment automation, or bulk engagement.
---

# LinkedIn Authority Post

Build a LinkedIn post that earns attention because it is genuinely useful and correctly sourced — not because it is loud. The output is a carousel plus caption, every factual claim traceable to a primary source, with reach mechanics and audience fit handled explicitly.

This skill covers **content production only**. Outreach messaging, comment automation, and bulk engagement are non-goals — see "Non-Goals" below.

## Inputs

- A topic: a regulation, circular, policy change, market rule, ruling, standard, or industry development.
- Optionally: a primary source URL or document, the poster's audience/ICP, brand colours or a cover image, prior post performance figures.

## Outputs

- `slides/` — numbered slide copy plus rendered images at 1080×1350.
- `carousel.pdf` — the same deck assembled for a document post.
- `caption.md` — post caption with source line and closing question.
- `sources.json` — every claim mapped to source, article reference, URL, and access date.
- `audience-note.md` — who it helps, who will engage, who it is not for, and the funnel-position caveat.
- `decision-packet.md` — options presented to the human and what they chose.

## Non-Goals

This skill does not send connection requests, post comments, send direct messages, scrape profiles, or automate any interaction with another user's account. LinkedIn's User Agreement prohibits automated messaging and unauthorized automated access. If a workflow that touches other users' accounts is ever added, it must be **draft-only**: the skill prepares text, a human reviews and sends. This is a fixed policy, not a default.

It also does not fabricate engagement predictions. Reach guidance here is mechanical (post format, link placement, reply timing), not a forecast.

## Route

**Fast path** — the topic is uncontroversial, the source is a single document the user already has, and the post is informational. Produce slides, caption, and sources; skip the full audience note.

**Deep path** — any of: the topic is legal, regulatory, tax, financial, or compliance-related; the post makes claims about deadlines, obligations, or rights; the source must be located and verified; the post is client-facing or brand-defining; imagery is licensed or third-party. Run every gate below.

**Blocked** — the primary source cannot be reached or read, the regulation's current status cannot be confirmed, or the user wants claims that the source does not support. Produce a decision packet and stop. Do not publish a sourced-looking post built on an unread source.

## Workflow

1. **Locate and read the primary source.** Not a summary, not a news article about it, not a search snippet. The instrument itself. Read `references/source-and-citation-policy.md`.
2. **Extract claims and map each to an article reference.** Every number, deadline, and obligation gets an article or section. Claims that cannot be mapped are cut, not softened.
3. **Check status and effective date.** Confirm the instrument is in force, has not been superseded, and note what it replaced. Record the access date.
4. **Find the qualifier most readers will miss.** Nearly every regulation has one — a condition, carve-out, or trigger that changes who is actually protected. This is the post's spine. See `references/carousel-production.md`.
5. **Map the audience.** Who it genuinely helps, who will actually engage, who it is not for, and honestly where it sits in the funnel. See `references/audience-and-funnel.md`.
6. **Draft slide copy**, then render. Structure in `references/carousel-production.md`; the deck format, design system and renderer in `references/rendering-and-design-system.md`. Write `deck.json` and run `scripts/render_slides.py` — do not lay slides out by hand, and always look at the rendered PNGs before delivering. For a distinctive cover, route that one slide through the `canvas-design` skill and keep the interior systematic.
7. **Draft the caption** for reach. Mechanics in `references/caption-and-reach.md`.
8. **Calibrate tone to the market** and present the user a genuine choice. Never pick the register silently. See `references/tone-calibration.md`.
9. **Run the gates below**, then deliver with the evidence table.

## Evidence Rule

A claim in a slide or caption is publishable only when `sources.json` carries, for that claim: the instrument name, the article or section reference, the source URL, the access date, and the source status. Anything else is cut.

Never cite a source that was not opened and read. A search result snippet, a news summary, a catalogue listing, or a model's recollection of a regulation is **not** a source — mark it `not_run` and go read the instrument, or drop the claim.

Never state an effective date, deadline, or numeric threshold that was not read directly in the instrument text.

Every delivered artifact is reported by path. If a render did not happen, say `not_run` — do not describe a slide as produced because it was planned.

## Failure Modes And Retry Policy

Use this closed taxonomy. Full table and escalation paths in `references/failure-modes.md`.

| failure_mode | Trigger here | Retry limit |
| --- | --- | --- |
| `source_unreachable` | Primary source is paywalled, blocked, or offline. | Try 1 alternate official mirror, then block. |
| `hallucinated_source` | A claim traces to recollection rather than a read document. | No retry — cut the claim. |
| `stale_data` | Instrument may be superseded or the effective date has passed. | 1 re-verification, then mark manual-review-required. |
| `unsupported_claim` | Source does not say what the draft slide says. | 1 rewrite against the text, then cut. |
| `ambiguous_scope` | Topic could mean several different instruments. | Ask once, narrowly. |
| `image_rights_unclear` | Cover or slide imagery may be licensed. | No retry — block publication until confirmed. |
| `render_failed` | Image or PDF generation did not complete. | 2 attempts, then deliver copy-only and say so. |
| `partial_output` | Some slides rendered, others missing. | 1 forward-fix, then report the gap. |

## Risk Gates

Applies on the deep path. Detail in `references/failure-modes.md`.

- **Citation gate.** Every factual claim maps to an article reference with an access date. Unmapped claim → cut.
- **Currency gate.** Instrument confirmed in force as of the access date; superseded instruments named. Regulatory, tax, and financial claims are treated as high freshness risk — recollection is never sufficient.
- **Qualifier gate.** If the regulation has a condition that changes who is protected, the post states it. Publishing the headline protection without its trigger is misleading even when every individual number is right.
- **No-advice gate.** The post informs; it does not tell readers what to do about their legal or financial position. No professional overclaim.
- **Image rights gate.** Any third-party or licensed image is confirmed cleared for commercial social use before publication. Currency, official emblems, and stock photography all trip this.
- **Human choice gate.** Tone register and the final compliment/closing line are presented as options with a recommendation. The human picks. See `references/tone-calibration.md`.

## Tool Verification

Verify before relying on any of these; declare the state honestly.

| Capability | Needed for | If unavailable |
| --- | --- | --- |
| Web fetch of the source domain | Reading the primary instrument | Ask the user to paste the text or supply the PDF. Do not route around a blocked domain. |
| Pillow | Slide PNGs at 1080×1350 via `scripts/render_slides.py` | Deliver slide copy as markdown, mark renders `not_run`. |
| PDF encoder (Pillow JPEG plugin, or ImageMagick) | Document-post carousel | The renderer falls back automatically; if all paths fail it reports `not_run` and the PNGs still ship as an image post. |
| `canvas-design` skill | Art-directed cover only | Use the system cover from `render_slides.py`. |
| Web search | Locating the instrument when no URL is given | Ask the user for the source directly. |

States: `verified` · `assumed` · `missing` · `fallback` · `manual_approval_required` · `hard_blocked`. Never install packages to fill a gap without explicit approval; never auto-approve unpinned versions.

Do not attempt to fetch a domain through an alternate method after a fetch tool reports it blocked. Report it and ask for the content.

## Final Review

Before delivering, run the user-journey pass in `references/final-review.md`. Score 0–2 across: source integrity · qualifier clarity · slide legibility · caption reach mechanics · audience honesty. Below 9/10, revise rather than deliver. Cite evidence for every deduction — a review that says "looks good" is not a review.

Run `scripts/check_citations.py` and `scripts/lint_skill.py` and keep the output as evidence.

## References

- `references/source-and-citation-policy.md` — what counts as a source, citation format, instrument naming.
- `references/carousel-production.md` — slide structure, specs, the qualifier spine, cover design.
- `references/rendering-and-design-system.md` — deck format, palette, type, the enforced legibility floor, and when to use `canvas-design`.
- `references/caption-and-reach.md` — caption shape, link placement, document vs image post, first-hour engagement.
- `references/tone-calibration.md` — regional register, the three-temperature method, why first-person wins.
- `references/audience-and-funnel.md` — audience mapping and the authority-vs-leadgen distinction.
- `references/failure-modes.md` — full taxonomy, retry policy, risk gates.
- `references/final-review.md` — review rubric and output format.

## Delivery Report

Report every time:

- artifact paths (slides, PDF, caption, sources, audience note)
- source instrument, article references used, access date, source status
- tool states: verified / assumed / missing / fallback / blocked
- checks run and their results
- review score with evidence for deductions
- gates skipped and residual risk
- what the human still has to decide before publishing
