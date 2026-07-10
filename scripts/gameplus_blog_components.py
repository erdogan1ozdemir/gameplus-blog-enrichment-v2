"""
Gameplus Blog Enrichment — Component Library
=============================================
Pure, reusable HTML component renderers for enriching gameplus.com.tr blog posts.
Final design (v9): dark theme (#000 bg), Turkish genre tags, trophy icon,
V8 rotating-conic-glow (TLDR/CTA outer), V9 layered frame (Hatırlatma/Editör/tables/card-table/compact CTA),
Controller-Tag compact CTA, Hover-Slide card-table rows, pulsing FAQ "+".

Import this module from a per-blog build script:
    from gameplus_blog_components import *
Then call render_*() to get HTML strings, assemble, and write out.

All components use inline CSS so they survive CMS paste. The one <style> block
(ANIMATED_BORDER_STYLE) must be prepended ONCE to the final body.
"""
import re
import json

# ============ v10 "Game+ UI" TEMA (Figma: Blog Detail / GFN Thursday) ============
# GFN yeşili KALDIRILDI, tek vurgu SARI. Kart #161616, ayraç #29292b, ikincil metin #B2B2B2.
# Başlıklar New Science SemiBold Extended, gövde Greycliff CF.
# GERİ DÖNÜŞ: GP_SURFACE_MODE / GP_BADGE_TEXT_MODE flag'lerini çevir (v9 için *.v9bak yedeği de var).
GP_ACCENT    = "#FFC900"   # v9: #FFC900 (GFN yeşili)
GP_ON_ACCENT = "#161616"   # sarı buton/pill üzeri koyu metin
GP_TEXT2     = "#B2B2B2"   # ikincil metin
GP_LINE      = "#29292b"   # ayraç
GP_SURFACE   = "#161616"   # kart zemini
GP_SURFACE_MODE    = "card"   # "card" -> #161616 | "transparent" -> v9 (geri dönüş)
GP_BADGE_TEXT_MODE = "full"   # "full" -> tasarım tam renk | "lighten" -> WCAG açık ton (geri dönüş)
def _surface():
    return GP_SURFACE if GP_SURFACE_MODE == "card" else "transparent"
# Tür rozeti renk paleti — Figma tasarımından birebir + eksikler atandı (tüm içerikte AYNI renk).
GENRE_BADGE_COLORS = {
    "AKSIYON":"#FF5C5C","MACERA":"#FF9F43","KORKU":"#F472B6","RPG":"#818CF8","CANLANDIRMA":"#818CF8",
    "FPS":"#FB7185","MMO":"#E879F9","MMORPG":"#2DD4BF","SPOR":"#FACC15","SIMULASYON":"#38BDF8",
    "STRATEJI":"#5B8DEF","GERCEK ZAMANLI STRATEJI":"#60A5FA","BAGIMSIZ":"#A3E635","INDIE":"#A3E635",
    "ROGUELIKE":"#A78BFA","BULMACA":"#C084FC","AILE":"#34D399","AILE DOSTU":"#34D399","HAYATTA KALMA":"#4ADE80",
    "YARIS":"#FB923C","DOVUS":"#E11D48","DOVUS OYUNU":"#E11D48","PLATFORM":"#F59E0B","ARCADE":"#FBBF24",
    "MOBA":"#14B8A6","BASIT EGLENCE":"#86EFAC","OYNAMASI UCRETSIZ":"#FCD34D","DEMO":"#94A3B8",
    "CO-OP":"#22D3EE","PARTI":"#FBBF24","SOULSLIKE":"#A3A3A3","METROIDVANIA":"#D8B4FE","JRPG":"#8B5CF6","GIZLILIK":"#22C55E",
}
def badge_color_for(genre, fallback=None):
    if not genre: return fallback or GP_ACCENT
    k=_fold(genre)
    if k in GENRE_BADGE_COLORS: return GENRE_BADGE_COLORS[k]
    for part in re.split(r"[-/–]", genre):
        pk=_fold(part)
        if pk in GENRE_BADGE_COLORS: return GENRE_BADGE_COLORS[pk]
    return fallback or GP_ACCENT
def _badge_text(color):
    return color if GP_BADGE_TEXT_MODE == "full" else lighten(color, 0.45)

# === HTML Wrapper ===
PAGE_HEAD = '''<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__TITLE__</title>
<style>
  /* Onizleme tipografisi Figma "Blog Detail (GFN Thursday)" ile: baslikar New Science SemiBold Extended, govde Greycliff CF, 1200px kolon. Yalnizca onizleme; CMS govdesi etkilenmez. */
  @font-face { font-family:'New Science'; font-style:normal; font-weight:600; font-display:swap; src:url('https://gameplus.com.tr/_next/static/media/NewScience-SemiBoldExt.otf') format('opentype'); }
  @font-face { font-family:'GreycliffCF'; font-style:normal; font-weight:400; font-display:swap; src:url('https://gameplus.com.tr/_next/static/media/GreycliffCF-Regular.55993c60.otf') format('opentype'); }
  @font-face { font-family:'GreycliffCF'; font-style:normal; font-weight:500; font-display:swap; src:url('https://gameplus.com.tr/_next/static/media/GreycliffCF-Medium.b24079d5.woff2') format('woff2'); }
  @font-face { font-family:'GreycliffCF'; font-style:normal; font-weight:700; font-display:swap; src:url('https://gameplus.com.tr/_next/static/media/GreycliffCF-Bold.d881132f.woff2') format('woff2'); }
  * { box-sizing: border-box; }
  body { font-family: GreycliffCF, -apple-system, "system-ui", "Segoe UI", Roboto, sans-serif; max-width: 1200px; margin: 0 auto; padding: 28px 20px 80px; color: #B2B2B2; font-size: 20px; line-height: 24px; background: #000; }
  h1,h2,h3,h4 { font-family: 'New Science', GreycliffCF, -apple-system, sans-serif; }
  h1 { font-size: 40px; font-weight: 600; line-height: 48px; margin: 0 0 16px; color: #fff; }
  h2 { font-size: 28px; font-weight: 600; line-height: 36px; margin: 40px 0 14px; color: #fff; }
  h3 { font-size: 24px; font-weight: 600; line-height: 32px; margin: 28px 0 12px; color: #fff; }
  h4 { font-size: 20px; font-weight: 600; line-height: 28px; margin: 20px 0 10px; color: #fff; }
  p { margin: 0 0 20px; color: #B2B2B2; }
  ul, ol { margin: 0 0 20px; padding-left: 24px; color: #B2B2B2; }
  li { margin: 4px 0; }
  ul li p, ol li p { margin: 0; }
  a { color: #FFC900; text-decoration: none; }
  a:hover { color: #ffd94d; }
  em { font-style: italic; }
  strong { font-weight: 700; }
  @media (max-width: 700px) {
    body { font-size: 16px; line-height: 24px; padding: 18px 16px 60px; }
    h1 { font-size: 30px; line-height: 1.15; } h2 { font-size: 22px; line-height: 1.2; } h3 { font-size: 19px; line-height: 1.25; } h4 { font-size: 17px; line-height: 1.3; }
  }
</style>
</head>
<body>
'''
PAGE_FOOT = '\n</body>\n</html>'


def embed_fonts(html):
    """Make a preview self-contained: replace the GreycliffCF gameplus URLs with
    base64 data URIs (gameplus serves fonts WITHOUT CORS, so cross-origin @font-face
    fails on localhost/Vercel). Reads the bundled fonts in scripts/_fonts/."""
    import base64, os
    base = os.path.join(os.path.dirname(__file__), "_fonts")
    mapping = {
        "https://gameplus.com.tr/_next/static/media/NewScience-SemiBoldExt.otf": ("new-science-semibold-ext.otf", "font/otf"),
        "https://gameplus.com.tr/_next/static/media/GreycliffCF-Regular.55993c60.otf": ("reg.otf", "font/otf"),
        "https://gameplus.com.tr/_next/static/media/GreycliffCF-Medium.b24079d5.woff2": ("med.woff2", "font/woff2"),
        "https://gameplus.com.tr/_next/static/media/GreycliffCF-Bold.d881132f.woff2": ("bold.woff2", "font/woff2"),
    }
    for url, (fn, mime) in mapping.items():
        fp = os.path.join(base, fn)
        if os.path.exists(fp):
            with open(fp, "rb") as f:
                html = html.replace(url, "data:%s;base64,%s" % (mime, base64.b64encode(f.read()).decode()))
    return html

