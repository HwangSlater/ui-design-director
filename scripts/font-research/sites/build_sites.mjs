// ranks.txt(출처|순위|도메인) → sites.csv. 같은 도메인은 처음 나온 출처를 쓰고 나머지 출처도 적는다
import { readFileSync, writeFileSync } from "node:fs";
const SRC = {
  SW: "Similarweb 한국 전체 2026-09 https://www.similarweb.com/top-websites/korea-republic-of/",
  SWfood: "Similarweb 한국 Food and Drink 2026-09 https://www.similarweb.com/top-websites/korea-republic-of/food-and-drink/",
  SWtravel: "Similarweb 한국 Travel and Tourism 2026-09 https://www.similarweb.com/top-websites/korea-republic-of/travel-and-tourism/",
  SWnews: "Similarweb 한국 News and Media 2026-09 https://www.similarweb.com/top-websites/korea-republic-of/news-and-media/",
  SMall: "Semrush 한국 전체 2026-09 https://www.semrush.com/website/top/south-korea/all/",
};
const SMSLUG = { SMmedia: "online-services", SMmass: "mass-media", SMnews: "newspapers", SMretail: "retail", SMbank: "banking", SMfin: "finance", SMinv: "investment", SMins: "insurance", SMtravel: "travel-and-tourism", SMgov: "government", SMedu: "education", SMfood: "food-and-beverages", SMapparel: "apparel-and-fashion", SMbeauty: "beauty-and-cosmetics", SMtel: "telecom", SMent: "entertainment", SMgame: "computer-and-video-games", SMlog: "transportation-and-logistics", SMhealth: "healthcare", SMair: "airlines", SMit: "information-technology", SMauto: "automotive", SMrest: "restaurants", SMsw: "computer-software-and-development" };
for (const [k, s] of Object.entries(SMSLUG)) SRC[k] = `Semrush 한국 ${s} 2026-09 https://www.semrush.com/trending-websites/kr/${s}`;
const DROP = new Set(["google.co.kr", "gemini.google.com", "weather.com", "buzzvil.com", "threads.com"]); // 200개 안으로: 중복·광고 기술·같은 엔진
const map = new Map();
for (const line of readFileSync("ranks.txt", "utf8").split(/\r?\n/)) {
  if (!line || line.startsWith("#")) continue;
  const [src, rank, dom] = line.split("|");
  if (DROP.has(dom)) continue;
  if (!map.has(dom)) map.set(dom, { dom, src: SRC[src], rank, also: [] });
  else map.get(dom).also.push(`${src}#${rank}`);
}
const q = (s) => `"${String(s).replace(/"/g, '""')}"`;
const rows = ["url,name,source,rank,also_in"];
for (const r of map.values()) rows.push([`https://${r.dom}/`, r.dom, r.src, r.rank, r.also.join(" ")].map(q).join(","));
writeFileSync("sites.csv", "﻿" + rows.join("\n") + "\n");
console.log(map.size);
