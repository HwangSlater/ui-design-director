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
  let refreshConfirm = () => {};
  const MODE = data.mode === "stack" ? "stack" : "tabs";
  const SPY_OFFSET = 48; // 이어 보기에서 이 높이 안에 들어온 구획을 「지금 화면」으로 친다
  // 사용자가 고른 화면(state.p)은 후보를 넘겨도 바꾸지 않는다. 없는 후보에서는 「없어요」를 보여 준다.
  const state = { c: 0, p: data.pages[0].key, v: "pc" };
  // 휴대폰 폭 창에서는 휴대폰 보기로 시작한다(주소에 v 가 있으면 그대로) — PC 보기는 글자가 안 읽힐 만큼 줄었다
  const NARROW = "(max-width: 600px)";

  function readHash() {
    const q = new URLSearchParams(location.hash.slice(1));
    const ci = data.candidates.findIndex((c) => c.id === q.get("c"));
    if (ci >= 0) state.c = ci;
    if (data.pages.some((p) => p.key === q.get("p"))) state.p = q.get("p");
    if (VIEWS.includes(q.get("v"))) state.v = q.get("v");
    else if (matchMedia(NARROW).matches) state.v = "phone";
  }

  function writeHash() {
    window.Dock.writeHash({ c: data.candidates[state.c].id, p: state.p, v: state.v });
  }

  function thumbSrc(cand) {
    const first = data.pages.map((p) => cand.pages[p.key]).find((p) => p && p.desktop);
    return first ? first.desktop : "";
  }

  // 실제 사이트 모드(data.live): 가운데에 캡처 대신 실제 페이지를 띄운다. 막대·썸네일·확정은 그대로.
  // 막는 사이트(cand.blocked)는 live_proxy.mjs(주소 ?proxy=)로, 우회가 없으면 캡처로 대신한다.
  const PROXY = new URLSearchParams(location.search).get("proxy") || "";
  const LIVE_W = { desktop: 1280, phone: 390 };
  const live = { x: false, js: {} }; // x: 바로 띄운 곳도 우회로 보기 · js: 후보별 스크립트 켬(자동 판단 뒤 사용자가 바꿈)
  // 띄운 틀은 버리지 않고 숨겨 둔다 — 넘겼다 돌아오면 처음부터 다시 불러왔다. 메모리 때문에 POOL_MAX 개까지(오래된 것부터 버림)
  const POOL_MAX = 4; // 지금 후보와 다음 후보(PC·휴대폰) — 6개는 숨긴 틀이 계속 그려 메모리가 1.5배(2.2GB)였다
  const pool = new Map(); // 열쇠(후보·화면 종류·주소·우회·스크립트) → iframe
  function poolFrame(key, box, make) {
    let f = pool.get(key);
    const created = !f;
    if (!f) {
      f = make();
      pool.set(key, f);
      while (pool.size > POOL_MAX) { const [oldKey, old] = pool.entries().next().value; pool.delete(oldKey); old.remove(); }
    } else { pool.delete(key); pool.set(key, f); } // 최근에 쓴 것을 뒤로
    if (f.parentNode !== box) box.append(f);
    return [f, created];
  }
  // 숨긴 틀은 안 보이게만 한다(display:none 이면 사이트가 그리기를 멈춰 다 뜨지 못했다 — 만개의레시피)
  const hideFrame = (f) => { Object.assign(f.style, { visibility: "hidden", position: "absolute", top: "0", left: "0" }); f.inert = true; };
  const showFrame = (f) => { Object.assign(f.style, { visibility: "visible", position: "static" }); f.inert = false; };
  // 칸보다 좁게 그리면 오른쪽에 흰 띠가 남았다 — 칸이 기준 폭보다 넓으면 칸 폭 그대로, 좁으면 기준 폭으로 그려 줄인다
  function sizeFrame(box, kind, f) {
    const bw = box.clientWidth, bh = box.clientHeight;
    if (!bw || !bh) return; // 숨은 칸은 크기가 0 — 보이게 되면 ResizeObserver 가 다시 맞춘다
    const k = Math.min(1, bw / LIVE_W[kind]);
    Object.assign(f.style, { width: `${bw / k}px`, height: `${bh / k}px`, transform: `scale(${k})`, transformOrigin: "0 0", border: "0" });
  }
  // 칸 크기가 바뀔 때(창 크기, 막대 높이, PC↔휴대폰) 띄운 틀을 모두 다시 맞춘다 — 처음 잴 때는 자리가 덜 잡혀 있었다
  function watchFrames() {
    const resize = (box) => box.querySelectorAll(":scope > iframe").forEach((f) => sizeFrame(box, box.dataset.kind, f));
    const ro = new ResizeObserver((entries) => entries.forEach((e) => resize(e.target)));
    frames().forEach(([sel, kind]) => { const box = $(sel); box.dataset.kind = kind; ro.observe(box); });
    window.addEventListener("resize", () => frames().forEach(([sel]) => resize($(sel))));
  }
  // show=false 면 뒤에서 미리 띄우기만 한다(다음·이전 후보)
  function liveFrame(box, kind, cand, url, alt, show = true) {
    if (show) {
      box.style.overflow = "hidden";
      box.querySelectorAll(":scope > :not(iframe)").forEach((n) => n.remove());
      box.querySelectorAll(":scope > iframe").forEach(hideFrame);
      if (document.activeElement && document.activeElement.tagName === "IFRAME") document.activeElement.blur(); // 넘긴 뒤 초점은 보기 화면에
    }
    const proxied = (cand.blocked || live.x) && PROXY;
    const place = (src, sandbox) => {
      const [f, created] = poolFrame(`${cand.id}|${kind}|${src}`, box, () => {
        const nf = el("iframe");
        nf.title = alt;
        if (sandbox !== null) nf.setAttribute("sandbox", sandbox);
        // 미리 띄우는 틀만 숨겨서 만든다 — 보여 줄 틀까지 숨긴 채 만들면 브라우저가 그리기를 늦춰 첫 화면이 두 배(6초→12초) 걸렸다
        if (!show) hideFrame(nf); // inert: 숨겨 둔 사이트가 키보드 초점을 가져가면 ←→ 로 후보를 넘길 수 없었다
        nf.addEventListener("load", () => { nf.dataset.loaded = "1"; if (show) preloadNeighbours(); }, { once: true });
        nf.src = src;
        return nf;
      });
      sizeFrame(box, kind, f);
      if (show && !created) setTimeout(preloadNeighbours, 0); // 이미 뜬 틀을 다시 꺼냈으면 load 가 다시 오지 않는다
      if (show && current(box, kind) === `${cand.id}|${url}`) { box.current = f; box.querySelectorAll(":scope > iframe").forEach((o) => (o === f ? showFrame(o) : hideFrame(o))); box.querySelector(":scope > .v-empty")?.remove(); }
    };
    if (show) box.dataset.want = `${kind}|${cand.id}|${url}`;
    if (!proxied) { place(url, null); return; }
    const src = `${PROXY}${encodeURIComponent(url)}?ua=${kind === "phone" ? "phone" : "pc"}`;
    // 맨 위 창을 바꾸지 못하게 샌드박스. 스크립트는 스크립트로 그리는 사이트에만
    const placeProxied = (js) => place(src + (js ? "&js=1" : ""), (js ? "allow-scripts " : "") + "allow-same-origin allow-popups allow-popups-to-escape-sandbox");
    const known = live.js[cand.id];
    if (typeof known === "boolean") { placeProxied(known); return; }
    if (show) box.append(el("p", "v-empty", `${cand.title} 불러오는 중…`));
    fetch(`${src}&probe=1`).then((r) => r.json()).then((j) => { live.js[cand.id] = !!j.js; refreshLiveButtons(); placeProxied(live.js[cand.id]); }).catch(() => placeProxied(false));
  }
  // 묻는 동안 다른 후보로 넘어갔으면 늦게 온 틀을 보이지 않게
  const current = (box, kind) => (box.dataset.want || "").replace(`${kind}|`, "");
  // 지금 후보가 PC·휴대폰 모두 다 뜬 뒤에 다음 후보 하나를 뒤에서 미리 띄운다
  // (한 화면만 떠도 시작하면 아직 받는 다른 화면과 대역폭을 나눠 첫 화면이 6초→12초로 느려졌다)
  function preloadNeighbours() {
    if (!data.live) return;
    // 판단은 칸마다 지금 보여 주는 틀(box.current)로 — 숨은 휴대폰 칸이 먼저 떠서 PC 화면이 받는 중에 미리 띄우기가 시작됐다(첫 화면 6초→12초)
    if (frames().some(([sel]) => !$(sel).current || $(sel).current.dataset.loaded !== "1")) return;
    const n = data.candidates.length;
    [1].forEach((d) => {
      const cand = data.candidates[(state.c + d + n) % n];
      const page = cand.pages[state.p];
      if (!page || !page.url || (cand.blocked && !PROXY)) return;
      frames().forEach(([sel, kind, name]) => liveFrame($(sel), kind, cand, page.url, `${cand.title} ${labelOf(state.p)} ${name} 화면`, false));
    });
  }
  let refreshLiveButtons = () => {};

  function fill(box, src, alt, emptyText) {
    // 숨겨 둔 실제 사이트 틀은 남긴다(지우면 다시 붙일 때 처음부터 불러온다)
    box.querySelectorAll(":scope > :not(iframe)").forEach((n) => n.remove());
    box.querySelectorAll(":scope > iframe").forEach(hideFrame);
    delete box.dataset.want;
    box.current = null;
    box.scrollTop = 0;
    box.style.overflow = "";
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
    frames().forEach(([sel, kind, name]) => {
      const alt = `${cand.title} ${label} ${name} 화면`;
      const showLive = data.live && page && page.url && (!cand.blocked || PROXY || !page[kind]);
      if (showLive) liveFrame($(sel), kind, cand, page.url, alt);
      else fill($(sel), page && page[kind], alt, page ? `${name} 화면 캡처 없음` : none);
    });
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
      if (b.dataset.key === state.p) b.scrollIntoView({ block: "nearest", inline: "nearest" }); // 탭이 많아 옆으로 넘겨도 고른 것이 보이게
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
    $$(".v-thumb")[state.c].scrollIntoView({ block: "nearest", inline: "nearest" }); // 썸네일이 많아 옆으로 넘겨도 고른 것이 보이게
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
    refreshConfirm();
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
    live.x = false; // 우회로 보기는 후보마다 다시 고른다
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

  // 실제 사이트 모드 단추: 우회로 보기 · 스크립트 켜기 · 실제 창으로 보기. 같은 막대, 같은 단추 모양
  let win = null;
  const WIN = { pc: [1280, 800], phone: [390, 844] };
  function currentUrl() { const p = data.candidates[state.c].pages[state.p]; return p && p.url; }
  function followWindow() {
    if (!win || win.closed) { win = null; return; }
    const [w, h] = WIN[state.v];
    try { win.resizeTo(w + 16, h + 88); } catch (e) { /* 브라우저가 막으면 크기는 그대로 */ }
    const url = currentUrl();
    if (url) win = window.open(url, "live-candidate") || win; // 다른 출처로 넘어간 창은 location 대입이 무시돼 같은 이름으로 다시 연다
  }
  function buildLive() {
    const confirm = $(".v-confirm");
    const add = (cls, label, tip, onClick) => {
      const b = el("button", `v-btn ${cls}`);
      b.type = "button";
      b.append(el("span", "v-label", label));
      b.dataset.tip = tip;
      b.setAttribute("aria-pressed", "false");
      b.addEventListener("click", onClick);
      confirm.before(b);
      return b;
    };
    const bx = add("v-live-proxy", "우회로 보기", "바로 띄운 화면이 막히거나 비면 우회해서 띄워요", () => { live.x = !live.x; render(); });
    const bj = add("v-live-js", "스크립트 켜기", "우회 화면이 비거나 사진이 안 나오면 사이트 스크립트를 켜요", () => { const c = data.candidates[state.c]; live.js[c.id] = live.js[c.id] !== true; render(); });
    const bw = add("v-live-win", "실제 창으로", "실제 사이트를 휴대폰·PC 크기 창으로 열어요. 후보를 넘기면 창도 따라가요 — 움직임·쓰는 느낌은 여기서", () => {
      if (win && !win.closed) { win.close(); win = null; refreshLiveButtons(); return; }
      const [w, h] = WIN[state.v];
      const left = Math.max(0, Math.min(screen.availWidth - w - 16, window.screenX + window.outerWidth));
      win = window.open("about:blank", "live-candidate", `popup,width=${w},height=${h},left=${left},top=${Math.max(0, window.screenY)}`);
      if (!win) { $(".v-meta").textContent = "브라우저가 새 창을 막았어요. 주소창 오른쪽의 팝업 차단을 풀어 주세요."; return; }
      followWindow(); refreshLiveButtons();
    });
    refreshLiveButtons = () => {
      const c = data.candidates[state.c];
      bx.hidden = !PROXY || !!c.blocked; // 막힌 곳은 늘 우회로 띄운다
      bx.setAttribute("aria-pressed", String(live.x));
      bj.hidden = !PROXY || !(c.blocked || live.x);
      bj.setAttribute("aria-pressed", String(live.js[c.id] === true));
      bw.setAttribute("aria-pressed", String(!!(win && !win.closed)));
    };
    const plain = render;
    render = function () { plain(); refreshLiveButtons(); followWindow(); };
  }

  // 실제 사이트 모드는 캡처가 없어 썸네일이 번호만 있었다 — live_proxy.mjs 가 뒤에서 찍는 thumbs/<id>.jpg 를 생길 때까지 다시 불러 본다.
  // 다 받은 뒤에만 붙인다(깨진 그림 표시가 보이지 않게). 번호 표시는 그대로.
  const THUMB_RETRY_MS = 3000;
  const THUMB_RETRY_MAX = 40; // 3초 × 40 = 2분 — 그 뒤에도 없으면 번호만
  function liveThumb(button, cand) {
    const base = `thumbs/${encodeURIComponent(cand.id)}.jpg`;
    let tries = 0;
    const img = el("img");
    img.alt = "";
    img.addEventListener("load", () => button.prepend(img), { once: true });
    img.addEventListener("error", () => { if (++tries < THUMB_RETRY_MAX) setTimeout(() => { img.src = `${base}?t=${tries}`; }, THUMB_RETRY_MS); });
    img.src = base;
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
      b.append(el("span", "v-thumb-num", c.id));
      if (src) {
        const img = el("img");
        img.src = src;
        img.alt = "";
        img.loading = "lazy";
        b.prepend(img);
      } else if (data.live) liveThumb(b, c);
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
    if (data.live) buildLive();
    watchFrames();
    window.Dock.reserveSpace($(".v-nav"));

    hideTip = window.Dock.installTip($(".v-nav"));
    refreshConfirm = window.Dock.installConfirm($(".v-nav"), $(".v-confirm"), () => {
      const cand = data.candidates[state.c];
      return { step: data.step, label: `${cand.id} ${cand.title}`, choice: { candidate: cand.id, title: cand.title } };
    });
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
