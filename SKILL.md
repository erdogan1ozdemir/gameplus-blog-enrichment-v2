---
name: gameplus-blog-enrich-v2
description: (v2, Figma "Game+ UI" tasarımı — sarı tema) Enrich gameplus.com.tr (GeForce NOW Türkiye, powered by GAME+) BLOG POSTS with premium dark-theme HTML components without rewriting the author's sentences. Takes blog drafts delivered as .docx (or html/md/text) and ADDS enrichment (TLDR, info-card, floating ToC, comparison tables, clickable game card-table, inline-tag game headings, CTA blocks, FAQ accordion, editor notes, GFN "previous weeks" grid), then outputs ready-to-paste HTML, by default an Excel rollup (title to html) or separate files / combined preview on request. Use whenever the user gives a Gameplus BLOG post (a guide, listicle, "remake nedir", "en iyi X oyunlar", weekly "GFN Thursday" roundup) and asks to enrich, format, style, add CTA/TLDR/FAQ/tables, or convert blog docs to HTML. Trigger on "blog içeriğini zenginleştir", "gfn thursday html", "bu blog yazısını formatla", "blog docx'lerini html yap", or when blog .docx files are handed over. Do NOT use for /gfn/oyunlar/* CATEGORY pages (that is gameplus-category-content).
---

# Gameplus Blog Enrichment (v2 — Game+ UI / Figma tabanlı)

Bu skill, **gameplus.com.tr blog yazılarını** (NVIDIA GeForce NOW powered by GAME+ Türkiye) zengin, koyu temalı, premium HTML bileşenleriyle süsler. Kritik kural: **yazarın cümlelerini değiştirmez** — sadece enrichment öğeleri EKLER (TLDR, info-card, ToC, tablolar, oyun kartları, CTA'lar, FAQ, editör notları). Çıktı CMS'e yapıştırılmaya hazır HTML'dir; varsayılan olarak Excel'de toplanır (başlık → html).

Bu tasarım, Gameplus ekibiyle çok turlu revizyonla oturmuş son haldir (v10.2, Figma "Game+ UI"). Tüm görsel ve içerik kuralları bu skill'de hazır gelir — sıfırdan tasarlamaya gerek yok.

## Ne zaman tetiklenir

- Kullanıcı bir veya birden fazla **blog yazısını** (.docx / .html / .md / yapıştırılmış metin) iletip "zenginleştir / formatla / HTML yap / CTA-TLDR-FAQ ekle" derse
- "GFN Thursday" haftalık oyun derlemesi iletildiğinde
- **NVIDIA'nın İngilizce embargo draft'ı** (`Embargoed_*ThisWeekOnGFN_*.docx`) iletildiğinde → önce TR'ye yerelleştir, sonra enrich et (bkz. `references/gfn-localization.md`)
- "En iyi X oyunlar", "X nedir", rehber/listicle tarzı blog taslağı iletildiğinde
- Blog docx'leri CMS'e hazırlanmak istendiğinde

**TetiklenME:** `/gfn/oyunlar/*` kategori sayfaları için DEĞİL — o ayrı `gameplus-category-content` skill'idir. Bu skill blog (`/blog/*`) içindir.

## İki blog tipi

Skill iki blog tipini ayırt eder; bileşen seti farklıdır:

| Öğe | Genel Blog (rehber/listicle) | GFN Thursday (haftalık) |
|---|---|---|
| Meta header | ❌ **EKLENMEZ** (site/CMS eklenme tarihi + GAME+ marka adını zaten gösterir; `render_meta` DEPRECATED) | ❌ **EKLENMEZ** |
| Info-card | ✅ (4 metrik: incelenen sayı, öne çıkan, türler…) | ✅ 4 metrik. **Aylık:** "Bu Ay Eklenen N". **Haftalık:** metrikleri o haftaya göre uyarla — yeni oyun olmayabilir (DLC/sezon/update/geri dönen); "0" gösterme (bkz. content-rules kural 10) |
| Card-table | "En İyi N …" tıklanabilir liste (oyun bölümlerine kayar) | "Bu Hafta Eklenen Oyunlar" (platform linkli) |
| CTA sayısı | **2-3** (her zaman 3 şart değil): Paketler + dual End zorunlu, CTA Oyunlar opsiyonel | **Tek** End CTA + 1 compact featured CTA |
| Compact CTA | yok | ✅ öne çıkan oyun için (Controller-Tag) |
| Önceki haftalar | yok | ✅ soft-border kart grid |
| Oyun başlığı | tür rozeti + isim + "Stüdyo · Yıl" | **rozet YOK** - isim + "Stüdyo · Yıl" (`badge=None`, v10.23) |
| Editör notu / Hatırlatma | ihtiyaç oldukça | ihtiyaç oldukça |

Detaylı yerleşim kuralları: **`references/placement-rules.md`**.

## Workflow

### 1. Taslağı oku ve yapıyı çıkar
- `.docx` ise: `python3 -c "from docx import Document; ..."` veya `references/docx-extract.md`'deki yöntemle paragraf/başlık/liste/link yapısını çıkar. YouTube embed'leri ve `<iframe>`'leri **olduğu gibi koru**.
- **İngilizce embargo GFN draft'ı ise** (`Embargoed_*ThisWeekOnGFN_*`): önce `references/gfn-localization.md`'ye göre **TR'ye yerelleştir** (canlı dil; kelime oyunları doğal; çıkış tarihi formatı; iç linkler; öne çıkan oyunlara YouTube fragmanı), sonra bu workflow'la enrich et. Teslim: doc (yerelleştirilmiş metin + `HTML Versiyon`).
- Başlıkları (H2/H3), paragrafları, listeleri, linkleri, görsel/video embed'lerini belirle.
- Blog tipini tespit et (GFN Thursday mı, genel blog mu).

### 2. Orijinal HTML gövdesini hazırla
- Yazarın metnini HTML'e çevir (H1 + H2/H3/H4, `<p>`, `<ul>`, `<a>`, embed'ler). **Cümleleri değiştirme.** **Gövde TEK bir H1 ile başlar** (ilk başlık = yazı başlığı, H1); taslakta H1 varsa korunur, yoksa build sonunda `ensure_leading_h1` ilk başlığı H1 yapar. Bölüm başlıkları H2/H3.
- `inject_heading_ids(html)` ile her H2/H3'e `id` ekle ve ToC öğelerini topla.
- `shrink_youtube_embeds(html)` ile embed'leri `.gp-yt-wrap` (max 720px, ortalı) yap.

