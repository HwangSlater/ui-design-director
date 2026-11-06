# 제작처 라이선스 페이지(또는 그 JS 묶음)에서 웹·임베딩 관련 문장만 뽑아 data/official.json 에 쌓는다.
# 사용: python -I check_official.py <글꼴이름> <URL> [<URL> ...]
import json, os, re, sys, html, datetime, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "data", "official.json")
KEYS = re.compile(r"(임베딩|웹\s?폰트|웹사이트|홈페이지|서버|게임|금지|승인|허가|등록|Update|업데이트)")


def text_of(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        raw = r.read()
    for enc in ("utf-8", "cp949"):
        try:
            s = raw.decode(enc); break
        except UnicodeDecodeError:
            s = raw.decode("utf-8", "replace")
    s = re.sub(r"\\u([0-9a-fA-F]{4})", lambda m: chr(int(m.group(1), 16)), s)
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", s, flags=re.S) if "<html" in s[:500].lower() else s
    s = html.unescape(re.sub(r"<[^>]+>", "\n", s))
    return [x.strip() for x in re.split(r"[\n\"]|(?<=다\.)", s) if 8 < len(x.strip()) < 300 and re.search(r"[가-힣]", x)]


if __name__ == "__main__":
    name, urls = sys.argv[1], sys.argv[2:]
    data = json.load(open(OUT, encoding="utf-8")) if os.path.exists(OUT) else {}
    hits = []
    for u in urls:
        try:
            hits += [x for x in text_of(u) if KEYS.search(x)]
        except Exception as e:
            hits.append(f"읽기 실패: {u} ({e.__class__.__name__})")
    data[name] = {"urls": urls, "read": datetime.date.today().isoformat(), "lines": list(dict.fromkeys(hits))[:40]}
    json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    sys.stdout.reconfigure(encoding="utf-8")
    for x in data[name]["lines"][:15]:
        print("-", x[:160])
