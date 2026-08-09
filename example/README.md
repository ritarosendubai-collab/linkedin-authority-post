# Worked Example

A complete output set, so you can see the shape before running the skill yourself.

**The regulation here is invented.** "Example Central Bank", "Circular No. 2 of 2026", the article numbers, and the `example-regulator.test` domain are all fabricated for illustration. Do not cite any of it. It exists to show the artifact structure and how the qualifier drives the deck — nothing more.

## What a run produces

| File | What it is |
| --- | --- |
| `sources.json` | Every claim mapped to an article reference, with URL, access date, and status. Passes `check_citations.py`. |
| `slides/copy.md` | Per-slide copy, ready to render at 1080×1350. |
| `caption.md` | The post caption. |
| `audience-note.md` | Who it helps, who engages, who it is not for, funnel position, follow-up. |
| `decision-packet.md` | The tone options presented and what the human chose. |

In a real run you would also get `slides/*.png` and `carousel.pdf`. Renders are omitted here because rendering is delegated to the runtime.

## Verify it

```bash
python3 ../scripts/check_citations.py sources.json --slides 11
```

Exits 0. CI runs this on every push, so the example cannot silently drift out of compliance with the skill's own citation gate.

## What to look at first

`slides/copy.md`, slide 07. That is the qualifier — the condition that changes who is actually protected. Every other slide in the deck is arranging context around it. If you take one structural idea from this example, take that one: find the qualifier, build the deck around it, and the post stops being a summary.
