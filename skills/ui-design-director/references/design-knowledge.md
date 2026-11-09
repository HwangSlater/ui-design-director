# Design knowledge

What practising designers teach for free, distilled into 700+ checkable rules with sources (researched 2026-11-09). Use them through the tool, not by reading: the rules live in `assets/knowledge/rules.json`, tagged by field, stage and part; the six long files below are the human-readable originals. They are background knowledge: the chosen base and `build-rules.md` come first, and a rule here never adds a part the base lacks.

## Contents
- The tool
- The long files
- How to use a rule
- Limits

## The tool

- `python ${CLAUDE_SKILL_DIR}/scripts/knowledge.py stage <step>` — the few rules that most often decide that step; `stage.py` prints them under the stage table automatically.
- `python ${CLAUDE_SKILL_DIR}/scripts/knowledge.py ask --part button,form [--stage main] [--q 예약] [--top 8]` — rules for the parts you are building, one line each (rule, values, author, disagreement). `knowledge.py parts` lists the part names.
- `python ${CLAUDE_SKILL_DIR}/scripts/knowledge.py show <id>` — one rule's reason and source link, for when the client asks why.
- Rules that can be measured (body line height and size, motion duration, wide tracking, emoji icons, glows, hover growth) are also checked by `check_site.py`; nothing to read for those.

## The long files

The six `knowledge-*.md` files are the human-readable originals the rules were taken from. The model never reads them: `knowledge.py show <id>` gives one rule's reason and source.

## How to use a rule

- Cite it when it decides something the client will see: 「줄 길이는 한글 기준 …(출처: …)」.
- When sources disagree, follow the base site's measured value; if the base has none, pick one side and say which.
- Values marked *(inference)* or 「확인 안 됨」 are guesses — never present them as a source's rule.
- A face named in a source (Pretendard, Noto Sans KR, Inter) is not a font candidate; fonts come only from [fonts.md](fonts.md).

## Limits

Video-only lessons could not be read, and several sites blocked automated reading (Medium, Material 3, parts of Apple HIG); each file's last section lists what was missed. Re-run the research when a file is more than a year old.
