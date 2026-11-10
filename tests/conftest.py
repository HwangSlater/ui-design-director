"""시험 공통 — 보내기 전 점검의 화면 재기(page_probe.mjs, 브라우저를 띄움)는 시험에서 끈다. 그 판단은 tests/test_page_probe.mjs 가 본다."""
import os

os.environ.setdefault("UIDD_NO_PROBE", "1")