# === SVG ICONS (premium replacements for emoji) ===
# Trophy icon for "Best Of" lists (replaces star)
SVG_TROPHY = '<svg width="24" height="24" viewBox="0 0 24 24" style="vertical-align:-6px;margin-right:10px;flex-shrink:0;"><defs><linearGradient id="gp-grad" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#FFC900"/><stop offset="100%" stop-color="#f59e0b"/></linearGradient></defs><path fill="url(#gp-grad)" d="M19 5h-2V3H7v2H5c-1.1 0-2 .9-2 2v1c0 2.55 1.92 4.63 4.39 4.94.63 1.5 1.98 2.63 3.61 2.96V19H7v2h10v-2h-4v-3.1c1.63-.33 2.98-1.46 3.61-2.96C19.08 12.63 21 10.55 21 8V7c0-1.1-.9-2-2-2zM5 8V7h2v3.82C5.84 10.4 5 9.3 5 8zm14 0c0 1.3-.84 2.4-2 2.82V7h2v1z"/></svg>'
# Green checkmark for TLDR/info-card items
SVG_CHECK_GREEN = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#FFC900" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0;"><polyline points="20 6 9 17 4 12"/></svg>'
# External link icon (small arrow up-right)
SVG_EXT_LINK = '<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:1px;margin-left:3px;opacity:0.65;"><path d="M7 17L17 7"/><polyline points="7 7 17 7 17 17"/></svg>'
# Old gradient star (kept for backward compat)
SVG_STAR_GRADIENT = SVG_TROPHY
SVG_DOC = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-4px;margin-right:8px;flex-shrink:0;"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="9" y1="13" x2="15" y2="13"/><line x1="9" y1="17" x2="15" y2="17"/></svg>'
SVG_BULB = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-4px;margin-right:8px;flex-shrink:0;"><path d="M9 18h6"/><path d="M10 22h4"/><path d="M15.09 14a5 5 0 1 0-6.18 0c.66.49 1.09 1.27 1.09 2.1V17h4v-.9c0-.83.43-1.61 1.09-2.1z"/></svg>'
SVG_CAL = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-2px;margin-right:6px;flex-shrink:0;"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>'
SVG_BOOKMARK = '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-3px;margin-right:8px;flex-shrink:0;"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>'
SVG_BOLT = '<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" style="vertical-align:-2px;margin-right:6px;flex-shrink:0;"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>'
SVG_NEWS = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-2px;margin-right:6px;flex-shrink:0;"><path d="M4 22h16a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v16a2 2 0 0 1-2 2zm0 0a2 2 0 0 1-2-2v-9c0-1.1.9-2 2-2h2"/><line x1="18" y1="14" x2="10" y2="14"/><line x1="15" y1="18" x2="10" y2="18"/><rect x="10" y="6" width="8" height="4"/></svg>'
SVG_ARROW = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-2px;margin-left:6px;flex-shrink:0;"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>'

# === DARK THEME BLOCK STYLES (CMS-portable inline) ===
# Common animated border style + mobile responsiveness + FAQ + table fixes
ANIMATED_BORDER_STYLE = '''<style>
:root{--gp-surface:#161616;--gp-line:#29292b;--gp-accent:#FFC900;}
@property --gp-conic-angle {
  syntax: '<angle>';
  initial-value: 0deg;
  inherits: false;
}
@keyframes gameplus-border-shimmer {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
@keyframes gp-rotate-conic {
  to { --gp-conic-angle: 360deg; }
}
@keyframes gp-pulse-plus {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.18); opacity: 0.85; }
}
.gp-animated-border { position: relative; border-radius: 12px; padding: 1px; background: linear-gradient(110deg, #FFC900 0%, #f59e0b 30%, #FFC900 60%, #f59e0b 100%); background-size: 300% 100%; animation: gameplus-border-shimmer 6s ease-in-out infinite; }
.gp-animated-border > .gp-inner { background: transparent; border-radius: 11px; padding: 22px 24px; }
/* V8: Rotating Conic Glow border */
.gp-conic { position: relative; border-radius: 12px; padding: 1.5px; }
.gp-conic::before {
  content:''; position:absolute; inset:0; border-radius:12px; padding:1.5px;
  background: conic-gradient(from var(--gp-conic-angle,0deg), transparent 0deg, var(--gp-glow,#FFC900) 60deg, transparent 120deg, transparent 360deg);
  -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
  -webkit-mask-composite: xor;
          mask-composite: exclude;
  animation: gp-rotate-conic 6s linear infinite;
  pointer-events: none;
}
.gp-conic > .gp-conic-inner { background:var(--gp-surface,#161616); border-radius:10.5px; position:relative; }
/* V9: Layered Frame */
.gp-layer { position:relative; border-radius:12px; border:1px solid var(--gp-frame,rgba(255,201,0,0.22)); background:var(--gp-surface,#161616); }
.gp-cell { position:relative; background:var(--gp-surface,#161616); border:1px solid var(--gp-line,#29292b); border-radius:10px; padding:14px 16px; }
.gp-layer::before { content:''; position:absolute; inset:5px; border:1px solid #29292b; border-radius:8px; pointer-events:none; }
/* FAQ + sign pulsing animation */
.faq-item .faq-icon { animation: gp-pulse-plus 2.2s ease-in-out infinite; }
.gp-card-table-inner .card-row:last-child { border-bottom: none !important; }
.gp-card-table-inner .card-row { position: relative; }
.gp-card-table-inner a.card-row { text-decoration: none !important; color: inherit !important; }
/* Hover Slide Accent: colored bar slides in from left on hover (Steam list vibe) */
.gp-card-table-inner .card-row::before { content:''; position:absolute; left:0; top:0; bottom:0; width:0; background:var(--row-c,#FFC900); transition:width 0.2s ease; }
.gp-card-table-inner .card-row:hover::before { width:4px; }
.gp-card-table-inner .card-row:hover { background: rgba(255,255,255,0.025) !important; }
.gp-card-table-inner a.card-row:hover .gp-name { color: #fff !important; }
/* Comparison table fixes */
.table-wrap tbody tr:last-child td { border-bottom: none !important; }
.table-wrap table { border-radius: 12px; }
/* FAQ + indicator */
.faq-item .faq-icon { transition: transform 0.25s ease, color 0.2s; }
.faq-item[open] .faq-icon { transform: rotate(45deg); color: #FFC900 !important; }
.faq-item summary:hover .faq-icon { color: #f59e0b; }
/* YouTube embed wrapper smaller + centered */
.gp-yt-wrap { max-width: 560px; margin: 1.5em 0 !important; }
/* Mobile: card-table responsive */
@media (max-width: 700px) {
  .gp-card-table-inner .card-row {
    grid-template-columns: auto 1fr !important;
    grid-template-rows: auto auto;
    gap: 6px 12px !important;
    padding: 14px 16px !important;
  }
  .gp-card-table-inner .card-row > .gp-badge {
    grid-row: 1; grid-column: 1;
    font-size: 0.54em !important;
    min-width: auto !important;
    padding: 4px 9px !important;
    letter-spacing: 0.08em !important;
  }
  .gp-card-table-inner .card-row > .gp-name {
    grid-row: 1; grid-column: 2;
    font-size: 0.95em !important;
    align-self: center;
  }
  .gp-card-table-inner .card-row > .gp-meta {
    grid-row: 2; grid-column: 1 / -1;
    text-align: left !important;
    font-size: 0.78em !important;
    padding-left: 0 !important;
  }
  .gp-game-inline > aside { float: none !important; width: 100% !important; margin: 0 0 16px 0 !important; }
  .gp-yt-wrap { margin: 1em 0 !important; }
}

/* ===== v10 genel revizeler: embed 16:9, tablo alt kapatma, kupa ortala, FAQ sol, mobil responsive ===== */
/* ===== YouTube embed: 16:9 (kare değil), sola dayalı, küçük ===== */
.gp-yt-wrap { max-width: 560px; margin: 1.5em 0 !important; }
.gp-yt-wrap iframe { display: block; width: 100% !important; aspect-ratio: 16 / 9 !important; height: auto !important; border: 0; border-radius: 12px; box-shadow: 0 4px 14px rgba(0,0,0,0.5); }

/* ===== Tabloların altını kapat: tek temiz çerçeve, son satır ayracı ===== */
.table-wrap.gp-layer::before,
.card-table.gp-layer::before { display: none !important; }
.table-wrap { border: 1px solid #29292B !important; }
.gp-card-table-inner { border: 1px solid #29292B !important; }
.table-wrap tbody tr:last-child td { border-bottom: none !important; }
.table-wrap tbody tr { transition: background 0.15s ease; }
.table-wrap tbody tr:hover > td { background: rgba(255,201,0,0.07) !important; }
.table-wrap tbody tr:hover > td:first-child { color: #FFC900 !important; }

/* ===== Card-table başlığı (kupa + başlık) tam ortalı ===== */
.card-table-wrap > div:first-child { text-align: center; }
.card-table-wrap h3 { display: flex !important; align-items: center !important; justify-content: center !important; gap: 9px !important; }
.card-table-wrap h3 > svg { margin-right: 0 !important; vertical-align: middle !important; }
.card-table-wrap h3 > span { min-width: 0; }

/* ===== FAQ soruları biraz daha sola dayalı ===== */
.faq-item summary { padding: 14px 16px !important; gap: 10px !important; }

/* ===== MOBİL (<=700px) ===== */
@media (max-width: 700px) {
  /* --- Karşılaştırma tablosu: yatay kaydırma yok, tüm sütunlar görünür, okunur punto --- */
  .table-wrap > div { overflow-x: visible !important; }
  .table-wrap table { font-size: 0.76em !important; table-layout: fixed; width: 100% !important; }
  .table-wrap th, .table-wrap td {
    padding: 8px 7px !important; white-space: normal !important;
    word-break: break-word; overflow-wrap: anywhere; vertical-align: top; line-height: 1.4 !important;
  }
  .table-wrap th { letter-spacing: 0.04em !important; }
  .table-wrap th:nth-child(1), .table-wrap td:nth-child(1) { width: 34%; }
  .table-wrap th:nth-child(2), .table-wrap td:nth-child(2) { width: 26%; }
  .table-wrap th:nth-child(3), .table-wrap td:nth-child(3) { width: 20%; }
  .table-wrap th:nth-child(4), .table-wrap td:nth-child(4) { width: 20%; }

  /* --- Card-table: TEK SATIR + rozet sütunu SABİT (oyun isimleri hizalı) --- */
  .gp-card-table-inner .card-row {
    grid-template-columns: 108px 1fr auto !important;
    grid-template-rows: auto !important;
    gap: 4px 9px !important; padding: 11px 12px !important; align-items: center !important;
  }
  .gp-card-table-inner .card-row > .gp-badge {
    grid-row: 1 !important; grid-column: 1 !important;
    width: 100% !important; min-width: 0 !important; box-sizing: border-box;
    font-size: 0.55em !important; padding: 3px 5px !important; letter-spacing: 0.02em !important; text-align: center;
  }
  .gp-card-table-inner .card-row > .gp-name {
    grid-row: 1 !important; grid-column: 2 !important; font-size: 0.8em !important; line-height: 1.28 !important;
  }
  .gp-card-table-inner .card-row > .gp-meta {
    grid-row: 1 !important; grid-column: 3 !important; text-align: right !important;
    font-size: 0.62em !important; padding-left: 0 !important; white-space: normal !important;
    max-width: 112px; line-height: 1.35 !important;
  }

  /* --- FAQ: soru ve cevap sola dayalı, okunur --- */
  .faq-item summary { padding: 13px 13px !important; gap: 9px !important; font-size: 0.95em !important; }
  .faq-item > div { padding: 12px 14px 15px 14px !important; }

  /* --- Hızlı Özet (TLDR): kompakt ve okunur --- */
  .tldr-block { padding: 16px !important; }
  .tldr-block li { gap: 9px !important; }

  /* --- CTA blokları: kompakt, butonlar tam genişlik --- */
  .cta-end .gp-conic-inner, .cta-paketler .gp-conic-inner, .cta-oyunlar .gp-conic-inner, .cta-compact .gp-conic-inner { padding: 18px 16px !important; }
  .cta-end a, .cta-paketler a, .cta-oyunlar a { flex: 1 1 100% !important; justify-content: center !important; box-sizing: border-box; }
  .cta-end .gp-conic-inner > div:last-child { gap: 9px !important; }

  /* --- info-card: 2 sütun --- */
  .info-card { grid-template-columns: repeat(2, 1fr) !important; gap: 10px !important; }
}
</style>
'''

