#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the static site from listings/*.json."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LISTINGS_DIR = ROOT / "listings"
SITE = ROOT / "site" if (ROOT / "site").is_dir() and not (ROOT / "jianan").is_dir() else ROOT

FONT_LINKS = """\
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Noto+Sans+TC:wght@300;400;500&family=Noto+Serif+TC:wght@400;500;600;700&display=swap" rel="stylesheet">"""

IG_SVG = """\
<svg class="ig-icon" viewBox="0 0 24 24" aria-hidden="true">
  <rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <circle cx="12" cy="12" r="4.2" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <circle cx="17.2" cy="6.8" r="1" fill="currentColor"/>
</svg>"""

PLAY_SVG = """\
<svg viewBox="0 0 24 24" aria-hidden="true"><polygon points="8,6 20,12 8,18"/></svg>"""

FOOTER = """\
  <footer class="site-footer">
    <a class="ig-entry" href="https://www.instagram.com/TMD_yogurt/" rel="noopener" target="_blank">
      {ig}
      <span class="ig-line">追蹤我，我是天母的優格</span>
      <span class="ig-handle">@TMD_yogurt</span>
    </a>
    <div class="legal">
      <p>※ 房屋登載資料依不動產說明書及最新謄本為準</p>
      <p>經紀業：圓璽房屋股份有限公司（中信房屋天母忠誠加盟店）</p>
      <p>經紀人：廖宜慈 (96)北縣字第001406號</p>
      <p>營業員：簡琛祐 (113)登字第460109號</p>
    </div>
    <p class="copyright">天母的優格 · 精選待售</p>
  </footer>""".format(ig=IG_SVG)

CONTACT = """\
    <section class="section contact" id="contact">
      <h2 class="section-title">看屋</h2>
      <p class="agent-name">簡琛祐</p>
      <div class="contact-actions">
        <a class="btn btn-solid" href="tel:0916601973">0916601973</a>
        <a class="btn btn-line" href="https://line.me/ti/p/G1rRvflCQE" rel="noopener" target="_blank">用 LINE 聯絡</a>
      </div>
    </section>"""


def header(home_href: str, asset: str) -> str:
    return f"""\
  <a class="skip" href="#main">跳到主要內容</a>
  <header class="site-header">
    <a class="wordmark" href="{home_href}">天母的優格</a>
    <span class="header-tag">精選待售</span>
  </header>"""


def head(title: str, desc: str, asset: str, canonical: str = "", og_image: str = "") -> str:
    og = ""
    if og_image:
        og = f"""
  <meta property="og:type" content="website">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="{og_image}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="{og_image}">"""
    can = f'\n  <link rel="canonical" href="{canonical}">' if canonical else ""
    return f"""\
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="theme-color" content="#f3eee4">{og}{can}
  <link rel="icon" href="{asset}/img/favicon.svg" type="image/svg+xml">
{FONT_LINKS}
  <link rel="stylesheet" href="{asset}/css/site.css">
<script data-goatcounter="https://tmdyogurt.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
</head>"""


