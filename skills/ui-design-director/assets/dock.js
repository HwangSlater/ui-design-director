/*
 * 아래 막대 공용 동작 — board.js(후보 보기)와 palette-switcher.js(팔레트 바꿔 보기)가 함께 쓴다.
 * 말풍선 하나, 숨기기/구석 알약, 단축키 뒤 포커스 맞추기.
 */
(function () {
  "use strict";

  const TIP_GAP = 10;
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

  window.Dock = { $, $$, el, installTip, syncFocus, toggleDock, onKeys };
})();