### 3. Bileşenleri üret (component library)
`scripts/gameplus_blog_components.py`'i import et. Her bileşen inline-CSS'li HTML string döndürür. İçeriğe göre (yazıyı OKUYARAK) doğru verileri sen kararlaştırırsın — TLDR maddeleri, hangi oyunların card-table'a gireceği, türleri, CTA metinleri.

```python
import sys; sys.path.insert(0, "<skill>/scripts")
from gameplus_blog_components import *

toc_items = []  # inject_heading_ids doldurur
body, toc_items = inject_heading_ids(body)
body = shrink_youtube_embeds(body)

tldr   = render_tldr(["<strong>…:</strong> …", ...])           # sarı • maddeler (meta header EKLENMEZ)
liste  = render_list(["…", "…"], marker="check")               # uygun yerlerde bullet listesi (content-rules 14)
info   = render_info_card([("İncelenen", "12 Yapım"), ...])    # her iki blog tipinde de ZORUNLU (GFN'de metrikleri o haftaya göre seç)
toc    = render_floating_toc(toc_items)
cta_p  = render_cta_paketler(headline, desc)
table  = render_table(["Tip","Kapsam",...], [[...],[...]])
cards  = render_card_table("En İyi 12 Remake Oyunu", games)    # games: aşağıda
faq    = render_faq_accordion([(soru, cevap), ...])
```

