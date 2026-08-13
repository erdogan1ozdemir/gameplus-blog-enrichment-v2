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
- `render_table(headers, rows, featured=None, first_col_strong=True, title=None)` — `title` verilirse tablonun üstüne
  `.gp-ct-title` başlığı basar (h-tag değil, H3 renk/ölçüsünde) ve bu başlık İçindekiler'e girer.
  Karşılaştırma tablolarında ne olduğunu anlatan bir başlık KONUR.
- `render_table` (eski açıklama) — mobilde tablo sıkıştırılmaz, yana kaydırılır; çıktı
  başına **"Tabloyu yana kaydır →"** ipucu (`.gp-table-hint`) basılır (masaüstünde gizli).
  **v10.12'den beri ipucu `.table-wrap`'in DIŞINDA, hemen ÜSTÜNDEKİ kardeş öğedir** (eskiden kabın
  içindeydi, çerçeveye taşıyordu). Gizleme `display` ile değil `.gp-hint-off` sınıfıyla yapılır -
  bunu değiştirme, tablo üstü boşluk kardeş seçiciye bağlı. Ölçüler: `design-system.md` → "v10.8" ve
  "v10.12".
- `render_table` (eski açıklama) — #161616 kap; thead #1E1E18 + SARI ORTALI başlıklar; hücreler 16/20 gri (oyun adı dahil normal); satırlar #29292B ayraçlı; **hover'da satır sarı %7 + ad sarı**; `featured=[i]` kalıcı vurgu.
- `render_genre_tags('Strateji','Aile')` — tür pill seti (tablo Tür hücresi); flex-wrap, üst üste binmez.
- `render_game_cell(name, meta=None, href=None)` — tablo Oyun hücresi: isim (+link, alt çizgisiz, **yeni sekme**: `target="_blank" rel="noopener noreferrer"`) + altında "Stüdyo · Yıl" 12px gri. Stüdyo/yıl KAYNAKLI olmalı (Steam API / resmi sayfa); bilinmiyorsa meta=None.
- `render_cta_paketler(h, d)` / `render_cta_oyunlar(h, d)` — glow'lu #161616 CTA kartı, sparkle eyebrow, New Science başlık; buton id: **packages-button / games-button**.
- `render_end_cta(h, d, btn2_label, btn2_url, chip2=None, eyebrow="GAME+ • BULUT OYUN")` — glow'lu kapanış kartı; butonlar: dolu sarı (id **end-packages-button**) + kontur (id **end-games-button**). GFN'de btn2=GeForce NOW Oyunları.
- `render_compact_cta(game, tagline, btn_label, btn_url, cta_id="featured-game-button")` — Öne Çıkan Oyun: glow + **gamepad ikonlu** eyebrow + sağda dolu sarı buton.
- `render_card_table(title, games, headers=("Oyun","Tür","Stüdyo · Yıl"))` — **v10.9'dan beri GERÇEK TABLO**
  (`render_table` çağırır): başlık satırı, satır hover vurgusu, yana kaydırma ve tipografi GFN oyun
  tablosuyla birebir aynı. Tablonun üstünde `.gp-ct-title` başlığı (h-tag DEĞİL, ikonsuz, düz beyaz, H3 ölçüsünde). `anchor` verilirse oyun adı
  yazı içindeki bölüme bağlanır.
- `move_game_descriptions(html, game_names)` -> **(html, tasinanlar)** TUPLE döndürür. "Oyun Adı: açıklama"
  paragraflarını ilgili oyunun başlık + fragman bloğunun altına taşır, öneki kaldırır. Kullanım:
  `body, tasinan = move_game_descriptions(body, oyun_adlari)`. Sıralama tablo olarak verilen yazılarda kullan.
