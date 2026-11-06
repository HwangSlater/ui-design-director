# 눈누 목록(조회순)과 각 폰트 상세를 모아 checkpoint 로 저장한다. 다시 돌리면 이어서 한다.
import json, os, re, sys, time, html, urllib.request, concurrent.futures as cf

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = json.load(open(os.path.join(HERE, "config.json"), encoding="utf-8"))
BASE = CFG["base"]
OUT = os.path.join(HERE, "data")
DET = os.path.join(OUT, "detail")
os.makedirs(DET, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (font-licence research; contact via noonnu if needed)"}


def get(url, tries=4):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:
            err = e
            time.sleep(CFG.get("backoff_sec", 20) * (i + 1))
    raise err


def clean(s):
    s = re.sub(r"<br\s*/?>", "\n", s)
    s = re.sub(r"<[^>]+>", "", s)
    return html.unescape(re.sub(r"[ \t]+", " ", s)).strip()


def crawl_list():
    path = os.path.join(OUT, "list.jsonl")
    done = {}
    if os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            r = json.loads(line); done[r["id"]] = r
    pages = {r["page"] for r in done.values()}
    page = max(pages) + 1 if pages else 1
    with open(path, "a", encoding="utf-8") as f:
        while True:
            h = get(f"{BASE}/index?order_by=vd&page={page}")
            cards = re.split(r'<a data-turbolinks="true" class="pt-4 px-5" href="/font_page/', h)[1:]
            new = 0
            for i, c in enumerate(cards):
                fid = int(re.match(r"(\d+)", c).group(1))
                if fid in done:
                    continue
                alt = re.search(r'alt="([^"]*)"', c)
                maker = re.search(r'<p class="text-sm font-bold truncate"[^>]*>(.*?)</p>', c, re.S)
                wt = re.search(r'data-fonts-target="fontVariantsCount">(.*?)</p>', c, re.S)
                r = {"id": fid, "page": page, "rank": len(done) + 1,
                     "name": clean(alt.group(1)) if alt else "",
                     "maker": clean(maker.group(1)) if maker else "",
                     "weights": clean(wt.group(1)) if wt else ""}
                done[fid] = r; new += 1
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
            f.flush()
            if not cards or new == 0:
                break
            page += 1
            time.sleep(0.4)
    print("list", len(done), "last page", page)
    return done


def parse_detail(fid, h):
    body = re.sub(r"<(script|svg)[^>]*>.*?</\1>", "", h, flags=re.S)
    t = clean(re.sub(r"<style[^>]*>.*?</style>", "", body, flags=re.S))
    lines = [x.strip() for x in t.split("\n") if x.strip()]
    d = {"id": fid, "url": f"{BASE}/font_page/{fid}"}
    def after(label, n=1):
        for i, x in enumerate(lines):
            if x == label and i + n < len(lines):
                return lines[i + n]
        return ""
    title = re.search(r"<title>(.*?)\|", h, re.S)
    d["name"] = clean(title.group(1)) if title else ""
    d["maker"] = after("제작")
    d["views"] = after("조회수")
    # 형태 태그: '형태' 다음부터 다운로드 버튼 전까지
    tags = []
    if "형태" in lines:
        i = lines.index("형태") + 1
        while i < len(lines) and not lines[i].startswith("fonts--") and "다운로드" not in lines[i] and len(tags) < 15:
            tags.append(lines[i]); i += 1
    d["tags"] = tags
    m = re.search(r'<a href="([^"]+)"[^>]*class="noon-yellow-button"', h)
    d["download"] = html.unescape(m.group(1)) if m else ""
    m = re.search(r"라이선스 본문(.*?)라이선스 요약표", body, re.S)
    lic_html = m.group(1) if m else ""
    d["licence_text"] = clean(lic_html)[:4000]
    links = re.findall(r'<a href="([^"]+)"', lic_html)
    d["licence_links"] = [html.unescape(x) for x in links]
    rows = {}
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", body, re.S):
        tds = [clean(x) for x in re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)]
        if len(tds) >= 3:
            rows[tds[0]] = tds[2]
        elif len(tds) == 2:
            rows[tds[0]] = tds[1]
    d["summary"] = rows
    d["face_weights"] = sorted(set(re.findall(r"font-weight:\s*([0-9a-z]+)", h)))
    return d


def crawl_details(ids):
    todo = [i for i in ids if not os.path.exists(os.path.join(DET, f"{i}.json"))]
    def one(fid):
        h = get(f"{BASE}/font_page/{fid}")
        d = parse_detail(fid, h)
        if not d["name"] or not d["summary"]:
            raise ValueError("빈 페이지")
        with open(os.path.join(DET, f"{fid}.json"), "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False)
        time.sleep(CFG["delay_sec"])
        return fid
    n = 0; fails = []
    with cf.ThreadPoolExecutor(CFG["workers"]) as ex:
        futs = {ex.submit(one, i): i for i in todo}
        for fu in cf.as_completed(futs):
            try:
                fu.result(); n += 1
            except Exception as e:
                fails.append(futs[fu])
            if n % 200 == 0:
                print("detail", n, "/", len(todo), flush=True)
    print("detail done", n, "fail", len(fails), fails[:20])


if __name__ == "__main__":
    lst = crawl_list()
    if "--list-only" not in sys.argv:
        # 개인 작가 폰트는 상세를 받지 않는다(--all 이면 전부).
        sys.path.insert(0, HERE)
        from classify import classify
        ids = [i for i, r in lst.items() if "--all" in sys.argv or classify(r["maker"])[0] != "개인"]
        print("detail targets", len(ids), flush=True)
        crawl_details(sorted(ids))
