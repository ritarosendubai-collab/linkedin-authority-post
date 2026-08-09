#!/usr/bin/env python3
"""Structural linter for this skill.

Checks that SKILL.md is well-formed, that every reference it links exists, that
the bundled scripts compile, and that the production gates it claims to enforce
are actually present in the body or a linked reference.

Usage:
    python3 scripts/lint_skill.py .
    python3 scripts/lint_skill.py . --json

Exit codes:
    0  no errors (warnings allowed)
    1  one or more errors
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

MAX_SKILL_MD_LINES = 500
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
REFERENCE_RE = re.compile(r"references/([A-Za-z0-9_.-]+\.md)")

REQUIRED_GATES = {
    "failure modes": r"failure[ _-]?modes?",
    "retry policy": r"retry (policy|limit)|retry_limit",
    "evidence rule": r"evidence rule",
    "tool verification": r"tool verification|dependency states|verify before relying",
    "final review": r"final review|review\.json",
    "citation gate": r"citation gate",
    "scope boundary": r"non-goals?|scope gate",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    meta: dict[str, str] = {}
    key = None
    for line in parts[1].splitlines():
        if not line.strip():
            continue
        if ":" in line and not line.startswith((" ", "\t")):
            key, _, value = line.partition(":")
            key = key.strip()
            meta[key] = value.strip()
        elif key:
            meta[key] += " " + line.strip()
    return meta, parts[2]


def lint(skill_path: Path) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    skill_path = skill_path.resolve()

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return {"errors": ["SKILL.md is missing"], "warnings": []}

    text = read(skill_md)
    meta, body = parse_frontmatter(text)

    name = meta.get("name", "")
    if not name:
        errors.append("frontmatter is missing 'name'")
    elif not NAME_RE.match(name):
        errors.append(f"name '{name}' is not kebab-case")
    elif name != skill_path.name:
        warnings.append(f"name '{name}' does not match directory '{skill_path.name}'")

    description = meta.get("description", "")
    if not description:
        errors.append("frontmatter is missing 'description'")
    else:
        if len(description) < 80:
            warnings.append("description is short -- trigger recall will suffer")
        if len(description) > 1200:
            warnings.append("description is very long -- tighten the trigger surface")

    line_count = len(text.splitlines())
    if line_count > MAX_SKILL_MD_LINES:
        warnings.append(
            f"SKILL.md has {line_count} lines; route more detail into references/"
        )

    linked = set(REFERENCE_RE.findall(body))
    for ref in sorted(linked):
        if not (skill_path / "references" / ref).exists():
            errors.append(f"SKILL.md links a missing file: references/{ref}")

    refs_dir = skill_path / "references"
    if refs_dir.exists():
        on_disk = {p.name for p in refs_dir.glob("*.md")}
        for orphan in sorted(on_disk - linked):
            warnings.append(f"references/{orphan} exists but SKILL.md never routes to it")

    combined = body
    for ref in sorted(linked):
        path = skill_path / "references" / ref
        if path.exists():
            combined += "\n\n" + read(path)

    for label, pattern in REQUIRED_GATES.items():
        if not re.search(pattern, combined, re.IGNORECASE | re.MULTILINE):
            errors.append(f"missing production gate: {label}")

    if not linked and re.search(r"evidence", body, re.IGNORECASE):
        errors.append(
            "keyword-only gates: gate language present but no references are linked"
        )

    scripts_dir = skill_path / "scripts"
    if scripts_dir.exists():
        for py in sorted(scripts_dir.glob("*.py")):
            try:
                compile(read(py), str(py), "exec")
            except SyntaxError as exc:
                errors.append(f"syntax error in scripts/{py.name}: {exc.msg} (line {exc.lineno})")
            except OSError as exc:
                errors.append(f"cannot read scripts/{py.name}: {exc}")

    evals = skill_path / "evals" / "evals.json"
    if not evals.exists():
        warnings.append("evals/evals.json is missing -- behaviour is unverified")
    else:
        try:
            data = json.loads(read(evals))
            cases = data.get("evals", [])
            if len(cases) < 3:
                warnings.append(f"only {len(cases)} eval cases -- add negative and edge cases")
            for i, case in enumerate(cases):
                if not case.get("expectations"):
                    errors.append(f"evals.json case {i} has no expectations")
        except json.JSONDecodeError as exc:
            errors.append(f"evals/evals.json is not valid JSON: {exc}")

    return {"errors": errors, "warnings": warnings}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("skill_path", type=Path, nargs="?", default=Path("."))
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    report = lint(args.skill_path)

    if args.as_json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"Lint report for {args.skill_path.resolve()}")
        for e in report["errors"]:
            print(f"  ERROR   {e}")
        for w in report["warnings"]:
            print(f"  warning {w}")
        if not report["errors"] and not report["warnings"]:
            print("  OK: no errors or warnings")
        elif not report["errors"]:
            print("  OK: no errors")

    return 1 if report["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
