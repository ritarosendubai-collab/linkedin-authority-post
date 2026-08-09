# Changelog

All notable changes to this project are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] — 2026-08-09

First public release. Extracted from a working LinkedIn content practice and hardened into a reusable skill.

### Added

- `SKILL.md` routing layer with inputs, outputs, explicit non-goals, route selection, and a delivery report format.
- Eight references covering source and citation policy, carousel production, caption and reach mechanics, rendering and design system, tone calibration, audience and funnel analysis, failure modes, and the final review gate.
- `check_citations.py` — validates a `sources.json` against the citation gate. Rejects unread sources, missing article references, and low-confidence claims. Accepts single and compound references.
- `lint_skill.py` — validates skill structure, dangling reference links, script syntax, and the presence of the five production gates. Detects keyword-only gates: gate language with no supporting references.
- `render_slides.py` — renders `deck.json` to 1080×1350 PNGs and a Flate-compressed PDF. Enforces a 36px legibility floor and fails rather than shrinking type below it.
- Eight eval cases: four positive and edge, three negative, one regression.
- Worked example built from an invented regulation, verified by CI against the citation gate.
- CI across Python 3.9, 3.11 and 3.13, including a scan that fails the build on leaked emails, local paths, or credentials.
- Caption and slide-copy templates.

### Design decisions worth recording

- **The legibility floor is enforced, not advised.** Tools that silently shrink type produce slides nobody can read on a phone, and the failure is invisible until publication. If copy will not fit at 36px, the run fails and the copy must be cut.
- **The citation gate is not waivable.** A sourced-looking post with unsourced claims is worse than no post.
- **Automation is out of scope permanently.** No sending, commenting, connecting, or scraping. LinkedIn's User Agreement prohibits automated messaging and unauthorised automated access; shipping it publicly would put an account-restriction risk on every installer.
- **The PDF writer is hand-rolled.** Pillow routes RGB PDFs through a JPEG encoder absent from some builds and writes paletted images uncompressed; ImageMagick's PDF coder is blocked by policy on many hosts. A 12-slide deck came to 33.8 MB before this change and 0.53 MB after.
- **Heads are anchored, not centred.** Centring balances individual slides but makes headings jump during a swipe.

### Known limitations

- The eval suite is a specification. No runner ships with this repo and no recorded runs are included, so behaviour under an independent executor is unverified.
- Trigger precision and recall have not been measured.
- Platform mechanics — the external-link reach penalty, document-post behaviour — reflect observed behaviour at time of writing and carry no dated citation.
- The regional tone guidance is a starting hypothesis to check against a real feed, not a measured claim.

[0.1.0]: https://github.com/ritarosendubai-collab/linkedin-authority-post/releases/tag/v0.1.0
