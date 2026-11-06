# 글꼴 실측 다시 하는 법

폴더: 이 저장소의 `scripts/font-research/sites/` 를 빈 작업 폴더로 복사해서 돌린다(결과는 저장소에 넣지 않는다). Node 18+, Edge 또는 Chrome.

## 파일

| 파일 | 하는 일 |
|---|---|
| ranks.txt | 순위표에서 옮겨 적은 `출처코드|순위|도메인` 목록 |
| build_sites.mjs | ranks.txt → sites.csv (중복 정리, 출처 URL 붙임, 200개) |
| measure.mjs | 사이트마다 헤드리스 Edge 로 첫 화면을 열고 글꼴을 재서 raw.jsonl 에 한 줄씩 덧붙임 |
| analyze.mjs | raw.jsonl → fonts.json·dropped.json·summary.json (이름 정리, 일반·시스템 글꼴 빼기) |
| licenses-base.json, licenses-agent.json | 글꼴별 라이선스·성격 (손으로 확인한 값). 둘을 합친 것이 licenses.json |
| report.mjs | → fonts-candidates.md, fonts-all.md |

## 처음부터 다시

```bash
cd <작업 폴더>
node build_sites.mjs                 # sites.csv 다시 만들기 (순위를 새로 받았으면 ranks.txt 먼저 고치기)
mv raw.jsonl raw-$(date +%Y%m%d).jsonl   # 예전 결과를 남겨 두고 새로 잴 때
node measure.mjs > run.log 2>&1      # 200곳, 브라우저 4개, 사이트당 25초 — 약 15분
node measure.mjs --retry-errors > run-retry.log 2>&1   # 실패한 곳만 한 번 더
node analyze.mjs
node -e "const f=require('fs');f.writeFileSync('licenses.json',JSON.stringify({...JSON.parse(f.readFileSync('licenses-base.json')),...JSON.parse(f.readFileSync('licenses-agent.json'))},null,1))"
node report.mjs                      # 끝에 「라이선스 표 없음: …」이 나오면 그 글꼴을 licenses-base.json 에 채운 뒤 다시
```

## 이어 하기·설정

- 중간에 끊겨도 `node measure.mjs` 를 다시 돌리면 raw.jsonl 에 이미 있는 사이트는 건너뛴다(한 사이트 끝날 때마다 바로 저장).
- 몇 곳만 시험: `node measure.mjs --limit 5`
- 바꿀 수 있는 값(환경 변수): `SITE_TIMEOUT_MS`(기본 25000), `WORKERS`(기본 4, 최대 4), `CAPTURE_BROWSER`(브라우저 경로).
- 잰 결과에는 화면 사진이나 페이지 HTML 을 남기지 않는다. 남는 것은 계산된 font-family, 실제로 그린 글꼴 이름(CDP `CSS.getPlatformFontsForNode`), `document.fonts` 의 loaded 이름뿐.

## 끝난 뒤 확인

브라우저가 남았는지(Windows):

```powershell
Get-CimInstance Win32_Process -Filter "Name='msedge.exe'" | Where-Object { $_.CommandLine -match 'capture-' -and $_.CommandLine -notmatch '--type=' } | Select-Object ProcessId, CreationDate
```

measure.mjs 는 끝날 때 `taskkill /T /F` 로 자기가 띄운 브라우저 트리를 끈다. 처음 판은 `proc.kill()` 만 써서 Edge 44개가 남았고(2026-11-06 실측), 그 뒤로 고쳤다. 다른 세션의 브라우저도 프로필 이름이 같은 `capture-` 로 시작하므로, 남은 것을 끌 때는 만든 시각으로 내 것만 골라야 한다.

## 주의

- 헤드리스 Windows 에서 쟀으므로, 로컬에 깔린 글꼴(맑은 고딕·Noto Sans KR 등)로 그려진 경우가 있다. 「쓰는 곳」은 CSS 맨 앞 이름까지 함께 세므로 사이트가 지정한 글꼴을 기준으로 한다.
- 사이트별 별명(notoR, NotoKrB, LGSmHaTB 같은 것)은 analyze.mjs 의 `FAMILY_RULES` 로 이름 꼴만 보고 한 가족으로 합친다. 새 별명이 나오면 거기에 줄을 더한다.
