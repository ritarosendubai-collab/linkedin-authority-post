#!/usr/bin/env python3
"""Validate a sources.json produced by the linkedin-authority-post skill.

Enforces the citation gate: every claim maps to an article reference, the
instrument's status and access date are recorded, and no claim ships at low
confidence or from an unread source.

Usage:
    python3 scripts/check_citations.py sources.json [--slides 11] [--json]

Exit codes:
    0  all checks passed (warnings allowed)
    1  one or more errors -- the post is not publishable
    2  the file could not be read or parsed
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import sys
from pathlib import Path

READABLE_STATUSES = {"verified", "partial", "user_provided"}
ALL_STATUSES = READABLE_STATUSES | {"unreachable", "stale_risk", "superseded"}
CONFIDENCES = {"high", "medium", "low"}
REQUIRED_TOP_LEVEL = ["instrument", "issuer", "url", "access_date", "source_status", "claims"]

# "Art. 4.2", "Article 12", "s. 3", "Section 4(1)(a)", "Reg 7", "para 2.1", "para 10-11"
ARTICLE_RE = re.compile(
    r"^(art\.?|article|s\.?|sec\.?|section|reg\.?|regulation|para\.?|paragraph|cl\.?|clause)"
    r"\s*\d+[\w.()\-]*$",
    re.IGNORECASE,
)


def article_ref_ok(value: str) -> bool:
    """Accept single or compound references.

    Press releases and un-numbered notices often need more than one anchor for
    a single claim ("para 6, para 9"), so a comma- or semicolon-separated list
    is valid as long as every component is a well-formed reference.
    """
    parts = [p.strip() for p in re.split(r"[;,]", value) if p.strip()]
    return bool(parts) and all(ARTICLE_RE.match(p) for p in parts)

STALE_AFTER_DAYS = 120


def _fail(msg: str) -> None:
    print(f"error: {msg}", file=sys.stderr)


def load(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        _fail(f"{path} not found")
        raise SystemExit(2)
    except json.JSONDecodeError as exc:
        _fail(f"{path} is not valid JSON: {exc}")
        raise SystemExit(2)


def parse_date(value: str) -> _dt.date | None:
    try:
        return _dt.date.fromisoformat(value)
    except (ValueError, TypeError):
        return None


def check(data: dict, expected_slides: int | None = None) -> dict:
    errors: list[str] = []
    warnings: list[str] = []

    for field in REQUIRED_TOP_LEVEL:
        if not data.get(field):
            errors.append(f"missing required field: {field}")

    status = data.get("source_status")
    if status and status not in ALL_STATUSES:
        errors.append(f"source_status '{status}' is not a recognised value")
    elif status and status not in READABLE_STATUSES:
        errors.append(
            f"source_status '{status}' means the instrument was not read -- "
            "no claim from it is publishable"
        )

    access = parse_date(data.get("access_date", ""))
    if data.get("access_date") and access is None:
        errors.append("access_date must be ISO format (YYYY-MM-DD)")
    elif access:
        age = (_dt.date.today() - access).days
        if age < 0:
            errors.append("access_date is in the future")
        elif age > STALE_AFTER_DAYS:
            warnings.append(
                f"access_date is {age} days old -- re-verify the instrument is unamended"
            )

    effective = data.get("effective_date")
    if effective and parse_date(effective) is None:
        errors.append("effective_date must be ISO format (YYYY-MM-DD)")

    if not data.get("instrument_number"):
        warnings.append("instrument_number is empty -- readers cannot look the instrument up")

    claims = data.get("claims") or []
    if not isinstance(claims, list):
        errors.append("claims must be a list")
        claims = []
    if not claims:
        errors.append("no claims recorded -- nothing to verify")

    seen_slides: set[int] = set()
    for i, claim in enumerate(claims):
        label = f"claim[{i}]"
        if not isinstance(claim, dict):
            errors.append(f"{label} is not an object")
            continue

        text = (claim.get("claim") or "").strip()
        if not text:
            errors.append(f"{label} has empty claim text")
        else:
            label = f"claim[{i}] ({text[:45]}...)" if len(text) > 45 else f"claim[{i}] ({text})"

        article = (claim.get("article") or "").strip()
        if not article:
            errors.append(f"{label} has no article reference -- cut it or find the article")
        elif not article_ref_ok(article):
            warnings.append(
                f"{label} article '{article}' does not look like a section reference"
            )

        confidence = claim.get("confidence")
        if confidence not in CONFIDENCES:
            errors.append(f"{label} confidence must be one of {sorted(CONFIDENCES)}")
        elif confidence == "low":
            errors.append(f"{label} is low confidence -- not publishable")

        qp = claim.get("quote_or_paraphrase")
        if qp not in {"quote", "paraphrase"}:
            warnings.append(f"{label} should mark quote_or_paraphrase")

        slide = claim.get("slide")
        if slide is None:
            warnings.append(f"{label} is not mapped to a slide")
        elif not isinstance(slide, int):
            errors.append(f"{label} slide must be an integer")
        else:
            seen_slides.add(slide)

    # Cover, context, turn, checklist and closing slides legitimately carry no
    # claim, so a low mapped-slide count is only meaningful at the bottom end:
    # a deck whose claims land on fewer than three slides is not a sourced deck.
    if expected_slides and len(seen_slides) < 3:
        warnings.append(
            f"claims land on only {len(seen_slides)} slide(s) of {expected_slides} -- "
            "thin for a sourced deck"
        )
    if expected_slides:
        overflow = sorted(n for n in seen_slides if n > expected_slides)
        if overflow:
            errors.append(f"claims reference slides beyond the deck: {overflow}")

    return {"errors": errors, "warnings": warnings, "claim_count": len(claims)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("sources", type=Path, help="path to sources.json")
    parser.add_argument("--slides", type=int, default=None, help="total slide count")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    report = check(load(args.sources), args.slides)

    if args.as_json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"Citation check: {args.sources} ({report['claim_count']} claims)")
        for e in report["errors"]:
            print(f"  ERROR   {e}")
        for w in report["warnings"]:
            print(f"  warning {w}")
        if not report["errors"] and not report["warnings"]:
            print("  OK: citation gate passed")
        elif not report["errors"]:
            print("  OK: citation gate passed with warnings")
        else:
            print("  BLOCKED: fix errors before publishing")

    return 1 if report["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
