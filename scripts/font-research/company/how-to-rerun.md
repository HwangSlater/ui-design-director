# 다시 돌리는 법

작업 폴더: 이 저장소의 `scripts/font-research/company/` 를 `<작업 폴더>/company/` 로 복사해서 돌린다.

1. `python -I crawl.py`
   - 눈누 목록을 조회순(`/index?order_by=vd&page=N`)으로 끝까지 받아 `data/list.jsonl` 에 한 줄씩 쌓는다.
   - 개인 작가가 아닌 글꼴만 상세(`/font_page/<id>`)를 받아 `data/detail/<id>.json` 에 저장한다. 원본 HTML 은 남기지 않는다.
   - 중간에 끊겨도 다시 실행하면 이미 받은 페이지·파일은 건너뛴다(checkpoint).
   - 처음부터 새로 받으려면 `data/` 를 지운다. 개인 작가 글꼴까지 받으려면 `--all`.
   - 눈누는 빠르게 요청하면 429(Too Many Requests)를 돌려준다. `config.json` 의 `workers` 1, `delay_sec` 1.2 이상을 지킨다.
2. `python -I build.py` → `company-fonts.json`, `company-fonts.md` 를 다시 만든다.
3. 웹폰트 글: `python -I webfont.py <저장소>/skills/ui-design-director/assets/fonts/fonts.json`
   - fonts.json 의 눈누 글꼴마다 상세 페이지의 「웹폰트로 사용」 @font-face 글만 시스템 임시 폴더 `uidd-noonnu-webfont/<id>.css` 에 둔다(없으면 `<id>.none`). 다시 돌리면 받은 것은 건너뛴다.
   - 1.2초에 한 번(약 830곳이면 20분). 합치기는 `merge.py --webfont <그 폴더> …/fonts.json` (조사를 다시 했으면 merge.py 끝에 `--webfont <그 폴더>`).

손볼 곳
- 만든 곳 갈래(회사/공공기관·지자체/단체/개인): `classify.py` 의 `INDIVIDUAL`, `FONT_CO`, `OVERRIDE`. 새 제작처가 생기면 여기에 넣는다.
- 조건 문구 규칙: `rules.py` 의 `RULES`, `WEB_APPROVAL`, `NON_COMMERCIAL`. 빈칸인 임베딩 칸은 눈누에서 "허용 안 함"이라 별도 승인 표로 보낸다.
- 판단 기준: 눈누 라이선스 요약표의 '임베딩'(웹사이트 및 프로그램 서버 내 폰트 탑재)이 '사용 가능' 또는 '조건부 허용'이고 '웹사이트'가 불가가 아니면 웹 임베딩 가능으로 본다. 본문에 웹·임베딩 승인 문구가 있으면 별도 승인 표로 보낸다.
- 눈누 요약은 참고용이다. 실제로 쓰기 전에 '라이선스 출처' 링크의 원문을 확인한다.

제작처 원문 확인
- `python -I check_official.py <이름> <URL>` 은 제작처 페이지(또는 JS 묶음)에서 웹·임베딩·승인 문장만 뽑아 `data/official.json` 에 쌓는다.
- 눈누 요약과 원문이 다르면 `official_overrides.json` 에 적는다(`web: approval` 이면 별도 승인 표로, `add` 는 조건에 덧붙임). 2026-11-06 기준 KoPub(한국출판인회의)와 쿠키런(데브시스터즈)을 원문으로 확인해 적어 두었다.
