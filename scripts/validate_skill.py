#!/usr/bin/env python3
"""Dependency-free structural checks for the ui-design-director skill."""

from __future__ import annotations

import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_NAME = "ui-design-director"
ROOT = REPO_ROOT / "skills" / SKILL_NAME
REQUIRED_FILES = (
    "SKILL.md",
    "agents/openai.yaml",
    "references/design-selection.md",
    "references/color-selection.md",
    "references/concept-preview.md",
    "references/guided-conversation.md",
    "references/reference-extraction.md",
    "references/design-md-format.md",
    "references/ui-review.md",
)
REPO_MARKDOWN_FILES = ("README.md", "README.en.md")
UNFINISHED_MARKERS = ("TODO", "TBD", "FIXME", "PLACEHOLDER")


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def parse_frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"\A---\n(.*?)\n---(?:\n|\Z)", text, re.DOTALL)
    if not match:
        fail("SKILL.md must begin with YAML frontmatter")

    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line or line.startswith((" ", "\t")):
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"\'')
    return values


def check_required_files() -> None:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).is_file()]
    if missing:
        fail("missing required files: " + ", ".join(missing))


def check_metadata() -> None:
    skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    metadata = parse_frontmatter(skill_text)

    if metadata.get("name") != SKILL_NAME:
        fail(f"frontmatter name must be {SKILL_NAME!r}")
    if not metadata.get("description"):
        fail("frontmatter description is required")
    if not re.fullmatch(r"[a-z0-9-]{1,64}", metadata["name"]):
        fail("frontmatter name must use lowercase letters, digits, and hyphens")

    interface_text = (ROOT / "agents/openai.yaml").read_text(encoding="utf-8")
    if "display_name:" not in interface_text or "short_description:" not in interface_text:
        fail("agents/openai.yaml must define display_name and short_description")
    if f"${SKILL_NAME}" not in interface_text:
        fail(f"agents/openai.yaml default_prompt must mention ${SKILL_NAME}")


def iter_markdown_files() -> list[Path]:
    files = [
        REPO_ROOT / path
        for path in REPO_MARKDOWN_FILES
        if (REPO_ROOT / path).is_file()
    ]
    files.append(ROOT / "SKILL.md")
    files.extend(sorted((ROOT / "references").glob("*.md")))
    return files


def check_markdown() -> None:
    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")

    for path in iter_markdown_files():
        text = path.read_text(encoding="utf-8")
        for marker in UNFINISHED_MARKERS:
            if re.search(rf"\b{marker}\b", text, re.IGNORECASE):
                fail(f"unfinished marker {marker!r} found in {path.relative_to(REPO_ROOT)}")

        for target in link_pattern.findall(text):
            if re.match(r"https?://", target):
                continue
            local_target = (path.parent / target).resolve()
            if not local_target.exists():
                fail(
                    f"broken local link in {path.relative_to(REPO_ROOT)}: {target}"
                )


def main() -> None:
    check_required_files()
    check_metadata()
    check_markdown()
    print("Skill validation passed.")


if __name__ == "__main__":
    main()