# --- TLDR "Hızlı Özet" (Figma: #161616 kart + 1px gradient kenarlık #FFC516->#545454, sarı bullet) ---
def render_tldr(items):
    items_html = "\n".join(
        f'    <li style="display:flex;gap:10px;margin:0 0 14px;list-style:none;align-items:flex-start;">'
        f'<span style="color:#FFC900;font-weight:700;font-size:16px;line-height:24px;flex-shrink:0;">&bull;</span>'
        f'<span style="color:#B2B2B2;font-size:16px;line-height:24px;">{x}</span></li>'
        for x in items
    )
    return f'''<div class="tldr-block gp-conic" style="--gp-glow:#FFC900;margin:24px 0;">
<div class="gp-conic-inner" style="background:#161616;border-radius:10.5px;padding:24px;">
  <h2 style="font-family:'New Science',GreycliffCF,-apple-system,sans-serif;font-size:24px;line-height:32px;font-weight:600;color:#fff;margin:0 0 14px;display:flex;align-items:center;"><span style="color:#FFC900;display:inline-flex;">{SVG_DOC}</span>Hızlı Özet</h2>
  <ul style="margin:0;padding:0;list-style:none;">
{items_html}
  </ul>
</div>
</div>
'''

# --- Genel içerik madde listesi (bullet) ---
def render_list(items, marker="dot", accent="#FFC900"):
    """Gövde içi madde (bullet) listesi. Uzun paragraf yerine SIRALANABİLİR bilgileri taranabilir
    kılmak için kullan: ön sipariş/paket faydaları, sürüm-ürün farkları, "nelere dikkat" uyarıları,
    adımlar, kısa "neler biliniyor" özetleri. items: HTML string listesi (madde içinde <strong> olabilir).
    marker: 'dot' (renkli nokta) | 'check' (yeşil ✓). accent: nokta rengi (uyarılarda ör. '#f59e0b').
    Inline-CSS + class='gp-list'; koyu temayla uyumlu, CMS'te tutarlı. Düz <ul><li> yerine bunu kullan."""
    lis = []
    for x in items:
        if marker == "check":
            m = f'<span style="flex-shrink:0;margin-top:2px;">{SVG_CHECK_GREEN}</span>'
        else:
            m = (f'<span style="flex-shrink:0;margin-top:10px;width:6px;height:6px;border-radius:50%;'
                 f'background:{accent};"></span>')
        lis.append(f'<li style="display:flex;gap:11px;margin:8px 0;align-items:flex-start;'
                   f'line-height:1.6;list-style:none;">{m}<span>{x}</span></li>')
    return ('<ul class="gp-list" style="margin:14px 0 18px;padding:0;list-style:none;color:#B2B2B2;">\n'
            + "\n".join(lis) + "\n</ul>")


# --- Info Strip / Stat kartları (Figma: #0D0D0D kart + #29292B kenarlık; DEĞER üstte New Science 28 sarı, etiket altta gri 16) ---
def render_info_card(badges, style="grid"):
    """badges: [(label, value), ...] — değer üstte büyük sarı, etiket altta."""
    if style == "checkmark":
        items = []
        for value in badges:
            items.append(f'<div style="display:flex;align-items:center;gap:11px;margin:8px 0;">{SVG_CHECK_GREEN}<span style="color:#e5e7eb;font-size:16px;font-weight:500;">{value}</span></div>')
        return f'''<div class="info-card" style="background:#0D0D0D;border:1px solid #29292B;border-radius:12px;padding:16px 22px;margin:24px 0;">
{chr(10).join(items)}
</div>
'''
    items = []
    for label, value in badges:
        items.append(f'''  <div class="gp-cell" style="background:#0D0D0D;border:1px solid #29292B;border-radius:12px;padding:20px;text-align:center;">
    <div style="font-family:'New Science',GreycliffCF,-apple-system,sans-serif;font-weight:600;font-size:24px;line-height:32px;color:#FFC900;margin-bottom:6px;">{value}</div>
    <div style="color:#B2B2B2;font-size:16px;line-height:24px;font-weight:500;">{label}</div>
  </div>''')
    return f'''<div class="info-card" style="margin:24px 0;display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;">
{chr(10).join(items)}
</div>
'''

# --- Article Meta — DEPRECATED: üst meta header artık EKLENMEZ ---
def render_meta(date, category="GAME+ Blog"):
    """DEPRECATED — ÜST META HEADER ARTIK KULLANILMIYOR. Site/CMS yazının eklenme tarihini ve
    marka adını (GAME+) zaten gösteriyor; gövdeye ikinci bir tarih/marka chip'i koymak tekrar olur.
    Fonksiyon yalnız eski script'ler kırılmasın diye duruyor; YENİ build'lerde ÇAĞIRMA."""
    return f'''<div class="article-meta" style="display:flex;gap:14px;flex-wrap:wrap;align-items:center;font-size:0.85em;color:#B2B2B2;margin:0 0 20px;padding:12px 0;border-bottom:1px solid #29292b;">
  <span style="display:inline-flex;align-items:center;background:transparent;padding:6px 14px;border-radius:999px;color:#FFC900;font-weight:700;border:1px solid #29292b;letter-spacing:0.02em;">{SVG_BOLT}{category}</span>
  <span style="display:inline-flex;align-items:center;font-weight:500;color:#B2B2B2;">{SVG_CAL}{date}</span>
</div>
'''

