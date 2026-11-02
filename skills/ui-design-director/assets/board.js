/*
 * 후보 보기 화면 — <script type="application/json" id="board-data"> 를 읽어 그린다.
 * ← → 후보 · ↑ ↓ 화면 · M PC/휴대폰 · H 막대 숨기기.
 * 화면 넘기는 방식 data.mode: "tabs"(한 화면씩) · "stack"(네 화면을 이어 붙여 스크롤만으로 보기).
 * 주소 #c=1&p=home&v=pc 로 보고 있던 자리를 기억한다.
 * 막대 공용 동작(말풍선·숨기기·단축키)은 dock.js.
 */
(function () {
  "use strict";

  const data = JSON.parse(document.getElementById("board-data").textContent);
  const { $, $$, el } = window.Dock;
  const VIEWS = ["pc", "phone"];
  let hideTip = () => {};
  const MODE = data.mode === "stack" ? "stack" : "tabs";
  const SPY_OFFSET = 48; // 이어 보기에서 이 높이 안에 들어온 구획을 「지금 화면」으로 친다
  // 사용자가 고른 화면(state.p)은 후보를 넘겨도 바꾸지 않는다. 없는 후보에서는 「없어요」를 보여 준다.
  const state = { c: 0, p: data.pages[0].key, v: "pc" };

  function readHash() {
    const q = new URLSearchParams(location.hash.slice(1));
    const ci = data.candidates.findIndex((c) => c.id === q.get("c"));
    if (ci >= 0) state.c = ci;
    if (data.pages.some((p) => p.key === q.get("p"))) state.p = q.get("p");
    if (VIEWS.includes(q.get("v"))) state.v = q.get("v");
  }

  function writeHash() {
    const id = encodeURIComponent(data.candidates[state.c].id);
    history.replaceState(null, "", `#c=${id}&p=${state.p}&v=${state.v}`);
  }

  function thumbSrc(cand) {
    const first = data.pages.map((p) => cand.pages[p.key]).find((p) => p && p.desktop);
    return first ? first.desktop : "";
  }

  function fill(box, src, alt, emptyText) {
    box.replaceChildren();
    box.scrollTop = 0;
    if (src) {
      const img = el("img");
      img.src = src;
      img.alt = alt;
      img.decoding = "async";
      box.append(img);
    } else {
      box.append(el("p", "v-empty", emptyText));
    }
  }

  const frames = () => [[".v-desktop .v-scroll", "desktop", "PC"], [".v-phone .v-scroll", "phone", "휴대폰"]];
  const labelOf = (key) => data.pages.find((p) => p.key === key).label;

  function renderTabsFrames(cand) {
    const page = cand.pages[state.p];
    const label = labelOf(state.p);
    const none = `${cand.title}에는 「${label}」 화면이 없어요. 다른 화면을 골라 보세요.`;
    frames().forEach(([sel, kind, name]) =>
      fill($(sel), page && page[kind], `${cand.title} ${label} ${name} 화면`, page ? `${name} 화면 캡처 없음` : none));
  }

  function renderStackFrames(cand) {
    frames().forEach(([sel, kind, name]) => {
      const box = $(sel);
      box.replaceChildren(...data.pages.map((p) => {
        const sec = el("section", "v-sec");
        sec.dataset.key = p.key;
        sec.append(el("div", "v-sec-head", p.label));
        const page = cand.pages[p.key];
        if (page && page[kind]) {
          const img = el("img");
          img.src = page[kind];
          img.alt = `${cand.title} ${p.label} ${name} 화면`;
          const size = page[`${kind}_size`];
          if (size) { img.width = size[0]; img.height = size[1]; } // 사진이 오기 전에 자리를 잡아 이동 위치가 맞게
          img.decoding = "async";
          sec.append(img);
        } else {
          sec.append(el("p", "v-sec-empty", `${cand.title}에는 「${p.label}」 화면이 없어요`));
        }
        return sec;
      }));
      scrollToPage(box, state.p, "instant");
    });
  }

  function scrollToPage(box, key, behavior) {
    const sec = box.querySelector(`.v-sec[data-key="${key}"]`);
    if (sec) box.scrollTo({ top: sec.offsetTop, behavior });
  }

  function updatePageTabs(cand) {
    $$(".v-pages .v-btn").forEach((b) => {
      const missing = !cand.pages[b.dataset.key];
      b.dataset.missing = String(missing);
      b.setAttribute("aria-selected", String(b.dataset.key === state.p));
      b.dataset.tip = missing ? `${cand.title}에는 이 화면이 없어요` : `${b.textContent}${MODE === "stack" ? "(으)로 이동" : " 보기"}|↑ ↓`;
    });
    document.title = `${data.step || ""} · ${cand.id} ${cand.title} · ${labelOf(state.p)}`;
    $(".v-reveal-where b").textContent = `${cand.id} ${cand.title}`;
    $(".v-reveal-where span").textContent = `${labelOf(state.p)} · ${state.v === "phone" ? "휴대폰" : "PC"}`;
    writeHash();
  }

  function render() {
    const cand = data.candidates[state.c];
    $$(".v-thumb").forEach((b, i) => b.setAttribute("aria-current", String(i === state.c)));
    const name = `${cand.id} ${cand.title}`;
    const meta = [cand.meta, cand.recommended ? "추천" : ""].filter(Boolean).join(" · ");
    $(".v-name").textContent = name;
    $(".v-name").dataset.tip = name; // 길어서 말줄임이 되면 말풍선으로 전체를 본다
    $(".v-meta").textContent = meta;
    $(".v-meta").dataset.tip = meta;
    $(".v-count").textContent = `${state.c + 1} / ${data.candidates.length}`;
    const demo = $(".v-demo");
    demo.hidden = !cand.demo;
    if (cand.demo) demo.href = cand.demo;
    $$(".v-view .v-btn").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.view === state.v)));
    document.body.classList.toggle("is-phone", state.v === "phone");
    (MODE === "stack" ? renderStackFrames : renderTabsFrames)(cand);
    updatePageTabs(cand);
  }

  function choosePage(key, behavior = "instant") { // 화면 사이가 수천 px라 부드럽게 넘기면 늦다
    state.p = key;
    if (MODE === "stack") {
      frames().forEach(([sel]) => scrollToPage($(sel), key, behavior));
      updatePageTabs(data.candidates[state.c]);
    } else {
      render();
    }
  }

  function movePage(step) {
    const i = data.pages.findIndex((p) => p.key === state.p);
    const next = data.pages[Math.min(Math.max(i + step, 0), data.pages.length - 1)];
    if (next.key !== state.p) choosePage(next.key);
  }

  // 이어 보기: 스크롤 위치로 지금 화면 탭을 맞춘다
  function spy(e) {
    if (MODE !== "stack") return;
    const box = e.currentTarget;
    const secs = Array.from(box.querySelectorAll(".v-sec"));
    const current = secs.filter((s) => s.offsetTop - box.scrollTop <= SPY_OFFSET).pop() || secs[0];
    if (current && current.dataset.key !== state.p) {
      state.p = current.dataset.key;
      updatePageTabs(data.candidates[state.c]);
    }
  }

  function moveCandidate(step) {
    state.c = (state.c + step + data.candidates.length) % data.candidates.length;
    render();
  }

  const GROUPS = [
    [".v-thumb", '.v-thumb[aria-current="true"]'],
    [".v-pages .v-btn", '.v-pages .v-btn[aria-selected="true"]'],
    [".v-view .v-btn", '.v-view .v-btn[aria-pressed="true"]'],
  ];
  function syncFocus() {
    window.Dock.syncFocus(GROUPS);
    hideTip();
  }

  function toggleDock() {
    hideTip();
    window.Dock.toggleDock();
  }

  // 휠은 어디서 굴려도 지금 보이는 시안을 내린다(막대 위, 휴대폰 바깥 포함)
  function forwardWheel(e) {
    if (e.target.closest(".v-scroll")) return;
    const box = document.body.classList.contains("is-phone") ? $(".v-phone .v-scroll") : $(".v-desktop .v-scroll");
    box.scrollBy({ top: e.deltaY });
    e.preventDefault();
  }

  function build() {
    const thumbs = $(".v-thumbs");
    data.candidates.forEach((c, i) => {
      const li = el("li");
      const b = el("button", "v-thumb");
      b.type = "button";
      b.setAttribute("aria-label", `${c.id}번 ${c.title}`);
      b.dataset.tip = `${c.id} ${c.title}${c.meta ? " · " + c.meta : ""}`;
      const src = thumbSrc(c);
      if (src) {
        const img = el("img");
        img.src = src;
        img.alt = "";
        img.loading = "lazy";
        b.append(img);
      }
      b.append(el("span", "v-thumb-num", c.id));
      b.addEventListener("click", () => { state.c = i; render(); });
      li.append(b);
      thumbs.append(li);
    });
    $(".v-prev").addEventListener("click", () => moveCandidate(-1));
    $(".v-next").addEventListener("click", () => moveCandidate(1));

    const pages = $(".v-pages");
    data.pages.forEach((p) => {
      const b = el("button", "v-btn");
      b.append(el("span", "v-label", p.label)); // 긴 이름은 말줄임, 전체는 말풍선에
      b.type = "button";
      b.dataset.key = p.key;
      b.setAttribute("role", "tab");
      b.addEventListener("click", () => choosePage(p.key));
      pages.append(b);
    });

    $$(".v-view .v-btn").forEach((b) => b.addEventListener("click", () => { state.v = b.dataset.view; render(); }));
    $(".v-hide").addEventListener("click", toggleDock);
    $(".v-reveal").addEventListener("click", toggleDock);

    hideTip = window.Dock.installTip($(".v-nav"));
    document.addEventListener("wheel", forwardWheel, { passive: false });
    frames().forEach(([sel]) => $(sel).addEventListener("scroll", spy, { passive: true }));
    document.body.classList.add(`mode-${MODE}`);

    const flipView = () => { state.v = state.v === "pc" ? "phone" : "pc"; render(); syncFocus(); };
    window.Dock.onKeys({
      ArrowRight: () => { moveCandidate(1); syncFocus(); },
      ArrowLeft: () => { moveCandidate(-1); syncFocus(); },
      ArrowDown: () => { movePage(1); syncFocus(); },
      ArrowUp: () => { movePage(-1); syncFocus(); },
      m: flipView,
      h: toggleDock,
    });

    // 다른 후보 사진을 미리 받아 넘길 때 비지 않게 한다
    window.addEventListener("load", () => {
      data.candidates.forEach((c) => Object.values(c.pages).forEach((p) => {
        [p.desktop, p.phone].filter(Boolean).forEach((src) => { const i = new Image(); i.src = src; });
      }));
    });
  }

  readHash();
  build();
  render();
})();
