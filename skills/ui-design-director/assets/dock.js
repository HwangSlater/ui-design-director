/*
 * 아래 막대 공용 동작 — board.js(후보 보기)와 palette-switcher.js(팔레트 바꿔 보기)가 함께 쓴다.
 * 말풍선 하나, 숨기기/구석 알약, 단축키 뒤 포커스 맞추기, 「확정」 단추.
 *
 * 고칠 때 지켜야 하는 동작(사용성 시험에서 나온 것):
 * - 고른 쪽 탭은 후보를 바꿔도 그대로. 그 쪽이 없는 후보는 화면에 「이 후보에는 … 쪽이 없어요」, 탭에 「없음」 — 몰래 다른 탭으로 넘기지 않는다.
 * - 말풍선은 막대 전체 위에 하나. 동작 먼저, 단축키는 뒤에. 마우스를 올리거나 키보드 포커스일 때만.
 * - 키보드 포커스 색은 「고른 상태」 색과 다르게. 단축키로 고르면 포커스도 새 항목으로 옮긴다.
 * - 휠은 어디서 굴려도(막대 위, 휴대폰 틀 옆) 보이는 쪽을 스크롤한다.
 * - 없는 쪽 표시는 탭 너비를 바꾸지 않는다(흐린 글자 + 구석 점). 후보를 바꿔도 막대 크기가 그대로.
 * - 쪽 이동은 즉시(부드러운 스크롤이면 다음 키가 엉뚱한 자리에서 시작한다).
 * - 숨기면 오른쪽 아래 알약으로 줄고, 알약에 후보·쪽·보기를 적는다(「2 Field · 상품 목록 · 휴대폰」). 누르거나 H 로 다시 연다.
 * - 긴 글은 막대 밖으로 나가지 않는다: 말줄임(메모 먼저, 후보 이름은 마지막에 줄임), 전체는 말풍선에. 이름 줄이 막대를 넓히지 않는다. 좁은 화면에서는 「n개 중 하나」를 뺀다.
 * - 후보·탭이 많아도 나머지를 누르지 않는다: 썸네일 줄은 최대 너비(--v-cands-max)에서 옆으로 스크롤, 탭은 이름을 다 보이고 옆으로 스크롤, 고른 썸네일·탭은 보이게 끌어온다.
 *   고친 뒤 후보 15개 이상·탭 6개 보기를 1280 과 390 에서 확인한다.
 * - 확정 단추 글자 너비는 그대로(확정 / 보내는 중 / 확정됨), 결과는 닫을 때까지 남는다.
 */