# --- Editör Notu (Figma: rgba(255,201,0,0.06) zemin + 4px sarı sol bar + sarı eyebrow; gövde beyaz 20/32) ---
def render_editor_note(text, title="GAME+ EDİTÖR NOTU"):
    return f'''<div class="editor-note" style="background:rgba(255,201,0,0.06);border-radius:12px;padding:18px 24px 18px 20px;margin:24px 0;display:flex;gap:16px;align-items:stretch;">
  <div style="width:4px;border-radius:2px;background:#FFC900;flex-shrink:0;"></div>
  <div>
    <div style="color:#FFC900;font-size:12px;line-height:16px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:6px;display:flex;align-items:center;">{SVG_DOC}{title}</div>
    <p style="margin:0;color:#fff;font-size:1em;line-height:1.5;">{text}</p>
  </div>
</div>
'''

# --- Hatırlatma (Figma: rgba(255,255,255,0.04) zemin + 4px sarı sol bar + sarı eyebrow; gövde beyaz 20/32) ---
def render_highlight(text, title="Hatırlatma"):
    return f'''<div class="highlight-box" style="background:rgba(255,255,255,0.04);border-radius:12px;padding:18px 24px 18px 20px;margin:24px 0;display:flex;gap:16px;align-items:stretch;">
  <div style="width:4px;border-radius:2px;background:#FFC900;flex-shrink:0;"></div>
  <div>
    <div style="color:#FFC900;font-size:12px;line-height:16px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:6px;display:flex;align-items:center;">{SVG_BULB}{title}</div>
    <p style="margin:0;color:#fff;font-size:1em;line-height:1.5;">{text}</p>
  </div>
</div>
'''

# --- CTA Paketler (Figma CTA kart dili: #161616, ★ eyebrow, dolu sarı buton; GA4 id=packages-button) ---
def render_cta_paketler(headline, desc):
    return f'''<div class="cta-paketler gp-conic" style="--gp-glow:#FFC900;margin:32px 0;">
<div class="gp-conic-inner" style="background:#161616;border-radius:10.5px;padding:24px;">
  <div style="display:flex;align-items:center;gap:8px;margin-bottom:16px;"><span style="color:#FFC900;font-size:12px;line-height:16px;font-weight:700;letter-spacing:0.08em;">&#9733; GAME+ &bull; BULUT OYUN</span></div>
  <div style="font-family:'New Science',GreycliffCF,-apple-system,sans-serif;font-weight:600;font-size:24px;line-height:32px;color:#fff;margin-bottom:8px;">{headline}</div>
  <p style="color:#B2B2B2;font-size:16px;line-height:24px;margin:0 0 20px;max-width:760px;">{desc}</p>
  <a id="packages-button" href="https://gameplus.com.tr/gfn/paketler" style="display:inline-flex;align-items:center;justify-content:center;background:#FFC900;color:#131313;padding:12px 16px;border-radius:8px;font-weight:700;font-size:16px;line-height:20px;text-decoration:none;">GeForce NOW Paketleri &rarr;</a>
</div>
</div>
'''

# --- CTA Oyunlar (kontur sarı buton; GA4 id=games-button) ---
def render_cta_oyunlar(headline, desc):
    return f'''<div class="cta-oyunlar gp-conic" style="--gp-glow:#FFC900;margin:32px 0;">
<div class="gp-conic-inner" style="background:#161616;border-radius:10.5px;padding:24px;">
  <div style="display:flex;align-items:center;gap:8px;margin-bottom:16px;"><span style="color:#FFC900;font-size:12px;line-height:16px;font-weight:700;letter-spacing:0.08em;">&#9733; GAME+ &bull; OYUN KÜTÜPHANESİ</span></div>
  <div style="font-family:'New Science',GreycliffCF,-apple-system,sans-serif;font-weight:600;font-size:24px;line-height:32px;color:#fff;margin-bottom:8px;">{headline}</div>
  <p style="color:#B2B2B2;font-size:16px;line-height:24px;margin:0 0 20px;max-width:760px;">{desc}</p>
  <a id="games-button" href="https://gameplus.com.tr/gfn/oyunlar" style="display:inline-flex;align-items:center;justify-content:center;background:transparent;border:1px solid #FFC900;color:#FFC900;padding:12px 16px;border-radius:8px;font-weight:700;font-size:16px;line-height:20px;text-decoration:none;">GeForce NOW Oyunları &rarr;</a>
</div>
</div>
'''

# --- End CTA (Figma "CTA - Bulutta Oyun Keyfi": #161616 kart, ★ eyebrow, New Science 32 başlık,
#     dolu sarı + kontur sarı buton; GA4 id=end-packages-button / end-games-button) ---
def render_end_cta(headline, desc, btn2_label="Güncel Fırsatlar", btn2_url="https://gameplus.com.tr/firsatlar", chip2=None, eyebrow="GAME+ &bull; BULUT OYUN"):
    return f'''<div class="cta-end gp-conic" style="--gp-glow:#FFC900;margin:40px 0 24px;">
<div class="gp-conic-inner" style="background:#161616;border-radius:10.5px;padding:24px;">
  <div style="display:flex;align-items:center;gap:8px;margin-bottom:24px;"><span style="color:#FFC900;font-size:12px;line-height:16px;font-weight:700;letter-spacing:0.08em;">&#9733; {eyebrow}</span></div>
  <div style="font-family:'New Science',GreycliffCF,-apple-system,sans-serif;font-weight:600;font-size:32px;line-height:40px;color:#fff;margin-bottom:8px;">{headline}</div>
  <p style="color:#B2B2B2;font-size:16px;line-height:20px;margin:0 0 24px;max-width:760px;">{desc}</p>
  <div style="display:flex;flex-wrap:wrap;gap:14px;">
    <a id="end-packages-button" href="https://gameplus.com.tr/gfn/paketler" style="display:inline-flex;align-items:center;justify-content:center;background:#FFC900;color:#131313;padding:12px 16px;border-radius:8px;font-weight:700;font-size:16px;line-height:20px;text-decoration:none;">GeForce NOW Paketleri &rarr;</a>
    <a id="end-games-button" href="{btn2_url}" style="display:inline-flex;align-items:center;justify-content:center;background:transparent;border:1px solid #FFC900;color:#FFC900;padding:12px 16px;border-radius:8px;font-weight:700;font-size:16px;line-height:20px;text-decoration:none;">{btn2_label}</a>
  </div>
</div>
</div>
'''

# --- Ubisoft+ CTA (premium Ubisoft blue, SVG arrow) ---
def render_ubisoft_cta(headline, desc):
    return f'''<div class="cta-ubisoft" style="background:{_surface()};border:1px solid #29292b;border-left:3px solid #0061ff;border-radius:10px;padding:22px 24px;margin:30px 0;box-shadow:0 2px 12px rgba(0,0,0,0.4);">
  <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
    <span style="display:inline-block;background:#0061ff;color:#fff;padding:4px 11px;border-radius:999px;font-size:0.6em;font-weight:800;letter-spacing:0.12em;text-transform:uppercase;box-shadow:inset 0 1px 0 rgba(255,255,255,0.18);">Ubisoft+</span>
  </div>
  <div style="font-weight:800;font-size:1.2em;margin-bottom:8px;line-height:1.3;color:#fff;letter-spacing:-0.01em;">{headline}</div>
  <p style="color:#B2B2B2;margin:0 0 16px 0;line-height:1.55;font-size:0.93em;">{desc}</p>
  <a id="ubisoft-packages-button" href="https://gameplus.com.tr/ubisoft/paketler" style="display:inline-flex;align-items:center;background:#0061ff;color:#fff;padding:11px 22px;border-radius:6px;font-weight:700;text-decoration:none;letter-spacing:-0.005em;font-size:0.94em;box-shadow:0 2px 8px rgba(0,97,255,0.4);">Ubisoft+ Paketlerini İncele{SVG_ARROW}</a>
</div>
'''

