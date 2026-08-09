# Rendering And Design System

Slide copy is data; the deck is generated from it. When a number turns out to be wrong, you change one field and re-run — you do not rebuild eleven slides by hand. A deck that has to be hand-rebuilt for a one-word fix ships with the error still in it.

## Pipeline

1. Write `deck.json` — one object per slide, typed.
2. `python3 scripts/render_slides.py deck.json --out slides/ --pdf carousel.pdf [--fonts DIR]`
3. Inspect the rendered PNGs before delivering. Rendering without looking is not a review.

The renderer requires Pillow. Everything else in this repo is standard library.

## deck.json

```json
{
  "theme": "neutral-consultancy",
  "slides": [
    {"n": 1, "type": "cover", "kicker": "…", "hero": "AED 80,000",
     "sub": "is not a cheque.", "standfirst": "…", "masthead": "Source: …"},
    {"n": 2, "type": "claim", "head": "…", "body": "…", "ref": "para 1-2"},
    {"n": 7, "type": "turn",  "head": "…", "body": "…", "ref": "para 4"},
    {"n": 8, "type": "claim", "head": "…", "body": "…", "callout": "…", "ref": "para 4"},
    {"n": 9, "type": "list",  "head": "…", "items": ["…", "…"], "ref": "para 10-11"},
    {"n": 11, "type": "statement", "body": "…", "ref": ""},
    {"n": 12, "type": "closing", "question": "…", "source": "…", "contact": "…"}
  ]
}
```

Types: `cover` · `claim` · `turn` · `list` · `statement` · `closing`. `turn` and `cover` render reversed on the accent field, which is what makes the qualifier slide read as the pivot of the deck without any extra decoration.

## The Legibility Floor Is Enforced, Not Advised

The renderer shrinks type to fit, but stops at **36px** and fails the run with a non-zero exit rather than going below it.

This is deliberate. Every carousel tool that silently shrinks type produces slides nobody can read on a phone, and the failure is invisible until it is published. If a slide will not fit at 36px, the copy is too long — cut it. That is the fix, and the script will not let you avoid it.

Overflowing lists and callouts fail the same way.

## Palette — `neutral-consultancy`

| Role | Hex | Use |
| --- | --- | --- |
| Paper | `#FBFAF8` | Interior background. Warm off-white, not pure white — pure white glares on a phone at full brightness. |
| Ink | `#14171A` | Body and headings. Near-black rather than black; softer on screen, and reads as considered. |
| Muted | `#6E6A63` | Footer references and slide numbers. |
| Rule | `#D8D5D0` | Hairlines. Never heavier than 2px. |
| Accent | `#2F4F45` | Cover and turn field, callout blocks, the em-dash list marker. |
| Accent ink | `#FBFAF8` | Type on the accent field. |

One accent, used sparingly. The restraint is the aesthetic — a consultancy deck reads as authoritative because it withholds, not because it decorates.

### On imitating a named firm

Requests for "Deloitte style", "McKinsey style", or "BCG style" almost always mean the *genre*: restrained palette, generous whitespace, strong typographic hierarchy, hairline rules, data-forward, no ornament. Build that — it is a legitimate design language and this system is exactly it.

Do not reproduce a named firm's actual brand identity: their specific corporate colour, logo, wordmark, or publication furniture. A post going out under someone else's name that looks like a Deloitte publication implies an association that does not exist, and that is a trademark problem rather than a taste one. The genre is available to everyone. The identity is not.

The same applies to the subject of the post: cite the issuing authority by name, never place its emblem or logo on the slides. On a commercial brand post that reads as endorsement.

## Type

Three roles, resolved from `--fonts` with a system fallback chain:

- **display / head** — Instrument Sans Bold, falling back to Work Sans Bold, then DejaVu Sans Bold.
- **body** — Work Sans Regular, falling back to Instrument Sans, then DejaVu Sans.
- **mono** — IBM Plex Mono, falling back to JetBrains Mono, then DejaVu Sans Mono.

Monospace for source anchors and slide numbers is doing real work: it signals "reference material" instantly and separates the citation layer from the argument layer without a rule or a box.

If a font is missing the renderer warns and continues on the fallback. It does not fail — a legible deck in the wrong face beats no deck.

The `canvas-design` skill ships an OFL font library that works well here; point `--fonts` at its `canvas-fonts` directory.

## Layout

- 1080 × 1350, 88px margins.
- Heads are anchored at a **consistent vertical position across slides**. Centring each slide's content would balance individual slides better but makes headings jump around during a swipe. Report decks anchor; so does this.
- Whitespace below short slides is intentional. Do not fill it.
- Footer: hairline rule, source anchor bottom-left, `NN/TT` bottom-right. Present on every slide except the cover and closing.
- The article or paragraph anchor on every claim slide is not decoration. It is what makes a screenshotted slide still verifiable when it travels alone.

## Using canvas-design For The Cover

The interior must carry legible copy and citations, which is not what `canvas-design` is for — that skill is explicitly "90% visual design, 10% essential text" and aimed at art objects. Routing the whole deck through it produces beautiful slides that fail as an explainer.

The cover is a different problem. It carries five words and one number, and it decides whether anyone swipes. That is a poster.

So: when the user wants a distinctive opener, generate the cover through `canvas-design` — its philosophy step first, then the visual expression — and render slides 2–N through this system. Keep the accent colour shared between them so the deck still reads as one object.

Two constraints on the art cover: the hero number and the swipe-driving line must remain legible at phone size, and it still needs the source line. An art cover that hides what the post is about wins attention and loses the reader on slide 2.

Cover art is the one place a human should look before publishing. Everything else in this pipeline is deterministic and can be trusted to a re-run; a generated cover cannot.
