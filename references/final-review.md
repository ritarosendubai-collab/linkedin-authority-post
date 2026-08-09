# Final Review Gate

Run after the citation check and before delivery. Per-claim checking can pass while the post as a whole is unusable — this pass reads the deck the way a stranger scrolling their feed would.

Files existing is not completion. A review that does not cite specifics is not a review.

## Rubric

Score each 0–2. Total /10. Pass at ≥ 9.

**Source integrity (0–2).** Every claim maps to an article reference with an access date. No claim rests on a summary, snippet, or recollection. Instrument status confirmed.
*0* — any unsourced factual claim. *1* — all sourced but status or access date missing. *2* — complete and current.

**Qualifier clarity (0–2).** The condition that changes who is protected is present, prominent, and in plain language.
*0* — absent, or buried on a late slide. *1* — present but hedged or unclear. *2* — it is the spine of the deck.

**Slide legibility (0–2).** Type readable at phone size, one idea per slide, article reference consistently placed, no copy overflow, cover earns the swipe.
*0* — copy does not fit or the cover is inert. *1* — readable but a slide is overloaded. *2* — clean throughout.

**Caption reach mechanics (0–2).** Hook in the first line, link placed deliberately, closing question aimed at a specific group and answerable in a word, three hashtags, caption does not duplicate the carousel.
*0* — link mid-caption or generic question. *1* — sound but the question is soft. *2* — all mechanics correct.

**Audience honesty (0–2).** The three audience groups are named, the funnel position is stated plainly, and the follow-up is proposed.
*0* — no audience note, or the post is implied to be lead-gen when it is not. *1* — audiences named, funnel caveat missing. *2* — complete and honest.

## Output

Save `review.json`:

```json
{
  "overall_score": 9,
  "review_mode": "inline_fallback",
  "rubric": {
    "source_integrity": 2,
    "qualifier_clarity": 2,
    "slide_legibility": 1,
    "caption_reach": 2,
    "audience_honesty": 2
  },
  "evidence": [
    "Slide legibility docked: slide 6 carries three obligations where the structure calls for one; body type dropped to 30px to fit."
  ],
  "gate_threshold": 9,
  "passed": true,
  "revision_instructions": ["Split slide 6 into two slides, restore 36px body type."]
}
```

`review_mode`: `subagent` when an independent reviewer is available and authorized · `inline_fallback` when the same agent reviews its own work in a separated pass, which is weaker isolation and must be labelled as such · `skipped` only with a stated reason. Skipped is not passed.

Below 9, revise and re-run. Stop after two revision cycles and report what remains unfixed rather than looping.

## Reader Pass

Before scoring, read the deck once as a stranger. Three questions:

1. After the cover alone — would I swipe?
2. After slide 3 — do I know whether this applies to me?
3. At the end — do I know what to do next, and could I explain the qualifier to a colleague?

A "no" to any of these is a structural problem, not a copy problem, and no amount of line editing will fix it.
