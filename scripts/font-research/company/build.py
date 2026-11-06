# data/ 의 목록·상세를 모아 company-fonts.json / company-fonts.md 를 만든다.
import json, os, re, sys, glob, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from classify import classify

LIST = [json.loads(l) for l in open(os.path.join(HERE, "data", "list.jsonl"), encoding="utf-8")]
DET = {}
for p in glob.glob(os.path.join(HERE, "data", "detail", "*.json")):
    d = json.load(open(p, encoding="utf-8"))
    d["read_date"] = datetime.date.fromtimestamp(os.path.getmtime(p)).isoformat()
    DET[d["id"]] = d

from rules import commercial_status, find_conditions, needs_web_approval, split_tags


def strip_ref(u):
    return re.sub(r"[?&]ref=noonnu\.cc", "", u or "")


def views_num(v):
    m = re.match(r"([\d.]+)\s*([KM]?)", v or "")
    if not m:
        return 0
    return int(float(m.group(1)) * {"": 1, "K": 1e3, "M": 1e6}[m.group(2)])


def character(tags):
    base = [t for t in ("고딕", "명조", "손글씨", "장식체", "제목용", "바탕체", "붓글씨") if t in tags]
    rest = [t for t in tags if t not in base][:2]
    return ", ".join(base + rest)


OVR = json.load(open(os.path.join(HERE, "official_overrides.json"), encoding="utf-8"))
rows, excluded, approval = [], {}, []
def ex(reason):
    excluded[reason] = excluded.get(reason, 0) + 1

for r in sorted(LIST, key=lambda x: x["rank"]):
    kind, note = classify(r["maker"])
    if kind == "개인":
        ex("개인·1인 작가"); continue
    d = DET.get(r["id"])
    if not d:
        ex("상세를 못 읽음"); continue
    s, text = d["summary"], d["licence_text"]
    conds = find_conditions(text)
    shape, wt = split_tags(d["tags"])
    fw = [x for x in d["face_weights"] if x != "normal"]
    wt = r["weights"] or wt or (f"{len(fw)}가지 굵기" if len(fw) > 1 else "표기 없음")
    row = {"글꼴": d["name"] or r["name"], "만든 곳": d["maker"] or r["maker"], "갈래": kind, "갈래 메모": note,
           "성격": character(shape), "형태 태그": shape, "굵기": wt,
           "눈누 요약": s, "조건": conds,
           "라이선스 출처": strip_ref((d["licence_links"] or [d["download"]])[0]), "받는 곳": strip_ref(d["download"]),
           "눈누": d["url"], "눈누 조회수": d["views"], "조회수(수)": views_num(d["views"]),
           "조회순 순위": r["rank"], "읽은 날": d["read_date"]}
    web = s.get("웹사이트", ""); emb = s.get("임베딩", "")
    o = OVR.get(r["maker"], {})
    if o:
        row["원문 확인"] = {"url": o["url"], "읽은 날": o["read"], "메모": o.get("reason", "")}
    if o.get("web") == "approval":
        row["제외 이유"] = o["reason"]; approval.append(row); ex("웹 임베딩 별도 승인(제작처 원문)"); continue
    cs = commercial_status(text)
    if cs == "partial" and not o.get("add"):
        conds.append("일부 용도 상업 이용 제한")
    if o.get("add"):
        # 원문으로 확인한 조건이 자동 추출한 업종 조건을 대신한다
        conds[:] = [c for c in conds if c != "업종 제한"] + o["add"]
    if cs == "no":
        row["제외 이유"] = "상업 이용 제한 문구"; ex("상업 이용 제한"); approval.append(row); continue
    if not emb:
        row["제외 이유"] = "눈누 표 임베딩 빈칸(허용 안 함) — 대개 제작처 별도 허락 필요"; approval.append(row); ex("눈누 표 임베딩 불가"); continue
    if "불가" in emb:
        ex("임베딩 불가(눈누 표)"); continue
    if "불가" in web:
        ex("웹사이트 사용 불가"); continue
    if emb == "조건부 허용" and needs_web_approval(text):
        row["제외 이유"] = "웹 임베딩에 별도 승인"; approval.append(row); ex("웹 임베딩 별도 승인"); continue
    row["임베딩"] = emb
    rows.append(row)

rows.sort(key=lambda x: -x["조회수(수)"])
today = datetime.date.today().isoformat()
summary = {"작성일": today, "눈누 전체": len(LIST),
           "회사·기관·단체 글꼴": sum(1 for r in LIST if classify(r["maker"])[0] != "개인"),
           "갈래별": {k: sum(1 for r in LIST if classify(r["maker"])[0] == k) for k in ("회사", "공공기관·지자체", "단체", "개인")},
           "웹 임베딩 가능": len(rows), "제외(이유별)": excluded}
json.dump({"summary": summary, "fonts": rows, "separate_approval": approval},
          open(os.path.join(HERE, "company-fonts.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def cell(x):
    return str(x).replace("|", "/").replace("\n", " ")


out = [f"# 회사·기관이 무료로 푼 한글 글꼴 — 웹 임베딩 가능 목록", "",
       f"- 작성일: {today} / 출처: 눈누(noonnu.cc) 전체 목록 조회순 + 각 글꼴 라이선스 본문",
       f"- 눈누 전체 {summary['눈누 전체']}개 중 회사·기관·단체 {summary['회사·기관·단체 글꼴']}개 "
       f"(회사 {summary['갈래별']['회사']}, 공공기관·지자체 {summary['갈래별']['공공기관·지자체']}, 단체 {summary['갈래별']['단체']}, 개인 {summary['갈래별']['개인']})",
       f"- 웹 임베딩 가능(눈누 표 '임베딩' 사용 가능·조건부): {len(rows)}개",
       "- 제외: " + ", ".join(f"{k} {v}" for k, v in excluded.items()),
       "- '조건'은 라이선스 본문에서 문구로 뽑은 것이라 빠지거나 넘칠 수 있음. '조건부 허용'은 원문을 꼭 확인.", "",
       "| 글꼴 | 만든 곳 | 갈래 | 성격 | 굵기 | 임베딩 | 조건 | 라이선스 출처 | 받는 곳 | 눈누 조회수 |",
       "|---|---|---|---|---|---|---|---|---|---|"]
for x in rows:
    out.append("| " + " | ".join(cell(v) for v in [f"[{x['글꼴']}]({x['눈누']})", x["만든 곳"], x["갈래"] + (f"({x['갈래 메모']})" if x["갈래 메모"] else ""),
                                                   x["성격"], x["굵기"], x["임베딩"], ", ".join(x["조건"]) or "-",
                                                   x["라이선스 출처"], x["받는 곳"], x["눈누 조회수"]]) + " |")
out += ["", "## 웹에 쓰려면 따로 승인·확인이 필요한 글꼴", "",
        "| 글꼴 | 만든 곳 | 이유 | 눈누 표(웹사이트/임베딩, 빈칸=불가) | 라이선스 출처 | 눈누 조회수 |", "|---|---|---|---|---|---|"]
for x in approval:
    out.append("| " + " | ".join(cell(v) for v in [f"[{x['글꼴']}]({x['눈누']})", x["만든 곳"], x["제외 이유"],
                                                   f"{x['눈누 요약'].get('웹사이트','')}/{x['눈누 요약'].get('임베딩','')}",
                                                   x["라이선스 출처"], x["눈누 조회수"]]) + " |")
open(os.path.join(HERE, "company-fonts.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")
print(json.dumps(summary, ensure_ascii=False))