### 4. Yerleştir (placement)
`references/placement-rules.md`'deki kurallara göre bileşenleri orijinal gövdeye `str.replace` / `re.sub` ile enjekte et. Özet:
- ToC + TLDR + (info-card) → H1'den hemen sonra enjekte edilir (**meta header YOK; render_meta DEPRECATED**); **build EN SON adımda `ensure_leading_h1(body)` ile gövdenin tek bir H1 ile başlamasını sağlar (ilk başlık = yazı başlığı)**
- Karşılaştırma tablosu → ilgili kavram paragrafından sonra
- **CTA Paketler** → 2. H2'den önce
- **Card-table** → listicle'ın yerine, ilk oyun H3'ünden ÖNCE (genel blog); GFN'de oyun listesi yerine
- Genel blogda VE etkinlik özetlerinde (State of Play vb.) her oyun H3'ü → `render_game_h3_inline()` ile **tür etiketi + isim + "Stüdyo · Yıl"** formatına çevir (ZORUNLU, düz başlık bırakma). **GFN Thursday'de tür rozeti KULLANILMAZ** (`badge=None`): başlık = isim + "Stüdyo · Yıl" (content-rules 11)
- **End CTA** → SSS H2'sinden önce
- **FAQ accordion** → SSS bölümündeki H3+P çiftlerinin yerine
- **Tercih edilen kaynak kartı (v10.22, HER BLOGDA, GFN Thursday dahil)** → yazının ortalarında bir başlığın
  hemen öncesine, tek kez. Elle yerleştirilmez: `body, bilgi = insert_preferred_source(body)`. Çağrı sırası
  `auto_link_categories` sonrası, `apply_link_policy` ve `group_into_sections` öncesi. Aday başlık h2/h3
  (oyun başlıkları dahil); başlığın önü düz metin olmalı (CTA, tablo, not, video arkasına konmaz); yüzde
  30-70 bandında yüzde 50'ye en yakın aday seçilir; kapanış CTA'sı ve SSS sonrası aday olmaz. Kart canlıdaki
  Ubisoft Ağustos yazısındaki kartın birebir işaretlemesidir (`render_preferred_source()`), GA4 kimlikleri
  `#preferred-source-button` ve `#preferred-source-link`. Bağlantı Google tercihler ekranına gider, yeni sekmede açılır.

### 5. Birleştir ve çıktı al
- `final = wrap_gp_content(ANIMATED_BORDER_STYLE + "\n" + group_into_sections(enriched_body))` — stil bloğu bir kez en başta,
  ardından gövde tek bir `.gp-content` sarmalayıcısına alınır. **Bu son adım atlanamaz:** tüm CSS seçicileri
  `.gp-content` önekiyle yazılıdır, sarmalayıcı yoksa hiçbir stil uygulanmaz (`verify_output` FAIL verir).
  Sarmalayıcı aynı zamanda stillerin sol menü/footer gibi site alanlarına taşmasını engeller.
- **`group_into_sections(body)` — Kural 22, DOM genişliği.** Sarmalamadan HEMEN ÖNCE çağrılır. `.gp-content`
  doğrudan çocuklarını `<section class="gp-sec">` altında gruplar: her `<h2>` yeni bölüm başlatır, eşiği
  (varsayılan 50 çocuk düğüm) aşan bölüm kalırsa o bölüm `<h3>`, gerekirse `<h4>` ile alt bölümlere ayrılır.
  `<h1>`, `<style>`, en üst seviye `<script>` ve floating ToC bölüm dışında kalır (ToC `position: fixed`).
  Gerekçe: Sitebulb "Avoid excessive DOM width" bir ebeveynde 60'tan fazla çocuk düğüm olduğunda uyarıyor
  ve `.gp-content` sayfadaki en geniş ebeveyndi. Metne ve işaretlemeye dokunmaz; `verify_output` denetler.
- **Bileşenler sınıf tabanlıdır (v10.7); renderer'lar inline stil yazmaz.** Yeni bileşen eklerken sınıf tanımla
  ve kuralı stil bloğuna `@media`'lardan ÖNCE ekle. Inline yalnız dinamik değerler için (tür rengi, `--gp-glow`,
  `--row-c`, `--gp-bw`, `--gp-thumb`). Detay: `references/design-system.md` -> "v10.6 / v10.7".
