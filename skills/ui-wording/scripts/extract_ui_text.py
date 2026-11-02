#!/usr/bin/env python3
"""화면에 보이는 문구를 모두 뽑아 목록으로 만든다 — 용어 검토의 재료.

    python extract_ui_text.py <폴더나 파일> [...] [--out ui-text.json]

읽는 것: HTML(글자, alt·aria-label·placeholder·title·value), JSX/TSX/JS/Vue/Svelte(태그 사이 글자와
같은 속성, 따옴표 문자열 중 한글이 든 것), Swift(Text/Button/Label/navigationTitle 등의 문자열),
Kotlin/Java·Android strings.xml, JSON·YAML 번역 파일의 값.
각 항목: file, line, kind(text|button|link|heading|label|attr|string), text.
외부 패키지 없음. 실행만 하고 파일은 고치지 않는다.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

SKIP_NAMES = {"wording.json", "ui-text.json"}  # 이 스킬이 만드는 파일은 화면이 아니다
SKIP_DIRS = {".git", "node_modules", "dist", "build", ".next", "out", "__pycache__", ".venv", "venv", "Pods", "DerivedData", "captures"}
ATTRS = ("alt", "aria-label", "placeholder", "title", "value", "content")
HANGUL = re.compile(r"[가-힣]")
KIND_BY_TAG = {"button": "button", "a": "link", "summary": "button", "label": "label", "th": "label",
               "h1": "heading", "h2": "heading", "h3": "heading", "h4": "heading", "h5": "heading", "h6": "heading", "title": "heading"}


class _HTML(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.items: list[tuple[int, str, str]] = []
        self.stack: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip += 1
        self.stack.append(tag)
        a = dict(attrs)
        if tag == "meta" and a.get("name") not in ("description",):
            return
        for k in ATTRS:
            v = a.get(k)
            if v and HANGUL.search(v):
                self.items.append((self.getpos()[0], "attr", v.strip()))

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self.skip:
            self.skip -= 1
        while self.stack:
            if self.stack.pop() == tag:
                break

    def handle_data(self, data):
        if self.skip:
            return
        text = " ".join(data.split())
        if not text or not HANGUL.search(text):
            return
        kind = "text"
        for t in reversed(self.stack):
            if t in KIND_BY_TAG:
                kind = KIND_BY_TAG[t]
                break
        self.items.append((self.getpos()[0], kind, text))


JSX_TEXT = re.compile(r">([^<>{}]*[가-힣][^<>{}]*)<")
QUOTED = re.compile(r"""(["'`])((?:(?!\1).)*[가-힣](?:(?!\1).)*)\1""")
SWIFT = re.compile(r"""\b(Text|Button|Label|Toggle|navigationTitle|alert|confirmationDialog|Section|TextField|Picker)\s*\(\s*"((?:[^"\\]|\\.)*)""")
XML_STRING = re.compile(r"<string[^>]*>([^<]*[가-힣][^<]*)</string>")


def _lines(text: str, pattern: re.Pattern, group: int, kind: str):
    for m in pattern.finditer(text):
        yield text.count("\n", 0, m.start()) + 1, kind, " ".join(m.group(group).split())


def extract_file(path: Path) -> list[dict]:
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return []
    ext = path.suffix.lower()
    found: list[tuple[int, str, str]] = []
    if ext in (".html", ".htm"):
        p = _HTML()
        p.feed(text)
        found = p.items
    elif ext in (".jsx", ".tsx", ".vue", ".svelte", ".js", ".ts", ".mjs"):
        found = list(_lines(text, JSX_TEXT, 1, "text")) + list(_lines(text, QUOTED, 2, "string"))
    elif ext == ".swift":
        found = list(_lines(text, SWIFT, 2, "string"))
    elif ext in (".kt", ".java"):
        found = list(_lines(text, QUOTED, 2, "string"))
    elif ext == ".xml":
        found = list(_lines(text, XML_STRING, 1, "string"))
    elif ext in (".json", ".yaml", ".yml", ".strings", ".po"):
        found = list(_lines(text, QUOTED, 2, "string"))
    seen = set()
    out = []
    for line, kind, t in found:
        if not t or (line, t) in seen:
            continue
        seen.add((line, t))
        out.append({"file": str(path), "line": line, "kind": kind, "text": t})
    return out


def walk(targets: list[str]) -> list[Path]:
    exts = {".html", ".htm", ".jsx", ".tsx", ".vue", ".svelte", ".js", ".ts", ".mjs", ".swift", ".kt", ".java", ".xml", ".json", ".yaml", ".yml", ".strings", ".po"}
    files: list[Path] = []
    for t in targets:
        p = Path(t)
        if p.is_file():
            files.append(p)
            continue
        for f in p.rglob("*"):
            if f.is_file() and f.suffix.lower() in exts and f.name not in SKIP_NAMES and not f.name.startswith("ui-text") and not any(part in SKIP_DIRS for part in f.parts):
                files.append(f)
    return sorted(set(files))


def main(argv: list[str]) -> int:
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("targets", nargs="+")
    ap.add_argument("--out", default="ui-text.json")
    a = ap.parse_args(argv)
    out_path = Path(a.out).resolve()
    items = [i for f in walk(a.targets) if f.resolve() != out_path for i in extract_file(f)]
    Path(a.out).write_text(json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8")
    kinds = {}
    for i in items:
        kinds[i["kind"]] = kinds.get(i["kind"], 0) + 1
    print(f"{len(items)}개 문구 → {a.out}  ({', '.join(f'{k} {v}' for k, v in sorted(kinds.items()))})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
