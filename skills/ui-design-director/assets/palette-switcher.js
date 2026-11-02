/*
 * 팔레트 바꿔 보기 — 시안 페이지 아래에 후보 보기(board)와 같은 두 층 막대를 붙인다.
 * 막대 모양과 공용 동작은 dock.css · dock.js, 이 파일은 팔레트 전용 부분만.
 * 페이지는 --c-bg, --c-surface, --c-text, --c-action, --c-on-action, --c-accent 만 쓰면 된다.
 * 후보는 <script type="application/json" id="palettes" data-step="팔레트 고르기"> 안에 넣는다:
 *   [{ "id": "A", "name": "크림과 흙빛", "source": "https://…", "colors": ["#…"],
 *      "roles": { "bg": "#…", "surface": "#…", "text": "#…", "action": "#…", "on-action": "#…", "accent": "#…" },
 *      "note": "선택 사항" }]
 * ← → 팔레트 · M PC/휴대폰 · H 숨기기. 주소 #p=A&v=phone 으로 보던 자리를 기억한다.
 */
(function () {
  "use strict";

  const { $, $$, el } = window.Dock;
  const ROLE_KEYS = ["bg", "surface", "text", "action", "on-action", "accent"];
  const PAIRS = [
    ["글자", "글자 / 배경", "text", "bg"],
    ["버튼", "버튼 글자 / 버튼", "on-action", "action"],
    ["강조", "강조색 / 배경", "accent", "bg"],
  ];
  const VIEWS = ["pc", "phone"];
  const ICONS = {
    prev: '<path d="M15 6l-6 6 6 6"/>',
    next: '<path d="M9 6l6 6-6 6"/>',
    pc: '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/>',
    phone: '<rect x="7" y="3" width="10" height="18" rx="2"/><path d="M11 18h2"/>',
    source: '<path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/>',
    hide: '<path d="M6 9l6 6 6-6"/>',
    show: '<path d="M6 15l6-6 6 6"/>',
  };
  const icon = (name) => `<svg viewBox="0 0 24 24" aria-hidden="true">${ICONS[name]}</svg>`;

  function luminance(hex) {
    let h = hex.replace("#", "");
    if (h.length === 3) h = h.split("").map((c) => c + c).join("");
    const lin = [0, 2, 4].map((i) => {
      const c = parseInt(h.slice(i, i + 2), 16) / 255;
      return c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
    });
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2];
  }

  function contrast(a, b) {
    const [hi, lo] = [luminance(a), luminance(b)].sort((x, y) => y - x);
    return (hi + 0.05) / (lo + 0.05);
  }

  function verdict(ratio) {
    if (ratio >= 4.5) return ["good", "본문 가능"];
    if (ratio >= 3) return ["warn", "큰 글자·버튼만"];
    return ["bad", "장식만"];
  }

  function readPalettes() {
    const source = document.getElementById("palettes");
    if (!source) return null;
    try {
      const list = JSON.parse(source.textContent).filter((p) => p.id && p.roles && ROLE_KEYS.every((k) => p.roles[k]));
      return { step: source.dataset.step || "팔레트 고르기", list };
    } catch (err) {
      console.error("팔레트 목록을 읽지 못했습니다", err);
      return null;
    }
  }

  // 텍스트는 모두 textContent 로 넣는다. 팔레트 이름·설명이 HTML 로 해석되지 않게.
  function barMarkup(total, step) {
    const nav = el("nav", "v-nav");
    nav.setAttribute("aria-label", "팔레트 고르기");
    const markup = `
<div class="v-bar-main v-bar">
<div class="v-group v-g-cands"><button class="v-btn icon v-prev" type="button" aria-label="이전 팔레트" data-tip="이전 팔레트|←">${icon("prev")}</button><ol class="v-thumbs" aria-label="팔레트"></ol><button class="v-btn icon v-next" type="button" aria-label="다음 팔레트" data-tip="다음 팔레트|→">${icon("next")}</button></div>
<div class="v-info" aria-live="polite"><span class="v-title"><b></b><span class="v-title-hint"> · <span class="ps-total"></span>개 중 하나를 골라 주세요</span></span><p class="v-name"></p><span class="v-meta"></span><span class="v-count"></span></div>
<div class="v-group v-g-pages"><ul class="ps-checks" aria-label="명암비"></ul></div>
<div class="v-group v-g-tools"><div class="v-seg v-view" role="group" aria-label="PC 또는 휴대폰"><button class="v-btn" type="button" data-view="pc" data-tip="PC 화면으로 보기|M">${icon("pc")}PC</button><button class="v-btn" type="button" data-view="phone" data-tip="휴대폰 폭으로 보기|M">${icon("phone")}휴대폰</button></div><a class="v-btn icon v-demo" href="#" target="_blank" rel="noopener" aria-label="팔레트 출처 새 창으로 열기" data-tip="팔레트 출처를 새 창으로 열기">${icon("source")}</a><button class="v-btn icon v-hide" type="button" aria-label="막대 숨기기" data-tip="막대 숨기기|H">${icon("hide")}</button></div>
<p class="v-keys"><kbd>←</kbd> <kbd>→</kbd> 팔레트 · <kbd>M</kbd> 휴대폰 · <kbd>H</kbd> 숨기기</p>
</div>
<button class="v-btn v-bar v-reveal" type="button" aria-label="조작 막대 다시 열기"><span class="v-reveal-where"><b></b><span></span></span><span class="v-reveal-open">${icon("show")}열기 H</span></button>`;
    nav.innerHTML = markup; // lint:allow inner-html 고정 틀과 아이콘 상수만 들어감. 팔레트 이름 등 바뀌는 글자는 아래에서 textContent 로 넣음
    nav.querySelector(".v-title b").textContent = step;
    nav.querySelector(".ps-total").textContent = String(total);
    return nav;
  }

  function build({ step, list }) {
    const state = { i: 0, v: "pc" };
    const q = new URLSearchParams(location.hash.slice(1));
    const wanted = list.findIndex((p) => p.id === q.get("p"));
    if (wanted >= 0) state.i = wanted;
    if (VIEWS.includes(q.get("v"))) state.v = q.get("v");

    const nav = barMarkup(list.length, step);
    document.body.classList.add("dock-2", "ps-on");
    document.body.append(nav);

    const thumbs = $(".v-thumbs");
    list.forEach((p, i) => {
      const li = el("li");
      const b = el("button", "v-thumb ps-chip");
      b.type = "button";
      b.setAttribute("aria-label", `${p.id} ${p.name || ""}`.trim());
      b.dataset.tip = `${p.id} ${p.name || ""}`.trim();
      const sw = el("span", "ps-sw");
      (p.colors || []).forEach((c) => {
        const dot = el("span");
        dot.style.background = c;
        sw.append(dot);
      });
      b.append(sw, el("span", "v-thumb-num", p.id));
      b.addEventListener("click", () => { state.i = i; apply(); });
      li.append(b);
      thumbs.append(li);
    });

    function apply() {
      const p = list[state.i];
      const root = document.documentElement.style;
      ROLE_KEYS.forEach((k) => root.setProperty(`--c-${k}`, p.roles[k]));
      $$(".ps-chip").forEach((b, i) => b.setAttribute("aria-current", String(i === state.i)));
      $$(".ps-chip")[state.i].scrollIntoView({ block: "nearest", inline: "nearest" }); // 좁은 화면에서 옆으로 넘긴 줄 안에 보이게
      const name = `${p.id} ${p.name || ""}`.trim();
      $(".v-name").textContent = name;
      $(".v-name").dataset.tip = name;
      $(".v-meta").textContent = p.note || "";
      $(".v-meta").dataset.tip = p.note || "";
      $(".v-count").textContent = `${state.i + 1} / ${list.length}`;
      $(".ps-checks").replaceChildren(...PAIRS.map(([short, full, fg, bg]) => {
        const ratio = contrast(p.roles[fg], p.roles[bg]);
        const [cls, word] = verdict(ratio);
        const li = el("li", "ps-check");
        li.tabIndex = 0;
        li.dataset.tip = `${full} 명암비 ${ratio.toFixed(2)} — 4.5 이상 본문, 3 이상 큰 글자·버튼`;
        li.append(el("span", null, short), el("b", null, ratio.toFixed(2)), el("span", `ps-${cls}`, word));
        return li;
      }));
      const demo = $(".v-demo");
      demo.hidden = !p.source;
      if (p.source) demo.href = p.source;
      $$(".v-view .v-btn").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.view === state.v)));
      document.body.classList.toggle("is-phone", state.v === "phone");
      $(".v-reveal-where b").textContent = name;
      $(".v-reveal-where span").textContent = state.v === "phone" ? "휴대폰" : "PC";
      document.title = `${step} · ${name}`;
      history.replaceState(null, "", `#p=${encodeURIComponent(p.id)}&v=${state.v}`);
    }

    const hideTip = window.Dock.installTip(nav);
    const GROUPS = [[".ps-chip", '.ps-chip[aria-current="true"]'], [".v-view .v-btn", '.v-view .v-btn[aria-pressed="true"]']];
    const after = () => { window.Dock.syncFocus(GROUPS); hideTip(); };
    const move = (step) => { state.i = (state.i + step + list.length) % list.length; apply(); after(); };
    const setView = (v) => { state.v = v; apply(); };
    const toggle = () => { hideTip(); window.Dock.toggleDock(); };

    $(".v-prev").addEventListener("click", () => move(-1));
    $(".v-next").addEventListener("click", () => move(1));
    $$(".v-view .v-btn").forEach((b) => b.addEventListener("click", () => setView(b.dataset.view)));
    $(".v-hide").addEventListener("click", toggle);
    $(".v-reveal").addEventListener("click", toggle);
    window.Dock.onKeys({
      ArrowRight: () => move(1),
      ArrowLeft: () => move(-1),
      m: () => { setView(state.v === "pc" ? "phone" : "pc"); after(); },
      h: toggle,
    });

    // 막대에 페이지 끝이 가리지 않게, 막대 높이만큼 아래 여백을 둔다
    const pad = () => { document.body.style.paddingBottom = `${Math.ceil(innerHeight - nav.getBoundingClientRect().top)}px`; };
    new ResizeObserver(pad).observe(nav);
    window.addEventListener("resize", pad);

    apply();
  }

  document.addEventListener("DOMContentLoaded", () => {
    const data = readPalettes();
    if (data && data.list.length) build(data);
  });
})();