# --- Tablo (Figma: #161616 kap + #1E1E18 başlık + sarı 16 bold başlık metni + #29292B ayraç;
#     oyun adı DemiBold beyaz; hover'da satır sarı %7 + ad sarı (normalde vurgu YOK); featured=[i] kalıcı vurgu) ---
def render_table(headers, rows, featured=None, first_col_strong=True):
    th = "".join(
        f'<th style="background:#1E1E18;padding:19px 24px;text-align:center;color:#FFC900;font-weight:700;font-size:16px;line-height:20px;border-bottom:1px solid rgba(255,201,0,0.3);">{h}</th>'
        for h in headers)
    feat = set(featured or [])
    body_rows = []
    for i, row in enumerate(rows):
        is_feat = i in feat
        row_bg = 'background:rgba(255,201,0,0.07);' if is_feat else ''
        tds = []
        for j, c in enumerate(row):
            if j == 0 and is_feat:
                base = 'color:#FFC900;font-weight:400;'   # kalıcı vurgu satırı
            else:
                base = 'color:#B2B2B2;font-weight:400;'   # oyun adı dahil normal renk/kalınlık (kullanıcı kuralı)
            top = '' if i == 0 else 'border-top:1px solid #29292B;'
            tds.append(f'<td style="padding:14px 24px;vertical-align:middle;{top}{row_bg}{base}font-size:16px;line-height:20px;">{c}</td>')
        body_rows.append(f'<tr>{"".join(tds)}</tr>')
    return f'''<div class="table-wrap gp-table" style="background:#161616;border:1px solid #29292B;border-radius:16px;margin:24px 0;overflow:hidden;">
  <div style="overflow-x:auto;">
    <table style="width:100%;border-collapse:collapse;background:transparent;">
      <thead><tr>{th}</tr></thead>
      <tbody>
{chr(10).join(body_rows)}
      </tbody>
    </table>
  </div>
</div>
'''

# --- Tür etiketi pill'leri (Figma "Tür Tag": renk %16 zemin + tam renk 12/16 bold metin, r6, kenarlıksız) ---
def render_genre_tags(*genres):
    """Tablo 'Tür' hücresi için pill seti: render_genre_tags('Strateji','Aile'). Renk merkezi
    GENRE_BADGE_COLORS paletinden gelir — aynı tür her içerikte AYNI renk. Sentence case yaz."""
    spans = []
    for g in genres:
        c = badge_color_for(g)
        spans.append(f'<span style="display:inline-block;background:{hex_to_rgba(c,0.16)};color:{c};border-radius:6px;padding:4px 10px;font-size:12px;line-height:16px;font-weight:700;white-space:nowrap;">{g}</span>')
    return '<span style="display:inline-flex;flex-wrap:wrap;gap:6px 8px;align-items:center;vertical-align:middle;">' + ''.join(spans) + '</span>'

# --- Tablo oyun hücresi: isim (+link) + altında "Stüdyo · Yıl" (kural 11 ile tutarlı) ---
def render_game_cell(name, meta=None, href=None):
    # GFN tablosu c0 hücresi: name beyaz DemiBold (satır stili tabloda); meta = 'Stüdyo · Yıl' 12px gri alt satır.
    nm = f'<a href="{href}" style="color:inherit;text-decoration:none;">{name}</a>' if href else name
    sub = f'<div style="color:#B2B2B2;font-size:12px;line-height:16px;font-weight:500;margin-top:4px;">{meta}</div>' if meta else ''
    return f'<div>{nm}{sub}</div>'

# --- Öne Çıkan Oyun (Figma: #161616 + 1.5px rgba(255,201,0,0.5) çerçeve, ★ ÖNE ÇIKAN OYUN eyebrow,
#     New Science 24 isim, sağda dolu sarı buton; GA4 id=featured-game-button) ---
def render_compact_cta(game_name, tagline, button_label, button_url, cta_id="featured-game-button"):
    gamepad = ('<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#FFC900" stroke-width="2" '
               'stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0;margin-right:8px;">'
               '<line x1="6" y1="11" x2="10" y2="11"/><line x1="8" y1="9" x2="8" y2="13"/>'
               '<line x1="15" y1="12" x2="15.01" y2="12"/><line x1="18" y1="10" x2="18.01" y2="10"/>'
               '<rect x="2" y="6" width="20" height="12" rx="6"/></svg>')
    return f'''<div class="cta-compact gp-conic" style="--gp-glow:#FFC900;margin:32px 0;">
<div class="gp-conic-inner" style="background:#161616;border-radius:10.5px;padding:28px;display:flex;align-items:center;justify-content:space-between;gap:24px;flex-wrap:wrap;">
  <div style="flex:1;min-width:260px;">
    <div style="color:#FFC900;font-size:12px;line-height:16px;font-weight:700;letter-spacing:0.08em;margin-bottom:8px;display:flex;align-items:center;">{gamepad}ÖNE ÇIKAN OYUN</div>
    <div style="font-family:'New Science',GreycliffCF,-apple-system,sans-serif;font-weight:600;font-size:24px;line-height:32px;color:#fff;margin-bottom:8px;">{game_name}</div>
    <div style="color:#B2B2B2;font-size:16px;line-height:24px;">{tagline}</div>
  </div>
  <a id="{cta_id}" href="{button_url}" style="display:inline-flex;align-items:center;justify-content:center;background:#FFC900;color:#131313;padding:14px 24px;border-radius:8px;font-weight:600;font-size:16px;line-height:20px;text-decoration:none;white-space:nowrap;">{button_label}</a>
</div>
</div>
'''

# --- Steam/Xbox/Epic link helper (adds external icon and clickable wrapping) ---
def linkify_platforms(meta_text, game_name):
    """Wrap Steam/Xbox/Epic/Game Pass mentions with search links + ext icon."""
    import urllib.parse
    q = urllib.parse.quote(game_name)
    platforms = {
        'Steam': f'https://store.steampowered.com/search/?term={q}',
        'Xbox': f'https://www.xbox.com/en-US/games/search?q={q}',
        'Epic Games Store': f'https://store.epicgames.com/en-US/browse?q={q}&sortBy=relevancy',
        'Epic Games': f'https://store.epicgames.com/en-US/browse?q={q}&sortBy=relevancy',
        'Game Pass': f'https://www.xbox.com/en-US/xbox-game-pass/games?q={q}',
    }
    out = meta_text
    for label, url in platforms.items():
        link = f'<a href="{url}" target="_blank" rel="nofollow noopener" style="color:inherit;text-decoration:none;border-bottom:1px dotted rgba(255,255,255,0.3);">{label}{SVG_EXT_LINK}</a>'
        # Replace only whole-word matches (so "Steam, Xbox" doesn't break)
        import re as _re
        out = _re.sub(r'\b' + _re.escape(label) + r'\b(?![^<]*</a>)', link, out, count=1)
    return out

# --- Helper: rgba from hex (for tag tints) ---
def hex_to_rgba(hex_color, alpha):
    h = hex_color.lstrip('#')
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f'rgba({r},{g},{b},{alpha})'

# --- Helper: rengi beyaza doğru karıştır (rozet METNİ için yüksek kontrast / WCAG AA-AAA) ---
def lighten(hex_color, amt=0.45):
    """Tür rozeti metni doygun renk yerine açık tonu kullanır; koyu rozet zemininde kontrast
    4.5:1'in çok üzerine çıkar (Lighthouse/PageSpeed kontrast uyarısını giderir). Rozetin
    kenarı + zemini hâlâ tür rengindedir, kimlik korunur. amt: 0=aynı, 1=beyaz."""
    h = hex_color.lstrip('#')
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    r = round(r + (255 - r) * amt); g = round(g + (255 - g) * amt); b = round(b + (255 - b) * amt)
    return '#%02x%02x%02x' % (r, g, b)

# --- Tür rozeti -> GFN kategori sayfası (iç link) ---
# Yalnızca markanın linklenebilir dediği kategoriler. SADECE tek/saf rozet linklenir; birleşik/çift
# rozetler (ayraçlı: 'Aksiyon-RPG', 'Aksiyon-Macera', 'Indie - RPG') temiz bir kategori karşılığı
# olmadığından LİNKLENMEZ. Aynı yazıda eşleşen HER rozet linklenir (DEDUP YOK) — yalnızca oyun
# başlıklarındaki rozetlerde; card-table indeksi/master tabloda kategori linki verilmez.
_GFN = "https://gameplus.com.tr/gfn/oyunlar/"
GFN_CATEGORY_URLS = {
    "STRATEJI": _GFN + "strateji", "AKSIYON": _GFN + "aksiyon", "SIMULASYON": _GFN + "simulasyon",
    "DOVUS": _GFN + "dovus-oyunu", "DOVUS OYUNU": _GFN + "dovus-oyunu", "YARIS": _GFN + "yaris",
    "FPS": _GFN + "fps", "MMO": _GFN + "mmo", "MACERA": _GFN + "macera", "STEAM": _GFN + "steam",
    "CANLANDIRMA": _GFN + "canlandirma", "RPG": _GFN + "canlandirma", "MOBA": _GFN + "moba",
    "BAGIMSIZ": _GFN + "bagimsiz", "INDIE": _GFN + "bagimsiz", "ARCADE": _GFN + "arcade",
    "BULMACA": _GFN + "bulmaca", "BASIT EGLENCE": _GFN + "basit-eglence", "AILE DOSTU": _GFN + "aile-dostu",
    "PLATFORM": _GFN + "platform", "SPOR": _GFN + "spor", "UBISOFT CONNECT": _GFN + "ubisoft-connect",
    "POPULER": _GFN + "populer-oyunlar", "POPULER OYUNLAR": _GFN + "populer-oyunlar",
}