(function () {
  "use strict";

  const TIP_GAP = 10;
  const SEND_TIMEOUT_MS = 4000; // 확정을 보낼 때 이만큼 답이 없으면 복사 방식으로 넘어간다

  // 주소의 wait=<포트>-<열쇠> — 에이전트가 scripts/wait_choice.mjs 로 기다리는 동안만 붙는다
  const WAIT = (() => {
    const m = (new URLSearchParams(location.hash.slice(1)).get("wait") || "").match(/^(\d{2,5})-([0-9a-f]{32})$/);
    return m ? { port: m[1], token: m[2] } : null;
  })();

  // 보던 자리를 주소에 남긴다. wait 는 지워지지 않게 다시 붙인다.
  function writeHash(params) {
    const q = new URLSearchParams(params);
    if (WAIT) q.set("wait", `${WAIT.port}-${WAIT.token}`);
    history.replaceState(null, "", `#${q.toString()}`);
  }
  const $ = (sel) => document.querySelector(sel);
  const $$ = (sel) => Array.from(document.querySelectorAll(sel));
  const el = (tag, cls, text) => {
    const n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text !== undefined) n.textContent = text;
    return n;
  };

  // 말풍선 — 막대 전체 위에 하나만. 마우스를 올렸을 때와 키보드 포커스일 때만 뜬다.
  // data-tip="설명|단축키" 를 단 요소에 뜬다.
  function installTip(nav) {
    const tip = el("div", "v-tip");
    tip.setAttribute("role", "tooltip");
    tip.hidden = true;
    document.body.append(tip);
    const hide = () => { tip.hidden = true; };
    const show = (target) => {
      const text = target.dataset.tip;
      if (!text) return hide();
      const [main, key] = text.split("|");
      tip.replaceChildren(document.createTextNode(main.trim()));
      if (key) tip.append(el("kbd", null, key.trim()));
      const r = target.getBoundingClientRect();
      const bar = nav.getBoundingClientRect();
      tip.hidden = false;
      const half = tip.offsetWidth / 2;
      tip.style.left = `${Math.min(Math.max(r.left + r.width / 2, half + TIP_GAP), innerWidth - half - TIP_GAP)}px`;
      tip.style.top = `${bar.top - tip.offsetHeight - TIP_GAP}px`;
    };
    nav.addEventListener("mouseover", (e) => { const t = e.target.closest("[data-tip]"); if (t) show(t); });
    nav.addEventListener("mouseleave", hide);
    nav.addEventListener("focusin", (e) => { if (e.target.matches(":focus-visible")) show(e.target); else hide(); });
    nav.addEventListener("focusout", hide);
    nav.addEventListener("click", hide);
    document.addEventListener("keydown", (e) => { if (e.key === "Escape") hide(); });
    return hide;
  }

  // 마우스로 누른 단추에 포커스가 남은 채 단축키를 쓰면 그 단추에 포커스 테두리가 켜져
  // 고른 것과 다른 것이 함께 강조된다. 같은 묶음 안에서 지금 고른 것으로 포커스를 옮긴다.
  // groups: [[묶음 선택자, 고른 것 선택자], …]
  function syncFocus(groups) {
    const active = document.activeElement;
    const group = active && groups.find(([member]) => active.matches(member));
    const target = group && $(group[1]);
    if (target) target.focus({ preventScroll: true });
  }

  // 숨기면 막대가 오른쪽 아래 알약(.v-reveal)으로 접힌다
  function toggleDock() {
    const hidden = document.body.classList.toggle("dock-hidden");
    ($(hidden ? ".v-reveal" : ".v-hide") || document.body).focus({ preventScroll: true });
  }

  // 단축키 — 입력 칸에 쓰는 중이거나 조합키를 누른 때는 건드리지 않는다
  function onKeys(map) {
    document.addEventListener("keydown", (e) => {
      if (e.altKey || e.ctrlKey || e.metaKey) return;
      if (e.target.closest && e.target.closest("input, textarea, select, [contenteditable]")) return;
      const fn = map[e.key.length === 1 ? e.key.toLowerCase() : e.key];
      if (!fn) return;
      e.preventDefault();
      fn();
    });
  }

  // 알림 줄 — 막대 위에 뜨고, 닫기 전까지 남는다(확정 결과처럼 놓치면 안 되는 것)
  function status(nav, message, copyText) {
    let box = $(".v-status");
    if (!box) {
      box = el("div", "v-status");
      box.setAttribute("role", "status");
      document.body.append(box);
    }
    const close = el("button", "v-btn icon v-status-close", "×");
    close.type = "button";
    close.setAttribute("aria-label", "알림 닫기");
    close.addEventListener("click", () => { box.hidden = true; });
    const body = el("div", "v-status-body");
    body.append(el("p", null, message));
    if (copyText) {
      const field = el("input", "v-status-copy");
      field.readOnly = true;
      field.value = copyText;
      field.setAttribute("aria-label", "채팅에 붙여 넣을 문구");
      field.addEventListener("focus", () => field.select());
      body.append(field);
    }
    box.replaceChildren(body, close);
    box.hidden = false;
    box.style.bottom = `${innerHeight - nav.getBoundingClientRect().top + TIP_GAP}px`;
  }

  // 「확정」 단추. getChoice() → { step, label, choice }.
  // 에이전트가 기다리고 있으면(wait) 바로 보내고, 아니면 확정 문구를 복사해 채팅에 붙이게 한다.
  // 돌려주는 refresh() 를 후보가 바뀔 때마다 부른다.
  function installConfirm(nav, button, getChoice) {
    let sentLabel = "";
    const labelEl = button.querySelector(".v-label");
    function refresh() {
      const { label } = getChoice();
      const sent = label === sentLabel;
      button.dataset.state = sent ? "sent" : "";
      labelEl.textContent = sent ? "확정됨" : "확정";
      button.dataset.tip = sent ? `「${label}」 확정을 전달했어요` : `「${label}」 확정하기`;
    }
    async function send(payload) {
      const ctrl = new AbortController();
      const timer = setTimeout(() => ctrl.abort(), SEND_TIMEOUT_MS);
      try {
        const res = await fetch(`http://127.0.0.1:${WAIT.port}/choice`, {
          method: "POST",
          headers: { "Content-Type": "text/plain" }, // 사전 확인 요청 없이 보내려고 text/plain
          body: JSON.stringify({ token: WAIT.token, ...payload }),
          signal: ctrl.signal,
        });
        return res.status;
      } catch {
        return 0;
      } finally {
        clearTimeout(timer);
      }
    }
    button.addEventListener("click", async () => {
      const c = getChoice();
      const text = `${c.step ? c.step + ": " : ""}${c.label} 확정`;
      button.disabled = true;
      labelEl.textContent = "보내는 중";
      const code = WAIT ? await send(c) : 0;
      button.disabled = false;
      if (code === 200) {
        sentLabel = c.label;
        refresh();
        status(nav, `「${c.label}」 확정을 전달했어요. 채팅으로 돌아가면 이어서 진행합니다.`);
        return;
      }
      refresh();
      const why = code === 409 ? "이미 다른 확정을 받아 기다리기를 마쳤어요."
        : !WAIT ? "이 주소로 열면 에이전트와 연결되지 않아요(에이전트가 알려 준 주소로 열어야 해요)."
        : "에이전트에 닿지 않았어요. 기다리기가 끝났거나 브라우저가 막았을 수 있어요.";
      let copied = false;
      try { await navigator.clipboard.writeText(text); copied = true; } catch { copied = false; }
      status(nav, `${why} ${copied ? "확정 문구를 복사했어요. 채팅에 붙여 넣어 주세요." : "아래 문구를 복사해 채팅에 붙여 넣어 주세요."}`, text);
    });
    refresh();
    return refresh;
  }

  // 막대가 차지하는 높이(화면 아래 끝에서 막대 맨 위까지)를 --v-dock-space 로 알린다.
  // 무대가 그만큼 비워 막대가 시안·사이트 아래쪽(단추 등)을 가리지 않게 한다. 숨기거나 펼치거나 줄이 바뀌면 다시 잰다.
  function reserveSpace(nav) {
    const measure = () => {
      const tops = [nav, ...nav.querySelectorAll(":scope > *, .v-info")].map((n) => n.getBoundingClientRect()).filter((r) => r.height > 0).map((r) => r.top);
      const space = tops.length ? Math.max(0, Math.ceil(innerHeight - Math.min(...tops))) : 0;
      document.documentElement.style.setProperty("--v-dock-space", `${space}px`);
    };
    new ResizeObserver(measure).observe(nav);
    window.addEventListener("resize", measure);
    new MutationObserver(measure).observe(document.body, { attributes: true, attributeFilter: ["class"] }); // 숨기기·펼치기
    measure();
  }

  window.Dock = { $, $$, el, installTip, syncFocus, toggleDock, onKeys, writeHash, installConfirm, reserveSpace, waiting: Boolean(WAIT) };
})();
