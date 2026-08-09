# LinkedIn Authority Post

[![checks](https://github.com/ritarosendubai-collab/linkedin-authority-post/actions/workflows/checks.yml/badge.svg)](https://github.com/ritarosendubai-collab/linkedin-authority-post/actions/workflows/checks.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)

An agent skill for turning a regulation, policy change, or industry development into a **sourced LinkedIn carousel and caption** — where every factual claim traces to an article reference in the primary instrument, and the post says the thing most summaries leave out.

Works with any agent runtime that loads `SKILL.md` files (Claude Code, Cowork, Codex, and similar).

## Why This Exists

Most "explainer" posts about a new regulation are assembled from news coverage and say the same five things. They are accurate enough and forgettable, and occasionally they are wrong in public.

This skill enforces three habits that change the result:

**Read the instrument, not the coverage.** A news article, a law firm alert, a search snippet, and a model's recollection are all pointers. None of them may be cited, and no number reaches a slide on their authority.

**Put the article reference on every slide.** Not on a sources slide at the end — on the slide making the claim. It is the strongest credibility signal in a regulatory carousel, and it makes the deck screenshot-safe: any slide that travels alone still carries its citation.

**Find the qualifier.** Nearly every regulation has a condition that changes who is actually protected — a clock that starts later than readers assume, a carve-out, a threshold. That qualifier is the post. Listing headline protections without their trigger is misleading even when every individual number is correct.

## What It Produces

```
slides/            numbered copy + rendered PNGs at 1080×1350
carousel.pdf       same deck assembled for a document post
caption.md         caption with source line and closing question
sources.json       every claim → article reference, URL, access date
audience-note.md   who it helps, who engages, who it isn't for, funnel position
decision-packet.md options presented to the human and what they chose
```

## Install

The skill is a plain directory of markdown plus three Python scripts — two of them dependency-free. How you install it depends on your runtime.

**Claude Code** — clone into the skills root:

```bash
git clone https://github.com/ritarosendubai-collab/linkedin-authority-post.git \
  ~/.claude/skills/linkedin-authority-post
```

Project-scoped instead of global: clone to `.claude/skills/` inside the repo you're working in.

**Codex / Gemini / other `SKILL.md` runtimes** — clone into whatever directory that runtime scans for skills. Check its docs for the path; the skill itself needs no adaptation.

**Claude Cowork** — Cowork loads *saved skills*, not directories, so cloning does nothing. Ask Claude to install it and point at this repo. Note that a saved skill stores a single `SKILL.md`: the eight references will not come with it, so either ask for them to be inlined into the body, or use the skill in a runtime that reads directories.

**No runtime at all** — the references are readable on their own. `carousel-production.md` and `tone-calibration.md` are useful as a checklist even if you never wire the skill up.

### Requirements

Python 3.9+. `lint_skill.py` and `check_citations.py` are standard library only. `render_slides.py` needs Pillow:

```bash
pip install Pillow
```

CI runs the standard-library scripts on 3.9, 3.11 and 3.13. The markdown has no requirements.

## Use

```
Build a LinkedIn carousel about <regulation>. Here's the source: <url or PDF>.
My audience is <ICP>.
```

The skill will read the instrument, extract and map claims, find the qualifier, draft slides and caption, map the audience, and stop to let you choose the tone register. It will not choose your voice for you.

See [`example/`](example/) for a complete output set from an invented regulation — slide copy, caption, sources, audience note, and decision packet.

## Verify

```bash
python3 scripts/lint_skill.py .                        # structure and gates
python3 scripts/check_citations.py example/sources.json --slides 11
```

Both exit non-zero on failure. [`.github/workflows/checks.yml`](.github/workflows/checks.yml) runs them on every push across three Python versions, plus a scan that fails the build if an email address, local path, or credential reaches the repo. Fixtures for the citation checker are in `evals/fixtures/`.

## Scope

**In scope:** content production — research, slide copy, caption, tone calibration, audience mapping, reach mechanics.

**Explicitly out of scope:** sending messages, posting comments, sending connection requests, scraping profiles, or automating any interaction with another user's account. LinkedIn's User Agreement prohibits automated messaging and unauthorized automated access; a tool that ships that behaviour puts an account-restriction risk on everyone who installs it.

If interaction workflows are ever added, they must be **draft-only** — the skill prepares text, a human reviews and sends. That is a fixed policy of this repository, not a default to be toggled.

## Regional Tuning

The tone calibration reference is written from UAE/Gulf B2B experience, where warmth about institutions is conventional and an understated register can read as faint praise. The method — read the actual feed, offer three temperatures, let the human choose, prefer the personal register — is portable. The regional observation is a starting hypothesis to check against the user's real feed, not a rule.

## Structure

```
SKILL.md                              routing layer
example/                              complete worked output (invented regulation)
references/
  source-and-citation-policy.md       what counts as a source; citation format; rights
  carousel-production.md              qualifier spine, deck structure, specs, cover design
  caption-and-reach.md                caption shape, link placement, document vs image post
  tone-calibration.md                 regional register, three-temperature method
  audience-and-funnel.md              audience mapping, authority vs lead-gen
  failure-modes.md                    closed taxonomy, retry limits, risk gates
  rendering-and-design-system.md      deck format, palette, type, legibility floor
  final-review.md                     review rubric
scripts/
  lint_skill.py                       structure and gate linter
  check_citations.py                  citation gate validator
  render_slides.py                    deck.json -> 1080x1350 PNGs + compressed PDF
assets/
  caption-template.md
  slide-copy-template.md
evals/
  evals.json                          8 cases: positive, edge, negative, regression
  fixtures/
```

## Limitations

- Slides render deterministically from `deck.json`, so a corrected number is a re-run rather than a rebuild. The renderer enforces a 36px legibility floor and **fails** rather than shrinking type below it — if a slide won't fit, cut the copy.
- Reach guidance is mechanical — post format, link placement, reply timing. It is not a forecast, and the skill will not predict engagement numbers.
- The eval suite defines expectations but ships no recorded runs. Behaviour under an independent executor is unverified; treat the cases as a specification, not as evidence. The CI checks verify structure and the citation gate — they do not verify that an agent follows the skill.
- The worked example uses an invented regulation. It demonstrates artifact structure, not a real legal position.
- Platform mechanics change. The link-penalty and document-post behaviours reflect observed platform behaviour at time of writing and are worth re-checking.

## Contributing

The most valuable contribution is a report that the skill got something wrong on a real task — see [CONTRIBUTING.md](CONTRIBUTING.md). Conduct expectations are in [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md); security reporting in [SECURITY.md](SECURITY.md); release history in [CHANGELOG.md](CHANGELOG.md).

## Licence

MIT — see [LICENSE](LICENSE).