- Önizleme için: `PAGE_HEAD.replace("__TITLE__", baslik) + body + PAGE_FOOT`
- **Çıktı:** `scripts/export_output.py` → `export(items, fmt="excel")`. Varsayılan Excel rollup (Başlık | HTML Part1 | HTML Part2 | Slug | Karakter). Kullanıcı farklı isterse: `fmt="files"` (ayrı body-only), `fmt="files-preview"` (tarayıcıda açılır tam HTML), `fmt="combined"` (tek dosyada toplu önizleme).

`items` formatı:
```python
items = [{"title": "Remake Nedir? …", "slug": "remake-nedir-…", "html": final_body}]
```

### 6. Doğrula (kontrol adımı — her çıktıda ZORUNLU, tutarlılık için)
Çıktıyı teslim etmeden önce final body üzerinde otomatik kontrol çalıştır. Bu adım, her yazının **aynı iskeletle** çıkmasını garanti eder (kullanıcının en çok önemsediği şey):
```python
from gameplus_blog_components import verify_output, print_report
res = verify_output(final_body, blog_type="general", n_games=12, expect_faq=True)  # GFN: blog_type="gfn", n_games=None
ok  = print_report(res)   # FAIL varsa TESLİM ETME, düzelt
```
Otomatik doğrulananlar: **oyun basınına link yok (FAIL)**, **göreli zaman ifadesi (genel blogda UYARI)**, **GFN Thursday'de başlık tür rozeti yok**, **tercih edilen kaynak kartı (tek kart, CSS, bağlantı, başlıktan hemen önce, yüzde 25-75 bandı)**, **DOM genişliği (Kural 22)**, **yazım - İngilizce terimde Türkçe İ** ve **büyük harf tuzağı (lang=tr + CSS uppercase; `Indie` -> ekranda `INDİE`)**, **tek H1 + ilk başlık H1**, **meta header yok**, ANIMATED_BORDER_STYLE 1x, **em dash yok**, floating ToC + TLDR (3-6 madde) + info-card, FAQ (varsa), oyun sayısı (**inline başlık = card-row = n_games**, düz `<hN>Oyun</hN>` kalmamış), YouTube embed `aspect-ratio` (kare-bug yok), PlayStation uyarısı. **FAIL = kural ihlali.** Ayrıca **`verify_source_preserved(original_body, final)` + `print_source_report`** ile yazarın metninin birebir korunduğunu doğrula (halüsinasyon/silme). Yargı gerektiren maddeler için **`references/qa-checklist.md`**'yi gözden geçir (yazarın cümleleri korundu mu, tür taksonomisi tutarlı mı, CTA dürüstlüğü, lisans hatırlatması, GFN tarih sütununda "-").

## Tasarım sistemi (v10.3 — "Game+ UI", Figma tabanlı)

Detaylar **`references/design-system.md`**'de. Özet:
- **Tek vurgu SARI `#FFC900`** (GFN yeşili tamamen kalktı); dolu sarı butonlarda koyu metin `#131313`.
- **Kartlar `#161616`** (stat karoselleri `#0D0D0D`), ayraç `#29292B`, ikincil metin `#B2B2B2`.
- **Başlıklar New Science SemiBold Extended** (H1 40/48 · H2 32/40 · H3 28/36 · H4 24/32), gövde Greycliff CF 20/24.
- **Dönen sarı glow (`gp-conic`)**: TLDR + tüm CTA'lar + Öne Çıkan Oyun.
- **Tablolar:** `#1E1E18` başlık satırı + sarı SOLA YASLI sütun başlıkları (yalnız sıra-no sütunu .gp-col-num ortalı); hücreler gri normal (oyun adı bold DEĞİL); oyun adının altında "Stüdyo · Yıl" (KAYNAKLI); Tür hücresi `render_genre_tags` pill'leri; satır vurgusu YALNIZ hover'da.
- **Tür rozeti paleti merkezi** (`GENRE_BADGE_COLORS`): aynı tür her içerikte AYNI renk.
- **İkonlar:** TLDR/Editör Notu doküman, Hatırlatma ampul, Öne Çıkan'da gamepad, CTA eyebrow'larında **sparkle** (★ karakteri kullanılmaz).
- **TLDR'da okuma süresi:** başlığın sağında "N dk okuma" (`estimate_reading_time(body)` ile hesaplanır). **TLDR başlığı `<div>` (heading değil).**
- **v10.3 tipografi:** başlıklar küçültüldü (H1 30.5/H2 22/H3 18.5/H4 15.5, mobil 20/17/15/14), gövde 16/24; CTA başlıkları en çok H2; tablolar mobilde başlıklı kalır + dikey ortalı + responsive içerik; yumuşak kaydırma (CSS). Detay `references/design-system.md`.
- **Linkler:** alt çizgi yok, renk yeterli; platform linkleri `color:inherit` + ↗. **Mağaza linkleri yeni sekmede** (`target="_blank" rel="noopener noreferrer"`).
- **Mobil:** tablo başlıkları hücreye ortalı; İçindekiler `bottom:16px`'e iner.
- **GA4 id'leri (statik):** packages-button · games-button · end-packages-button · end-games-button · featured-game-button · ubisoft-packages-button.
- **Link politikası (Kural 21):** `body, sayac = apply_link_policy(body)` — dış linkler `nofollow`,
  tüm linkler yeni sekmede, sayfa içi çapalara dokunulmaz. `ensure_leading_h1`den hemen önce.