def listing_html(item: dict, base_url: str) -> str:
    slug = item["slug"]
    asset = "../assets"
    img = f"{asset}/img/{slug}"
    title = f"{item['name']}｜天母的優格 精選待售"
    desc = f"{item['district']}，{item['lead']}，開價{item['price']}"
    og_image = f"{base_url}{slug}/" if False else f"{base_url}assets/img/{slug}/{item['hero']}" if base_url else ""
    canonical = f"{base_url}{slug}/" if base_url else ""

    specs = "\n".join(
        f'        <div><dt>{s["label"]}</dt><dd>{s["value"]}</dd></div>'
        for s in item["specs"]
    )
    features = "\n".join(f"        <li>{f}</li>" for f in item["features"])
    intro = "\n".join(f"      <p>{p}</p>" for p in item["intro"])

    photos = []
    gallery_items = list(item["photos"])
    # floorplan also in lightbox at the end
    for i, p in enumerate(gallery_items):
        classes = "span-2 wide" if p.get("span") == 2 else ""
        src = f"{img}/{p['file']}"
        cls = f' class="{classes}"' if classes else ""
        eager = "eager" if i < 2 else "lazy"
        photos.append(
            f'      <a{cls} href="{src}" data-gallery data-caption="{p["alt"]}">'
            f'<img src="{src}" alt="{p["alt"]}" width="1200" height="900" loading="{eager}"></a>'
        )
    # include floorplan in gallery lightbox via a dedicated section, also data-gallery
    fp = item.get("floorplan")
    fp_html = ""
    if fp:
        src = f"{img}/{fp['file']}"
        fp_html = f"""\
    <section class="section" id="floorplan">
      <h2 class="section-title">格局</h2>
      <div class="floorplan-frame">
        <a href="{src}" data-gallery data-caption="{fp['caption']}">
          <img src="{src}" alt="{fp['alt']}" width="1200" height="805" loading="lazy">
        </a>
      </div>
      <p class="caption">{fp['caption']}</p>
    </section>"""

    video = (item.get("video") or "").strip()
    video_attr = f' data-video="{video}"' if video else ""

    return f"""\
{head(title, desc, asset, canonical, og_image)}
<body>
{header("../", asset)}
  <main id="main">
    <figure class="hero reveal">
      <img src="{img}/{item['hero']}" alt="{item['heroAlt']}" width="1200" height="900" fetchpriority="high">
    </figure>

    <section class="title-block reveal">
      <p class="eyebrow">{item['eyebrow']}</p>
      <h1>{item['name']}</h1>
      <p class="lead">{item['lead']}</p>
      <p class="price"><span class="num">{item['priceNum']}</span><span class="unit">{item['priceUnit']}</span></p>
    </section>

    <section class="intro reveal">
      <hr class="rule">
{intro}
    </section>

    <section class="section" id="specs">
      <h2 class="section-title">物件概況</h2>
      <dl class="specs-grid">
{specs}
      </dl>
    </section>

    <section class="section" id="video" data-listing="../listings/{slug}.json"{video_attr}>
      <h2 class="section-title">影片</h2>
      <div class="video-frame is-empty" id="video-frame">
        <div class="video-placeholder">
          <div class="mark">{PLAY_SVG}</div>
          <p>影片即將上線</p>
        </div>
      </div>
    </section>

    <section class="section" id="photos">
      <h2 class="section-title">照片</h2>
      <div class="gallery-grid">
{chr(10).join(photos)}
      </div>
    </section>

    <section class="section" id="features">
      <h2 class="section-title">特色</h2>
      <ul class="feature-list">
{features}
      </ul>
    </section>

{fp_html}

{CONTACT}
  </main>
{FOOTER}
  <script src="{asset}/js/site.js"></script>
</body>
</html>
"""


def home_html(items: list[dict], base_url: str) -> str:
    title = "精選待售案件｜天母的優格"
    desc = "天母的優格精選待售案件，松山、士林與北士科一帶的住宅"
    og_image = ""
    if items and base_url:
        og_image = f"{base_url}assets/img/{items[0]['slug']}/{items[0]['hero']}"
    canonical = base_url if base_url else ""
    cards = []
    for it in items:
        img = f"assets/img/{it['slug']}/{it['hero']}"
        cards.append(f"""\
      <a class="listing-card" href="{it['slug']}/">
        <div class="card-photo">
          <img src="{img}" alt="{it['heroAlt']}" width="1200" height="900">
          <span class="card-overlay" aria-hidden="true">
            <span class="card-cta">看這間 <i>→</i></span>
          </span>
        </div>
        <div class="card-meta">
          <p class="loc">{it['eyebrow']}</p>
          <h2>{it['name']}</h2>
          <p class="sum">{it.get('card', {}).get('summary', it['lead'])}</p>
          <p class="card-price">{it['priceNum']}<small>{it['priceUnit']}</small></p>
        </div>
      </a>""")
    body_cards = "\n".join(cards) if cards else '<p class="empty-listings">目前沒有待售案件</p>'
    return f"""\
{head(title, desc, "assets", canonical, og_image)}
<body>
{header("./", "assets")}
  <main id="main">
    <section class="home-hero reveal">
      <p class="home-kicker">TMD YOGURT</p>
      <h1>天母的優格</h1>
      <p class="sub">精選待售案件</p>
    </section>
    <section class="listings">
{body_cards}
    </section>
  </main>
{FOOTER}
</body>
</html>
"""


