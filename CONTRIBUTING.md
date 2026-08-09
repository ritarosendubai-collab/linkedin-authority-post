# Contributing

Thanks for considering a contribution. This repo is a *skill* — instructions an AI agent follows — so contributions are a little different from a normal codebase. What matters most is whether a change makes the agent behave better, and whether you can show that it does.

## What Makes A Good Contribution Here

The references encode judgment: what counts as a source, how to find the qualifier in a regulation, how tone shifts by market. The most valuable contributions are usually not new features but **corrections drawn from real use** — a case where the skill gave bad guidance, a market whose register the tone reference gets wrong, a source type the citation policy does not handle.

If you have run this skill and it produced something wrong, that is worth an issue even if you have no fix.

## Ground Rules

**Evidence over assertion.** This applies to the repo itself, not just its output. If you change guidance, say what it is based on: a run that failed, a platform behaviour you observed and when, a source you can point to. "I think this reads better" is a fine reason for a wording change and not a sufficient reason to change a gate.

**Do not weaken the gates casually.** The citation gate, the 36px legibility floor, and the scope boundary on automation are load-bearing. They exist because the failures they prevent are invisible until something is already published. If one is genuinely wrong, argue the case in an issue first.

**Keep the scope boundary.** This skill does content production. It does not send messages, post comments, send connection requests, or automate interaction with other users' accounts. Pull requests adding those will be declined regardless of implementation quality — see [SECURITY.md](SECURITY.md) for the reasoning.

**No brand identity replication.** Design contributions are welcome. Reproducing a named firm's corporate colour, logo, wordmark, or publication furniture is not — the genre is available to everyone, the identity is not.

## Before You Open A Pull Request

```bash
python3 scripts/lint_skill.py .
python3 scripts/check_citations.py evals/fixtures/sources.valid.json --slides 11
python3 scripts/check_citations.py evals/fixtures/sources.invalid.json   # must exit 1
python3 scripts/check_citations.py example/sources.json --slides 11
python3 -m py_compile scripts/*.py
```

CI runs these on Python 3.9, 3.11 and 3.13, plus a scan that fails the build if an email address, local path, or credential reaches the repo. All of it must pass.

If you touched `render_slides.py`, render a deck and **look at the output**. Rendering without inspecting is not testing.

## Changing A Reference

- Keep `SKILL.md` a routing layer. Detail belongs in `references/`. The linter warns past 500 lines.
- Every `references/*.md` file you add must be linked from `SKILL.md`, or the linter fails.
- The five production gates — failure modes, retry policy, evidence rule, tool verification, final review — must remain present in the body or a linked reference.

## Changing The Evals

`evals/evals.json` is a specification, not a test suite: no runner ships with this repo. Cases should be realistic prompts, not synthetic ones, and each needs concrete expectations that a reviewer could check by reading an output. Negative cases matter as much as positive ones.

## Style

British spelling in prose. Sentences over bullet fragments where the reasoning matters — a reader needs to understand *why* a rule exists to apply it to a case the rule did not anticipate. Standard library only for `lint_skill.py` and `check_citations.py`; `render_slides.py` may use Pillow.

## Reporting Problems

Open an issue. If the skill produced something wrong, include the prompt, what it produced, and what it should have done. That is the most useful bug report this project can receive.