def _fold(s):
    """Türkçe + büyük/küçük harf duyarsız anahtar (İ/ı/ş/ğ/ü/ö/ç sadeleştirilir)."""
    s = (s or "").strip().upper()
    for a, b in (("İ", "I"), ("I", "I"), ("Ş", "S"), ("Ğ", "G"), ("Ü", "U"), ("Ö", "O"), ("Ç", "C"), ("Â", "A")):
        s = s.replace(a, b)
    return s

def category_url_for(badge):
    """Tür rozetini GFN kategori URL'ine eşle (yoksa None). YALNIZCA tek/saf rozet linklenir.
    Birleşik/çift rozetler — ayraçlı yazılanlar ('Aksiyon-RPG', 'Aksiyon-Macera', 'Indie - RPG') —
    temiz bir kategori karşılığı olmadığından LİNKLENMEZ (tür tutarlılığı). Çok kelimeli tekil
    kategoriler (örn. 'Dövüş Oyunu', 'Aile Dostu') boşlukla yazıldığı için bundan etkilenmez."""
    if not badge:
        return None
    if re.search(r"[-–/]", badge):   # birleşik/çift tag (ayraçlı) -> link yok
        return None
    return GFN_CATEGORY_URLS.get(_fold(badge))

# --- Card-Table: compact rows with text-like tags ---
def render_card_table(title, games):
    """games: list of {name, badge, badge_color, meta, anchor (optional)}"""
    # Rozet sütunu TÜM satırlarda AYNI genişlikte (en uzun rozete göre) -> oyun isimleri HİZALI kalır
    # ve uzun/birleşik rozetler (AKSİYON-MACERA vb.) KIRPILMAZ. Her .card-row ayrı grid olduğundan
    # 'max-content' kullanılırsa sütun satır-satır değişir ve isimler kayar; bu yüzden sabit px.
    # (Canlı blog ve önizleme aynı GreycliffCF fontunu kullandığından karakter-bazlı tahmin tutarlı.)
    _bl = [len(g.get('badge') or '') for g in games if g.get('badge')]
    bw = max(120, round(10.2 * max(_bl)) + 24) if _bl else 120
    rows = []
    for g in games:
        color = badge_color_for(g.get("badge"), g.get("badge_color"))
        tint = hex_to_rgba(color, 0.16)
        border = hex_to_rgba(color, 0.45)
        badge_text = _badge_text(color)
        badge_html = ''
        if g.get('badge'):
            badge_html = f'<span class="gp-badge" style="display:inline-block;color:{badge_text};background:{tint};padding:4px 10px;border-radius:6px;font-size:12px;line-height:16px;font-weight:700;white-space:nowrap;min-width:120px;text-align:center;">{g["badge"]}</span>'
        meta_html = ''
        if g.get('meta'):
            meta_html = f'<div class="gp-meta" style="color:#B2B2B2;font-size:0.78em;text-align:right;white-space:nowrap;font-weight:500;letter-spacing:0.01em;">{g["meta"]}</div>'
        name_html = f'<div class="gp-name" style="font-weight:600;color:#f3f4f6;font-size:0.98em;letter-spacing:-0.005em;transition:color 0.2s;">{g["name"]}</div>'
        # If anchor provided, make row a clickable anchor link
        if g.get('anchor'):
            row_tag = 'a'
            attrs = f' href="#{g["anchor"]}"'
        else:
            row_tag = 'div'
            attrs = ''
        # tür rozeti GFN kategorisine iç link — yalnızca satır kendisi link DEĞİLSE (iç içe <a> geçersiz)
        if g.get('badge_href') and row_tag != 'a' and badge_html:
            badge_html = f'<a href="{g["badge_href"]}" style="text-decoration:none;line-height:0;display:inline-flex;">{badge_html}</a>'
        rows.append(f'''  <{row_tag} class="card-row"{attrs} style="--row-c:{color};display:grid;grid-template-columns:{bw}px 1fr auto;gap:14px;padding:8px 18px;border-bottom:1px solid #29292b;align-items:center;transition:background 0.2s ease;text-decoration:none;color:inherit;">
    {badge_html}
    {name_html}
    {meta_html}
  </{row_tag}>''')
    return f'''<div class="card-table-wrap" style="margin:28px 0;">
  <div style="text-align:center;margin-bottom:14px;">
    <h3 style="display:inline-flex;align-items:center;justify-content:center;font-size:1.3em;font-weight:800;letter-spacing:-0.01em;margin:0;">
      {SVG_TROPHY}<span style="background:linear-gradient(110deg,#FFC900,#f59e0b);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">{title}</span>
    </h3>
  </div>
  <div class="card-table gp-layer gp-card-table-inner" style="--gp-frame:rgba(255,201,0,0.22);overflow:hidden;box-shadow:0 4px 18px rgba(0,0,0,0.5);">
    <div style="position:relative;z-index:1;">
{chr(10).join(rows)}
    </div>
  </div>
</div>
'''

# --- Game heading (H2/H3/H4) with inline tag + studio metadata (matches card-table style) ---
def render_game_h3_inline(anchor, name, badge, badge_color, meta_text, level="h3", badge_href=None):
    """Oyun başlığı. level: birden fazla oyun anlatılıyorsa her oyuna eklenir (h2/h3/h4 — çevredeki seviyeye göre).
    Başlık metnine RENK atanmaz (CMS başlık rengini zaten verir; yük azalır). badge_href verilirse tür rozeti
    o GFN kategori sayfasına iç link olur. **badge_href=None (varsayılan) = OTOMATİK:** tek/saf rozet kendi
    kategorisine; **BİRLEŞİK rozet (AKSİYON-MACERA) HER PARÇAYI ayrı ayrı** linkler (AKSİYON→/aksiyon,
    MACERA→/macera). **badge_href=False = link YOK** (tek-tür seride link stuffing'i önlemek için). **URL =
    tüm rozeti o URL'e linkle.**"""
    badge_color = badge_color_for(badge, badge_color)  # tür -> standart palet rengi (tüm içerikte aynı)
    tint = hex_to_rgba(badge_color, 0.16)
    border = hex_to_rgba(badge_color, 0.45)
    badge_text = _badge_text(badge_color)
    inner, whole_href = badge, None
    if badge_href is False:
        pass  # link YOK
    elif badge_href:
        whole_href = badge_href  # açık URL -> tüm rozet
    elif re.search(r'[-–/]', badge or ''):  # birleşik -> her parçayı kendi kategorisine linkle
        seg = []
        for p in re.split(r'(\s*[-–/]\s*)', badge):
            if re.fullmatch(r'\s*[-–/]\s*', p):
                seg.append(p)
            else:
                u = GFN_CATEGORY_URLS.get(_fold(p))
                seg.append(f'<a href="{u}" style="color:inherit;text-decoration:none;">{p}</a>' if u else p)
        inner = ''.join(seg)
    else:  # tek/saf rozet -> tüm rozet (kategori varsa)
        whole_href = GFN_CATEGORY_URLS.get(_fold(badge or ''))
    badge_html = (f'<span style="display:inline-block;color:{badge_text};background:{tint};'
                  f'padding:4px 10px;border-radius:6px;font-size:12px;line-height:16px;font-weight:700;'
                  f'white-space:nowrap;">{inner}</span>')
    if whole_href:
        # display:contents -> anchor kutu üretmez; rozet linksizle birebir aynı yerleşir.
        badge_html = f'<a href="{whole_href}" style="text-decoration:none;display:contents;">{badge_html}</a>'
    return f'''<{level} id="{anchor}" style="display:flex;flex-wrap:wrap;align-items:center;gap:12px;margin:32px 0 14px;line-height:1.4;">
  {badge_html}
  <span style="font-weight:700;letter-spacing:-0.01em;">{name}</span>
  <span style="font-size:0.52em;color:#B2B2B2;font-weight:500;letter-spacing:0.02em;flex-basis:100%;margin-top:-4px;">{meta_text}</span>
</{level}>'''