def notfound_html() -> str:
    title = "找不到頁面｜天母的優格"
    return f"""\
{head(title, "找不到這個頁面", "assets")}
<body>
{header("./", "assets")}
  <main class="notfound" id="main">
    <h1>找不到這個頁面</h1>
    <p>這則案件可能已經售出，或網址打錯了</p>
    <a class="btn btn-solid" href="./">回到精選待售</a>
  </main>
{FOOTER}
</body>
</html>
"""


FAVICON = """\
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <rect width="64" height="64" fill="#1b1714"/>
  <text x="32" y="44" text-anchor="middle" font-family="Noto Serif TC, serif" font-size="36" fill="#f3eee4">優</text>
</svg>
"""


README = """\
# 天母的優格｜精選待售案件

靜態銷售網站，給批踢踢售屋文當照片連結用。

- 首頁：案件列表
- 每案一個穩定網址，例如 `/jianan/`

## 加入新案件

1. 在 `listings/` 新增一份 JSON，檔名用網址代稱，例如 `listings/tianmu-xx.json`，可先複製 `listings/jianan.json`
2. 把照片放到 `site/assets/img/<代稱>/`，主視覺檔名寫進 JSON 的 `hero`
3. 在專案根目錄執行：

```bash
python3 build.py
```

4. 把更新推上 GitHub（`main` 分支），GitHub Pages 會自動更新

JSON 必填欄位：`slug`（要跟資料夾和檔名一致）、`name`、`price`、`priceNum`、`priceUnit`、`hero`、`photos`、`specs`。`video` 可先留空。

## 填入影片連結

打開該案的 JSON，例如 `listings/jianan.json`，把 `video` 從空字串改成網址：

```json
"video": "https://www.youtube.com/watch?v=xxxxxxxxxxx"
```

或 IG Reels：

```json
"video": "https://www.instagram.com/reel/xxxxxxxxxxx/"
```

然後再跑一次 `python3 build.py` 並推上 GitHub。頁面也會在瀏覽時讀取 `site/listings/` 裡的 JSON，所以只改 JSON 並推上也可以讓影片出現。沒填的時候，影片區會顯示「影片即將上線」。

## 本地預覽

```bash
cd site
python3 -m http.server 8080
```

打開 http://127.0.0.1:8080/
"""


def load_listings() -> list[dict]:
    items = []
    for p in sorted(LISTINGS_DIR.glob("*.json")):
        items.append(json.loads(p.read_text(encoding="utf-8")))
    return items


def main() -> None:
    items = load_listings()
    base_url = ""  # filled later if known; relative og skips if empty
    # Try to read optional base
    cfg = ROOT / "site-config.json"
    if cfg.exists():
        base_url = json.loads(cfg.read_text()).get("base_url", "")
        if base_url and not base_url.endswith("/"):
            base_url += "/"

    (SITE / "assets" / "img").mkdir(parents=True, exist_ok=True)
    (SITE / "listings").mkdir(parents=True, exist_ok=True)

    # copy listing json into site for runtime video updates
    for p in LISTINGS_DIR.glob("*.json"):
        shutil.copy2(p, SITE / "listings" / p.name)

    (SITE / "index.html").write_text(home_html(items, base_url), encoding="utf-8")
    (SITE / "404.html").write_text(notfound_html(), encoding="utf-8")
    (SITE / "assets" / "img" / "favicon.svg").write_text(FAVICON, encoding="utf-8")
    (SITE / ".nojekyll").write_text("", encoding="utf-8")
    if not (ROOT / "README.md").exists():
        (ROOT / "README.md").write_text(README, encoding="utf-8")
    if SITE != ROOT and not (SITE / "README.md").exists():
        (SITE / "README.md").write_text(README, encoding="utf-8")

    for it in items:
        d = SITE / it["slug"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(listing_html(it, base_url), encoding="utf-8")
        print(f"wrote {it['slug']}/index.html")

    print(f"wrote {len(items)} listing(s)")


if __name__ == "__main__":
    main()
