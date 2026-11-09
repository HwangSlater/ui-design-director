#!/usr/bin/env python3
"""Dependency-free structural checks for every skill in skills/*/SKILL.md and the Claude Code plugin."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
PLUGIN_DIR = REPO_ROOT / ".claude-plugin"
HOOKS_FILE = REPO_ROOT / "hooks" / "hooks.json"

# 스킬마다 반드시 있어야 하는 파일(스킬 폴더 기준). 여기 없는 스킬은 SKILL.md 만 본다.
REQUIRED_FILES: dict[str, tuple[str, ...]] = {
    "ui-design-director": (
        "SKILL.md",
        "TOOLS.md",
        "agents/openai.yaml",
        "assets/board.css",
        "assets/board.js",
        "assets/dock.css",
        "assets/dock.js",
        "assets/palette-switcher.css",
        "assets/palette-switcher.js",
        "assets/fonts/fonts.json",
        "assets/fonts/ai-fonts.json",
        "assets/knowledge/rules.json",
        "references/blind-judge.md",
        "references/design-knowledge.md",
        "references/knowledge-colour-motion.md",
        "references/knowledge-designers-global.md",
        "references/knowledge-designers-korea.md",
        "references/knowledge-layout.md",
        "references/knowledge-typography.md",
        "references/knowledge-ux.md",
        "references/build-rules.md",
        "references/color-selection.md",
        "references/companion-skills.md",
        "references/comparison-board.md",
        "references/concept-preview.md",
        "references/design-md-format.md",
        "references/design-selection.md",
        "references/fonts.md",
        "references/guided-conversation.md",
        "references/mockup-content.md",
        "references/owner-screens.md",
        "references/page-design.md",
        "references/reference-extraction.md",
        "references/sample-photos.md",
        "references/site-build.md",
        "references/site-plan.md",
        "references/ui-review.md",
        "scripts/anchor_check.py",
        "scripts/blind_sheet.py",
        "scripts/block_colours.py",
        "scripts/browser.mjs",
        "scripts/capture.mjs",
        "scripts/check_shots.py",
        "scripts/check_site.py",
        "scripts/compose_metrics.mjs",
        "scripts/extract_styles.mjs",
        "scripts/fonts.py",
        "scripts/frame_check.py",
        "scripts/judge_fill.mjs",
        "scripts/knowledge.py",
        "scripts/live_proxy.mjs",
        "scripts/make_board.py",
        "scripts/make_live_board.py",
        "scripts/motion.mjs",
        "scripts/page_rules.py",
        "scripts/preflight.py",
        "scripts/side_by_side.py",
        "scripts/skeleton.mjs",
        "scripts/skeleton_base.mjs",
        "scripts/snapshot.mjs",
        "scripts/stage.py",
        "scripts/wait_choice.mjs",
    ),
    "ui-wording": (
        "SKILL.md",
        "agents/openai.yaml",
        "references/conventions-ko.md",
        "scripts/extract_ui_text.py",
        "scripts/term_check.py",
    ),
}
REPO_MARKDOWN_FILES = ("README.md", "README.en.md", "docs/README.md")
UNFINISHED_MARKERS = ("TODO", "TBD", "FIXME", "PLACEHOLDER")


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def discover_skills() -> list[Path]:
    skills = sorted(path.parent for path in SKILLS_DIR.glob("*/SKILL.md"))
    if not skills:
        fail("no skills found under skills/*/SKILL.md")
    unknown = sorted(set(REQUIRED_FILES) - {path.name for path in skills})
    if unknown:
        fail("REQUIRED_FILES names skills that do not exist: " + ", ".join(unknown))
    return skills


def parse_frontmatter(text: str, where: str) -> dict[str, str]:
    match = re.match(r"\A---\n(.*?)\n---(?:\n|\Z)", text, re.DOTALL)
    if not match:
        fail(f"{where} must begin with YAML frontmatter")

    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line or line.startswith((" ", "\t")):
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"\'')
    return values


def check_skill(root: Path) -> None:
    name = root.name
    where = f"skills/{name}"
    missing = [path for path in REQUIRED_FILES.get(name, ("SKILL.md",)) if not (root / path).is_file()]
    if missing:
        fail(f"{where}: missing required files: " + ", ".join(missing))

    metadata = parse_frontmatter((root / "SKILL.md").read_text(encoding="utf-8"), f"{where}/SKILL.md")
    if metadata.get("name") != name:
        fail(f"{where}/SKILL.md: frontmatter name must be {name!r}")
    if not re.fullmatch(r"[a-z0-9-]{1,64}", name):
        fail(f"{where}: name must use lowercase letters, digits, and hyphens")
    if not metadata.get("description"):
        fail(f"{where}/SKILL.md: frontmatter description is required")

    interface = root / "agents" / "openai.yaml"
    if interface.is_file():
        text = interface.read_text(encoding="utf-8")
        if "display_name:" not in text or "short_description:" not in text:
            fail(f"{where}/agents/openai.yaml must define display_name and short_description")
        if f"${name}" not in text:
            fail(f"{where}/agents/openai.yaml default_prompt must mention ${name}")


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        fail(f"cannot read {path.relative_to(REPO_ROOT)}: {error}")
    raise AssertionError  # fail() 가 끝낸다


def check_plugin() -> None:
    """plugin.json·marketplace.json 의 이름·버전이 맞는지, 훅이 가리키는 파일이 있는지 본다."""
    plugin = load_json(PLUGIN_DIR / "plugin.json")
    market = load_json(PLUGIN_DIR / "marketplace.json")
    name = plugin.get("name")
    if not name or not re.fullmatch(r"\d+\.\d+\.\d+", str(plugin.get("version", ""))):
        fail("plugin.json needs a name and a semantic version")
    entries = [entry for entry in market.get("plugins", []) if entry.get("name") == name]
    if not entries:
        fail(f"marketplace.json does not list the plugin {name!r}")
    for entry in entries:
        if "version" in entry and entry["version"] != plugin["version"]:
            fail(f"marketplace.json version {entry['version']} != plugin.json version {plugin['version']}")
        source = (REPO_ROOT / entry.get("source", "./")).resolve()
        if source != REPO_ROOT.resolve():
            fail(f"marketplace.json source {entry.get('source')!r} must point at the repository root")

    hooks_text = HOOKS_FILE.read_text(encoding="utf-8")
    load_json(HOOKS_FILE)
    paths = re.findall(r"\$\{CLAUDE_PLUGIN_ROOT\}/([^\"'\\\s]+)", hooks_text)
    if not paths:
        fail("hooks/hooks.json has no ${CLAUDE_PLUGIN_ROOT}/… command")
    missing = sorted({path for path in paths if not (REPO_ROOT / path).is_file()})
    if missing:
        fail("hooks/hooks.json points at missing files: " + ", ".join(missing))


def iter_markdown_files(skills: list[Path]) -> list[Path]:
    files = [REPO_ROOT / path for path in REPO_MARKDOWN_FILES if (REPO_ROOT / path).is_file()]
    for root in skills:
        files.extend(sorted(root.glob("*.md")))
        files.extend(sorted((root / "references").glob("*.md")))
    return files


def github_slug(heading: str) -> str:
    """GitHub 이 제목에 붙이는 앵커: 소문자, 글자·숫자·공백·하이픈만 남기고 공백은 하이픈."""
    text = re.sub(r"[`*_~]|<[^>]+>", "", heading).strip().lower()
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def check_markdown(skills: list[Path]) -> None:
    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")

    for path in iter_markdown_files(skills):
        where = path.relative_to(REPO_ROOT)
        text = path.read_text(encoding="utf-8")
        for marker in UNFINISHED_MARKERS:
            if re.search(rf"\b{marker}\b", text):  # 대문자 표시만 — UX 용어 placeholder 가 잘못 걸렸다
                fail(f"unfinished marker {marker!r} found in {where}")

        anchors = {github_slug(h) for h in re.findall(r"^#{1,6}\s+(.+?)\s*$", text, re.MULTILINE)}
        for target in link_pattern.findall(text):
            if re.match(r"https?://", target):
                continue
            if target.startswith("#"):
                # 같은 파일 안 제목으로 가는 링크는 GitHub 이 만드는 앵커와 맞춰 본다
                if target[1:] not in anchors:
                    fail(f"broken anchor in {where}: {target}")
                continue
            local_target = (path.parent / target.split("#", 1)[0]).resolve()
            if not local_target.exists():
                fail(f"broken local link in {where}: {target}")


def main() -> None:
    skills = discover_skills()
    for root in skills:
        check_skill(root)
    check_plugin()
    check_markdown(skills)
    print(f"Skill validation passed ({', '.join(root.name for root in skills)}; plugin).")


if __name__ == "__main__":
    main()
