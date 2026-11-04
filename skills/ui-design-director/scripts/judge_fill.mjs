// 블라인드 판정용 사본만: 견본 흔적을 걷어 낸다. 의뢰인에게 보내는 그림에는 쓰지 않는다.
// 판정자는 「0000」 번호·빗금 사진 자리·「견본」 표시를 디자인보다 먼저 AI 흔적으로 꼽았다(횟집 95%, 마당집 카페) —
// 그러면 그림이 디자인이 아니라 견본 자리를 잰다. capture.mjs 의 일감에 "judge": true 를 주면 페이지를 연 뒤 이것을 돈다.
//  1. .sample · .proto · [data-sample] 과 빗금·빈 자리(클래스 slot/placeholder/hatch) 를 숨긴다
//  2. 「0000」이 든 전화번호를 그럴듯한 번호로 바꾼다(글과 tel: 주소 둘 다, 같은 번호는 같은 값으로)
//  3. 그래도 남은 흔적(0000, ○○, 견본, 「…자리」)을 돌려준다 — capture.mjs 가 찍고 알린다

export const JUDGE_HIDE = ".sample, .proto, [data-sample], [class*='slot'], [class*='placeholder'], [class*='hatch']";
export const LEFT_MARKS = /0000|○○|견본|사진 자리|지도 자리/g;

// 페이지 안에서 도는 식. 번호는 원래 번호에서 정해지므로 다시 찍어도 같다
export const judgeFillExpr = () => `(() => {
  const hide = ${JSON.stringify(JUDGE_HIDE)};
  document.querySelectorAll(hide).forEach((n) => n.style.setProperty("display", "none", "important"));
  const st = document.createElement("style"); st.textContent = hide + "{display:none !important}"; document.head.appendChild(st);
  const seed = (s) => { let h = 7; for (const c of s) h = (h * 31 + c.charCodeAt(0)) % 9973; return h; };
  const digits = (h, n) => String((h * 7919) % (10 ** n)).padStart(n, "0").replace(/^0/, "4");
  const fix = (num) => { const parts = num.split("-"), h = seed(num);
    return parts.map((p, i) => (i === 0 || !/^0+$/.test(p) ? p : digits(h + i, p.length))).join("-"); };
  const PHONE = /0\\d{1,2}-\\d{3,4}-\\d{4}/g;
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  for (let n = walker.nextNode(); n; n = walker.nextNode()) if (/0000/.test(n.nodeValue)) n.nodeValue = n.nodeValue.replace(PHONE, (m) => (m.includes("0000") ? fix(m) : m));
  document.querySelectorAll('a[href^="tel:"]').forEach((a) => { a.href = a.getAttribute("href").replace(PHONE, (m) => (m.includes("0000") ? fix(m) : m)); });
  const left = (document.body.innerText.match(${LEFT_MARKS}) || []);
  return [...new Set(left)];
})()`;
