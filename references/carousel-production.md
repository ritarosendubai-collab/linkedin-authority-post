# Carousel Production

## The Qualifier Spine

Before designing anything, find the qualifier.

Nearly every regulation has a condition that changes who is actually protected — a trigger, a carve-out, an exemption, a clock that starts later than readers assume. Examples of the shape:

- a deadline that starts when the file is *complete*, not when it is submitted;
- a protection that is waived where another compliance regime applies;
- a right that attaches only above or below a size threshold;
- an obligation on the institution that the customer must still qualify for.

This qualifier is the post. Everyone else summarising the same regulation will list the headline protections. The qualifier is what makes a reader stop, and it is what makes the post *useful* rather than merely accurate.

Structure the deck so the headline protections come first and the qualifier lands in the middle as a turn — "here's the part most people miss" — followed by what the reader should have ready. A deck that only lists protections is a press release. A deck that lists protections and then explains why they might not apply to you is worth swiping through.

**Integrity note.** Stating headline protections without their trigger is misleading even when every individual number is correct. The qualifier gate exists for this.

## Deck Structure

A 9–12 slide deck that works:

1. **Cover.** The stake, not the topic. See below.
2. **What changes.** One line of context: who issued it, when it takes effect.
3–6. **The protections.** One per slide. Number, obligation, article reference. Short.
7. **The turn.** "Here's the part most people miss." The qualifier.
8. **What that means.** The practical consequence of the qualifier.
9. **Readiness checklist.** What the reader should have ready, concretely. Name the item that most applications get wrong.
10. **The considered close.** Optional — a fair, warm observation about the change itself. See `tone-calibration.md`.
11. **Closing slide.** The question, the source line, contact.

Keep one idea per slide. If a slide needs two sentences of explanation, it is two slides.

## The Cover

The cover decides whether anyone swipes.

**Lead with the stake, not the subject.** "35 DAYS until X" beats "New SME Banking Regulation Explained." A countdown, a number, or a consequence as the hero; the topic demoted to small type underneath. The subject line is orientation, not the headline.

**Give type a clean field.** Photographic covers usually fail because text sits on a busy or washed-out image. A hard block of solid colour behind the type outperforms a soft gradient fade: it reads as deliberate design rather than a filter, it hides any baked-in text in the source image, and it matches interior slides so the deck feels like one object.

**Fix the image before you fix the layout.** Washed-out, low-contrast source images flatten everything on top of them. Crop tighter on the subject, lift contrast, pull out milkiness. A tight crop of a detail usually beats the whole object.

**Bookend the deck.** Carry a treated crop of the cover image into the closing slide — as a band, a tint, or a corner. The deck then reads as designed rather than assembled.

## Specs

- **1080 × 1350** (4:5 portrait). Takes the most vertical feed space on mobile. Not square, not 1080×1080.
- Numbered filenames in swipe order: `01-cover.png`, `02-context.png`, … Zero-padded, so they sort correctly everywhere.
- Also assemble `carousel.pdf` in the same order for the document-post option.
- Minimum body type ~36px at this canvas size. If copy does not fit at that size, the copy is too long — cut it, do not shrink the type.
- Consistent position for the article reference on every claim slide.
- High contrast between text and background. Assume a phone screen in daylight.
- If a masthead or issuer bar is used, keep it consistent across slides — and check the emblem rights question in `source-and-citation-policy.md`.

## Slide Copy Rules

- Numbers as numerals, not words. "Three business days" → "3 business days" on a slide; spell out in the caption where it reads better.
- One obligation per slide.
- Active voice, present tense for what the rule does.
- No slide-filler ("In today's fast-moving regulatory environment…").
- Article reference on every slide that makes a claim.
- Do not put a call to action on every slide. One, at the end.

## Rendering

Render deterministically where possible — HTML/CSS to PNG, or a scripted image pipeline — so the deck can be regenerated when a number changes. A deck that has to be hand-rebuilt for a one-word fix will ship with the error in it.

If rendering is unavailable, deliver `slides/copy.md` with the full per-slide copy and mark renders `not_run`. Copy is the valuable part; the user can lay it out. Never claim slides exist that were not produced.