- `render_prev_weeks_cards([{url, date, label, img}])` — ilgili yazı kartları; `img` = yazının og:image kapağı (koyu overlay otomatik).
- `render_floating_toc(items, title=None)` — İçindekiler kartı: #161616 + sarı 01/02 numaralar (yalnız h2'ler numaralanır).
  **İLK madde H1'dir** (yazı başlığı, yukarı-ok işaretli); hedefi başa-dön butonuyla aynıdır: sayfa başı. `inject_heading_ids` H1'i de toplar (level 1); `items`'ı FİLTRELEME (`l in (1,2)`), yoksa başlık maddesi düşer. level-1 yoksa `title=` ile verilebilir.
  **Konum/boyut stilleri inline YAZILMAZ** — `ANIMATED_BORDER_STYLE`'daki `.floating-toc` kuralları kullanılır (CLS).
  **Inline `onclick` KULLANILMAZ** — CMS siliyor; davranışlar `<script>` içinde `addEventListener` ile bağlanır.
- `render_game_h3_inline(anchor, name, badge, badge_color, meta, level, badge_href=None)` — oyun başlığı: pill (paletten) + isim + "Stüdyo · Yıl". badge_href None=otomatik kategori linki (birleşikte her parça), False=link yok.
- `render_faq_accordion(pairs)`
- `render_ubisoft_cta(headline, desc, eyebrow="UBISOFT+ · BULUT OYUN", btn_label=…, btn_url=…)` —
  **CTA Paketler ile yapı olarak BİREBİR AYNI**: `gp-conic` çerçeve + `gp-cta-eyebrow` / `gp-cta-title` /
  `gp-cta-desc` / `gp-btn gp-btn-solid`. Tek fark renk: `.cta-ubisoft` sınıfı `--gp-accent` ve `--gp-btn-fg`
  token'larını Ubisoft mavisine (#0061FF / #FFFFFF) çevirir. Buton id **ubisoft-packages-button**.
  Ayrı bir tipografi/zemin/padding değeri YOKTUR; inline stil yazma (yalnız `--gp-glow`).
- `wrap_gp_content(html)` — **build'in EN SON adımı; atlanamaz.** Gövdeyi `.gp-content` sarmalayıcısına alır:
  `final = wrap_gp_content(ANIMATED_BORDER_STYLE + "\n" + body)`. Tüm CSS bu sınıfa bağlı olduğu için
  sarmalayıcı yoksa hiçbir stil uygulanmaz. `verify_output` eksikse FAIL verir.

## v10.7 notu — bileşenler SINIF tabanlıdır
Renderer'lar artık inline stil yazmaz; kurallar `ANIMATED_BORDER_STYLE` içindedir. Yeni bir bileşen
eklerken **inline stil kullanma** — sınıf tanımla ve kuralı stil bloğuna, `@media` bloklarından ÖNCE ekle.
Inline kalması gereken tek şey dinamik değerlerdir (tür rengi, `--gp-glow`, `--row-c`, `--gp-bw`, `--gp-thumb`).
Sınıf listesi ve gerekçeler: `references/design-system.md` -> "v10.6 / v10.7".

## DEPRECATED (çağırma)
`render_meta` (meta header eklenmez) · `demote_h1` (H1 artık korunur) · `render_inline_game_card` · `linkify_platforms` (gerçek mağaza URL'si varken kullanma; doc linkleriyle platform kelimesini linkle).

## Çıktı hijyeni (yeni bileşen yazarken)

Yeni bir renderer'ın çıktısında ŞUNLAR OLMAZ - `verify_output` bunları FAIL ile yakalar:
HTML/CSS/JS yorumu · inline `on*` özniteliği · base64 gömülü font · sürüm etiketi ("v10.x").
Stil bloğu `_yorumsuz()` süzgecinden geçer; renderer'a elle yorum yazma.

**Inline kalması gereken TEK şey dinamik değerlerdir:** `--gp-glow` (conic glow rengi),
`--gp-dot` (`render_list` nokta rengi), `--gp-thumb` (önceki hafta kapak görseli) ve tür renkleri.
(`--row-c` ve `--gp-bw` v10.9'da kaldırıldı; artık hiçbir renderer basmıyor.)

`embed_fonts(html)` YALNIZ yerel önizleme içindir; CMS'e giden gövdeye UYGULANMAZ
(lisans + `verify_output` "Gömülü font yok" FAIL verir).

`SVG_TROPHY` / `SVG_STAR_GRADIENT` DEPRECATED (kupa ikonu v10.10'da kaldırıldı) - çağırma.
