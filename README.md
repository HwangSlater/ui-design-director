# UI Design Director

[English](README.en.md)

`ui-design-director`는 프로젝트의 전체 UI 컨셉을 정하고, 그 컨셉으로 웹사이트나 웹앱 전체를 디자인하는 스킬입니다. Codex와 Claude Code에서 모두 동작합니다. 실제 템플릿과 3~4색 팔레트를 조사하고, 사용자가 디자인 형식과 색상을 직접 선택하도록 돕습니다. 선택한 후보는 간단한 코드 시안으로 비교한 뒤 재사용 가능한 `DESIGN.md`로 정리합니다. 이어서 페이지 목록을 정하고, 페이지마다 레이아웃 시안과 완성 시안을 승인받은 뒤에 실제 코드로 옮깁니다.

사용자는 디자인 용어나 전체 요구사항을 미리 알 필요가 없습니다. “디자인을 선정하고 싶어”라고 시작하면 스킬이 한 번에 하나씩 중요한 질문을 하고, 구체적인 선택지와 추천을 제공하며 다음 단계로 안내합니다.

이 스킬의 목적은 “Linear처럼 만들어줘” 같은 모호한 지시를 색상, 타이포그래피, 간격, 레이아웃, 컴포넌트, 상태 및 접근성 규칙으로 바꾸는 것입니다.

## 주요 기능

- 제품 유형(마케팅 사이트·대시보드·편집 도구·폼 워크플로·콘텐츠 리더)에 맞는 출처에서 실제 템플릿과 디자인 시스템 후보 조사
- 후보와 권장 의존성의 라이선스를 원문으로 확인하고, 상업 이용이 불가능한 것은 취향을 따지기 전에 제외
- 전체 디자인 형식과 컬러 팔레트를 독립적으로 선택
- Coolors, Color Hunt, Adobe Color, Huemint 등의 3~4색 조합 비교
- 색상별 UI 역할과 사용 비중 분석, 명암비는 눈대중이 아니라 hex 값에서 계산해 확인
- 동일한 콘텐츠를 사용한 2~3개의 코드 UI 시안 비교, 제시 전 넘침·줄바꿈·상태 자체 점검
- 선택한 디자인 언어를 프로젝트 루트의 `DESIGN.md`로 변환
- 화면 문구와 용어를 사용자 숙련도에 맞춘 규칙으로 고정
- 이후 구현에서 공통 토큰과 컴포넌트 사용 유도
- 피드백을 일회성 CSS가 아닌 지속적인 디자인 규칙으로 누적
- 반응형, 포커스, 오류, 로딩, 빈 상태 및 접근성 검수
- 모호한 요청에서도 시작되는 단계별 대화형 디자인 선정
- 사이트 전체 계획: 페이지 목록, 주요 이동 경로, 내비게이션, 페이지별 진행 상태를 `SITE-PLAN.md`에 기록
- 소개 페이지처럼 읽는 화면과 대시보드처럼 일하는 화면을 구분해 각각에 맞는 규칙 적용
- 페이지 유형마다 번호를 붙인 흑백 레이아웃 시안 2~3개를 보여 주고, 고른 것으로 완성 시안 제작
- 완성 시안은 토큰·컴포넌트 스타일시트 하나를 공유하므로 승인 후 코드로 그대로 옮김
- 외부 패키지 없는 정적 검사 스크립트(`check_site.py`): 접근성 필수 항목, 토큰을 거치지 않은 값, 흔한 AI 티 패턴을 세 단계로 보고
- 세 가지 화면 폭 렌더링 점검과, 내 판단을 모르는 별도 리뷰어의 검토

## 작동 방식

```text
프로젝트 맥락 파악
→ 디자인 형식 후보 조사
→ 3~4색 팔레트 후보 조사
→ 사용자가 형식과 색상을 각각 선택
→ 최종 조합을 코드 UI 시안으로 비교
→ 선택 결과를 DESIGN.md로 문서화
→ 페이지 목록과 이동 경로를 SITE-PLAN.md로 정리
→ 페이지 유형별 레이아웃 시안 중 선택
→ 페이지별 완성 시안 승인(세 가지 화면 폭, 모든 상태)
→ 대표 페이지부터 코드로 옮기고 나머지 페이지 확장
→ 정적 검사 · 렌더링 점검 · 별도 리뷰어 검수
```

사용자가 선택하기 전에는 디자인 시스템이나 제품 UI를 확정하지 않습니다. 템플릿은 하나의 주 레퍼런스를 중심으로 사용하며, 다른 레퍼런스의 특징은 “타이포그래피 위계” 또는 “대시보드 밀도”처럼 범위를 명확히 지정한 경우에만 혼합합니다.

## 설치

### Codex: GitHub URL로 설치

