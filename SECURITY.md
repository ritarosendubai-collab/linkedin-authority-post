# Security Policy

## Reporting a Vulnerability

Use GitHub's **private vulnerability reporting** — the "Report a vulnerability" button under this repository's Security tab. That keeps the report private until a fix exists.

Please do not open a public issue for a security problem.

Expect an acknowledgement within a few days. This is a small project maintained alongside other work, so please be patient with fix timelines.

## Scope

This repository contains markdown instructions and three Python scripts. It runs no server, stores no credentials, and makes no network requests. The realistic security surface is small but not empty:

**In scope**

- Code execution or path traversal in `render_slides.py`, `check_citations.py`, or `lint_skill.py` — particularly via a crafted `deck.json` or `sources.json`.
- A crafted deck or sources file causing resource exhaustion.
- Prompt injection: content in a `deck.json`, `sources.json`, or a fetched source that causes an agent following this skill to take actions outside its stated scope.
- Anything in the repo that leaks data belonging to whoever runs it.

**Out of scope**

- The agent runtime you run the skill in. Report those to the runtime's maintainers.
- LinkedIn platform behaviour.
- The accuracy of a post produced using the skill. That is a correctness issue — open a normal issue.

## Prompt Injection

This skill instructs an agent to read external sources: regulations, press releases, official notices. A hostile document could contain text aimed at the agent rather than the reader.

The skill's defence is its evidence discipline — claims must map to article or paragraph references in the source, and instructions found inside a fetched document are data, not commands. If you find a way to make an agent following this skill act on instructions embedded in a source document, that is a genuine vulnerability and worth reporting privately.

## A Note On Scope Boundaries

This skill deliberately does not send messages, post comments, send connection requests, or automate interaction with other users' LinkedIn accounts. LinkedIn's User Agreement prohibits automated messaging and unauthorised automated access, and a widely-installed tool that does it puts an account-restriction risk on everyone who installs it.

Pull requests adding those capabilities will be declined. If you find a way to make the skill perform them despite the stated boundary — for example through a crafted input that reframes the task — please report it privately. That is a security issue, not a feature request.

## Data Handling

The skill writes generated artifacts to the working directory. `.gitignore` excludes them at the repo root, because a real run contains client work: source documents, drafts, audience analysis. Check `git status` before committing after a run.

If you fork this repo and use it commercially, that hygiene is yours to maintain.