# --- Inline Game Card (small, premium, in game description section) ---
def render_inline_game_card(name, badge, badge_color, meta_lines):
    """Small card to be floated alongside game description text."""
    meta_html = '<br>'.join(meta_lines)
    return f'''<aside class="gp-game-info-card" style="float:right;width:210px;margin:0 0 16px 22px;background:{_surface()};border:1px solid #29292b;border-radius:10px;padding:16px;font-size:0.9em;box-shadow:0 4px 12px rgba(0,0,0,0.5),inset 0 1px 0 rgba(255,255,255,0.04);">
  <span style="display:inline-block;background:{badge_color};color:#fff;padding:4px 11px;border-radius:999px;font-size:0.62em;font-weight:800;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:10px;box-shadow:inset 0 1px 0 rgba(255,255,255,0.18),0 2px 4px rgba(0,0,0,0.4);">{badge}</span>
  <div style="font-weight:700;color:#fff;font-size:1.04em;line-height:1.3;margin-bottom:8px;letter-spacing:-0.01em;">{name}</div>
  <div style="color:#B2B2B2;font-size:0.82em;line-height:1.55;font-weight:500;">{meta_html}</div>
</aside>
'''

# --- İlgili Yazı Kartları (Figma "Related Card": #161616 + #29292B, 150px thumb + GFN THURSDAY etiketi,
#     tarih 12 gri, başlık 20 bold beyaz, "Devamını oku →" sarı) ---
def render_prev_weeks_cards(items):
    cards = []
    for item in items:
        cards.append(f'''  <a href="{item["url"]}" class="gp-prev-week" style="display:block;text-decoration:none;background:#161616;border:1px solid #29292B;border-radius:16px;overflow:hidden;color:inherit;transition:border-color 0.25s,transform 0.25s,box-shadow 0.25s;">
    <div style="height:150px;background:{('url(' + chr(39) + item['img'] + chr(39) + ') center/cover no-repeat' if item.get('img') else 'linear-gradient(135deg,#1c1a0e,#0d0d0d 70%')});display:flex;align-items:flex-end;padding:14px 20px;position:relative;">
      <div style="position:absolute;inset:0;background:linear-gradient(to top, rgba(0,0,0,0.78), rgba(0,0,0,0.05) 60%);"></div>
      <span style="color:#FFC900;font-size:12px;line-height:16px;font-weight:700;letter-spacing:0.08em;position:relative;">GFN THURSDAY</span>
    </div>
    <div style="padding:18px 20px 20px;">
      <div style="color:#B2B2B2;font-size:12px;line-height:16px;font-weight:500;margin-bottom:8px;">{item["date"]}</div>
      <div style="color:#fff;font-size:20px;line-height:24px;font-weight:700;margin-bottom:8px;">{item["label"]}</div>
      <div style="color:#FFC900;font-size:16px;line-height:20px;font-weight:600;">Devamını oku &rarr;</div>
    </div>
  </a>''')
    return f'''<div class="prev-weeks-grid" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:24px;margin:24px 0 32px;">
{chr(10).join(cards)}
</div>
<style>
  .gp-prev-week:hover {{ border-color: rgba(255,201,0,0.5) !important; transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,0.5); }}
</style>
'''

# --- İçindekiler (Figma: #161616 kart + #29292B kenarlık + New Science başlık + sarı 01/02 numaralar) ---
def render_floating_toc(items):
    li_items = []
    num = 0
    for level, text, anchor in items:
        if level == 2:
            num += 1
            marker = f'<span style="color:#FFC900;font-size:12px;line-height:16px;font-weight:700;flex-shrink:0;margin-top:4px;">{num:02d}</span>'
        else:
            marker = '<span style="width:16px;flex-shrink:0;"></span>'
        li_items.append(
            f'    <li style="display:flex;gap:10px;margin:12px 0;list-style:none;">{marker}'
            f'<a href="#{anchor}" onclick="this.closest(&quot;details&quot;).removeAttribute(&quot;open&quot;)" style="color:#B2B2B2;text-decoration:none;font-size:16px;line-height:24px;">{text}</a></li>')
    body = chr(10).join(li_items)
    return f'''<details class="floating-toc" style="position:fixed;top:120px;right:16px;z-index:100;max-width:320px;background:#161616;border:1px solid #29292B;border-radius:16px;box-shadow:0 8px 28px rgba(0,0,0,0.6);">
  <summary style="display:flex;align-items:center;padding:16px 20px;color:#fff;cursor:pointer;font-family:'New Science',GreycliffCF,-apple-system,sans-serif;font-weight:600;font-size:20px;line-height:28px;list-style:none;user-select:none;">İçindekiler</summary>
  <ul style="margin:0;padding:0 20px 16px;max-height:60vh;overflow-y:auto;list-style:none;">
{body}
  </ul>
</details>
<style>
  .floating-toc summary::-webkit-details-marker {{{{ display: none; }}}}
  .floating-toc summary::marker {{{{ display: none; }}}}
  .floating-toc ul li a:hover {{{{ color: #FFC900 !important; }}}}
  @media (max-width: 900px) {{{{
    .floating-toc {{{{ top: auto !important; bottom: 16px !important; max-width: 240px !important; }}}}
  }}}}
</style>
'''

# --- FAQ Accordion (premium dark, Game+ '+' indicator that rotates) ---
def render_faq_accordion(pairs):
    items = []
    for q, a in pairs:
        items.append(f'''  <details class="faq-item" style="margin-bottom:10px;border:1px solid #29292b;border-radius:10px;overflow:hidden;background:transparent;box-shadow:0 2px 8px rgba(0,0,0,0.4);">
    <summary style="display:flex;align-items:center;gap:14px;padding:16px 20px;cursor:pointer;background:transparent;font-weight:700;color:#f3f4f6;letter-spacing:-0.005em;list-style:none;">
      <span class="faq-icon" style="display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;flex-shrink:0;color:#FFC900;font-size:1.5em;font-weight:300;line-height:1;">+</span>
      <span style="flex:1;">{q.strip()}</span>
    </summary>
    <div style="padding:14px 20px 18px 56px;border-top:1px solid #29292b;background:transparent;"><p style="margin:0;color:#B2B2B2;line-height:1.55;font-size:0.94em;">{a.strip()}</p></div>
  </details>''')
    return f'<div class="faq-block" style="margin:24px 0;">\n{chr(10).join(items)}\n</div>'

# --- Slug helper ---
def slugify(text):
    text = text.lower()
    text = re.sub(r'[ığüşöç]', lambda m: {'ı':'i','ğ':'g','ü':'u','ş':'s','ö':'o','ç':'c'}[m.group()], text)
    text = re.sub(r'[^a-z0-9]+', '-', text).strip('-')
    return text[:60]

def inject_heading_ids(html):
    toc_items = []
    def replace_h(match):
        tag = match.group(1)
        text = match.group(2)
        clean = re.sub(r'<[^>]+>', '', text)
        anchor = slugify(clean)
        toc_items.append((int(tag[1]), clean, anchor))
        return f'<{tag} id="{anchor}">{text}</{tag}>'
    new_html = re.sub(r'<(h[23])>(.*?)</\1>', replace_h, html, flags=re.DOTALL)
    return new_html, toc_items


def ensure_leading_h1(html):
    """Blog gövdesi İLK başlığıyla (yazı başlığı) bir H1 olarak başlar. Taslakta zaten <h1> varsa
    DOKUNULMAZ. Eskiden CMS başlığı ayrı bastığı için gövde H1'i H2'ye çevriliyordu (demote_h1);
    KURAL TERSİNE DÖNDÜ — artık her blog yazısı gövdede TEK bir H1 ile başlar (ilk başlık H1 olur).
    Taslakta H1 yoksa gövdedeki İLK başlık (h2-h6) H1'e yükseltilir; sonraki başlıklar olduğu gibi kalır.
    Build akışının EN SON adımında çağır (ToC '</h1>' çapasıyla enjekte edildikten sonra)."""
    if re.search(r'<h1\b', html, flags=re.IGNORECASE):
        return html
    return re.sub(r'<(h[2-6])(\b[^>]*)>(.*?)</\1>',
                  lambda m: f'<h1{m.group(2)}>{m.group(3)}</h1>',
                  html, count=1, flags=re.DOTALL | re.IGNORECASE)


def demote_h1(html):
    """DEPRECATED — eski kural (gövde H1 İÇERMEZ; başlığı H2'ye çevir) ARTIK GEÇERSİZ.
    Yeni kural: gövde tek bir H1 ile başlar (bkz. ensure_leading_h1). Bu shim geriye dönük
    uyumluluk için H1'i KORUR (artık H2'ye ÇEVİRMEZ); yeni build'lerde ensure_leading_h1 kullan."""
    return ensure_leading_h1(html)


