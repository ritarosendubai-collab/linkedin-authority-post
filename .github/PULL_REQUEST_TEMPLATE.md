# What this changes

<!-- One or two sentences. What behaves differently after this merges? -->

## Why

<!-- What is this based on? A run that went wrong, platform behaviour you observed and when,
     a market whose conventions differ, a source you can cite. For a pure wording or
     refactor change, say so — that is a fine reason on its own. -->

## Type

- [ ] Guidance change (a reference)
- [ ] Script change
- [ ] New eval case
- [ ] Docs / wording
- [ ] Other

## Checks

```
python3 scripts/lint_skill.py .
python3 scripts/check_citations.py evals/fixtures/sources.valid.json --slides 11
python3 scripts/check_citations.py evals/fixtures/sources.invalid.json   # must exit 1
python3 scripts/check_citations.py example/sources.json --slides 11
python3 -m py_compile scripts/*.py
```

- [ ] All of the above pass locally
- [ ] If I touched `render_slides.py`, I rendered a deck **and looked at the output**
- [ ] If I added a reference, `SKILL.md` routes to it
- [ ] No client-confidential material, emails, local paths, or credentials in the diff

## Gates

The citation gate, the 36px legibility floor, and the automation scope boundary are load-bearing — they prevent failures that stay invisible until something is published.

- [ ] This does not weaken any of them
- [ ] It does, and I have argued the case above (an issue first is usually the faster route)

## Anything you are unsure about

<!-- Genuinely useful. Flagging a part you are not confident in gets a better review
     than presenting the whole thing as finished. -->
