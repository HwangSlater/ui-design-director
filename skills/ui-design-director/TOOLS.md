# 도구 목록

`scripts/` 의 도구마다 한 줄. 쓰는 법은 각 파일 맨 위 설명에 있어요. 외부 패키지 없이 Python 3.10+·Node 18+·Edge/Chrome 으로 돌아가요(`check_shots.py`·`blind_sheet.py` 는 Pillow).

## 단계·점검

- `stage.py` — 지금 어느 단계인지, 앞 단계가 확정됐는지, 다음에 돌릴 명령(스킬을 열 때 자동 실행)
- `preflight.py` — 의뢰인에게 보내기 전 점검: 말한 채널, 공통점 셈, 사장님 들어가기·폰 분실, 같은 크기 단추 쌍, AI 글꼴
- `check_site.py` — 시안·사이트 HTML·CSS 정적 검사(접근성 바닥, 토큰 어긋남, 생성 티)
- `anchor_check.py` — 같은 페이지 안 링크(`#…`)가 기대한 제목으로 가는지(`check_site.py` 가 씀)
- `page_rules.py` — 탭 제목·같은 제목·사진 되쓰기·근거 없는 시간 같은 리뷰 실수(`check_site.py` 가 씀)
- `block_colours.py` — 큰 덩어리를 칠한 진한 색이 하나뿐인지(`check_site.py` 가 씀)
- `check_shots.py` — 보내기 전 캡처 확인: 비었거나 한 색뿐인 화면(불러오는 중·입구 화면·검은 첫 화면)

## 참고 사이트 보여 주기

- `make_board.py` — 캡처로 후보 보기 화면(한 번에 한 후보, 컴퓨터·휴대폰 틀)을 만들고 캡처 일감 목록을 뽑음
- `make_live_board.py` — 참고 사이트를 실제로 띄워 넘겨 보는 공용 보기 화면
- `live_proxy.mjs` — 틀 안 띄우기를 막는 사이트도 보기 화면에 띄우는 내 컴퓨터 안 프록시. OPEN 주소 하나를 찍고 「확정」도 직접 기록
- `frame_check.py` — 사이트가 다른 페이지 안에 뜰 수 있는지 응답 머리로 봄(바로 띄울지 우회할지)
- `wait_choice.mjs` — 팔레트 화면의 「확정」을 기다렸다가 결정을 파일로 넘김(내 컴퓨터 안, 한 번 쓰는 열쇠). 보기 화면의 확정은 live_proxy.mjs 가 같은 방식으로 받음
- `capture.mjs` — 실제 기기 폭으로 페이지 전체 캡처, 찍기 전 동작·이어 찍기. `node capture.mjs <jobs.json> <출력 폴더> [--widths 1280,390] [--scale 2]`(배율 1~3, 기본 2배)
  - 일감 하나: `id`(파일 이름 `<id>-<폭>.jpg`), `url`(`"@current"` 면 steps 를 마친 화면 그대로), `steps`(`{"goto": 주소}`·`{"click": "선택자"}`·`{"wait": ms}`), `scrollY`(그 위치 한 화면만 — 따라붙는 단추·칩 확인), `keepOverlays: true`(쿠키·동의 창을 걷지 않음), `judge: true`(블라인드 판정용 사본, judge_fill.mjs), `scale`(이 일감만 배율)
  - 이미 있는 파일은 건너뛰어 끊겨도 이어 찍음, 문서 응답 400 이상은 저장하지 않고 실패로 보고
- `snapshot.mjs` — 그려진 페이지를 HTML 하나로 저장(못 띄우는 후보도 선명하게 끝까지)
- `browser.mjs` — 측정 도구들이 함께 쓰는 브라우저 띄우기·끄기, `--sweep` 으로 남은 브라우저 치우기

## 바탕 재기

- `base_material.py` — 바탕을 고른 뒤 처음 돌림: `formats/jobs-base.json`(캡처·스냅샷 일감)과 `바탕-구성.md` 틀을 만들고(있으면 건너뜀) 다음에 돌릴 명령을 찍음. 주소 없이 `base_material.py <프로젝트>` 로 돌리면 보기 화면 결정(`formats/decision.json`)의 바탕 주소를 씀
- `skeleton.mjs` — 화면 짜임(한 단 비율, 단 수, 둥근 모양, 넘기는 띠)을 폰·컴퓨터 따로 잼, `--base` 로 바탕과 비교
- `skeleton_base.mjs` — 바탕과 관련 사이트를 견줘 「바꿀 곳」(n/N)을 뽑음(`skeleton.mjs --base` 가 씀)
- `extract_styles.mjs` — 바탕에서 실제로 쓰인 글자 크기·둥글기·그림자·여백·단추 모양을 숫자로
- `compose_metrics.mjs` — 첫 화면 구성(사진·색 판·빈 바탕 비율, 가장 큰 글자, 진한 덩어리 수)을 실제 사이트와 숫자로 비교
- `motion.mjs` — 바탕의 움직임(전환 길이·곡선, 마우스 올림 전후)을 값과 전후 그림으로 남김
- `knowledge.py` — 디자인 규칙 표(`assets/knowledge/rules.json`)에서 만드는 부품·단계에 맞는 규칙만 한 줄씩(`ask --part button,form`, `stage`, `show`, `parts`). 부품 이름은 한국어로도 됨(`--part "첫 화면,단추,입력 양식"`), 모르는 이름은 가까운 이름을 알려 줌
- `fonts.py` — 근거 있는 글꼴 표(`assets/fonts/fonts.json`)에서 후보 고르기(`pick`, 후보마다 웹폰트 줄), 파일로만 나온 글꼴의 `@font-face` 찍기(`face <이름>`, 팔레트 화면 `faces` 에 옮김), AI 글꼴 검사(`check`)

## 비교·판정

- `side_by_side.py` — 우리 화면과 바탕을 같은 폭으로 나란히 놓고 시각 층 대조표를 붙인 페이지
- `blind_sheet.py` — 우리 화면과 실제 사이트를 섞고 로고를 가린 블라인드 판정 그림·요청 글
- `judge_fill.mjs` — 블라인드 판정용 사본에서만 견본 흔적을 걷어 냄(`capture.mjs` 일감에 `"judge": true`)

## 저장소 쪽 도구

- `../../scripts/validate_skill.py` — 두 스킬의 구조·frontmatter·필수 파일·플러그인 설정·문서 링크 검사
- `../../scripts/check_all.py` — `validate_skill.py`, pytest, `node --test` 를 한 번에
- `../../scripts/board_bench.mjs` — 보기 화면 속도·메모리 재기(후보를 넘기며 다 뜨는 시간, 끝난 뒤 브라우저 메모리). 실제 사이트를 불러온다
- `../../scripts/roleplay_tokens.py` — 역할극 구간별 토큰 세기
- `../../scripts/font-research/` — 글꼴 표를 다시 재는 도구
