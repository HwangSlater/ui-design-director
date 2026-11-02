/*
 * 팔레트 바꿔 보기 — 시안 페이지 아래에 후보 보기(board)와 같은 두 층 막대를 붙인다.
 * 막대 모양과 공용 동작은 dock.css · dock.js, 이 파일은 팔레트 전용 부분만.
 * 페이지는 --c-bg, --c-surface, --c-text, --c-action, --c-on-action, --c-accent 만 쓰면 된다.
 * 후보는 <script type="application/json" id="palettes" data-step="팔레트 고르기"> 안에 넣는다:
 *   [{ "id": "A", "name": "크림과 흙빛", "source": "https://…", "colors": ["#…"],
 *      "roles": { "bg": "#…", "surface": "#…", "text": "#…", "action": "#…", "on-action": "#…", "accent": "#…" },
 *      "note": "선택 사항" }]
 * 글꼴 후보(선택)는 <script type="application/json" id="fonts"> 에 넣는다. 페이지는 --f-heading, --f-body 를 쓴다:
 *   [{ "id": "1", "name": "고운바탕 + 고운돋움", "heading": "\"Gowun Batang\", serif", "body": "…",
 *      "css": ["https://fonts.googleapis.com/…"], "license": "OFL", "source": "https://…", "note": "선택 사항" }]
 * ← → 팔레트 · F 글꼴 · M PC/휴대폰 · H 숨기기. 주소 #p=A&f=1&v=phone 으로 보던 자리를 기억한다.
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
  const MENU_GAP = 10; // 글꼴 메뉴와 막대 사이
  const ICONS = {
    prev: '<path d="M15 6l-6 6 6 6"/>',
    next: '<path d="M9 6l6 6-6 6"/>',
    pc: '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/>',
    phone: '<rect x="7" y="3" width="10" height="18" rx="2"/><path d="M11 18h2"/>',
    source: '<path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/>',
    hide: '<path d="M6 9l6 6 6-6"/>',
    show: '<path d="M6 15l6-6 6 6"/>',
    down: '<path d="M8 10l4 4 4-4"/>',
    check: '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
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

  function readFonts() {
    const source = document.getElementById("fonts");
    if (!source) return [];
    try {
      return JSON.parse(source.textContent).filter((f) => f.id && f.heading && f.body);
    } catch (err) {
      console.error("글꼴 목록을 읽지 못했습니다", err);
      return [];
    }
  }

  // 글꼴 파일은 처음 쓸 때 한 번만 불러온다
  const loadedCss = new Set();
  function loadFont(f) {
    (f.css || []).forEach((href) => {
      if (loadedCss.has(href)) return;
      loadedCss.add(href);
      const link = el("link");
      link.rel = "stylesheet";
      link.href = href;
      document.head.append(link);
    });
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
<div class="v-group v-g-tools"><div class="v-seg v-view" role="group" aria-label="PC 또는 휴대폰"><button class="v-btn" type="button" data-view="pc" data-tip="PC 화면으로 보기|M">${icon("pc")}PC</button><button class="v-btn" type="button" data-view="phone" data-tip="휴대폰 폭으로 보기|M">${icon("phone")}휴대폰</button></div><div class="ps-font"><button class="v-btn ps-font-btn" type="button" aria-haspopup="true" aria-expanded="false" data-tip="글꼴 바꾸기|F"><span class="ps-aa" aria-hidden="true">가</span><span class="v-label"></span>${icon("down")}</button><div class="ps-font-menu" role="group" aria-label="글꼴 후보" hidden></div></div><a class="v-btn icon v-demo" href="#" target="_blank" rel="noopener" aria-label="팔레트 출처 새 창으로 열기" data-tip="팔레트 출처를 새 창으로 열기">${icon("source")}</a><button class="v-btn v-confirm" type="button">${icon("check")}<span class="v-label">확정</span></button><button class="v-btn icon v-hide" type="button" aria-label="막대 숨기기" data-tip="막대 숨기기|H">${icon("hide")}</button></div>
<p class="v-keys"><kbd>←</kbd> <kbd>→</kbd> 팔레트 · <kbd>F</kbd> 글꼴 · <kbd>M</kbd> 휴대폰 · <kbd>H</kbd> 숨기기</p>
</div>
<button class="v-btn v-bar v-reveal" type="button" aria-label="조작 막대 다시 열기"><span class="v-reveal-where"><b></b><span></span></span><span class="v-reveal-open">${icon("show")}열기 H</span></button>`;
    nav.innerHTML = markup; // lint:allow inner-html 고정 틀과 아이콘 상수만 들어감. 팔레트 이름 등 바뀌는 글자는 아래에서 textContent 로 넣음
    nav.querySelector(".v-title b").textContent = step;
    nav.querySelector(".ps-total").textContent = String(total);
    return nav;
  }

  function build({ step, list }, fonts) {
    const state = { i: 0, f: 0, v: "pc" };
    const q = new URLSearchParams(location.hash.slice(1));
    const wanted = list.findIndex((p) => p.id === q.get("p"));
    if (wanted >= 0) state.i = wanted;
    if (VIEWS.includes(q.get("v"))) state.v = q.get("v");
    const wantedFont = fonts.findIndex((f) => f.id === q.get("f"));
    if (wantedFont >= 0) state.f = wantedFont;

    const nav = barMarkup(list.length, step);
    document.body.classList.add("dock-2", "ps-on");
    document.body.append(nav);
    if (!fonts.length) $(".ps-font").remove();

    // 글꼴 메뉴 — 항목마다 그 글꼴로 이름과 견본 문장을 보여 준다
    const menu = $(".ps-font-menu");
    const fontBtn = $(".ps-font-btn");
    fonts.forEach((f, i) => {
      const b = el("button", "ps-font-item");
      b.type = "button";
      const title = el("b", null, `${f.id} ${f.name || ""}`.trim());
      title.style.fontFamily = f.heading;
      const sample = el("span", null, "손으로 빚어 매일 쓰는 그릇 · 38,000원");
      sample.style.fontFamily = f.body;
      b.append(title, sample, el("small", null, [f.license, f.note].filter(Boolean).join(" · ")));
      b.addEventListener("click", () => { state.f = i; apply(); closeMenu(); fontBtn.focus({ preventScroll: true }); });
      menu.append(b);
    });
    function openMenu() {
      fonts.forEach(loadFont);
      menu.hidden = false;
      fontBtn.setAttribute("aria-expanded", "true");
      const r = fontBtn.getBoundingClientRect();
      const bar = nav.getBoundingClientRect();
      // 단추 오른쪽 끝에 맞추되 화면 밖으로 나가지 않게
      const left = Math.min(Math.max(r.right - menu.offsetWidth, MENU_GAP), innerWidth - menu.offsetWidth - MENU_GAP);
      menu.style.left = `${left}px`;
      menu.style.bottom = `${innerHeight - bar.top + MENU_GAP}px`;
      hideTip();
      (menu.querySelector('[aria-pressed="true"]') || menu.firstChild).focus({ preventScroll: true });
    }
    function closeMenu() {
      if (menu.hidden) return;
      menu.hidden = true;
      fontBtn.setAttribute("aria-expanded", "false");
    }
    if (fonts.length) {
      fontBtn.addEventListener("click", () => (menu.hidden ? openMenu() : closeMenu()));
      document.addEventListener("pointerdown", (e) => { if (!e.target.closest(".ps-font")) closeMenu(); });
      window.addEventListener("resize", closeMenu); // 열린 자리가 단추와 어긋나지 않게
      document.addEventListener("keydown", (e) => { if (e.key === "Escape" && !menu.hidden) { closeMenu(); fontBtn.focus({ preventScroll: true }); } });
    }

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
      const f = fonts[state.f];
      if (f) {
        loadFont(f);
        root.setProperty("--f-heading", f.heading);
        root.setProperty("--f-body", f.body);
        fontBtn.querySelector(".v-label").textContent = `글꼴 ${f.id}`;
        fontBtn.dataset.tip = `글꼴 ${f.id} ${f.name || ""} 바꾸기|F`;
        $$(".ps-font-item").forEach((b, i) => b.setAttribute("aria-pressed", String(i === state.f)));
      }
      const meta = [f ? `글꼴 ${f.id} ${f.name || ""}`.trim() : "", p.note || ""].filter(Boolean).join(" · ");
      $(".v-name").textContent = name;
      $(".v-name").dataset.tip = name;
      $(".v-meta").textContent = meta;
      $(".v-meta").dataset.tip = meta;
      $(".v-count").textContent = `${state.i + 1} / ${list.length}`;
      $(".ps-checks").replaceChildren(...PAIRS.map(([short, full, fg, bg]) => {
        const ratio = contrast(p.roles[fg], p.roles[bg]);
        const [cls, word] = verdict(ratio);
        const li = el("li", "ps-check");
        li.tabIndex = 0;
        li.dataset.tip = `${full} 명암비 ${ratio.toFixed(2)} — 4.5 이상 본문, 3 이상 큰 글자·버튼`;
        const top = el("span", "ps-check-top");
        top.append(el("span", null, short), el("b", null, ratio.toFixed(2)));
        li.append(top, el("span", `ps-${cls}`, word));
        return li;
      }));
      const demo = $(".v-demo");
      demo.hidden = !p.source;
      if (p.source) demo.href = p.source;
      $$(".v-view .v-btn").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.view === state.v)));
      document.body.classList.toggle("is-phone", state.v === "phone");
      $(".v-reveal-where b").textContent = name;
      const where = [f ? `글꼴 ${f.id}` : "", state.v === "phone" ? "휴대폰" : "PC"].filter(Boolean).join(" · ");
      $(".v-reveal-where span").textContent = where;
      document.title = `${step} · ${name}${f ? " · " + f.name : ""}`;
      window.Dock.writeHash(f ? { p: p.id, f: f.id, v: state.v } : { p: p.id, v: state.v });
      refreshConfirm();
    }

    const hideTip = window.Dock.installTip(nav);
    const refreshConfirm = window.Dock.installConfirm(nav, $(".v-confirm"), () => {
      const p = list[state.i];
      const f = fonts[state.f];
      const label = [`${p.id} ${p.name || ""}`.trim(), f ? `글꼴 ${f.id} ${f.name || ""}`.trim() : ""].filter(Boolean).join(" + ");
      return { step, label, choice: { palette: p.id, colors: p.roles, font: f ? { id: f.id, name: f.name, heading: f.heading, body: f.body } : null } };
    });
    const GROUPS = [[".ps-chip", '.ps-chip[aria-current="true"]'], [".v-view .v-btn", '.v-view .v-btn[aria-pressed="true"]']];
    const after = () => { window.Dock.syncFocus(GROUPS); hideTip(); };
    const move = (step) => { state.i = (state.i + step + list.length) % list.length; apply(); after(); };
    const setView = (v) => { state.v = v; apply(); };
    const toggle = () => { hideTip(); closeMenu(); window.Dock.toggleDock(); };
    const nextFont = () => { if (!fonts.length) return; state.f = (state.f + 1) % fonts.length; apply(); hideTip(); };

    $(".v-prev").addEventListener("click", () => move(-1));
    $(".v-next").addEventListener("click", () => move(1));
    $$(".v-view .v-btn").forEach((b) => b.addEventListener("click", () => setView(b.dataset.view)));
    $(".v-hide").addEventListener("click", toggle);
    $(".v-reveal").addEventListener("click", toggle);
    window.Dock.onKeys({
      ArrowRight: () => move(1),
      ArrowLeft: () => move(-1),
      m: () => { setView(state.v === "pc" ? "phone" : "pc"); after(); },
      f: nextFont,
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
    if (data && data.list.length) build(data, readFonts());
  });
})();