이 저장소를 GitHub에 올린 뒤 Codex 채팅에서 다음처럼 요청합니다.

```text
$skill-installer로 아래 스킬을 설치해줘.
https://github.com/HwangSlater/ui-design-director/tree/main/skills/ui-design-director
```

사용자는 저장소를 복제하거나 별도 셸 명령을 실행할 필요가 없습니다. 공개 저장소는 URL에서 직접 내려받고, 비공개 저장소는 사용자의 Git 자격 증명 또는 토큰을 사용할 수 있습니다. 설치 후 다음 대화부터 `$ui-design-director`를 호출할 수 있습니다.

복사해서 설치하려면 저장소 디렉터리 전체가 다음 구조로 위치해야 합니다.

```text
repository/skills/ui-design-director/
├── SKILL.md
├── agents/
└── references/
```

동일한 이름의 디렉터리가 이미 있다면 덮어쓰지 말고 기존 설치를 먼저 확인하세요. 설치 후 스킬이 목록에 나타나지 않으면 Codex를 다시 시작하거나 새 세션을 여세요.

### Claude Code: 개인 스킬 디렉터리에 연결

`skills/ui-design-director` 디렉터리를 `~/.claude/skills/` 아래에 두면 됩니다. `SKILL.md`의 frontmatter가 그대로 호환되므로 파일은 수정할 필요가 없고, `agents/openai.yaml`이 함께 있어도 무해합니다.

저장소에서 계속 스킬을 고칠 예정이라면 복사보다 링크가 낫습니다. 저장소를 고치면 설치본에 바로 반영됩니다.

```bash
# macOS · Linux
ln -s "$PWD/skills/ui-design-director" ~/.claude/skills/ui-design-director
```

```powershell
# Windows (관리자 권한 없이 동작하는 정션)
New-Item -ItemType Junction `
  -Path  "$env:USERPROFILE\.claude\skills\ui-design-director" `
  -Target "$PWD\skills\ui-design-director"
```

연결만으로 같은 세션에서 즉시 인식되며, 다음 턴부터 `$ui-design-director` 또는 `/ui-design-director`로 호출할 수 있습니다. 링크 대신 복사해도 동작하지만, 그 경우 저장소를 고칠 때마다 다시 복사해야 합니다.

두 환경의 설치 경로는 각각 다음과 같습니다.

```text
~/.codex/skills/ui-design-director
~/.claude/skills/ui-design-director
```

## 사용법

가장 간단하게 시작하려면:

```text
$ui-design-director를 사용해서 디자인을 선정하고 싶어.
내가 디자인 용어를 잘 몰라도 한 단계씩 질문하며 이끌어줘.
```

스킬은 제품과 사용자부터 확인하고, 디자인 형식 후보, 색상 조합, 코드 시안, 최종 승인 순서로 대화를 이어갑니다. 한 번에 하나의 중요한 선택을 묻고, “모르겠어”라고 답하면 대비되는 예시나 잠정 추천으로 선택 범위를 줄여줍니다.

전체 컨셉을 처음부터 선정하려면:

```text
$ui-design-director를 사용해 이 프로젝트의 제품 성격과 사용자를 파악해줘.
적합한 실제 템플릿과 3~4색 팔레트 후보를 조사하고,
내가 디자인 형식과 색상을 각각 선택할 수 있게 해줘.
```

코드 시안까지 비교하려면:

```text
$ui-design-director로 선택한 형식과 팔레트의 최종 조합 2~3개를
동일한 콘텐츠의 간단한 UI 코드로 만들어 보여줘.
내가 승인하기 전에는 제품 UI에 적용하지 마.
```

선택한 컨셉을 문서화하려면:

```text
$ui-design-director를 사용해 승인한 디자인 형식과 팔레트를
프로젝트 루트의 DESIGN.md로 정리해줘.
관찰한 규칙, 추론한 규칙, 제품에 맞게 보정한 규칙을 구분해줘.
```

사이트 전체를 디자인하려면:

```text
$ui-design-director로 DESIGN.md를 바탕으로 이 사이트에 필요한 페이지 목록과
주요 이동 경로를 정리해줘. 승인하면 페이지 유형마다 레이아웃 시안을 보여줘.
```

승인한 시안을 코드로 옮기려면:

```text
$ui-design-director로 승인된 시안을 코드로 옮겨줘.
대표 페이지 하나를 먼저 보여 주고, 확인하면 나머지 페이지로 넓혀줘.
```

기존 구현을 검수하려면:

```text
$ui-design-director로 렌더링된 UI가 DESIGN.md를 준수하는지 검수해줘.
수정은 하지 말고 심각도와 근거를 함께 보고해줘.
```

## 선택 및 승인 원칙

