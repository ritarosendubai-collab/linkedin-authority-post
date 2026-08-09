# Source And Citation Policy

The whole value of an authority post is that it is right. One wrong deadline in a carousel about deadlines destroys the credibility the post was built to earn — and on LinkedIn the correction is public.

## What Counts As A Source

**Accepted.** The instrument itself: the regulation, circular, rulebook page, statute, standard, official gazette entry, court decision, or the issuing authority's own published notice. A PDF of it. A screenshot of the relevant article, if the user supplies it.

**Not accepted, ever.**

- A news article *about* the regulation.
- A law firm's client alert summarising it.
- A search-result snippet.
- A LinkedIn post by someone else about it.
- The model's recollection of what the regulation says.
- A catalogue or index entry that lists the instrument without its text.

The second list is useful for *finding* the instrument. None of it may be cited, and none of it may be the basis for a number on a slide.

## Evidence Ladder

Reach the top before publishing. Anything below step 5 is not publishable.

1. `instrument_identified` — you know its name and number.
2. `source_located` — you have a URL or document for the instrument itself.
3. `source_opened` — the document was actually fetched and read.
4. `articles_extracted` — the specific articles supporting each claim are quoted or paraphrased from the text.
5. `status_confirmed` — in force, effective date read from the text, superseded instruments identified.
6. `claims_mapped` — every slide number and deadline maps to an article.
7. `qualifier_identified` — the condition that changes who is protected is found and stated.
8. `accepted` — publishable.

If the source cannot be opened, stop at step 2 and report `source_unreachable`. Do not proceed on a summary.

## Citation Format

`sources.json`:

Illustrative shape only — the values below are invented, not a real instrument. Fill from the document you actually read.

```json
{
  "instrument": "Example SME Customer Protection Regulation",
  "instrument_number": "Circular No. 2 of 2026",
  "issuer": "Example Central Bank",
  "url": "https://rulebook.example-regulator.test/...",
  "access_date": "2026-08-09",
  "source_status": "verified",
  "effective_date": "2026-09-13",
  "supersedes": ["Circular No. 1/2021, dated 26/01/2021"],
  "claims": [
    {
      "claim": "Banks must open an SME account within three business days.",
      "article": "Art. 4.2",
      "slide": 3,
      "quote_or_paraphrase": "paraphrase",
      "confidence": "high"
    },
    {
      "claim": "The three-day clock starts when the file is complete, not on application.",
      "article": "Art. 4.3",
      "slide": 5,
      "quote_or_paraphrase": "paraphrase",
      "confidence": "high"
    }
  ]
}
```

`source_status` values: `verified` (opened and read) · `partial` (some articles read, others not) · `user_provided` (user supplied the text; you did not fetch it) · `unreachable` · `stale_risk` · `superseded`.

`confidence`: `high` (read directly in the text) · `medium` (inferred from the text's structure) · `low` (do not publish).

## On Every Slide

Put the article reference on the slide that makes the claim. Not just on a sources slide at the end — on the slide itself, small, in a consistent position. This is the single strongest credibility signal in a regulatory carousel, and it makes the deck screenshot-safe: any slide that travels alone still carries its citation.

The caption carries the instrument name, number, and the issuer's domain.

## Instrument Naming For Mixed Audiences

Official shorthand is precise and often illegible to half the audience.

A regulator's own citation format — `C 2/2026`, `SI 2024/113`, `Reg. (EU) 2016/679` — reads instantly to specialists and means nothing to the business owners the post is usually for. Specialists are not confused by the long form; non-specialists are completely blocked by the short form. So the long form wins.

Write **"Circular No. 2 of 2026"** on the slides. Keep the official abbreviation for the sources line if you want the specialist signal.

Watch for instrument-type words used both narrowly and broadly in the same document. Many rulebooks define "Regulation" expansively — covering resolutions, circulars, rules, instructions, standards, and notices — while also using "Circular" for the specific instrument. Both words then appear in one citation without contradiction. If a reader could reasonably think that is an error, spend one line explaining it; a reader who spots an apparent inconsistency and is not given the explanation assumes the author did not know.

## Status And Currency

Regulatory, tax, financial, pricing, and deadline claims are high freshness risk. Always:

- read the effective date in the text, never from a summary;
- check whether the instrument has been amended or replaced since publication;
- name what it supersedes, if anything — this is often the most interesting slide;
- record the access date and put it in `sources.json`.

If the instrument was published more than a few months before the post and you cannot confirm it is unamended, mark `stale_risk` and tell the user to confirm before publishing. Do not quietly assume currency.

## Quoting And Rights

Paraphrase obligations; quote sparingly and only short passages. Do not reproduce substantial portions of a copyrighted standard — many technical standards are copyrighted even when compliance is mandatory.

Never copy another creator's slide layout, illustration set, or post structure. Reference for principle, build original execution.

## Imagery Rights

Before publication, confirm every image is cleared for commercial social use. Common traps:

- **Currency and banknotes.** Editorial use of currency imagery is usually fine; many jurisdictions restrict reproduction, and stock licences often exclude commercial use. If the image came from a stock site, confirm the licence covers a commercial brand post.
- **Official emblems, crests, and logos** of regulators or governments. Using a regulator's masthead can imply endorsement.
- **Stock photography** under an editorial-only licence.
- **Screenshots of paywalled documents.**

If rights are unclear, this is `image_rights_unclear` — block publication until confirmed. Do not publish and fix later; the post is the exposure.
