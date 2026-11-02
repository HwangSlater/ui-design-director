/*
 * 팔레트 바꿔 보기 — 시안 페이지 아래에 팔레트 막대를 붙인다.
 * 페이지는 --c-bg, --c-surface, --c-text, --c-action, --c-on-action, --c-accent 만 쓰면 된다.
 * 후보는 <script type="application/json" id="palettes"> 안에 넣는다:
 *   [{ "id": "A", "name": "크림과 흙빛", "source": "https://…", "colors": ["#…"],
 *      "roles": { "bg": "#…", "surface": "#…", "text": "#…", "action": "#…", "on-action": "#…", "accent": "#…" },
 *      "note": "선택 사항" }]
 * 주소 끝 #p=A 로 처음 보여 줄 팔레트를 고를 수 있다.
 */
(function () {
  "use strict";

  const ROLE_KEYS = ["bg", "surface", "text", "action", "on-action", "accent"];
  const PAIRS = [
    ["글자 / 배경", "text", "bg"],
    ["버튼 글자 / 버튼", "on-action", "action"],
    ["강조 / 배경", "accent", "bg"],
  ];

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

  function el(tag, cls, text) {
    const node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function readPalettes() {
    const source = document.getElementById("palettes");
    if (!source) return [];
    try {
      const list = JSON.parse(source.textContent);
      return list.filter((p) => p.id && p.roles && ROLE_KEYS.every((k) => p.roles[k]));
    } catch (err) {
      console.error("팔레트 목록을 읽지 못했습니다", err);
      return [];
    }
  }

  function build(palettes) {
    const bar = el("aside", "ps-bar");
    bar.setAttribute("aria-label", "팔레트 바꿔 보기");

    const chips = el("div", "ps-chips");
    chips.setAttribute("role", "group");
    chips.setAttribute("aria-label", "팔레트 후보");

    const detail = el("div", "ps-detail");
    const title = el("p", "ps-title");
    const checks = el("ul", "ps-checks");
    const note = el("p", "ps-note");
    const link = el("a", "ps-source", "출처");
    link.target = "_blank";
    link.rel = "noopener";
    detail.append(title, checks, note, link);

    const width = el("button", "ps-width", "휴대폰 폭으로 보기");
    width.type = "button";
    width.setAttribute("aria-pressed", "false");
    width.addEventListener("click", () => {
      const on = document.body.classList.toggle("ps-phone");
      width.setAttribute("aria-pressed", String(on));
      width.textContent = on ? "넓은 화면으로 보기" : "휴대폰 폭으로 보기";
    });

    const buttons = palettes.map((p) => {
      const btn = el("button", "ps-chip");
      btn.type = "button";
      btn.setAttribute("aria-pressed", "false");
      btn.setAttribute("aria-label", `${p.id} ${p.name || ""}`.trim());
      const sw = el("span", "ps-sw");
      (p.colors || []).forEach((c) => {
        const dot = el("span");
        dot.style.background = c;
        sw.append(dot);
      });
      btn.append(el("b", null, p.id), sw);
      btn.addEventListener("click", () => apply(p));
      chips.append(btn);
      return btn;
    });

    function apply(p) {
      const root = document.documentElement.style;
      ROLE_KEYS.forEach((k) => root.setProperty(`--c-${k}`, p.roles[k]));
      buttons.forEach((b, i) => b.setAttribute("aria-pressed", String(palettes[i] === p)));
      title.textContent = `${p.id} · ${p.name || ""}`;
      checks.replaceChildren(
        ...PAIRS.map(([label, fg, bg]) => {
          const ratio = contrast(p.roles[fg], p.roles[bg]);
          const [cls, word] = verdict(ratio);
          const li = el("li");
          li.append(el("span", null, label), el("span", `ps-${cls}`, `${ratio.toFixed(2)} ${word}`));
          return li;
        })
      );
      note.textContent = p.note || "";
      link.hidden = !p.source;
      if (p.source) link.href = p.source;
      history.replaceState(null, "", `#p=${encodeURIComponent(p.id)}`);
    }

    bar.append(chips, detail, width);
    document.body.append(bar);

    const wanted = decodeURIComponent((location.hash.match(/p=([^&]+)/) || [])[1] || "");
    apply(palettes.find((p) => p.id === wanted) || palettes[0]);
  }

  document.addEventListener("DOMContentLoaded", () => {
    const palettes = readPalettes();
    if (palettes.length) build(palettes);
  });
})();
