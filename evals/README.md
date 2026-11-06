# 평가 시나리오

공식 작성 지침(Agent Skills best practices)의 평가 꼴: `skills`, `query`, `files`, `expected_behavior`. 실행기는 따로 없다 — 새 세션에 `query` 를 주고(역할극이면 의뢰인 세션이 답한다) 결과를 `expected_behavior` 하나씩 대조한다. 같은 `query` 를 스킬 없이도 한 번 돌려 나란히 본다(스킬 없는 결과보다 나아야 한다). 지금까지의 역할극 결과와 판별은 `docs/역할극-기록.md`.

- `bookshop-main-page.json` — 메인 페이지만, 바탕 따르기·색·글꼴·AI 티(9차 책방 오후)
- `marketplace-famous-base.json` — 유명 서비스가 바탕일 때, 사진·개인정보 위험(6차 옆집마켓)
- `festival-time-states.json` — 날짜·결정에 따라 바뀌는 첫 화면, 운영자 화면(5차 진주 축제)

## 결과

| 날짜 | 시나리오 | 모델 | 본 것 |
|---|---|---|---|
| 2026-11-06 | bookshop 첫 단계 | Sonnet | 스킬이 열려 맥락을 concept-brief.md 에 남기고 바탕 고르기 화면으로 감. 싫은 것(큰 서점 느낌)을 「원함」으로 잘못 옮김 → 맥락 정리 뒤 싫은 것을 의뢰인에게 한 줄로 되짚는 확인이 필요 |
| 2026-11-06 | bookshop 첫 단계 | Haiku | 맥락 정리, 짐작은 [추정] 표시, 질문 하나만 하고 멈춤 — 지침대로 |
| 2026-11-06 | bookshop 첫 단계 | Opus | 슬래시·자동 부르기 모두 단계 표가 지시문 맨 앞에 들어옴 |

시험 주의: `claude -p`(비대화)로 돌릴 때는 `--allowedTools=Skill` 을 주어야 스킬이 열린다 — 주지 않으면 「Execute skill」 한 줄만 돌아오고 스킬 없이 진행해 스킬 탓으로 잘못 읽게 된다. 대화 모드에서는 이 자리에서 허락을 묻는다.