- **Gövde içinde 1-2 GFN kategori linki** (Kural 20): `body, kat = auto_link_categories(body, max_links=2)`.
  Zorlama yok, doğal geçiş yoksa link kurulmaz. Anchor'lar `CATEGORY_ANCHORS`'ta arama hacmiyle sıralı.
- **Başa dön butonu ilk başlığa gider** (v10.20). `.gp-toptop` ve İçindekiler'in ilk maddesi artık `scrollTo(top:0)` yapmaz; hedef, İçindekiler ilk maddesinin çapası (yoksa gövdedeki ilk H1/H2, o da yoksa CMS'in bastığı H1) ve 28px üst boşlukla konumlanır. Canlıda sayfa başı site menüsüne/hero görseline denk geliyordu (yazı başlığı ~370-670px aşağıdaydı). **Script her yazının gövdesine gömülü olduğu için yayındaki yazılar bu düzeltmeyi kendiliğinden almaz;** güncel script bloğuyla değiştirilmeli (`scripts/basa_don_yamasi.py`).
- **`/firsatlar`'a yönlendirme YOK** (v10.13, marka kararı). CTA hedefleri: `/gfn/paketler`, `/gfn/oyunlar`, Ubisoft yazılarında `/paketler` ve `/ubisoft/*`. `render_end_cta` ikinci butonunun varsayılanı artık **GeForce NOW Oyunları → `/gfn/oyunlar`**. `verify_output` fırsatlar linkini ve CTA hedef çakışmasını denetler.

## İçerik kuralları (zorunlu)

Tam liste **`references/content-rules.md`**'de. En kritikleri:
- **Yazarın cümlelerini ASLA değiştirme.** Sadece enrichment ekle.
- **Yazıyı bu skill ile biz yazıyorsak** (inceleme, rehber, derleme) `references/inceleme-yazisi.md`
  geçerlidir. **Hazır taslak geldiğinde bu tarz kuralları yazarın metnine UYGULANMAZ**, yalnız bizim
  eklediğimiz parçalara (TLDR, editör notu, CTA, SSS) uygulanır. Kurallar: ham büyük sayılar yuvarlanır (25.851 -> "25 binden fazla"), "Türk oyuncular" yerine
  "yerli oyuncu toplulukları" / "globaldeki oyuncu toplulukları", editör notu buyurgan değil olanak
  dilinde, GFN bölümü tek paragraf, sistem gereksinimleri tablosu blogda yer almaz.
- **Yeni içerikte SEO/GEO (Kural 25, inceleme ve listicle dahil):** yazmadan önce DataForSEO ile
  hacim + PAA + ilgili aramalar + Türkçe rakipler; her H2'nin ilk cümlesi başlığı yanıtlar; H2'lerin
  çoğunda oyun adı; SSS arama talebinden (Türkçe ve GFN soruları her yazıda); alternatif ad metinde
  ("Control 2"); göreli zaman yok, tarih var; veri sitelerine (OpenCritic, Metacritic, HowLongToBeat)
  nofollow link verilir, **oyun basınına (GameSpot, IGN, Oyungezer vb.) asla link verilmez**; ilgili
  GFN Thursday yazısına iç link (soft 404 nedeniyle önce başlığı doğrulanır).
