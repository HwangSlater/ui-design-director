#!/usr/bin/env python3
"""의뢰인이 준 사실(이름·가격·시간·수)이 시안에 그대로 들어갔는지 본다.

    python facts.py <project folder>     # concept-brief.md 「페이지 사실:」 아래 값 가운데 mockups/index.html 에 없는 것

디자이너가 견본 값부터 넣고 의뢰인이 바로잡는 일, 준 사실을 확인 중이라며 빼는 일이 되풀이됐다
(애견미용 21·24차, 빵집 33~37차, 자전거 38차, 네일 43차). 세션 점검(저장소 scripts/session_audit.py)도 같은 판단을 쓴다.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import mock_dir, read, utf8_console  # noqa: E402

UNITS = "만원|원|개|마리|시|명|팀|주|회"
NATIVE = {1: "한", 2: "두", 3: "세", 4: "네", 5: "다섯", 6: "여섯", 7: "일곱", 8: "여덟", 9: "아홉", 10: "열"}
SKIP_LINE = re.compile(r"\s*-\s*(싫은 것|그 밖에)")  # 싫은 것·「그 밖에 물으면」 줄은 사실이 아니다
FACTS_HEAD = re.compile(r"페이지\s*사실\s*[:：]")
MONEY = re.compile(r"(\d+)\s*만\s*(?:(\d+)\s*천)?\s*원")  # 「4만5천원」「1만원」


def values(text: str) -> list[str]:
    """사실 글의 값 — 「」 이름, 「4만5천원」 같은 돈, 단위 붙은 숫자. 「1시간」은 시각이 아니다."""
    facts = "\n".join(line for line in text.splitlines() if not SKIP_LINE.match(line))
    names = re.findall(r"「([^」]{1,20})」", facts)
    money = [m.group(0).replace(" ", "") for m in MONEY.finditer(facts)]
    rest = MONEY.sub(" ", facts)
    nums = [re.sub(r"\s+", "", n) for n in re.findall(rf"\d+\s*(?:{UNITS.replace('시', '시(?!간)')})", rest)]
    return list(dict.fromkeys(names + money + nums))


def flat_text(html: str) -> str:
    """시안 HTML 의 보이는 글 — 태그·띄어쓰기를 지운 한 줄."""
    html = re.sub(r"<(script|style)\b.*?</\1>", " ", html, flags=re.S | re.I)
    return re.sub(r"\s+", "", re.sub(r"<[^>]+>", " ", html))


def in_page(value: str, flat: str) -> bool:
    """값이 시안 글에 있나 — 「9시」는 09:00 도, 「40개」는 40자리·40팀도, 「6마리」는 「여섯 마리」도, 「4만5천원」은 45,000 도."""
    v = re.sub(r"\s+", "", value)
    if v in flat:
        return True
    money = MONEY.fullmatch(v)
    if money:
        won = int(money.group(1)) * 10000 + int(money.group(2) or 0) * 1000
        return f"{won:,}" in flat or str(won) in flat
    m = re.fullmatch(rf"(\d+)({UNITS})", v)
    if not m:
        return False
    n, unit = m.groups()
    if unit == "시":
        return re.search(rf"(?<!\d)(0?{n}|{int(n) + 12}):00", flat) is not None
    word = NATIVE.get(int(n))
    if word and unit in ("마리", "명", "개", "팀", "회") and f"{word}{unit}" in flat:
        return True
    return re.search(rf"(?<!\d){n}(?!\d)", flat) is not None


def brief_facts(brief: str) -> str:
    """concept-brief.md 의 「페이지 사실:」 부터 다음 제목(#)이나 빈 줄 둘까지."""
    m = FACTS_HEAD.search(brief)
    if not m:
        return ""
    tail = brief[m.end():]
    end = re.search(r"\n#|\n\s*\n\s*\n", tail)
    return tail[: end.start()] if end else tail


def missing(root: Path) -> list[str]:
    page = mock_dir(root) / "index.html"
    facts = brief_facts(read(root / "concept-brief.md"))
    if not facts or not page.is_file():
        return []
    flat = flat_text(read(page))
    # 「견본」이라고 적은 값은 의뢰인 사실이 아니다
    facts = "\n".join(line for line in facts.splitlines() if "견본" not in line)
    return [v for v in values(facts) if not in_page(v, flat)]


def check_project(root: Path) -> list[str]:
    """preflight.py 가 부른다."""
    lost = missing(root)
    return [f"페이지 사실 빠짐: {', '.join(lost)} — 의뢰인이 준 값은 확인을 묻는 중이어도 시안에 그대로(guided-conversation.md § Ask for the page's facts)"] if lost else []


def main(argv: list[str]) -> int:
    utf8_console()
    if not argv:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    lines = check_project(Path(argv[0]))
    for line in lines:
        print(line)
    return 1 if lines else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
