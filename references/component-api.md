# Component API — `gameplus_blog_components.py` (v10.3)

```python
import sys; sys.path.insert(0, "<skill>/scripts")
from gameplus_blog_components import *
```

## Sabitler & tema
- `ANIMATED_BORDER_STYLE` — TEK `<style>` bloğu; final gövdenin en başına BİR KEZ.
- `PAGE_HEAD` / `PAGE_FOOT` — önizleme sarmalayıcı (New Science başlıklar + Greycliff gövde, 1200px). `embed_fonts(html)` fontları base64 gömer (New Science dahil).
- `GP_ACCENT #FFC900` · `GP_SURFACE #161616` · `GP_LINE #29292b` · `GP_TEXT2 #B2B2B2`; geri dönüş: `GP_SURFACE_MODE`, `GP_BADGE_TEXT_MODE`.
- `SVG_SPARKLE` — CTA eyebrow ikonu (4 uçlu sarı yıldız; ★ karakteri kullanılmaz). `SVG_DOC`, `SVG_BULB`, `SVG_EXT_LINK` de mevcut.
- `GENRE_BADGE_COLORS` + `badge_color_for(genre)` — tür→renk (tüm içerikte aynı). `GFN_CATEGORY_URLS` + `category_url_for(badge)` — rozet→GFN kategori iç linki.

## Yardımcılar
- `slugify` · `hex_to_rgba` · `lighten` · `inject_heading_ids(html) -> (html, toc_items)`
- `ensure_leading_h1(html)` — gövde TEK H1 ile başlar (taslakta varsa korur, yoksa ilk başlığı yükseltir). Build'in SON adımı. (`demote_h1` DEPRECATED shim.)
- `verify_output(final, blog_type, n_games, expect_faq)` + `print_report` — zorunlu çıktı kontrolü (tek H1, meta yok, TLDR 3-6, info-card, **Editör Notu + Hatırlatma zorunlu**, **CSS parantez kaçışı** (çıktıda `{{`/`}}` kalırsa FAIL), madde listesi uyarısı, embed 16:9, oyun sayısı, PlayStation uyarısı).
- `estimate_reading_time(html, wpm=200)` — gövdeden dakika cinsinden okuma süresi; `render_tldr(reading_time=...)`'a verilir. Sabit süre YAZMA.
- `verify_source_preserved(orig, final)` + `print_source_report` — yazar metni korunmuş mu (halüsinasyon/silme yakalar). Her build'de çalıştır.

## Bileşenler
- `render_tldr(items, reading_time=None)` — "Hızlı Özet": #161616 kart + dönen sarı glow + doküman ikonu; maddeler sarı `•` + gri 16/24. 3-6 madde. **Başlık `<div>`'dir (heading değil — SEO).** `reading_time` verilirse başlığın sağında gri "N dk okuma" çıkar (`estimate_reading_time(body)` ile hesapla).
- `render_info_card([(label, value), ...])` — stat karoselleri: #0D0D0D kart; **değer üstte** New Science 24px SARI, etiket altta gri; **içerik ortalı**. Değer **sayı olmak zorunda değil** - kısa metin/insight da olabilir ("Strateji ağırlıklı"). Kısa tut (<=22 karakter) ve yazıdan gelen gerçek bilgi olsun (kural 15).
- `render_list(items, marker="dot"|"check", accent)` — gövde içi madde listesi (kural 14).
- `render_editor_note(text, title="GAME+ EDİTÖR NOTU")` — sarı %6 zemin + 4px sarı bar + doküman ikonu; gövde 1em (paragrafla aynı boy). **Her yazıda zorunlu.**
- `render_highlight(text, title="Hatırlatma")` — beyaz %4 zemin + sarı bar + ampul ikonu; 1em. **Her yazıda zorunlu.**
- `render_table(headers, rows, featured=None)` — #161616 kap; thead #1E1E18 + SARI ORTALI başlıklar; hücreler 16/20 gri (oyun adı dahil normal); satırlar #29292B ayraçlı; **hover'da satır sarı %7 + ad sarı**; `featured=[i]` kalıcı vurgu.
- `render_genre_tags('Strateji','Aile')` — tür pill seti (tablo Tür hücresi); flex-wrap, üst üste binmez.
- `render_game_cell(name, meta=None, href=None)` — tablo Oyun hücresi: isim (+link, alt çizgisiz, **yeni sekme**: `target="_blank" rel="noopener noreferrer"`) + altında "Stüdyo · Yıl" 12px gri. Stüdyo/yıl KAYNAKLI olmalı (Steam API / resmi sayfa); bilinmiyorsa meta=None.
- `render_cta_paketler(h, d)` / `render_cta_oyunlar(h, d)` — glow'lu #161616 CTA kartı, sparkle eyebrow, New Science başlık; buton id: **packages-button / games-button**.
- `render_end_cta(h, d, btn2_label, btn2_url, chip2=None, eyebrow="GAME+ • BULUT OYUN")` — glow'lu kapanış kartı; butonlar: dolu sarı (id **end-packages-button**) + kontur (id **end-games-button**). GFN'de btn2=GeForce NOW Oyunları.
- `render_compact_cta(game, tagline, btn_label, btn_url, cta_id="featured-game-button")` — Öne Çıkan Oyun: glow + **gamepad ikonlu** eyebrow + sağda dolu sarı buton.
- `render_prev_weeks_cards([{url, date, label, img}])` — ilgili yazı kartları; `img` = yazının og:image kapağı (koyu overlay otomatik).
- `render_floating_toc(items)` — İçindekiler kartı: #161616 + sarı 01/02 numaralar (yalnız h2'ler numaralanır).
- `render_game_h3_inline(anchor, name, badge, badge_color, meta, level, badge_href=None)` — oyun başlığı: pill (paletten) + isim + "Stüdyo · Yıl". badge_href None=otomatik kategori linki (birleşikte her parça), False=link yok.
- `render_faq_accordion(pairs)` · `render_ubisoft_cta(h, d)` (buton id **ubisoft-packages-button**).

## DEPRECATED (çağırma)
`render_meta` (meta header eklenmez) · `demote_h1` (H1 artık korunur) · `render_inline_game_card` · `linkify_platforms` (gerçek mağaza URL'si varken kullanma; doc linkleriyle platform kelimesini linkle).
