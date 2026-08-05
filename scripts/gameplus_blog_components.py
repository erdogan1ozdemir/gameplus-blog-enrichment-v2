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
# DEPRECATED (v10.10): kupa ikonu kaldırıldı, artık kullanılmıyor. Yeni içerikte ÇAĞIRMA.
SVG_TROPHY = '<svg width="24" height="24" viewBox="0 0 24 24" style="vertical-align:-6px;margin-right:10px;flex-shrink:0;"><defs><linearGradient id="gp-grad" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#FFC900"/><stop offset="100%" stop-color="#f59e0b"/></linearGradient></defs><path fill="url(#gp-grad)" d="M19 5h-2V3H7v2H5c-1.1 0-2 .9-2 2v1c0 2.55 1.92 4.63 4.39 4.94.63 1.5 1.98 2.63 3.61 2.96V19H7v2h10v-2h-4v-3.1c1.63-.33 2.98-1.46 3.61-2.96C19.08 12.63 21 10.55 21 8V7c0-1.1-.9-2-2-2zM5 8V7h2v3.82C5.84 10.4 5 9.3 5 8zm14 0c0 1.3-.84 2.4-2 2.82V7h2v1z"/></svg>'
# Green checkmark for TLDR/info-card items
SVG_CHECK_GREEN = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#FFC900" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0;"><polyline points="20 6 9 17 4 12"/></svg>'
# External link icon (small arrow up-right)
SVG_EXT_LINK = '<svg class="gp-ext" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M7 17L17 7"/><polyline points="7 7 17 7 17 17"/></svg>'
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
.gp-content {--gp-surface:#161616;--gp-line:#29292b;--gp-accent:#FFC900;}
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
.gp-content .gp-animated-border { position: relative; border-radius: 12px; padding: 1px; background: linear-gradient(110deg, #FFC900 0%, #f59e0b 30%, #FFC900 60%, #f59e0b 100%); background-size: 300% 100%; animation: gameplus-border-shimmer 6s ease-in-out infinite; }
.gp-content .gp-animated-border > .gp-inner { background: transparent; border-radius: 11px; padding: 22px 24px; }
/* V8: Rotating Conic Glow border */
.gp-content .gp-conic { position: relative; border-radius: 12px; padding: 1.5px; }
.gp-content .gp-conic::before {
  content:''; position:absolute; inset:0; border-radius:12px; padding:1.5px;
  background: conic-gradient(from var(--gp-conic-angle,0deg), transparent 0deg, var(--gp-glow,#FFC900) 60deg, transparent 120deg, transparent 360deg);
  -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
  -webkit-mask-composite: xor;
          mask-composite: exclude;
  animation: gp-rotate-conic 6s linear infinite;
  pointer-events: none;
}
.gp-content .gp-conic > .gp-conic-inner { background:var(--gp-surface,#161616); border-radius:10.5px; position:relative; }
/* V9: Layered Frame */
.gp-content .gp-layer { position:relative; border-radius:12px; border:1px solid var(--gp-frame,rgba(255,201,0,0.22)); background:var(--gp-surface,#161616); }
.gp-content .gp-cell { position:relative; background:var(--gp-surface,#161616); border:1px solid var(--gp-line,#29292b); border-radius:10px; padding:14px 16px; }
.gp-content .gp-layer::before { content:''; position:absolute; inset:5px; border:1px solid #29292b; border-radius:8px; pointer-events:none; }
/* FAQ + sign pulsing animation */
.gp-content .faq-item .faq-icon { animation: gp-pulse-plus 2.2s ease-in-out infinite; }
.gp-content .gp-card-table-inner .card-row:last-child { border-bottom: none; }
.gp-content .gp-card-table-inner .card-row { position: relative; }
.gp-content .gp-card-table-inner a.card-row { text-decoration: none; color: inherit; }
/* Hover Slide Accent: colored bar slides in from left on hover (Steam list vibe) */
.gp-content .gp-card-table-inner .card-row::before { content:''; position:absolute; left:0; top:0; bottom:0; width:0; background:var(--row-c,#FFC900); transition:width 0.2s ease; }
.gp-content .gp-card-table-inner .card-row:hover::before { width:4px; }
.gp-content .gp-card-table-inner .card-row:hover { background: rgba(255,255,255,0.025); }
.gp-content .gp-card-table-inner a.card-row:hover .gp-name { color: #fff; }
/* Comparison table fixes */
.gp-content .table-wrap table { border-radius: 12px; }

/* ================= v10.7 - Geçiş 3: tablo / card-table / oyun başlığı / tür rozeti =================
   Inline stiller sınıflara taşındı. Dinamik kalanlar inline: tür renkleri (--row-c, background/color)
   ve card-table rozet sütunu genişliği (--gp-bw). */

/* --- Karşılaştırma / oyun tablosu --- */
.gp-content .table-wrap { margin: 24px 0; border-radius: 16px; overflow: hidden; }
.gp-content .gp-table-scroll { overflow-x: auto;
  /* Kaydırma çubuğu HER GENİŞLİKTE gizli: kaydırma çalışır, bant görünmez.
     Kaydırılabilirliği "Tabloyu yana kaydır ->" ipucu anlatıyor. */
  scrollbar-width: none; -ms-overflow-style: none; }
.gp-content .gp-table-scroll::-webkit-scrollbar { display: none; width: 0; height: 0; }
.gp-content .gp-table-hint { display: none; font-size: 12px; line-height: 16px; font-weight: 500;
  color: #B2B2B2; padding: 10px 14px 0; }
.gp-content .table-wrap table { width: 100%; border-collapse: collapse; background: transparent; }
.gp-content .table-wrap th { background: #1E1E18; padding: 19px 24px; text-align: center; color: #FFC900;
  font-weight: 700; font-size: 16px; line-height: 20px; border-bottom: 1px solid rgba(255,201,0,0.3); }
.gp-content .table-wrap td { padding: 14px 24px; vertical-align: middle; color: #B2B2B2; font-weight: 400;
  font-size: 16px; line-height: 20px; }
.gp-content .table-wrap tbody tr + tr td { border-top: 1px solid #29292B; }
/* Sıra numarası sütunu: içeriği kadar yer kaplar, iki yanında eşit boşluk */
.gp-content .table-wrap th.gp-col-num, .gp-content .table-wrap td.gp-col-num {
  width: 1%; white-space: nowrap; text-align: center; padding-left: 20px; padding-right: 20px; }
/* Sıralama tablosu (ilk sütun sıra no): oyun adları card-table'daki gibi beyaz ve yarı kalın */
.gp-content .gp-table-rank td:not(.gp-col-num) { color: #fff; font-weight: 400; }
/* Sıralama tablosunda hover: TÜM hücreler sarıya döner. Genel hover kuralı yalnız
   `td:first-child`'ı hedefliyor; orada sıra numarası olduğu için oyun adları beyaz kalıyordu. */
.gp-content .table-wrap.gp-table-rank tbody tr:hover > td,
.gp-content .table-wrap.gp-table-rank tbody tr:hover > td .gp-tg-link,
.gp-content .table-wrap.gp-table-rank tr.gp-row-feat > td,
.gp-content .table-wrap.gp-table-rank tr.gp-row-feat > td .gp-tg-link { color: #FFC900; }
/* Sıralama tablosunda başlık ve hücreler SOLA yaslı; yalnız sıra-no sütunu ortalı.
   `tr` eklenmesi bilinçli: eski GFN 3-sütun kuralı (:nth-last-child(3) ~ :nth-child(2))
   2. sütunu ortalıyor ve specificity'si (0,4,2); eşitlemek için gerekiyor. */
.gp-content .table-wrap.gp-table-rank tr th:not(.gp-col-num),
.gp-content .table-wrap.gp-table-rank tr td:not(.gp-col-num) { text-align: left; }
.gp-content .table-wrap.gp-table-rank tr th.gp-col-num,
.gp-content .table-wrap.gp-table-rank tr td.gp-col-num { text-align: center; }
/* Eski GFN kuralı (:first-child:nth-last-child(3) ~ :nth-child(2)) 2. sütunu ortalıyor ve
   specificity'si (0,5,1); sıralama tablosunda aynı deseni .gp-table-rank ile (0,6,1) yapıp aşıyoruz. */
.gp-content .table-wrap.gp-table-rank tr > :first-child:nth-last-child(3) ~ :nth-child(2),
.gp-content .table-wrap.gp-table-rank tr > :first-child:nth-last-child(3) ~ :nth-child(3),
.gp-content .table-wrap.gp-table-rank tr > :first-child:nth-last-child(4) ~ :nth-child(2),
.gp-content .table-wrap.gp-table-rank tr > :first-child:nth-last-child(4) ~ :nth-child(3),
.gp-content .table-wrap.gp-table-rank tr > :first-child:nth-last-child(4) ~ :nth-child(4) { text-align: left; }

/* --- v10.9: iki tablo tipinde de sütunlar dar, taşan metin ALTA sarar --- */
@media (max-width: 700px) {
  /* Sıralama tablosu: iki sıra sütunu eşit paylaşsın, uzun oyun adı alt satıra insin */
  .gp-content .table-wrap.gp-table-rank tr > :first-child:nth-last-child(3) ~ :nth-child(2),
  .gp-content .table-wrap.gp-table-rank tr > :first-child:nth-last-child(3) ~ :nth-child(3) {
    white-space: normal; width: 44%; overflow-wrap: break-word; }
  .gp-content .table-wrap.gp-table-rank tr > :first-child:nth-last-child(3) { width: 12%; }
  /* Tür sütunu (rozetler) dar kalsın, rozetler alt alta sarsın */
  .gp-content .table-wrap td .gp-genres { flex-wrap: wrap; }
}
.gp-content .table-wrap tr.gp-row-feat td { background: rgba(255,201,0,0.12); }
.gp-content .table-wrap tr.gp-row-feat td:first-child,
.gp-content .table-wrap tr.gp-row-feat td:first-child .gp-tg-link { color: #FFC900; }

/* --- Tür rozetleri (tablo 'Tür' hücresi) --- */
.gp-content .gp-genres { display: inline-flex; flex-wrap: wrap; gap: 6px 8px; align-items: center;
  vertical-align: middle; }
.gp-content .gp-genre { display: inline-block; border-radius: 6px; padding: 4px 10px; font-size: 12px;
  line-height: 16px; font-weight: 700; white-space: nowrap; }

/* --- Card-table ("En İyi N ..." tıklanabilir liste) --- */
.gp-content .card-table-wrap { margin: 28px 0; }
/* Tablo üstü başlık: h-tag DEĞİL (SEO outline'ına girmesin), ama H2 tipografisinde.
   Kupa ikonu v10.10'da kaldırıldı; gradient yerine düz sarı. */
.gp-content .gp-ct-title { font-family: 'New Science', GreycliffCF, -apple-system, sans-serif;
  font-weight: 600; color: #FFC900; margin: 0 0 14px; text-align: left; }
.gp-content .card-table { overflow: hidden; box-shadow: 0 4px 18px rgba(0,0,0,0.5); }
.gp-content .gp-card-rows { position: relative; z-index: 1; }
.gp-content .card-row { display: grid; grid-template-columns: var(--gp-bw,120px) 1fr auto; gap: 14px;
  padding: 8px 18px; border-bottom: 1px solid #29292b; align-items: center;
  transition: background 0.2s ease; text-decoration: none; color: inherit; }
.gp-content .gp-badge { display: inline-block; padding: 4px 10px; border-radius: 6px; font-size: 12px;
  line-height: 16px; font-weight: 700; white-space: nowrap; width: 100%; box-sizing: border-box;
  text-align: center; }
.gp-content .gp-badge-link { text-decoration: none; line-height: 0; display: inline-flex; }
.gp-content .gp-name { font-weight: 600; color: #f3f4f6; font-size: 0.98em; letter-spacing: -0.005em;
  transition: color 0.2s; }
.gp-content .gp-meta { color: #B2B2B2; font-size: 0.78em; text-align: right; white-space: nowrap;
  font-weight: 500; letter-spacing: 0.01em; }

/* --- Oyun başlığı (tür rozeti + isim + "Stüdyo · Yıl") --- */
.gp-content .gp-game-head { display: flex; flex-wrap: wrap; align-items: center; gap: 12px;
  margin: 32px 0 14px; line-height: 1.4; }
/* Oyun adı H2 ÖLÇÜSÜNDE basılır; yazıda oyuna ayrı bir başlık seviyesi verilmediği için
   h3/h4 ile render edilse bile H2'den BÜYÜK görünmemeli (mobilde h3 24/32 iken h2 21/28). */
.gp-content .gp-game-head .gp-game-name { font-size: 32px; line-height: 40px; color: #fff; }
@media (max-width: 700px) {
  .gp-content .gp-game-head .gp-game-name { font-size: 21px; line-height: 28px; }
}
.gp-content .gp-game-badge { display: inline-block; padding: 4px 10px; border-radius: 6px; font-size: 12px;
  line-height: 16px; font-weight: 700; white-space: nowrap; }
.gp-content .gp-game-badge-link { text-decoration: none; display: contents; }
.gp-content .gp-game-name { font-weight: 700; letter-spacing: -0.01em; }
.gp-content .gp-game-meta { font-size: 0.52em; color: #B2B2B2; font-weight: 500; letter-spacing: 0.02em;
  flex-basis: 100%; margin-top: -4px; }

/* --- Tablo oyun hücresi + dış link ikonu --- */
.gp-content .gp-tg-link { color: inherit; text-decoration: none; }
.gp-content .gp-tg-meta { color: #B2B2B2; font-size: 12px; line-height: 16px; font-weight: 500; margin-top: 4px; }
.gp-content .gp-ext { width: 11px; height: 11px; vertical-align: 1px; margin-left: 3px; opacity: 0.65; }

/* --- Önceki haftalar kartları (Figma "Related Card") --- */
.gp-content .prev-weeks-grid { display: grid; grid-template-columns: repeat(auto-fit,minmax(280px,1fr));
  gap: 24px; margin: 24px 0 32px; }
.gp-content .gp-prev-week { display: block; text-decoration: none; background: #161616;
  border: 1px solid #29292B; border-radius: 16px; overflow: hidden; color: inherit;
  transition: border-color 0.25s, transform 0.25s, box-shadow 0.25s; }
.gp-content .gp-prev-week:hover { border-color: rgba(255,201,0,0.5); transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.5); }
.gp-content .gp-pw-thumb { height: 150px; background-color: #0d0d0d;
  background: var(--gp-thumb, linear-gradient(135deg,#1c1a0e,#0d0d0d 70%)) center/cover no-repeat;
  display: flex; align-items: flex-end; padding: 14px 20px; position: relative; }
.gp-content .gp-pw-scrim { position: absolute; inset: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.78), rgba(0,0,0,0.05) 60%); }
.gp-content .gp-pw-tag { color: #FFC900; font-size: 12px; line-height: 16px; font-weight: 700;
  letter-spacing: 0.08em; position: relative; }
.gp-content .gp-pw-body { padding: 18px 20px 20px; }
.gp-content .gp-pw-date { color: #B2B2B2; font-size: 12px; line-height: 16px; font-weight: 500; margin-bottom: 8px; }
.gp-content .gp-pw-title { color: #fff; font-size: 20px; line-height: 24px; font-weight: 700; margin-bottom: 8px; }
.gp-content .gp-pw-more { color: #FFC900; font-size: 16px; line-height: 20px; font-weight: 600; }

/* --- Yana yaslı oyun bilgi kartı --- */
.gp-content .gp-game-info-card { float: right; width: 210px; margin: 0 0 16px 22px; background: #161616;
  border: 1px solid #29292b; border-radius: 10px; padding: 16px; font-size: 0.9em;
  box-shadow: 0 4px 12px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.04); }
.gp-content .gp-gic-badge { display: inline-block; color: #fff; padding: 4px 11px; border-radius: 999px;
  font-size: 0.62em; font-weight: 800; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 10px;
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.18), 0 2px 4px rgba(0,0,0,0.4); }
.gp-content .gp-gic-name { font-weight: 700; color: #fff; font-size: 1.04em; line-height: 1.3;
  margin-bottom: 8px; letter-spacing: -0.01em; }
.gp-content .gp-gic-meta { color: #B2B2B2; font-size: 0.82em; line-height: 1.55; font-weight: 500; }
/* ================= v10.7 - Geçiş 4: FAQ / gövde listesi / İçindekiler ================= */

/* --- SSS akordiyonu --- */
.gp-content .faq-block { margin: 24px 0; }
.gp-content .faq-item { margin-bottom: 10px; border: 1px solid #29292b; border-radius: 10px;
  overflow: hidden; background: transparent; box-shadow: 0 2px 8px rgba(0,0,0,0.4); }
.gp-content .faq-item summary { display: flex; align-items: center; gap: 14px; padding: 16px 20px;
  cursor: pointer; background: transparent; font-weight: 700; color: #f3f4f6; letter-spacing: -0.005em;
  list-style: none; }
.gp-content .faq-item .faq-icon { display: inline-flex; align-items: center; justify-content: center;
  width: 22px; height: 22px; flex-shrink: 0; color: #FFC900; font-size: 1.5em; font-weight: 300; line-height: 1; }
.gp-content .faq-item .faq-q { flex: 1; }
.gp-content .faq-item > div { padding: 14px 20px 18px 56px; border-top: 1px solid #29292b; background: transparent; }
.gp-content .faq-item > div p { margin: 0; color: #B2B2B2; line-height: 1.55; font-size: 0.94em; }

/* --- Gövde madde listesi --- */
.gp-content .gp-list { margin: 14px 0 18px; padding: 0; list-style: none; color: #B2B2B2; }
.gp-content .gp-list li { display: flex; gap: 11px; margin: 8px 0; align-items: flex-start;
  line-height: 1.6; list-style: none; }
.gp-content .gp-list-dot { flex-shrink: 0; margin-top: 10px; width: 6px; height: 6px; border-radius: 50%;
  background: var(--gp-dot,#FFC900); }
.gp-content .gp-list-check { flex-shrink: 0; margin-top: 2px; }
/* FAQ + indicator */
.gp-content .faq-item .faq-icon { transition: transform 0.25s ease, color 0.2s; }
/* transform !important ZORUNLU: .faq-icon üzerinde gp-pulse-plus animasyonu çalışıyor ve
   CSS animasyonları normal bildirimleri ezer; !important olmadan [open] dönüşü uygulanmaz. */
.gp-content .faq-item[open] .faq-icon { transform: rotate(45deg) !important; color: #FFC900; }
.gp-content .faq-item summary:hover .faq-icon { color: #f59e0b; }
/* YouTube embed wrapper smaller + centered */
/* Mobile: card-table responsive */
@media (max-width: 700px) {
  .gp-content .gp-game-inline > aside { float: none; width: 100%; margin: 0 0 16px 0; }
  .gp-content .gp-yt-wrap { margin: 1em 0 !important; }
}

/* ===== v10 genel revizeler: embed 16:9, tablo alt kapatma, kupa ortala, FAQ sol, mobil responsive ===== */
/* ===== YouTube embed: 16:9 (kare değil), sola dayalı, küçük ===== */
.gp-content .gp-yt-wrap { max-width: 560px; margin: 1.5em 0 !important; }
.gp-content .gp-yt-wrap iframe { display: block; width: 100% !important; aspect-ratio: 16 / 9 !important; height: auto !important; border: 0; border-radius: 12px; box-shadow: 0 4px 14px rgba(0,0,0,0.5); }

/* ===== Tabloların altını kapat: tek temiz çerçeve, son satır ayracı ===== */
.gp-content .table-wrap.gp-layer::before, .gp-content .card-table.gp-layer::before { display: none; }
.gp-content .table-wrap { border: 1px solid #29292B; }
.gp-content .gp-card-table-inner { border: 1px solid #29292B; }
/* Gövde madde listeleri: nokta rengi Hızlı Özet bullet'ı ile aynı (#FFC900) */
.gp-content ul li::marker { color: #FFC900; }
.gp-content .table-wrap tbody tr { transition: background 0.15s ease; }

/* ===== Card-table başlığı (kupa + başlık) tam ortalı ===== */

/* ===== FAQ soruları biraz daha sola dayalı ===== */
.gp-content .faq-item summary { padding: 14px 16px; gap: 10px; }

/* ===== MOBİL (<=700px) ===== */
@media (max-width: 700px) {
  /* Uzun tür etiketi dar sütunda taşmasın */
  .gp-content .table-wrap .gp-genre { white-space: normal; }

  /* --- Card-table: TEK SATIR + rozet sütunu SABİT (oyun isimleri hizalı) --- */
  .gp-content .gp-card-table-inner .card-row {
    grid-template-columns: var(--gp-bw,96px) 1fr auto;
    grid-template-rows: auto;
    gap: 4px 9px; padding: 11px 12px; align-items: center;
  }
  .gp-content .gp-card-table-inner .card-row > .gp-badge {
    grid-row: 1; grid-column: 1;
    width: 100%; box-sizing: border-box;
    font-size: 0.55em; padding: 3px 5px; letter-spacing: 0.02em; text-align: center;
  }
  .gp-content .gp-card-table-inner .card-row > .gp-name {
    grid-row: 1; grid-column: 2; font-size: 0.8em; line-height: 1.28;
  }
  .gp-content .gp-card-table-inner .card-row > .gp-meta {
    grid-row: 1; grid-column: 3; text-align: right;
    font-size: 0.62em; padding-left: 0; white-space: normal;
    max-width: 112px; line-height: 1.35;
  }

  /* --- FAQ: soru ve cevap sola dayalı, okunur --- */
  .gp-content .faq-item summary { padding: 13px 13px; gap: 9px; font-size: 0.95em; }
  .gp-content .faq-item > div { padding: 12px 14px 15px 14px; }

  /* --- Hızlı Özet (TLDR): kompakt ve okunur --- */

  /* --- info-card: 2 sütun --- */}

/* ================= v10.3: onaylanan tipografi + responsive ince ayarlar ================= */
/* Yumuşak ToC kaydırma (saf CSS, JS yok) */

.gp-content h1, .gp-content h2, .gp-content h3, .gp-content h4 { scroll-margin-top: 28px; }
/* Başlık ölçekleri (boyut + line-height; renk CMS'ten gelir, atanmaz) */
.gp-content h1 { font-size: 40px; line-height: 48px; }
.gp-content h2 { font-size: 28px; line-height: 36px; }
.gp-content h3 { font-size: 24px; line-height: 32px; }
.gp-content h4 { font-size: 20px; line-height: 28px; }
/* Gövde paragrafı (inline-stilli callout/CTA p'leri etkilenmez) */
.gp-content p { font-size: 20px; line-height: 24px; }
@media (max-width: 700px) {
  .gp-content h1 { font-size: 30px; line-height: 1.15; }
  .gp-content h2 { font-size: 22px; line-height: 1.2; }
  .gp-content h3 { font-size: 19px; line-height: 1.25; }
  .gp-content h4 { font-size: 17px; line-height: 1.3; }
  .gp-content p { font-size: 16px; line-height: 24px; }
}
/* TLDR "Hızlı Özet": başlık ölçeği + sıkı iç boşluk */
@media (max-width: 700px) {}
/* info-card / gp-cell responsive: dar ekranda taşma yok + değer-etiket küçülür */
@media (max-width: 700px) {  .gp-content .gp-cell > div:last-child { font-size: 13px; line-height: 18px; }
}
@media (max-width: 400px) {  .gp-content .gp-cell > div:last-child { font-size: 12px; line-height: 16px; }
}
/* Tablolar mobilde: BAŞLIK SATIRI KALIR; hücreler dikey ortalı; içerik responsive; GFN-özel düzen 3 sütuna scoped */
@media (max-width: 700px) {
  .gp-content .table-wrap > div { overflow-x: visible; }
  .gp-content .table-wrap table { font-size: 12px; table-layout: fixed; width: 100%; }
  .gp-content .table-wrap thead { display: table-header-group; }
  .gp-content .table-wrap th, .gp-content .table-wrap td { padding: 10px 6px; vertical-align: middle; line-height: 1.35; overflow-wrap: normal; word-break: normal; hyphens: none; }
  .gp-content .table-wrap th { font-size: 13px; letter-spacing: 0.02em; text-align: center; padding: 12px 6px; }
  .gp-content .table-wrap td { text-align: left; }
  .gp-content .table-wrap td:first-child { color: #fff; }
  .gp-content .table-wrap td:first-child div { font-size: 10.5px; }
  .gp-content .table-wrap td .gp-genres { flex-wrap: wrap; gap: 5px 6px; justify-content: center; }
  .gp-content .table-wrap td .gp-genre { font-size: 10.5px; padding: 3px 7px; }
  .gp-content .table-wrap td svg { width: 11px; height: 11px; }
  /* 3 sütunlu GFN tablosu (Oyun / Tür / Platform-Çıkış): oyun adı büyük, tür ortalı, platform küçük + ok bitişik */
  .gp-content .table-wrap tr > :first-child:nth-last-child(3) { width: 40%; font-size: 14px; }
  .gp-content .table-wrap tr > :first-child:nth-last-child(3) ~ :nth-child(2) { width: 26%; text-align: center; }
  .gp-content .table-wrap tr > :first-child:nth-last-child(3) ~ :nth-child(3) { width: 34%; overflow-wrap: anywhere; font-size: 11px; }
  .gp-content .table-wrap tr > :first-child:nth-last-child(3) ~ :nth-child(3) a { white-space: nowrap; }
  .gp-content .table-wrap tr > :first-child:nth-last-child(3) ~ :nth-child(3) a svg { margin-left: 2px; }
}
@media (max-width: 400px) {
  .gp-content .table-wrap th { font-size: 12px; }
  .gp-content .table-wrap td .gp-genre { font-size: 10px; padding: 2px 6px; }
  .gp-content .table-wrap tr > :first-child:nth-last-child(3) { font-size: 13px; }
  .gp-content .table-wrap tr > :first-child:nth-last-child(3) div { font-size: 10px; }
  .gp-content .table-wrap tr > :first-child:nth-last-child(3) ~ :nth-child(3) { font-size: 10px; }
}

/* ================= v10.4: kart arka planı şeffaf + not/info-card/CTA boyut + 4-sütun tablo ================= */
/* Kart arka planları ŞEFFAF: CMS/site zaten siyah; #161616/#0D0D0D kutu izini kaldırır.
   Parlayan kenar (conic) ve çerçeveler durduğu için kartlar yine ayrışır; not kutuları kendi tint'ini korur. */
.gp-content .tldr-block .gp-conic-inner, .gp-content .gp-cell, .gp-content .table-wrap, .gp-content .gp-table, .gp-content .card-table, .gp-content .gp-card-table-inner, .gp-content .gp-layer { background: transparent; }
/* Not kutuları (Editör Notu / Hatırlatma): gövdeyle tutarlı 18 / mobil 17 */
/* Info-card değer: desktop 22 (mobil skil değeri 19/17 korunur) */
/* Mobil 4-sütunlu GFN tablosu (Oyun / Tür / Stüdyo / Platform-Çıkış): oyun adı-stüdyo-platform aynı punto (12) */
@media (max-width: 700px) {
  .gp-content .table-wrap tr > :first-child:nth-last-child(4) { width: 30%; }
  .gp-content .table-wrap tr > :first-child:nth-last-child(4) div { font-size: 12px; font-weight: 600; }
  .gp-content .table-wrap tr > :first-child:nth-last-child(4) ~ :nth-child(2) { width: 20%; text-align: center; }
  .gp-content .table-wrap tr > :first-child:nth-last-child(4) ~ :nth-child(3) { width: 24%; font-size: 12px; }
  .gp-content .table-wrap tr > :first-child:nth-last-child(4) ~ :nth-child(4) { width: 26%; font-size: 12px; overflow-wrap: anywhere; }
  .gp-content .table-wrap tr > :first-child:nth-last-child(4) ~ :nth-child(4) a { white-space: nowrap; }
  .gp-content .table-wrap tr > :first-child:nth-last-child(4) ~ :nth-child(4) a svg { margin-left: 2px; }
}

/* ================= v10.5: floating ToC kuralları ANA blokta (CLS düzeltmesi) =================
   ÖNEMLİ: Bu kurallar eskiden ToC elemanından SONRAKİ ayrı bir stil bloğundaydı. Mobilde
   (max-width:900px) konum top:120px -> bottom:16px değiştiği için tarayıcı elemanı önce üstte
   boyayıp sonra aşağı taşıyordu = ~0.125 CLS. Kurallar artık eleman parse edilmeden ÖNCE
   uygulandığından ilk boyama doğru konumda oluyor (kayma 0). Konum/boyut inline YAZILMAZ. */
.gp-content .floating-toc { position: fixed; top: 120px; right: 16px; z-index: 100; max-width: 320px;
  background: #161616; border: 1px solid #29292B; border-radius: 16px; box-shadow: 0 8px 28px rgba(0,0,0,0.6); }
.gp-content .floating-toc > summary { display: flex; align-items: center; padding: 16px 20px; color: #fff; cursor: pointer;
  font-family: 'New Science', GreycliffCF, -apple-system, sans-serif; font-weight: 600;
  font-size: 20px; line-height: 28px; list-style: none; user-select: none; }
.gp-content .floating-toc > ul { margin: 0; padding: 0 20px 16px; max-height: 60vh; overflow-y: auto; list-style: none; }
.gp-content .floating-toc summary::-webkit-details-marker { display: none; }
.gp-content .floating-toc summary::marker { display: none; }
.gp-content .floating-toc ul li a:hover { color: #FFC900; }
.gp-content .gp-toptop:hover { background: rgba(255,201,0,0.15); }
/* --- İçindekiler maddeleri --- */
.gp-content .floating-toc ul li { display: flex; gap: 10px; margin: 12px 0; list-style: none; }
.gp-content .floating-toc ul li a { color: #B2B2B2; text-decoration: none; font-size: 16px; line-height: 24px; }
.gp-content .gp-toc-num { color: #FFC900; font-size: 12px; line-height: 16px; font-weight: 700;
  flex-shrink: 0; margin-top: 4px; }
.gp-content .gp-toc-gap { width: 16px; flex-shrink: 0; }
.gp-content .gp-toptop { margin-left: 12px; display: inline-flex; align-items: center; justify-content: center;
  width: 26px; height: 26px; border-radius: 50%; border: 1.5px solid #FFC900; flex-shrink: 0;
  cursor: pointer; line-height: 0; vertical-align: middle; }
.gp-content .gp-toptop svg { display: block; width: 14px; height: 14px; }
@media (max-width: 900px) {
  .gp-content .floating-toc { top: auto; bottom: 16px; max-width: 240px; }
}
@media (max-width: 700px) {
  .gp-content .floating-toc > summary { font-size: 16px; line-height: 22px; padding: 13px 16px; }
  .gp-content .floating-toc > ul { padding: 0 16px 13px; }
  .gp-content .floating-toc ul li a { font-size: 13px; line-height: 19px; }
  .gp-content .floating-toc ul li span:not(.gp-toptop) { font-size: 10px; }
  .gp-content .gp-toptop { width: 21px; height: 21px; margin-left: 10px; }
  .gp-content .gp-toptop svg { width: 12px; height: 12px; }
}

/* ================= v10.7 - Geçiş 1: TLDR / info-card / not kutuları =================
   Inline stiller kaldırıldı; kurallar burada. .gp-content öneki specificity'yi (0,2,x)
   yaptığı için GEREKMİYOR. Dinamik kalan tek şey: --gp-glow (conic rengi). */

/* --- TLDR "Hızlı Özet" --- */
.gp-content .tldr-block { margin: 20px 0; }
.gp-content .tldr-block .gp-conic-inner { border-radius: 10.5px; padding: 15px 18px; }
.gp-content .gp-tldr-title { font-family: 'New Science', GreycliffCF, -apple-system, sans-serif;
  font-size: 22px; line-height: 29px; font-weight: 600; color: #fff; margin: 0 0 8px;
  display: flex; align-items: center; flex-wrap: wrap; }
.gp-content .gp-tldr-icon { color: #FFC900; display: inline-flex; }
.gp-content .gp-tldr-rt { display: inline-flex; align-items: center; gap: 8px; margin-left: 20px;
  font-family: GreycliffCF, -apple-system, sans-serif; font-size: 14px; line-height: 20px;
  font-weight: 500; color: #B2B2B2; }
.gp-content .gp-tldr-rt-dot { width: 4px; height: 4px; border-radius: 50%; background: #B2B2B2; flex-shrink: 0; }
.gp-content .tldr-block ul { margin: 0; padding: 0; list-style: none; }
.gp-content .tldr-block ul li { display: flex; gap: 10px; margin: 0 0 8px; list-style: none; align-items: flex-start; }
.gp-content .tldr-block ul li:last-child { margin-bottom: 0; }
.gp-content .gp-tldr-bullet { color: #FFC900; font-weight: 700; font-size: 16px; line-height: 24px; flex-shrink: 0; }
.gp-content .gp-tldr-text { color: #B2B2B2; font-size: 18px; line-height: 27px; }
@media (max-width: 700px) {
  .gp-content .tldr-block { padding: 16px; }
  .gp-content .tldr-block ul li { gap: 9px; }
  .gp-content .gp-tldr-title { font-size: 18px; line-height: 24px; }
  .gp-content .gp-tldr-text { font-size: 16px; line-height: 24px; }
}

/* --- info-card / stat hücreleri --- */
.gp-content .info-card { margin: 24px 0; display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; }
.gp-content .info-card.gp-check { display: block; background: #0D0D0D; border: 1px solid #29292B;
  border-radius: 12px; padding: 16px 22px; }
.gp-content .gp-check-row { display: flex; align-items: center; gap: 11px; margin: 8px 0; }
.gp-content .gp-check-row span { color: #e5e7eb; font-size: 16px; font-weight: 500; }
.gp-content .gp-cell { border: 1px solid #29292B; border-radius: 12px; padding: 20px; text-align: center; }
.gp-content .gp-cell-value { font-family: 'New Science', GreycliffCF, -apple-system, sans-serif;
  font-weight: 600; font-size: 22px; line-height: 29px; color: #FFC900; margin-bottom: 6px; overflow-wrap: break-word; }
.gp-content .gp-cell-label { color: #B2B2B2; font-size: 16px; line-height: 24px; font-weight: 500; }
@media (max-width: 700px) {
  .gp-content .info-card { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; }
  .gp-content .gp-cell { padding: 14px 10px; }
  .gp-content .gp-cell-value { font-size: 19px; line-height: 25px; }
  .gp-content .gp-cell-label { font-size: 13px; line-height: 18px; }
}
@media (max-width: 400px) {
  .gp-content .gp-cell-value { font-size: 17px; line-height: 23px; }
  .gp-content .gp-cell-label { font-size: 12px; line-height: 16px; }
}

/* --- Editör Notu / Hatırlatma --- */
.gp-content .editor-note, .gp-content .highlight-box { border-radius: 12px;
  padding: 18px 24px 18px 20px; margin: 24px 0; display: flex; gap: 16px; align-items: stretch; }
.gp-content .editor-note { background: rgba(255,201,0,0.06); }
.gp-content .highlight-box { background: rgba(255,255,255,0.04); }
.gp-content .gp-note-bar { width: 4px; border-radius: 2px; background: #FFC900; flex-shrink: 0; }
.gp-content .gp-note-eyebrow { color: #FFC900; font-size: 12px; line-height: 16px; font-weight: 700;
  letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 6px; display: flex; align-items: center; }
.gp-content .editor-note p, .gp-content .highlight-box p { margin: 0; color: #fff; font-size: 18px; line-height: 27px; }
@media (max-width: 700px) {
  .gp-content .editor-note p, .gp-content .highlight-box p { font-size: 17px; line-height: 26px; }
}

/* ================= v10.7 - Geçiş 2: CTA blokları =================
   4 CTA tipi (paketler / oyunlar / end / compact) inline stilden sınıfa taşındı.
   .gp-content öneki specificity'yi yükselttiği için !important gerekmiyor. */
.gp-content .cta-paketler, .gp-content .cta-oyunlar, .gp-content .cta-compact { margin: 32px 0; }
.gp-content .cta-end { margin: 40px 0 24px; }
.gp-content .cta-paketler .gp-conic-inner, .gp-content .cta-oyunlar .gp-conic-inner,
.gp-content .cta-end .gp-conic-inner, .gp-content .cta-compact .gp-conic-inner {
  border-radius: 10.5px; padding: 20px; background: transparent; }

.gp-content .gp-cta-eyebrow { display: flex; align-items: center; gap: 8px; margin-bottom: 16px; }
.gp-content .cta-end .gp-cta-eyebrow { margin-bottom: 24px; }
.gp-content .gp-cta-eyebrow span { color: #FFC900; font-size: 11px; line-height: 16px; font-weight: 700;
  letter-spacing: 0.08em; display: inline-flex; align-items: center; }

.gp-content .gp-cta-title { font-family: 'New Science', GreycliffCF, -apple-system, sans-serif;
  font-weight: 600; font-size: 22px; line-height: 28px; color: #fff; margin-bottom: 8px; }
.gp-content .cta-end .gp-cta-title { font-size: 24px; line-height: 30px; }

.gp-content .gp-cta-desc { color: #B2B2B2; font-size: 16px; line-height: 20px; margin: 0 0 20px; max-width: 760px; }
.gp-content .cta-end .gp-cta-desc { margin-bottom: 24px; }

.gp-content .gp-cta-actions { display: flex; flex-wrap: wrap; gap: 14px; }

.gp-content .gp-btn { display: inline-flex; align-items: center; justify-content: center;
  padding: 12px 16px; border-radius: 8px; font-weight: 700; font-size: 16px; line-height: 20px;
  text-decoration: none; white-space: normal; text-wrap: balance; box-sizing: border-box; }
.gp-content .gp-btn-solid { background: #FFC900; color: #131313; }
.gp-content .gp-btn-outline { background: transparent; border: 1px solid #FFC900; color: #FFC900; }
.gp-content a.gp-btn-solid:hover { color: #131313; }
.gp-content a.gp-btn-outline:hover { color: #FFC900; }

/* compact CTA (öne çıkan oyun) */
.gp-content .cta-compact .gp-conic-inner { display: flex; align-items: center;
  justify-content: space-between; gap: 24px; flex-wrap: wrap; }
.gp-content .gp-cta-compact-main { flex: 1; min-width: 260px; }
.gp-content .gp-cta-compact-tagline { color: #B2B2B2; font-size: 16px; line-height: 20px; }
.gp-content .gp-btn-lg { padding: 14px 24px; font-weight: 600; }

@media (max-width: 700px) {
  .gp-content .cta-paketler .gp-conic-inner, .gp-content .cta-oyunlar .gp-conic-inner,
  .gp-content .cta-end .gp-conic-inner, .gp-content .cta-compact .gp-conic-inner { padding: 14px; }
  .gp-content .gp-cta-eyebrow, .gp-content .cta-end .gp-cta-eyebrow { margin-bottom: 8px; }
  .gp-content .gp-cta-title { font-size: 19px; line-height: 25px; margin-bottom: 4px; }
  .gp-content .cta-end .gp-cta-title { font-size: 20px; line-height: 26px; }
  .gp-content .gp-cta-desc, .gp-content .cta-end .gp-cta-desc { margin-bottom: 12px; }
  .gp-content .gp-btn { padding-top: 9px; padding-bottom: 9px; }
  .gp-content .cta-paketler .gp-btn, .gp-content .cta-oyunlar .gp-btn { flex: 1 1 100%; }
  /* End CTA: iki buton mobilde YAN YANA (alt alta 2 satır yerine tek sıra) */
  .gp-content .gp-cta-actions { gap: 8px; flex-wrap: nowrap; }
  .gp-content .gp-cta-actions .gp-btn { flex: 1 1 0; min-width: 0;
    padding-left: 8px; padding-right: 8px; font-size: 12.5px; line-height: 1.2; text-align: center; }
}



/* ================= v10.6: renkler içerikte (site CSS'inden bağımsız) =================
   Frontend notu: site tipografi/renk kuralları gövdeden çekildi. İçerik artık kendi rengini
   kendi taşır. a:hover AYRI yazılır: global.scss'teki `a:hover{color:inherit}` (0,1,1) bizim
   (0,0,1) kuralımızı yenerdi; .gp-content a:hover (0,2,1) ile eşitlenip sıra avantajı alınır.
   Inline stilli öğeler (CTA butonları, tablo/ToC linkleri) inline rengini korur. */
.gp-content { color: #B2B2B2; font-family: GreycliffCF, -apple-system, 'system-ui', 'Segoe UI', Roboto, sans-serif;
  font-size: 20px; line-height: 24px; }
@media (max-width: 700px) { .gp-content { font-size: 16px; line-height: 24px; } }
.gp-content strong { font-weight: 700; }
.gp-content p { color: #B2B2B2; }
.gp-content h1, .gp-content h2, .gp-content h3, .gp-content h4 { color: #fff;
  /* ÖNEMLİ: font-family eskiden yalnız önizleme <head>'indeydi; CMS'e gitmediği için canlıda
     başlıklar New Science'ı hiç istemiyordu. Artık gövde CSS'i istiyor (frontend alias'ı ekledi). */
  font-family: 'New Science', GreycliffCF, -apple-system, sans-serif; font-weight: 600; }
.gp-content a { color: #FFC900; text-decoration: none; }
.gp-content a:hover { color: #ffd94d; text-decoration: none; }


/* ================= v10.8 - Marka Font Kullanım Rehberi (Blog Detay) =================
   Kaynak: markadan gelen "Font Kullanım Rehberi" (masaüstü + mobil 360px).
   2 font ailesi: New Science (başlıklar) + GreycliffCF (gövde).
   Bu blok EN SONDA durur; önceki tüm kuralları bilinçli olarak ezer. */

/* --- MASAÜSTÜ --- */
.gp-content { font-size: 16px; line-height: 24px; }
.gp-content p { font-size: 16px; line-height: 24px; color: #B2B2B2; }
.gp-content h1 { font-size: 40px; line-height: 48px; color: #fff; }
.gp-content h2 { font-size: 32px; line-height: 40px; color: #fff; }
.gp-content h3 { font-size: 28px; line-height: 36px; color: #fff; }
.gp-content h4 { font-size: 24px; line-height: 32px; color: #fff; }

/* Kart/kutu başlıkları = H4 rolü (Hızlı Özet, İçindekiler, card-table) */
.gp-content .gp-tldr-title,
.gp-content .floating-toc > summary { font-size: 24px; line-height: 32px; color: #fff; }
.gp-content .gp-ct-title { font-size: 32px; line-height: 40px; }
/* CTA başlıkları = H2 rolü (rehber: "Kapak başlığı, CTA ve İlgili Yazılar") */
.gp-content .gp-cta-title, .gp-content .cta-end .gp-cta-title { font-size: 32px; line-height: 40px; }

/* İstatistik sayısı = H3 rolü (New Science, sarı) */
.gp-content .gp-cell-value { font-size: 28px; line-height: 36px; color: #FFC900; }
.gp-content .gp-cell-label { font-size: 16px; line-height: 24px; font-weight: 500; color: #B2B2B2; }

/* Gövde paragraf ailesi (16/24) */
.gp-content .gp-tldr-text { font-size: 16px; line-height: 24px; color: #B2B2B2; }
.gp-content .gp-tldr-bullet { font-size: 16px; line-height: 24px; font-weight: 700; color: #FFC900; }
.gp-content .gp-list li { font-size: 16px; line-height: 24px; }

/* Infobox açıklama metni (Editör Notu / Hatırlatma) = 20/32 beyaz */
.gp-content .editor-note p, .gp-content .highlight-box p { font-size: 16px; line-height: 22px; color: #fff; }

/* Gövde 16/20 ailesi: tablo, CTA metni, butonlar */
.gp-content .table-wrap th { font-size: 16px; line-height: 20px; font-weight: 700; color: #FFC900; }
.gp-content .table-wrap td { font-size: 16px; line-height: 20px; color: #B2B2B2; }
.gp-content .gp-tg-link, .gp-content .table-wrap td:first-child { font-size: 16px; line-height: 20px;
  font-weight: 400; color: #fff; }
.gp-content .gp-cta-desc, .gp-content .gp-cta-compact-tagline { font-size: 16px; line-height: 20px; }
.gp-content .gp-btn { font-size: 16px; line-height: 20px; font-weight: 700; }
.gp-content .gp-pw-more { font-size: 16px; line-height: 20px; font-weight: 600; color: #FFC900; }

/* İlgili yazı kartı başlığı = GreycliffCF Bold 20/24 beyaz */
.gp-content .gp-pw-title { font-size: 20px; line-height: 24px; font-weight: 700; color: #fff; }

/* Küçük metin (12/16): eyebrow, meta, ToC numarası, tür etiketi, tarih, ToC madde metni */
.gp-content .gp-cta-eyebrow span, .gp-content .gp-note-eyebrow, .gp-content .gp-pw-tag
  { font-size: 12px; line-height: 16px; font-weight: 700; color: #FFC900; }
/* İçindekiler masaüstünde daha okunur: madde metni ve numarası 16/20 */
.gp-content .gp-toc-num { font-size: 16px; line-height: 20px; font-weight: 700; color: #FFC900; }
.gp-content .gp-genre, .gp-content .gp-badge, .gp-content .gp-game-badge {
  font-size: 12px; line-height: 16px; font-weight: 700; }
.gp-content .gp-pw-date, .gp-content .gp-tldr-rt { font-size: 12px; line-height: 16px;
  font-weight: 500; color: #B2B2B2; }
.gp-content .floating-toc ul li a { font-size: 16px; line-height: 20px; font-weight: 400; color: #B2B2B2; }
.gp-content .gp-tg-meta, .gp-content .gp-meta, .gp-content .gp-game-meta {
  font-size: 12px; line-height: 16px; color: #B2B2B2; }
.gp-content .gp-name { font-size: 16px; line-height: 20px; font-weight: 600; color: #fff; }

/* Satır hover: arka plan sarı tint + oyun adı sarı (oyun adı <a> içinde olduğu için link de hedeflenir) */
/* Satır vurgusu (hover + seçili): arka plan ve oyun adı BİRLİKTE sarıya döner - marka tasarım görseli.
   Tipografi bloklarından SONRA durmalı; yoksa .gp-tg-link beyaz kuralı rengi geri alır. */
.gp-content .table-wrap tbody tr:hover > td { background: rgba(255,201,0,0.12); }
.gp-content .table-wrap tbody tr:hover > td:first-child,
.gp-content .table-wrap tbody tr:hover > td:first-child .gp-tg-link { color: #FFC900; }
.gp-content .table-wrap tr.gp-row-feat > td { background: rgba(255,201,0,0.12); }
.gp-content .table-wrap tr.gp-row-feat > td:first-child,
.gp-content .table-wrap tr.gp-row-feat > td:first-child .gp-tg-link { color: #FFC900; }
.gp-content .gp-tg-link { transition: color 0.15s ease; }

/* --- MOBİL (360 px) --- */
@media (max-width: 700px) {
  /* Rehber: hero + TÜM bölüm ve kart başlıkları tek kademe: 24/32 */
  .gp-content h1, .gp-content h3, .gp-content h4,
  .gp-content .card-table-wrap h3 { font-size: 24px; line-height: 32px; }
  .gp-content h2 { font-size: 21px; line-height: 28px; }
  .gp-content .gp-ct-title { font-size: 21px; line-height: 28px; }
  .gp-content .floating-toc > summary { font-size: 20px; line-height: 26px; }
  /* Kullanıcı onaylı mobil ölçüler (rehberden ayrışan bilinçli değerler) */
  .gp-content .gp-tldr-title { font-size: 20px; line-height: 24px; }
  .gp-content .gp-cta-title, .gp-content .cta-end .gp-cta-title { font-size: 19px; line-height: 25px; }
  .gp-content .gp-cell-value { font-size: 17px; line-height: 23px; }
  .gp-content .gp-cell-label { font-size: 13px; line-height: 17px; }
  .gp-content p, .gp-content .gp-tldr-text, .gp-content .gp-list li { font-size: 16px; line-height: 24px; }
  .gp-content .editor-note p, .gp-content .highlight-box p { font-size: 15px; line-height: 22px; }
  .gp-content .table-wrap th, .gp-content .table-wrap td,
  .gp-content .gp-tg-link, .gp-content .table-wrap td:first-child,
  .gp-content .gp-cta-desc, .gp-content .gp-cta-compact-tagline,
  .gp-content .gp-btn, .gp-content .gp-pw-more, .gp-content .gp-name { font-size: 16px; line-height: 20px; }
  .gp-content .gp-pw-title { font-size: 20px; line-height: 24px; }
  .gp-content .gp-genre, .gp-content .gp-badge, .gp-content .gp-game-badge,
  .gp-content .gp-toc-num, .gp-content .gp-pw-date, .gp-content .gp-tldr-rt,
  .gp-content .floating-toc ul li a, .gp-content .gp-tg-meta, .gp-content .gp-meta,
  .gp-content .gp-game-meta { font-size: 12px; line-height: 16px; }
  /* Tablo dar ekranda SIKIŞTIRILMAZ: hücreler tek satırda kalır, tablo yana kaydırılır */
  .gp-content .table-wrap > div.gp-table-scroll { overflow-x: auto; -webkit-overflow-scrolling: touch;
    overscroll-behavior-x: contain; }
  .gp-content .table-wrap table { table-layout: auto; width: auto; min-width: 100%; }
  .gp-content .table-wrap th, .gp-content .table-wrap td { padding: 12px 14px; white-space: nowrap; }
  /* İlk sütun (Oyun) DAR ve SARABİLİR: uzun oyun adı alt satıra iner, böylece sağdaki
     Tür sütunu ekrana girer ve tablonun kaydırılabilir olduğu görülür. */
  .gp-content .table-wrap th:first-child:not(.gp-col-num),
  .gp-content .table-wrap td:first-child:not(.gp-col-num) {
    white-space: normal; width: 170px; min-width: 170px; max-width: 170px; overflow-wrap: break-word; }
  .gp-content .table-wrap th.gp-col-num, .gp-content .table-wrap td.gp-col-num {
    padding-left: 14px; padding-right: 14px; }
  .gp-content .table-wrap .gp-genres { flex-wrap: nowrap; }
  .gp-content .gp-table-hint { display: block; }
  .gp-content .table-wrap tr > :first-child:nth-last-child(3),
  .gp-content .table-wrap tr > :first-child:nth-last-child(3) ~ :nth-child(2),
  .gp-content .table-wrap tr > :first-child:nth-last-child(3) ~ :nth-child(3),
  .gp-content .table-wrap tr > :first-child:nth-last-child(4),
  .gp-content .table-wrap tr > :first-child:nth-last-child(4) ~ :nth-child(2),
  .gp-content .table-wrap tr > :first-child:nth-last-child(4) ~ :nth-child(3),
  .gp-content .table-wrap tr > :first-child:nth-last-child(4) ~ :nth-child(4) { width: auto; }
  /* Eski mobil punto kuralları rehberin ölçülerini eziyordu; sütun-bazlı seçicilerle eşitleniyor */
  .gp-content .table-wrap tr > :first-child:nth-last-child(3),
  .gp-content .table-wrap tr > :first-child:nth-last-child(3) ~ :nth-child(2),
  .gp-content .table-wrap tr > :first-child:nth-last-child(3) ~ :nth-child(3),
  .gp-content .table-wrap tr > :first-child:nth-last-child(4),
  .gp-content .table-wrap tr > :first-child:nth-last-child(4) ~ :nth-child(2),
  .gp-content .table-wrap tr > :first-child:nth-last-child(4) ~ :nth-child(3),
  .gp-content .table-wrap tr > :first-child:nth-last-child(4) ~ :nth-child(4) {
    font-size: 16px; line-height: 20px; }
  .gp-content .table-wrap td:first-child div,
  .gp-content .table-wrap tr > :first-child:nth-last-child(3) div,
  .gp-content .table-wrap tr > :first-child:nth-last-child(4) div { font-size: 12px; line-height: 16px; }
  .gp-content .table-wrap td .gp-genre { font-size: 12px !important; line-height: 16px !important;
    padding: 4px 10px !important; }
  .gp-content .floating-toc ul li span:not(.gp-toptop) { font-size: 12px; line-height: 16px; }
  .gp-content .gp-cell > div:last-child { font-size: 13px; line-height: 17px; }
  .gp-content .gp-cell > div:first-child { font-size: 17px; line-height: 23px; }
}
@media (max-width: 400px) {
  /* <=400 kademesi rehberde ayrı tanımlı değil; 360 px referans alındığı için mobil ölçüler korunur */
  .gp-content .table-wrap th, .gp-content .table-wrap td,
  .gp-content .table-wrap tr > :first-child:nth-last-child(3),
  .gp-content .table-wrap tr > :first-child:nth-last-child(3) ~ :nth-child(3),
  .gp-content .table-wrap tr > :first-child:nth-last-child(4) { font-size: 16px; line-height: 20px; }
  .gp-content .table-wrap tr > :first-child:nth-last-child(3) div,
  .gp-content .table-wrap tr > :first-child:nth-last-child(4) div { font-size: 12px; line-height: 16px; }
  .gp-content .table-wrap td .gp-genre { font-size: 12px !important; padding: 4px 10px !important; }
  .gp-content .gp-cell > div:last-child { font-size: 13px; line-height: 17px; }
  .gp-content .gp-cell > div:first-child { font-size: 17px; line-height: 23px; }
}
</style>
'''

# --- Sparkle (4 uçlu yıldız) — CTA eyebrow'larında ★ yerine kullanılır ---
SVG_SPARKLE = ('<svg width="14" height="14" viewBox="0 0 24 24" fill="#FFC900" style="flex-shrink:0;'
               'margin-right:6px;vertical-align:-2px;"><path d="M12 1.5c.3 4.6 2.4 7.4 6.9 8.2'
               '.7.1.7 1.1 0 1.2-4.5.8-6.6 3.6-6.9 8.2 0 .8-1.1.8-1.2 0-.3-4.6-2.4-7.4-6.9-8.2'
               '-.7-.1-.7-1.1 0-1.2 4.5-.8 6.6-3.6 6.9-8.2.1-.8 1.2-.8 1.2 0z"/></svg>')

# --- Okuma süresi (TLDR başlığında gösterilir) ---
def estimate_reading_time(html, wpm=200):
    """Gövde HTML'inden dakika cinsinden okuma süresi. Enrichment blokları da dahil edilebilir;
    farkı 1 dk'yı geçmez. wpm=200 Türkçe için makul bir ortalamadır."""
    import re as _re
    text = _re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', html, flags=_re.S | _re.I)
    text = _re.sub(r'<[^>]+>', ' ', text)
    words = len([w for w in text.split() if any(ch.isalnum() for ch in w)])
    return max(1, round(words / wpm))

# --- TLDR "Hızlı Özet" (Figma: #161616 kart + 1px gradient kenarlık #FFC516->#545454, sarı bullet) ---
def render_tldr(items, reading_time=None):
    """items: 3-6 madde. reading_time: dakika (int) — verilirse başlığın sağında "N dk okuma" çıkar.
    Stiller .gp-content sınıflarında (v10.7); burada inline stil YOK (dinamik --gp-glow hariç)."""
    rt_html = ""
    if reading_time:
        rt_html = (f'<span class="gp-tldr-rt"><span class="gp-tldr-rt-dot"></span>'
                   f'{reading_time} dk okuma</span>')
    items_html = "\n".join(
        f'    <li><span class="gp-tldr-bullet">&bull;</span>'
        f'<span class="gp-tldr-text">{x}</span></li>'
        for x in items
    )
    return f'''<div class="tldr-block gp-conic" style="--gp-glow:#FFC900;">
<div class="gp-conic-inner">
  <div class="gp-tldr-title"><span class="gp-tldr-icon">{SVG_DOC}</span>Hızlı Özet{rt_html}</div>
  <ul>
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
    Stiller .gp-content sınıflarında (v10.7); dinamik kalan tek şey nokta rengi (--gp-dot)."""
    lis = []
    for x in items:
        if marker == "check":
            m = f'<span class="gp-list-check">{SVG_CHECK_GREEN}</span>'
        else:
            m = '<span class="gp-list-dot"></span>'
        lis.append(f'<li>{m}<span>{x}</span></li>')
    style = f' style="--gp-dot:{accent};"' if marker != "check" and accent != "#FFC900" else ''
    return (f'<ul class="gp-list"{style}>\n' + "\n".join(lis) + "\n</ul>")

# --- Info Strip / Stat kartları (Figma: #0D0D0D kart + #29292B kenarlık; DEĞER üstte New Science 28 sarı, etiket altta gri 16) ---
def render_info_card(badges, style="grid"):
    """badges: [(label, value), ...] — DEĞER üstte büyük sarı, etiket altta.
    Değer sayı olmak ZORUNDA DEĞİL; kısa tut (<=22 karakter) ve yazının İÇİNDEN gelsin.
    Stiller .gp-content sınıflarında (v10.7)."""
    if style == "checkmark":
        items = [f'<div class="gp-check-row">{SVG_CHECK_GREEN}<span>{v}</span></div>' for v in badges]
        return f'''<div class="info-card gp-check">
{chr(10).join(items)}
</div>
'''
    items = []
    for label, value in badges:
        items.append(f'''  <div class="gp-cell">
    <div class="gp-cell-value">{value}</div>
    <div class="gp-cell-label">{label}</div>
  </div>''')
    return f'''<div class="info-card">
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
    return f'''<div class="editor-note">
  <div class="gp-note-bar"></div>
  <div>
    <div class="gp-note-eyebrow">{SVG_DOC}{title}</div>
    <p>{text}</p>
  </div>
</div>
'''

# --- Hatırlatma (Figma: rgba(255,255,255,0.04) zemin + 4px sarı sol bar + sarı eyebrow; gövde beyaz 20/32) ---
def render_highlight(text, title="Hatırlatma"):
    return f'''<div class="highlight-box">
  <div class="gp-note-bar"></div>
  <div>
    <div class="gp-note-eyebrow">{SVG_BULB}{title}</div>
    <p>{text}</p>
  </div>
</div>
'''

# --- CTA Paketler (Figma CTA kart dili: #161616, ★ eyebrow, dolu sarı buton; GA4 id=packages-button) ---
def render_cta_paketler(headline, desc):
    return f'''<div class="cta-paketler gp-conic" style="--gp-glow:#FFC900;">
<div class="gp-conic-inner">
  <div class="gp-cta-eyebrow"><span>{SVG_SPARKLE}GAME+ &bull; BULUT OYUN</span></div>
  <div class="gp-cta-title">{headline}</div>
  <p class="gp-cta-desc">{desc}</p>
  <a class="gp-btn gp-btn-solid" id="packages-button" href="https://gameplus.com.tr/gfn/paketler">GeForce NOW Paketleri &rarr;</a>
</div>
</div>
'''

# --- CTA Oyunlar (kontur sarı buton; GA4 id=games-button) ---
def render_cta_oyunlar(headline, desc):
    return f'''<div class="cta-oyunlar gp-conic" style="--gp-glow:#FFC900;">
<div class="gp-conic-inner">
  <div class="gp-cta-eyebrow"><span>{SVG_SPARKLE}GAME+ &bull; OYUN KÜTÜPHANESİ</span></div>
  <div class="gp-cta-title">{headline}</div>
  <p class="gp-cta-desc">{desc}</p>
  <a class="gp-btn gp-btn-outline" id="games-button" href="https://gameplus.com.tr/gfn/oyunlar">GeForce NOW Oyunları &rarr;</a>
</div>
</div>
'''

# --- End CTA (Figma "CTA - Bulutta Oyun Keyfi": #161616 kart, ★ eyebrow, New Science 32 başlık,
#     dolu sarı + kontur sarı buton; GA4 id=end-packages-button / end-games-button) ---
def render_end_cta(headline, desc, btn2_label="Güncel Fırsatlar", btn2_url="https://gameplus.com.tr/firsatlar", chip2=None, eyebrow="GAME+ &bull; BULUT OYUN"):
    return f'''<div class="cta-end gp-conic" style="--gp-glow:#FFC900;">
<div class="gp-conic-inner">
  <div class="gp-cta-eyebrow"><span>{SVG_SPARKLE}{eyebrow}</span></div>
  <div class="gp-cta-title">{headline}</div>
  <p class="gp-cta-desc">{desc}</p>
  <div class="gp-cta-actions">
    <a class="gp-btn gp-btn-solid" id="end-packages-button" href="https://gameplus.com.tr/gfn/paketler">GeForce NOW Paketleri &rarr;</a>
    <a class="gp-btn gp-btn-outline" id="end-games-button" href="{btn2_url}">{btn2_label}</a>
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
    """İlk sütun KISA ise (sıra numarası, '#', yıl gibi <=4 karakter) otomatik olarak
    `gp-col-num` sınıfını alır: içeriği kadar yer kaplar, iki yanında eşit boşluk kalır.
    Oyun adı gibi geniş ilk sütunlar etkilenmez."""
    def _duz(x):
        return re.sub(r'<[^>]+>', '', str(x)).strip()
    ilk_dar = bool(rows) and all(len(_duz(r[0])) <= 4 for r in rows if r)
    kolon_cls = ' class="gp-col-num"' if ilk_dar else ''
    sar_cls = "table-wrap gp-table gp-table-rank" if ilk_dar else "table-wrap gp-table"
    th = "".join(f'<th{kolon_cls if j == 0 else ""}>{h}</th>' for j, h in enumerate(headers))
    feat = set(featured or [])
    body_rows = []
    for i, row in enumerate(rows):
        cls = ' class="gp-row-feat"' if i in feat else ''
        tds = "".join(f'<td{kolon_cls if j == 0 else ""}>{c}</td>' for j, c in enumerate(row))
        body_rows.append(f'<tr{cls}>{tds}</tr>')
    return f'''<div class="{sar_cls}">
  <div class="gp-table-hint">Tabloyu yana kaydır &rarr;</div>
  <div class="gp-table-scroll">
    <table>
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
    GENRE_BADGE_COLORS paletinden gelir - aynı tür her içerikte AYNI renk. Sentence case yaz."""
    spans = []
    for g in genres:
        c = badge_color_for(g)
        spans.append(f'<span class="gp-genre" style="background:{hex_to_rgba(c,0.16)};color:{c};">{g}</span>')
    return '<span class="gp-genres">' + ''.join(spans) + '</span>'

# --- Oyun açıklamalarını başlık + video altına taşı (sıralama zaten tabloda) ---
def move_game_descriptions(html, game_names):
    """Sıralamayı TABLO olarak verdiğimiz yazılarda ("Çıkış Sırası", "Oynama Sırası"),
    gövdede "Oyun Adı: açıklama" biçiminde duran paragrafları ilgili oyunun
    BAŞLIĞI + FRAGMANI altına taşır ve baştaki "Oyun Adı:" önekini kaldırır.

    Neden: sıra tabloda verildiği için aynı bilgi iki kez okunuyor; açıklama, oyunun
    kendi bölümünde videodan hemen sonra daha yararlı.

    DİKKAT - eşleşme sırası: adlar UZUNDAN KISAYA denenir ve eşleşen paragraf
    "sahiplenilir". Yoksa "Halo 3", "Halo 3: ODST: ..." paragrafını kapar
    (ikisi de "Halo 3:" ile başlıyor). Başlık eşleşmesi de TAM ad üzerinden yapılır.
    Karşılığı olmayan paragraf yerinde bırakılır (ör. bölümü olmayan bir oyun).

    Döndürür: (yeni_html, tasinanlar) - tasinanlar {oyun: onek_kaldirilmis_metin}."""
    adlar = sorted(set(game_names), key=len, reverse=True)
    paragraflar = [(mm.start(), mm.end(), mm.group(1)) for mm in re.finditer(r'<p>(.*?)</p>', html, re.S)]
    sahiplenen = set()
    tasinan, kaldirilacak = {}, []

    for ad in adlar:
        for idx, (a, b, ic) in enumerate(paragraflar):
            if idx in sahiplenen:
                continue
            duz = re.sub(r'<[^>]+>', '', ic).strip()
            if not duz.startswith(ad + ':'):
                continue
            sahiplenen.add(idx)
            onek = r'^\s*(<(?:strong|b)>)?\s*' + re.escape(ad) + r'\s*:\s*(</(?:strong|b)>)?\s*'
            yeni = re.sub(onek, '', ic, count=1).strip()
            if yeni:
                yeni = yeni[0].upper() + yeni[1:]
            tasinan[ad] = yeni
            kaldirilacak.append((a, b))
            break

    for a, b in sorted(kaldirilacak, reverse=True):
        html = html[:a] + html[b:]

    for ad, metin in tasinan.items():
        basdes = (r'<(h[1-6])\b[^>]*class="gp-game-head"[^>]*>.*?'
                  r'<span class="gp-game-name">\s*' + re.escape(ad) + r'\s*</span>.*?</\1>')
        bas = re.search(basdes, html, re.S)
        if not bas:
            continue
        son = bas.end()
        yt = re.match(r'\s*<div class="gp-yt-wrap".*?</div>', html[son:son + 1500], re.S)
        if yt:
            son += yt.end()
        html = html[:son] + '\n<p>' + metin + '</p>' + html[son:]
    return html, tasinan


# --- Tablo oyun hücresi: isim (+link) + altında "Stüdyo · Yıl" (kural 11 ile tutarlı) ---
def render_game_cell(name, meta=None, href=None):
    # GFN tablosu c0 hücresi: name beyaz DemiBold (satır stili tabloda); meta = 'Stüdyo · Yıl' 12px gri alt satır.
    nm = (f'<a class="gp-tg-link" href="{href}" target="_blank" rel="noopener noreferrer">'
          f'{name}</a>') if href else name
    sub = f'<div class="gp-tg-meta">{meta}</div>' if meta else ''
    return f'<div>{nm}{sub}</div>'

# --- Öne Çıkan Oyun (Figma: #161616 + 1.5px rgba(255,201,0,0.5) çerçeve, ★ ÖNE ÇIKAN OYUN eyebrow,
#     New Science 24 isim, sağda dolu sarı buton; GA4 id=featured-game-button) ---
def render_compact_cta(game_name, tagline, button_label, button_url, cta_id="featured-game-button"):
    gamepad = ('<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#FFC900" stroke-width="2" '
               'stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0;margin-right:8px;">'
               '<line x1="6" y1="11" x2="10" y2="11"/><line x1="8" y1="9" x2="8" y2="13"/>'
               '<line x1="15" y1="12" x2="15.01" y2="12"/><line x1="18" y1="10" x2="18.01" y2="10"/>'
               '<rect x="2" y="6" width="20" height="12" rx="6"/></svg>')
    return f'''<div class="cta-compact gp-conic" style="--gp-glow:#FFC900;">
<div class="gp-conic-inner">
  <div class="gp-cta-compact-main">
    <div class="gp-cta-eyebrow"><span>{gamepad}ÖNE ÇIKAN OYUN</span></div>
    <div class="gp-cta-title">{game_name}</div>
    <div class="gp-cta-compact-tagline">{tagline}</div>
  </div>
  <a class="gp-btn gp-btn-solid gp-btn-lg" id="{cta_id}" href="{button_url}">{button_label}</a>
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
def render_card_table(title, games, headers=("Oyun", "Tür", "Stüdyo · Yıl")):
    """"En İyi N ..." / "Çıkış Sırası" listesi. v10.9'dan beri GFN oyun tablosuyla AYNI yapı:
    gerçek <table> + <thead> + `.table-wrap` sarmalayıcı. Böylece başlık satırı, satır hover
    vurgusu, yana kaydırma ve tipografi tek yerden (tablo kuralları) geliyor.
    games: [{name, badge, badge_color, meta, anchor (opsiyonel), badge_href (opsiyonel)}]
    Oyun adı `anchor` verilirse yazı içindeki bölüme bağlanır."""
    rows = []
    for g in games:
        color = badge_color_for(g.get("badge"), g.get("badge_color"))
        badge_html = ''
        if g.get('badge'):
            badge_html = (f'<span class="gp-genre" style="background:{hex_to_rgba(color,0.16)};'
                          f'color:{_badge_text(color)};">{g["badge"]}</span>')
            if g.get('badge_href'):
                badge_html = f'<a class="gp-badge-link" href="{g["badge_href"]}">{badge_html}</a>'
            badge_html = f'<span class="gp-genres">{badge_html}</span>'
        ad = g["name"]
        if g.get('anchor'):
            ad = f'<a class="gp-tg-link" href="#{g["anchor"]}">{ad}</a>'
        rows.append([ad, badge_html, g.get('meta', '')])
    tablo = render_table(list(headers), rows)
    return f'''<div class="card-table-wrap">
  <div class="gp-ct-title">{title}</div>
{tablo}</div>
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
    badge_html = (f'<span class="gp-game-badge" style="color:{badge_text};background:{tint};">'
                  f'{inner}</span>')
    if whole_href:
        # display:contents -> anchor kutu üretmez; rozet linksizle birebir aynı yerleşir.
        badge_html = f'<a class="gp-game-badge-link" href="{whole_href}">{badge_html}</a>'
    return f'''<{level} id="{anchor}" class="gp-game-head">
  {badge_html}
  <span class="gp-game-name">{name}</span>
  <span class="gp-game-meta">{meta_text}</span>
</{level}>'''

# --- Inline Game Card (small, premium, in game description section) ---
def render_inline_game_card(name, badge, badge_color, meta_lines):
    """Small card to be floated alongside game description text."""
    meta_html = '<br>'.join(meta_lines)
    return f'''<aside class="gp-game-info-card">
  <span class="gp-gic-badge" style="background:{badge_color};">{badge}</span>
  <div class="gp-gic-name">{name}</div>
  <div class="gp-gic-meta">{meta_html}</div>
</aside>
'''

# --- İlgili Yazı Kartları (Figma "Related Card": #161616 + #29292B, 150px thumb + GFN THURSDAY etiketi,
#     tarih 12 gri, başlık 20 bold beyaz, "Devamını oku →" sarı) ---
def render_prev_weeks_cards(items):
    """items: [{url, date, label, img}] - img = yazının kapak görseli (og:image). Yoksa gradient fallback.
    Stiller ANIMATED_BORDER_STYLE'da; burada AYRI <style> bloğu ÜRETİLMEZ (ikinci stil bloğu CLS'e
    ve CMS'te sıra sorunlarına yol açıyordu)."""
    cards = []
    for item in items:
        img = item.get("img")
        thumb = f' style="--gp-thumb:url(\'{img}\');"' if img else ''
        cards.append(f'''  <a class="gp-prev-week" href="{item["url"]}">
    <div class="gp-pw-thumb"{thumb}>
      <div class="gp-pw-scrim"></div>
      <span class="gp-pw-tag">GFN THURSDAY</span>
    </div>
    <div class="gp-pw-body">
      <div class="gp-pw-date">{item["date"]}</div>
      <div class="gp-pw-title">{item["label"]}</div>
      <div class="gp-pw-more">Devamını oku &rarr;</div>
    </div>
  </a>''')
    return f'''<div class="prev-weeks-grid">
{chr(10).join(cards)}
</div>
'''

# --- İçindekiler (Figma: #161616 kart + #29292B kenarlık + New Science başlık + sarı 01/02 numaralar) ---
def render_floating_toc(items, title=None):
    """items: inject_heading_ids çıktısı [(level, text, anchor), ...] — H1 dahil (level 1).
    title: items içinde level-1 yoksa yazı başlığını buradan verebilirsin.

    KURAL 1 (CLS): Konum/boyut stilleri INLINE YAZILMAZ; ANIMATED_BORDER_STYLE'daki .floating-toc
    kuralları kullanılır. Inline top:120px + sonradan gelen mobil bottom:16px kuralı, elemanın ilk
    boyamadan sonra ~626px aşağı atlamasına ve ~0.125 CLS'e yol açıyordu.
    KURAL 2 (CMS): Inline onclick KULLANILMAZ — CMS bu öznitelikleri siliyor (canlıda doğrulandı).
    Başa dön, link kapatma ve otomatik kapanma <script> içinde addEventListener ile bağlanır;
    script bloğu CMS'te çalışıyor."""
    # H1 (yazı başlığı) ToC'nin İLK maddesi olur; hedefi başa-dön butonuyla aynıdır (sayfa başı).
    h1 = next(((t, a) for (l, t, a) in items if l == 1), None)
    if h1 is None and title:
        h1 = (title, None)

    def _num(n):
        return f'<span class="gp-toc-num">{n:02d}</span>'

    li_items = []
    num = 0
    if h1:
        h1_text, h1_anchor = h1
        num = 1                           # H1 = 01; sonraki H2'ler 02, 03, ... diye devam eder
        href = f'#{h1_anchor}' if h1_anchor else '#'
        li_items.append(
            f'    <li>{_num(num)}<a class="gp-toc-top" href="{href}">{h1_text}</a></li>')

    for level, text, anchor in items:
        if level == 1:
            continue                      # H1 yukarıda eklendi
        if level == 2:
            num += 1
            marker = _num(num)
        else:
            marker = '<span class="gp-toc-gap"></span>'
        li_items.append(
            f'    <li>{marker}<a href="#{anchor}">{text}</a></li>')
    body = chr(10).join(li_items)
    return f'''<details class="floating-toc">
  <summary>İçindekiler<span class="gp-toptop" title="Başa dön" ><svg viewBox="0 0 24 24" fill="none" stroke="#FFC900" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><polyline points="18 14 12 8 6 14"/><line x1="12" y1="8" x2="12" y2="16"/></svg></span></summary>
  <ul>
{body}
  </ul>
</details>
<script>
(function(){{
  var t = document.querySelector('.floating-toc');
  if (!t) return;
  var close = function(){{ if (t.hasAttribute('open')) t.removeAttribute('open'); }};
  var toTop = function(e){{
    e.stopPropagation(); e.preventDefault(); close();
    var y = window.pageYOffset || document.documentElement.scrollTop || 0;
    try {{ window.scrollTo({{top:0, behavior:'smooth'}}); }} catch (err) {{ window.scrollTo(0,0); }}
    /* Güvenlik ağı: smooth animasyon başlamazsa (bazı gömülü/webview ortamları) anında başa al */
    setTimeout(function(){{
      var y2 = window.pageYOffset || document.documentElement.scrollTop || 0;
      if (y2 > 0 && y2 >= y - 1) window.scrollTo(0, 0);
    }}, 400);
  }};
  var btn = t.querySelector('.gp-toptop');
  if (btn) btn.addEventListener('click', toTop);
  var first = t.querySelector('.gp-toc-top');
  if (first) first.addEventListener('click', toTop);
  t.querySelectorAll('ul li a').forEach(function(a){{ a.addEventListener('click', close); }});
  window.addEventListener('scroll', close, {{passive:true}});
  document.addEventListener('click', function(e){{ if (!t.contains(e.target)) close(); }}, true);

  /* html{{scroll-behavior:smooth}} kaldırıldı (scope'lanamıyor, site geneline taşıyordu). */
  /* İç bağlantılarda (ToC + card-table) yumuşak kaydırma artık burada. */
  var root = t.closest('.gp-content') || document;
  root.querySelectorAll('a[href^="#"]').forEach(function(a){{
    if (a.classList.contains('gp-toc-top')) return;      /* o zaten sayfa başına gidiyor */
    a.addEventListener('click', function(e){{
      var id = a.getAttribute('href').slice(1);
      if (!id) return;
      var el = document.getElementById(id);
      if (!el) return;
      e.preventDefault(); close();
      try {{ el.scrollIntoView({{behavior:'smooth', block:'start'}}); }}
      catch (err) {{ el.scrollIntoView(); }}
    }});
  }});
}})();
</script>
'''


def wrap_gp_content(html):
    """Gövdeyi .gp-content wrapper'ına alır — build'in EN SON adımı:
        final = wrap_gp_content(ANIMATED_BORDER_STYLE + "\\n" + body)

    NEDEN: Frontend ekibi site tipografi/renk kurallarını blog gövdesinden çekti. Buna karşılık
    bizim CSS'imizdeki class'sız seçiciler (h1-h4, p, ul li::marker, html) SAYFANIN TAMAMINA
    (sol menü, footer) taşıyordu. Artık tüm kurallar .gp-content ile başlıyor; wrapper zorunlu.
    Ayrıca .gp-content (0,1,0) öneki specificity'yi yükselttiği için h1-h4/p'de !important gerekmiyor."""
    if 'class="gp-content"' in html:
        return html
    return '<div class="gp-content">\n' + html + '\n</div>\n'

# --- FAQ Accordion (premium dark, Game+ '+' indicator that rotates) ---
def render_faq_accordion(pairs):
    items = []
    for q, a in pairs:
        items.append(f'''  <details class="faq-item">
    <summary>
      <span class="faq-icon">+</span>
      <span class="faq-q">{q.strip()}</span>
    </summary>
    <div><p>{a.strip()}</p></div>
  </details>''')
    return f'<div class="faq-block">\n{chr(10).join(items)}\n</div>'

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
    # H1 de toplanır (level 1): floating ToC'nin İLK maddesi yazı başlığı olur, hedefi sayfa başı.
    new_html = re.sub(r'<(h[123])>(.*?)</\1>', replace_h, html, flags=re.DOTALL)
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

    # 8z) CSS süslü parantez kaçışı (f-string hatası: çıktıda "{{" kalırsa CSS kuralı geçersiz olur)
    add('{{' not in final_html and '}}' not in final_html, "CSS parantez kaçışı",
        "temiz", "çıktıda çift süslü parantez var - f-string kaçış hatası, CSS kuralları geçersiz")

    # 8a) Editör Notu + Hatırlatma (her yazıda zorunlu)
    add('class="editor-note"' in final_html, "Editör Notu", "var", "Editör Notu yok (her yazıda zorunlu)")
    add('class="highlight-box"' in final_html, "Hatırlatma", "var", "Hatırlatma yok (her yazıda zorunlu)")

    # 8b) Madde listesi (taranabilirlik) — uygun yerlerde render_list kullan
    add('class="gp-list"' in final_html, "Madde listesi", "var",
        "gövdede madde (bullet) listesi yok — uygun yerlerde render_list kullan", warn=True)

    # 9) Oyun sayısı tutarlı: inline başlık == card-row == n_games (genel listicle)
    if n_games is not None:
        n_inline = final_html.count('class="gp-game-head"')               # render_game_h3_inline imzası
        # v10.9: card-table artık gerçek <table>; satırlar tbody içindeki <tr>
        _ct = re.search(r'<div class="card-table-wrap">.*?</table>', final_html, re.S)
        n_rows = len(re.findall(r'<tr\b', _ct.group(0).split("<tbody>")[-1])) if _ct else 0
        add(n_inline == n_games, "Inline oyun başlığı",
            f"{n_inline} başlık", f"{n_inline} inline başlık (beklenen {n_games}) — düz <hN>Oyun</hN> kalmış olabilir")
        add(n_rows == n_games, "Card-table satırı", f"{n_rows} satır", f"{n_rows} card-row (beklenen {n_games})")

    # 10) YouTube embed: aspect-ratio var, padding-bottom % hack yok (kare-bug)
    if 'youtube.com/embed' in final_html:
        add('aspect-ratio' in final_html, "Embed aspect-ratio", "16/9", "aspect-ratio yok (embed kare görünebilir)")
        add(not re.search(r'padding-bottom:\s*5[0-9]', final_html), "Embed padding-hack yok",
            "yok", "padding-bottom % hack var — aspect-ratio kullan", warn=True)

    # 10b) .gp-content wrapper (frontend zorunlu: CSS scope'u buna bağlı)
    add('class="gp-content"' in final_html, ".gp-content wrapper",
        "var", "YOK — wrap_gp_content(final) çağır; CSS'in tamamı .gp-content'e bağlı, wrapper'sız hiçbir stil uygulanmaz")
    # 10c) class'sız (siteye taşan) seçici kalmamalı
    import re as _re2
    _css = "".join(_re2.findall(r'<style>(.*?)</style>', final_html, _re2.S))
    _bare = [b for b in _re2.findall(r'(?m)^\s*([a-z][a-z0-9]*(?:\s*,\s*[a-z][a-z0-9]*)*)\s*\{', _css)
             if b not in ("to", "from")]
    add(not _bare, "CSS scope (.gp-content)", "tüm seçiciler scoped",
        f"class'sız seçici siteye taşıyor: {_bare[:5]}")

    # 10d) floating ToC'nin İLK maddesi H1 (yazı başlığı) olmalı — build'de l==2 filtresi bunu düşürür
    if 'floating-toc' in final_html:
        _h1m = re.search(r'<h1[^>]*>(.*?)</h1>', final_html, re.S)
        _h1t = re.sub(r'<[^>]+>', '', _h1m.group(1)).strip() if _h1m else None
        _toc1 = re.search(r'class="floating-toc".*?<ul>\s*<li[^>]*>.*?<a[^>]*>(.*?)</a>', final_html, re.S)
        _t1 = re.sub(r'<[^>]+>', '', _toc1.group(1)).strip() if _toc1 else None
        add(bool(_h1t) and _t1 == _h1t, "ToC ilk madde = H1",
            "yazı başlığı ilk sırada",
            f"ToC ilk maddesi H1 değil ({_t1!r}) — render_floating_toc'a items'ı l in (1,2) ile ver")

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
