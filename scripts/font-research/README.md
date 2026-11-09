# 글꼴 조사 다시 하기

스킬의 `assets/fonts/fonts.json` 을 만드는 도구다. 결과(사이트별 측정, 눈누 원본)는 저장소에 넣지 않는다.

1. `sites/` 를 빈 작업 폴더에 복사 → `sites/how-to-rerun.md` 대로 방문 상위 사이트 글꼴을 잰다(→ `licenses.json`, `fonts.json`). `measure.mjs` 는 스킬의 `browser.mjs` 를 쓰므로 저장소 안 경로를 고치지 않는다(복사한 폴더에서는 import 경로를 저장소의 browser.mjs 로 바꾼다).
2. `company/` 를 `<작업 폴더>/company/` 로 복사 → `company/how-to-rerun.md` 대로 눈누 전체에서 회사·기관 공개 글꼴을 모은다(→ `company/company-fonts.json`).
3. `python -X utf8 scripts/font-research/merge.py <작업 폴더> skills/ui-design-director/assets/fonts/fonts.json [--webfont <웹폰트 폴더>]`
4. 웹폰트 글(`webfont`)만 새로 붙일 때: `python -I scripts/font-research/company/webfont.py skills/ui-design-director/assets/fonts/fonts.json` → `python -X utf8 scripts/font-research/merge.py --webfont <임시 폴더/uidd-noonnu-webfont> skills/ui-design-director/assets/fonts/fonts.json`. 받은 글은 임시 폴더에만 두고 저장소에 넣지 않는다.

AI 글꼴 목록(`assets/fonts/ai-fonts.json`)은 따로 고친다 — 새 시안에 기본 글꼴이 보이면 더한다.