- **Basın adı metinde geçmez (v10.26):** incelemeler araştırılır ama "IGN'e göre", "GameSpot 9 verdi"
  yazılmaz; bulgular genel ifadeyle derlenir, puan tablosunda site puanları yerine puan aralığı.
  Yeni içerik build'lerinde `verify_output(..., yeni_icerik=True)` çağrılır (basın adında FAIL).
- **Brief Excel'i (v10.27, yalnız yeni içerik):** yazmadan önce `scripts/blog_brief_satiri.py` ile
  `Game+ Blogları/Game+ Blog Briefleri.xlsx`'e satır eklenir: KW + hacim, H2'ler, kurgu, linkler, SSS,
  **I Listeleme başlığı (Title), M Meta Title, O Meta Description**. Hazır taslakta brief yazılmaz.
  Detay: `references/inceleme-yazisi.md` bölüm 7.
- **Veri yoksa alan yazılmaz (v10.28):** oluşmamış metrik (çıkış günü Steam kullanıcı incelemesi,
  Metacritic kullanıcı puanı "tbd") ne tabloya "-" olarak ne metne "henüz oluşmamıştı" diye girer;
  alan tamamen çıkarılır. `verify_output(..., yeni_icerik=True)` FAIL verir (content-rules 25.11).
- **Video sayısı (v10.29):** incelemede **2-4 video** (fragman `Nedir?` bölümünde, oynanış videosu
  dövüş/oynanış bölümünde, başlığa özel sistem videosu ilgili bölümde); listicle'da oyun başına bir
  video olabilir (10 oyun = 10 video); rehberde içeriğe göre. Yayıncı/platform kanalı, basın kanalı yok,
  yaş kısıtı tarayıcıda test edilir.
- **İç linkleme (v10.30, yeni içerik):** yazı başına 7-11 gövde içi iç link: sabit üçlü (`/gfn`
  "GeForce NOW", `/gfn/paketler` "GeForce NOW fiyat", `/gfn/oyunlar` "GeForce NOW oyunları"),
  1-2 GFN kategori, 2-4 ilgili blog yazısı (headline ile doğrulanmış), ilgili GFN Thursday.
  Anchor aranan kelime biçiminde. Detay: `references/ic-linkleme.md`.
