#!/usr/bin/env python3
"""뽑은 문구(ui-text.json)에서 용어·말투가 어긋난 곳을 찾고, 승인된 용어표대로 한꺼번에 고친다.

    python term_check.py ui-text.json --glossary wording.json            # 보고만
    python term_check.py ui-text.json --glossary wording.json --apply    # 표대로 고침(파일 수정)
    python term_check.py ui-text.json --suggest                           # 용어표 없이 흔들리는 곳만

wording.json 형식:
  {"service": "학원·교습소",
   "terms": [{"use": "체험 수업", "not": ["무료 체험", "체험 레슨", "맛보기 수업"], "why": "학원 업계 관행"}],
   "tone": "해요",            # 해요 | 합니다 — 안내 문장 끝
   "buttons": "동사"}          # 동사(예약하기) | 명사(예약) — 버튼 이름 꼴

찾는 것
  1. 용어표의 「not」 말이 쓰인 곳(파일:줄)
  2. 표에 없어도 같은 말이 띄어쓰기·「하기」·「보기」만 다르게 섞인 곳(예: 예약 / 예약하기 / 예약 하기)
  3. 안내 문장 끝 말투가 섞인 곳(해요체와 합니다체)
  4. 버튼 이름 꼴이 섞인 곳(명사로 끝남 / 「하기」로 끝남)
  5. 한국어 화면에 섞인 영어 단어(FAQ, Book, Contact 같은)
--apply 는 용어표의 「not」 → 「use」만 바꾼다. 2~5는 사람이 보고 표에 넣은 뒤 다시 돌린다.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

HAEYO = re.compile(r"(요|죠|세요|네요|래요|어요|아요|해요|예요|이에요)[.!?]?$")
HAPNIDA = re.compile(r"(습니다|ㅂ니다|니다|십시오|하십시오)[.!?]?$")
ENGLISH_WORD = re.compile(r"\b[A-Za-z][A-Za-z]{2,}\b")
ALLOWED_EN = {"DM", "SNS", "PC", "OK", "TV", "QR"}  # 한국어 화면에서도 그대로 쓰는 말


def norm(t: str) -> str:
    t = re.sub(r"\s+", "", t)
    t = re.sub(r"(하기|보기|하세요|해요)$", "", t)
    return t


def load(p: str) -> list[dict]:
    return json.loads(Path(p).read_text(encoding="utf-8"))


def where(items: list[dict]) -> str:
    shown = [f'{Path(i["file"]).name}:{i["line"]}' for i in items[:4]]
    more = f" 외 {len(items) - 4}곳" if len(items) > 4 else ""
    return ", ".join(shown) + more


def report(items: list[dict], glossary: dict | None) -> tuple[list[str], int]:
    out, problems = [], 0
    # 1. 용어표 위반
    if glossary:
        out.append("## 1. 용어표와 다른 말\n")
        rows = []
        for term in glossary.get("terms", []):
            for bad in term.get("not", []):
                hits = [i for i in items if bad in i["text"].replace(term["use"], "")]
                if hits:
                    rows.append(f'| {bad} | {term["use"]} | {len(hits)} | {where(hits)} | {term.get("why", "")} |')
        if rows:
            problems += len(rows)
            out += ["| 쓰인 말 | 바꿀 말 | 곳 | 어디 | 이유 |", "|---|---|---|---|---|", *rows, ""]
        else:
            out.append("없음\n")
    # 2. 같은 말이 여러 꼴로
    out.append("## 2. 같은 말이 여러 꼴로 섞인 곳\n")
    short = [i for i in items if i["kind"] in ("button", "link", "label", "heading") and len(i["text"]) <= 14]
    groups: dict[str, dict[str, list]] = defaultdict(lambda: defaultdict(list))
    for i in short:
        groups[norm(i["text"])][i["text"]].append(i)
    rows = []
    for key, forms in groups.items():
        if len(forms) > 1:
            rows.append("| " + " / ".join(f"「{f}」 {len(v)}" for f, v in sorted(forms.items(), key=lambda kv: -len(kv[1]))) + " | " + where([x for v in forms.values() for x in v]) + " |")
    if rows:
        problems += len(rows)
        out += ["| 섞인 꼴(곳 수) | 어디 |", "|---|---|", *rows, ""]
    else:
        out.append("없음\n")
    # 3. 말투
    out.append("## 3. 안내 문장 말투\n")
    sentences = [i for i in items if i["kind"] in ("text", "attr", "string") and len(i["text"]) >= 8]
    haeyo = [i for i in sentences if HAEYO.search(i["text"])]
    hapnida = [i for i in sentences if HAPNIDA.search(i["text"])]
    want = (glossary or {}).get("tone")
    if haeyo and hapnida:
        problems += 1
        minority = hapnida if (want == "해요" or (not want and len(haeyo) >= len(hapnida))) else haeyo
        label = "합니다체" if minority is hapnida else "해요체"
        out.append(f"섞여 있음: 해요체 {len(haeyo)}곳, 합니다체 {len(hapnida)}곳. 적은 쪽({label}) 예: {where(minority)}\n")
    else:
        out.append("한 가지로 맞음\n")
    # 4. 버튼 꼴
    out.append("## 4. 버튼 이름 꼴\n")
    buttons = [i for i in items if i["kind"] == "button"]
    verb = [i for i in buttons if re.search(r"(하기|보기|받기|묻기|가기|기)$", i["text"])]
    noun = [i for i in buttons if i not in verb]
    if verb and noun and len(buttons) >= 4:
        problems += 1
        out.append(f"섞여 있음: 「~하기」 꼴 {len(verb)}개({where(verb)}), 명사 꼴 {len(noun)}개({where(noun)}). 업계 관행을 보고 한 가지로 정하세요.\n")
    else:
        out.append("한 가지로 맞음(또는 버튼이 적음)\n")
    # 5. 영어 단어
    out.append("## 5. 한국어 화면에 섞인 영어 단어\n")
    allowed = set(ALLOWED_EN) | set((glossary or {}).get("allow_english", []))
    en = defaultdict(list)
    for i in items:
        for w in ENGLISH_WORD.findall(i["text"]):
            if w not in allowed:
                en[w].append(i)
    rows = [f"| {w} | {len(v)} | {where(v)} |" for w, v in sorted(en.items(), key=lambda kv: -len(kv[1]))]
    if rows:
        problems += len(rows)
        out += ["| 단어 | 곳 | 어디 |", "|---|---|---|", *rows, ""]
    else:
        out.append("없음\n")
    return out, problems


def apply(items: list[dict], glossary: dict) -> int:
    changed = 0
    files = sorted({i["file"] for i in items if Path(i["file"]).name not in ("wording.json",) and not Path(i["file"]).name.startswith("ui-text")})
    for f in files:
        p = Path(f)
        t = p.read_text(encoding="utf-8")
        new = t
        for term in glossary.get("terms", []):
            use = term["use"]
            keep = "<<KEEP-WORDING>>"
            new = new.replace(use, keep)  # 이미 맞는 말은 건드리지 않게(「네이버 예약」→「네이버 예약에서 보기」를 두 번 돌려도 안전)
            for bad in term.get("not", []):
                new = new.replace(bad, keep)
            new = new.replace(keep, use)
        if new != t:
            p.write_text(new, encoding="utf-8")
            changed += 1
            print(f"고침: {f}")
    return changed


def main(argv: list[str]) -> int:
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("inventory")
    ap.add_argument("--glossary")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--suggest", action="store_true")
    a = ap.parse_args(argv)
    items = load(a.inventory)
    glossary = json.loads(Path(a.glossary).read_text(encoding="utf-8")) if a.glossary else None
    if a.apply:
        if not glossary:
            print("--apply 에는 --glossary 가 필요해요", file=sys.stderr)
            return 2
        n = apply(items, glossary)
        print(f"{n}개 파일 고침. extract_ui_text.py 로 다시 뽑아 확인하세요.")
        return 0
    lines, problems = report(items, glossary)
    print(f"# 문구 검토 — {len(items)}개 문구, 걸린 것 {problems}건\n")
    print("\n".join(lines))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