- 디자인 형식, 팔레트 및 타이포그래피는 서로 구분된 선택으로 다룹니다.
- 형식 하나를 골라도 색상이 자동으로 승인되지는 않습니다.
- 3~4색 원본 팔레트와 실제 UI에 사용하는 접근 가능한 토큰을 구분합니다.
- 상업 운영 제품에서는 라이선스가 취향보다 앞선 기준입니다. 상업 이용을 금지하거나 유료로 요구하는 후보는 각주가 아니라 탈락 사유입니다.
- 사용자가 선택을 위임한 경우에도 위임 사실과 선정 근거를 기록합니다.
- 형식, 팔레트, 중요한 보정 사항 및 요청한 코드 시안 피드백이 확정돼야 `DESIGN.md`를 승인 상태로 표시합니다.
- 코드 시안은 비교용 산출물이며 제품 구현이나 승인된 디자인 시스템이 아닙니다.
- 「사이트를 디자인해 줘」는 시안까지의 승인입니다. 제품 코드는 사용자가 요청하고 해당 페이지 시안이 승인된 뒤에만 씁니다.
- 지어낸 후기·고객 로고·수치를 실제처럼 넣지 않습니다. 없으면 빈 자리로 표시합니다.

## 스킬 구조

```text
.
├── README.md
├── README.en.md
├── scripts/
│   └── validate_skill.py
└── skills/
    └── ui-design-director/
        ├── SKILL.md
        ├── agents/
        │   └── openai.yaml
        ├── scripts/
        │   └── check_site.py
        └── references/
            ├── design-selection.md
            ├── guided-conversation.md
            ├── color-selection.md
            ├── concept-preview.md
            ├── reference-extraction.md
            ├── design-md-format.md
            ├── site-plan.md
            ├── page-design.md
            ├── site-build.md
            └── ui-review.md
```

- `SKILL.md`: 모드 선택, 승인 단계 및 공통 원칙
- `validate_skill.py`: 외부 패키지 없이 구조와 문서 링크 검증
- `guided-conversation.md`: 사용자를 한 단계씩 안내하는 대화 규칙
- `design-selection.md`: 템플릿 및 전체 디자인 형식 선정
- `color-selection.md`: 색상 조합 조사와 접근성 검토
- `concept-preview.md`: 비교 가능한 코드 UI 시안 제작
- `reference-extraction.md`: 선택한 레퍼런스에서 디자인 규칙 추출
- `design-md-format.md`: `DESIGN.md` 구조와 피드백 누적 방식
- `site-plan.md`: 페이지 목록·이동 경로·`SITE-PLAN.md` 작성
- `page-design.md`: 페이지 유형별 레이아웃 시안과 완성 시안
- `site-build.md`: 승인된 시안을 제품 코드로 옮기는 순서와 기준
- `ui-review.md`: 렌더링 결과의 일관성 및 접근성 검수, 사이트 전체 점검
- `check_site.py`: HTML·CSS 정적 검사(외부 패키지 없음, `python scripts/check_site.py <폴더>`)

## 컨텍스트 크기

전체 스킬 지침은 약 53KB이지만 한 번에 모두 읽지 않습니다. 기본 `SKILL.md`를 읽은 뒤 현재 작업에 필요한 참조 문서만 추가로 로드합니다.

| 모드 | 대략적인 로드 크기 | 평가 |
|---|---:|---|
| 기본 진입 | 9.6KB | 가벼움~보통 |
| 대화형 전체 선정 | 24.0KB | 보통 |
| 컨셉·색상 선정 | 19.0KB | 보통 |
| 코드 시안 | 12.8KB | 가벼움~보통 |
| DESIGN.md 추출 | 18.5KB | 보통 |
| 사이트 계획 | 14.2KB | 가벼움~보통 |
| 페이지 시안 | 18.4KB | 보통 |
| 코드 제작 | 17.1KB | 보통 |
| UI 검수 | 13.5KB | 가벼움~보통 |

필요한 문서만 단계적으로 읽는 구조이므로 프로젝트 컨텍스트를 과도하게 소비하지 않습니다.

## 개발 및 검증

스킬 이름, frontmatter, 필수 파일, Codex 메타데이터, 미완성 표식 및 Markdown 링크를 검사하려면:

```bash
python3 scripts/validate_skill.py
```

공식 `skill-creator` 검증기가 설치된 개발 환경에서는 스킬 폴더를 직접 검사할 수도 있습니다.

```bash
python3 /path/to/skill-creator/scripts/quick_validate.py skills/ui-design-director
```

이 검증은 구조적 오류를 확인하며, 실제 품질을 확인하려면 템플릿 선정, 팔레트 선택, 코드 시안, `DESIGN.md` 생성의 전체 대화 흐름도 테스트해야 합니다.