- **Doc biçimi:** içerik kısmında başlıklar ve metin siyah (Word mavi teması yok), önce yazı sonra HTML.
- **Özet (TLDR) madde sayısı:** duruma göre **3-6 madde** (her zaman 4 olması şart değil).
- **Oyun giriş formatı (HER YAZIDA AYNI):** **Yazıda birden fazla oyundan bahsediliyorsa** her oyunun başına oyun başlığı ekle; **tür etiketi + Stüdyo · Yıl** taşı. Başlık **H2/H3/H4** olabilir (çevredeki seviyeye uy): `render_game_h3_inline(anchor, isim, "TÜR", renk, "Stüdyo · Yıl", level="h2|h3|h4")`. Düz `<h2/h3/h4>Oyun Adı</…>` bırakma. **Başlık metnine RENK atama** (CMS verir, yük azalır). Card-table'da `badge`=tür, `meta`="Stüdyo · Yıl". Yıl yoksa dönem ("2027 (beklenen)", "Belirsiz", "Yayında"). Tek oyun anlatılıyorsa başlık şart değil. Detay: `content-rules.md` kural 11.
- **Tür rozeti → GFN kategorisi iç linki:** `render_game_h3_inline(badge_href=None)` (varsayılan) otomatik: **tek/saf rozet → tüm rozet** kendi kategorisine; **birleşik rozet (Aksiyon-Macera, Aksiyon-RPG) → HER PARÇA ayrı ayrı** kendi kategorisine linklenir (Aksiyon-Macera → /aksiyon + /macera). `badge_href=False` = link yok (tek-tür seride stuffing önlemi). **Dedup YOK** — eşleşen her rozet linklenir (sadece oyun başlığında; liste/tabloda değil). Detay: `content-rules.md` kural 12.
- **Türler:** Mümkünse GFN kategorilerini kullan (oyun GFN'de varsa hangi kategoriye giriyorsa). GFN'de yoksa uygun türü seç; birden fazla türe uyuyorsa birleşik yaz (Aksiyon-Macera, Aksiyon-RPG, Indie-RPG).
- **CTA dürüstlüğü:** "tüm yapımlara erişebilirsin" DEME (her oyun GFN'de olmayabilir). "satın aldığın / sahip olduğun / kütüphanendeki oyunlar" de.
- **Lisans hatırlatması:** GFN oyun satmaz, sadece çalıştırır; oyunun ilgili platformda (Steam/Xbox/Epic) lisansına sahip olmak gerekir.
- **GFN Thursday'de tek CTA** yeterli (Paketler + Oyunlar yönlendirmesi). İki ayrı blok koyma.
- Em dash (—) kullanma; nokta veya virgülle böl.
- **Gövde TEK bir H1 ile başlar** (ilk başlık = yazı başlığı, H1). `ensure_leading_h1` build'in son adımı: taslakta H1 varsa korur, yoksa ilk başlığı H1 yapar. Yalnız 1 adet H1; bölüm başlıkları H2/H3. (`demote_h1` DEPRECATED.)
- **Üst meta header / tarih-marka chip'i EKLEME** (`render_meta` DEPRECATED) — site/CMS eklenme tarihini ve GAME+ marka adını zaten gösterir.
- **Madde listesi kullan (taranabilirlik):** sıralanabilir bilgileri (faydalar, farklar, uyarılar, adımlar) düz paragraf yerine `render_list` ile bullet yap. Her şey paragraf olmasın; düz `<ul><li>` yazma (content-rules 14). `verify_output` hiç liste yoksa uyarır.
- **GFN embargo yerelleştirmesinde** (İngilizce→TR; enrichment'tan farklı olarak burada metin çevrilir): kelime oyunlarını/deyimleri **doğal ve anlamlı** Türkçeyle ver; birebir oturmuyor ve çiğ kalıyorsa ZORLAMA, espriyi/tonu taşıyan temiz bir ifadeyle değiştir (ör. "license to stream" zorlaması yerine doğal bir cümle). Mekanik/tarih/teknik bilgi birebir korunur. Detay: `references/gfn-localization.md`.
- **Her yazıda Editör Notu + Hatırlatma bulunur** (verify FAIL verir) — kural 15.
- **Stat karoselleri:** değer sayı ya da kısa metin/insight olabilir (<=22 karakter), yazıdan gerçek bilgi, kart içinde ortalı; "Stüdyo · Yıl" gibi veriler KAYNAKLI (Steam API/resmî sayfa), uydurma yok.
- **Üslup (kural 16):** klişe açılış ve hype yasak; doğal oyuncu dili; GFN ifade varyasyonu — eklediğimiz TÜM metinlerde ve bu skill ile yazılan yazılarda.
- Görsel alt text / caption / şema markup EKLEME (kullanıcı istemiyor).
- YouTube embed'leri ve mevcut linkleri koru.

## Çıktı formatları

| `fmt` | Sonuç |
|---|---|
| `excel` (varsayılan çıktının parçası) | `gameplus-blog-icerikler.xlsx` — satır başına blog: Başlık \| Slug \| Karakter \| HTML 1 \| HTML 2 \| … . 32.767 char limiti için HTML gereken kadar parçaya bölünür; **HTML 1..N sırayla birleştirilince tam body olur.** Markanın CMS'e yapıştırıp canlıya alması için. |
| `files` | Her blog için ayrı `ornek-blog-<slug>-body-only.html` |
| `files-preview` | Her blog için tarayıcıda açılır tam HTML — **canlı gameplus tipografisi** (GreycliffCF, 20px gövde, 1200px kolon). `embed_fonts(html)` ile fontları base64 göm → self-contained, Vercel'de de birebir. |
| `combined` | Tek dosyada tüm bloglar (hızlı önizleme) |

Çıkışı CWD'ye yaz (genelde `/Users/Erdo/Desktop/Claude Projects/Dispatch/`). **Varsayılan: her zaman İKİ çıktıyı birden üret** — (1) `files-preview` (canlı tipografili, `embed_fonts()` ile GreycliffCF gömülü, bire bir önizleme; markaya/müşteriye gösterilir, istenirse GitHub/Vercel'e push edilir) ve (2) `excel` rollup (body HTML; markanın CMS'e yapıştırıp canlıya alması için). Kullanıcı tersini söylemedikçe ikisini de teslim et. Önizleme tipografisi `PAGE_HEAD`'de gameplus blog ile birebir (GreycliffCF @font-face, 1200px kolon, 20px gövde, h1 40 / h2 32 / h3 22.75px); bu yalnızca önizleme içindir, CMS body'si etkilenmez.


- **Çıktıya yorum YAZMA.** CMS'e giden HTML'de CSS/JS/HTML yorumu, sürüm notu ("v10.7", "Geçiş 1"),
  gerekçe açıklaması bulunmaz. Stil bloğu `_yorumsuz()`'dan geçer; renderer'lara elle yorum ekleme.
  `verify_output` "Çıktıda yorum yok" kontrolüyle bunu ZORLAR - ihlalde build FAIL verir.
  Açıklamalar Python kaynağında ve `references/` altında tutulur.


- **Kural 17:** oyunun tek oyunculu hikaye moduna Türkçe metinde "kampanya" DENMEZ ->
  "hikaye modu (campaign)". Oyun adının parçasıysa aynen kalır (*Halo: Campaign Evolved*).
- **Sıralamayı tablo olarak verdiğin yazılarda** `body, tasinan = move_game_descriptions(body, adlar)`
  ile oyun açıklamalarını başlık + fragman altına taşı.
- **`shrink_youtube_embeds` bir HTML YORUMU işaretçisine bağlıdır** (`<!-- Embed Başlangıcı -->`);
  bu işaretçiler taslakta kalır ama BUILD SONUNDA gövdede hiçbir HTML yorumu kalmamalıdır.
- **`verify_output` kontrol listesi** için tek kaynak: `references/qa-checklist.md`.

## Referans dosyaları

- `references/design-system.md` — tüm renkler, V8/V9 efektleri, bileşen görünümleri
- `references/placement-rules.md` — bileşenlerin yazıya nereye/nasıl enjekte edileceği, GFN vs genel blog
- `references/content-rules.md` — dürüstlük, kopya, taksonomi, yasak öğeler, çıktı kontrolü (kural 13)
- `references/qa-checklist.md` — teslim öncesi çıktı kontrol listesi (`verify_output` + manuel/yargısal maddeler)
- `references/component-api.md` — her `render_*` fonksiyonunun imzası, parametreleri, örnek çağrı
- `references/docx-extract.md` — .docx'ten yapı çıkarma yöntemi
- `references/ga4-tracking.md` — **CTA id'leri + GTM/GA4 kurulumu** (blog_cta_click); çalışır demo `examples/ga4-cta-tracking-demo.html`
- `references/inceleme-yazisi.md` — **inceleme ve genel blog yazım tarzı (v10.24)**: bölüm akışı, sayı
  yuvarlama, "yerli / globaldeki oyuncu toplulukları" ifadesi, yumuşak öneri dili, GFN bölümünün tek
  paragraf olması, sistem gereksinimleri tablosunun detay sayfasına bırakılması, kaynak doğrulama ve
  yaş kısıtlı video yasağı
- `references/gfn-localization.md` — **GFN embargo (EN) → TR yerelleştirme** kuralları (canlı dil, kelime oyunu doğallığı, çıkış tarihi formatı, iç linkler, YouTube, önceki haftalar, teslim doc + `HTML Versiyon`)
- `examples/` — v10.1 referans build script'leri (GFN Thursday + listicle) ve örnek gövde çıktısı

Yeni bir blog geldiğinde şablon al: GFN Thursday için **`examples/build-gfn-thursday-reference.py`**, listicle için **`examples/build-battle-royale-reference.py`**.