# --- YouTube embed shrink (720px max, centered) ---
def shrink_youtube_embeds(html):
    """Add .gp-yt-wrap class to existing embed divs (CSS caps width to 720px and centers)."""
    return re.sub(
        r'(<!--[^>]*Embed Ba[şs]lang[ıi]c[ıi][^>]*-->)\s*<div style="width: 100%;',
        r'\1\n<div class="gp-yt-wrap" style="width: 100%;',
        html
    )


# --- Çıktı doğrulama (her build'in EN SON adımı) ------------------------------
# Amaç: her yazının AYNI iskeletle çıkmasını garanti etmek (tutarlı çıktı). Build script
# final body'yi (ANIMATED_BORDER_STYLE + enjekte edilmiş gövde) verir; print_report raporu basar.
# FAIL = çıktı kuralı ihlali, teslimden ÖNCE düzelt. WARN = göz at, bağlama göre kabul edilebilir.
# Bu programatik kontrol; yargı gerektiren maddeler için references/qa-checklist.md'ye de bak.
def verify_output(final_html, blog_type="general", n_games=None, expect_faq=False):
    """final_html: build'in son hali (ANIMATED_BORDER_STYLE + gövde).
    blog_type: 'general' (rehber/listicle) | 'gfn' (GFN Thursday).
    n_games: birden çok oyun anlatan yazıda oyun sayısı (inline başlık + card-row bununla eşleşmeli).
    expect_faq: SSS bölümü olan yazılarda True.
    Dönüş: [(durum, ad, detay)]; durum 'PASS'|'FAIL'|'WARN'."""
    r = []
    def add(cond, name, ok_d="", fail_d="", warn=False):
        r.append(("PASS" if cond else ("WARN" if warn else "FAIL"), name, ok_d if cond else fail_d))

    # 1) Tek H1 ve İLK başlık H1 (yeni kural: her yazı gövdede tek H1 ile başlar)
    h1n = len(re.findall(r'<h1\b', final_html, re.I))
    first = re.search(r'<h([1-6])\b', final_html, re.I)
    add(h1n == 1, "Tek H1", f"{h1n} adet H1", f"{h1n} adet H1 (tam 1 olmalı)")
    add(bool(first) and first.group(1) == '1', "İlk başlık H1",
        "ilk başlık H1", "ilk başlık H1 değil (ensure_leading_h1 çağır)")

    # 2) Üst meta header EKLENMEMİŞ (CMS tarih + marka adını zaten gösteriyor)
    add('class="article-meta"' not in final_html, "Meta header yok",
        "meta header eklenmemiş", "article-meta meta header var — KALDIR (render_meta kullanma)")

    # 3) ANIMATED_BORDER_STYLE tam 1 kez
    style_n = final_html.count('@keyframes gameplus-border-shimmer')
    add(style_n == 1, "Stil bloğu (1x)", "bir kez", f"{style_n} kez (1 olmalı, en başta)")

    # 4) Em dash (—) yok (en dash – tür rozetinde ayraç olabilir, o serbest)
    add('—' not in final_html, "Em dash yok", "yok", "em dash (—) var — nokta/virgülle böl")

    # 5) Floating ToC
    add('class="floating-toc"' in final_html, "Floating ToC", "var", "floating ToC yok")

    # 6) TLDR + 3-6 madde
    tl = re.search(r'class="tldr-block.*?</ul>', final_html, re.S)
    add(bool(tl), "TLDR var", "var", "TLDR (Hızlı Özet) yok")
    if tl:
        n_tldr = len(re.findall(r'<li[ >]', tl.group(0)))   # <li ...> (SVG <line> ile karışmasın)
        add(3 <= n_tldr <= 6, "TLDR 3-6 madde", f"{n_tldr} madde", f"{n_tldr} madde (3-6 olmalı)")

    # 7) Info-card (TLDR ile birlikte her iki blog tipinde de zorunlu)
    add('class="info-card"' in final_html, "Info-card", "var", "info-card yok (genel blog ve GFN'de zorunlu)")

    # 8) FAQ (SSS bölümü varsa accordion)
    if expect_faq:
        add('class="faq-block"' in final_html, "FAQ accordion", "var",
            "FAQ yok (SSS H3+P çiftleri accordion'a çevrilmeli)")

    # 8a) Editör Notu + Hatırlatma (her yazıda zorunlu)
    add('class="editor-note"' in final_html, "Editör Notu", "var", "Editör Notu yok (her yazıda zorunlu)")
    add('class="highlight-box"' in final_html, "Hatırlatma", "var", "Hatırlatma yok (her yazıda zorunlu)")

    # 8b) Madde listesi (taranabilirlik) — uygun yerlerde render_list kullan
    add('class="gp-list"' in final_html, "Madde listesi", "var",
        "gövdede madde (bullet) listesi yok — uygun yerlerde render_list kullan", warn=True)

    # 9) Oyun sayısı tutarlı: inline başlık == card-row == n_games (genel listicle)
    if n_games is not None:
        n_inline = final_html.count('flex-basis:100%;margin-top:-4px;')   # render_game_h3_inline imzası
        n_rows = final_html.count('class="card-row"')
        add(n_inline == n_games, "Inline oyun başlığı",
            f"{n_inline} başlık", f"{n_inline} inline başlık (beklenen {n_games}) — düz <hN>Oyun</hN> kalmış olabilir")
        add(n_rows == n_games, "Card-table satırı", f"{n_rows} satır", f"{n_rows} card-row (beklenen {n_games})")

    # 10) YouTube embed: aspect-ratio var, padding-bottom % hack yok (kare-bug)
    if 'youtube.com/embed' in final_html:
        add('aspect-ratio' in final_html, "Embed aspect-ratio", "16/9", "aspect-ratio yok (embed kare görünebilir)")
        add(not re.search(r'padding-bottom:\s*5[0-9]', final_html), "Embed padding-hack yok",
            "yok", "padding-bottom % hack var — aspect-ratio kullan", warn=True)

    # 11) PlayStation (GFN platform/lisans/CTA bağlamında YASAK — WARN, haber yazıları hariç)
    if re.search(r'playstation', final_html, re.I):
        add(False, "PlayStation geçiyor", "",
            "'PlayStation' var — GFN platform/lisans/CTA bağlamında OLMADIĞINDAN emin ol", warn=True)

    return r


def print_report(results, label=""):
    """verify_output sonucunu bas; FAIL yoksa True döner."""
    sym = {"PASS": "✓", "FAIL": "✗", "WARN": "!"}
    print(("── Çıktı kontrolü " + label + " ").ljust(58, "─"))
    for status, name, detail in results:
        print(f"  {sym[status]} {name}" + (f" — {detail}" if detail else ""))
    fails = [x for x in results if x[0] == "FAIL"]
    warns = [x for x in results if x[0] == "WARN"]
    print(f"  → {'GEÇTI' if not fails else str(len(fails)) + ' HATA'}" + (f", {len(warns)} uyarı" if warns else ""))
    return not fails


# --- Kontrol noktası: yazarın metni korundu mu (enrichment yalnız EKLER) ---
def verify_source_preserved(original_html, final_html, min_ratio=0.97):
    """original_html'deki (ham taslak) her anlamlı metin parçası final'de var mı?
    Halüsinasyon / cümle değiştirme / paragraf silme yakalar. Dönüş: (ok, missing_list, oran)."""
    def norm(h):
        h = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', h, flags=re.S | re.I)
        h = re.sub(r'<[^>]+>', ' ', h)
        h = (h.replace('&amp;', '&').replace('&nbsp;', ' ')
               .replace('&#39;', "'").replace('&quot;', '"').replace('&lt;', '<').replace('&gt;', '>'))
        return re.sub(r'\s+', ' ', h).strip()
    def chunks(h):
        out = []
        for m in re.findall(r'<(?:p|h[1-6]|li)\b[^>]*>(.*?)</(?:p|h[1-6]|li)>', h, flags=re.S | re.I):
            t = norm(m)
            if len(t) >= 25:
                out.append(t)
        return out
    orig = chunks(original_html)
    hay = norm(final_html)
    missing = [t for t in orig if t[:70].lower() not in hay.lower()]
    ratio = 1.0 if not orig else round(1 - len(missing) / len(orig), 3)
    return (ratio >= min_ratio, missing, ratio)

def print_source_report(original_html, final_html):
    ok, missing, ratio = verify_source_preserved(original_html, final_html)
    print(("── Kaynak metin korundu mu (%.0f%%) " % (ratio * 100)).ljust(58, "─"))
    if ok and not missing:
        print("  ✓ Yazarın tüm metin parçaları çıktıda mevcut (halüsinasyon/silme yok).")
    else:
        print("  ✗ EKSİK/DEĞİŞMİŞ %d parça (ilk 5):" % len(missing))
        for t in missing[:5]:
            print("     -", t[:80])
    return ok
