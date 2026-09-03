# Tasarım Sistemi — v10.3 "Game+ UI" (Figma: Blog Detail / GFN Thursday)

Kaynak: Figma "Blog" dosyası (frame `Blog Detail - GFN Thursday (Game UI)`) + Font Kullanım Rehberi; tüm değerler node'lardan birebir çekildi. **GFN yeşili (#76b900) tamamen kaldırıldı; tek vurgu SARI.**

## Renkler

| Token | Değer | Kullanım |
|---|---|---|
| Vurgu (accent) | `#FFC900` | butonlar, eyebrow, tablo sütun başlığı, madde işaretleri, glow, stat değerleri |
| Buton üzeri metin | `#131313` | dolu sarı butonların yazısı (beyaz DEĞİL) |
| Kart zemini | `#161616` | TLDR, CTA'lar, tablolar, ToC, ilgili yazı kartları |
| Stat kart zemini | `#0D0D0D` | info-card karoselleri |
| Tablo başlık satırı | `#1E1E18` | thead zemin (+altında 1px `rgba(255,201,0,0.3)`) |
| Ayraç / kenarlık | `#29292B` | kart kenarlıkları, tablo satır ayraçları |
| İkincil metin | `#B2B2B2` | gövde paragraf, tablo hücreleri (oyun adı DAHİL - bold/beyaz değil) |
| Editör Notu zemini | `rgba(255,201,0,0.06)` | + 4px sarı sol bar (r2) + doküman ikonu |
| Hatırlatma zemini | `rgba(255,255,255,0.04)` | + 4px sarı sol bar (r2) + ampul ikonu |
| Hover satır | `rgba(255,201,0,0.07)` + ad `#FFC900` | tablo satırı YALNIZ hover'da vurgulanır (normalde vurgusuz); kalıcı için `featured=[i]` |

**Geri dönüş flag'leri** (`gameplus_blog_components.py` başında): `GP_SURFACE_MODE` ("card"→#161616 / "transparent"→v9), `GP_BADGE_TEXT_MODE` ("full"→tam renk / "lighten"→WCAG açık ton). v9 yedeği: `gameplus_blog_components.py.v9bak`.

## Tipografi

| Rol | Font | Boyut | Renk |
|---|---|---|---|
| H1 (yazı başlığı) | New Science SemiBold Extended | 30.5/38 (mobil 20/26) | #fff |
| H2 (bölüm) | New Science SemiBold Ext | 22/28 (mobil 17/23) | #fff |
| H3 | New Science SemiBold Ext | 18.5/25 (mobil 15/20) | #fff |
| H4 | New Science SemiBold Ext | 15.5/21 (mobil 14/19) | #fff |
| Stat değeri (karosel, ortalı) | New Science SemiBold Ext | 24/32 | **#FFC900** |
| Gövde paragraf | Greycliff CF Regular | 16/24 (mobil 15/22) | #B2B2B2 |
| Callout gövdesi | Greycliff CF | **1em/1.5 (paragrafla aynı boy)** | #fff |
| Tablo hücre | Greycliff CF | 16/20 | tümü #B2B2B2 normal; sütun başlığı Bold **#FFC900**, ORTALI |
| Stüdyo · Yıl alt satırı | Greycliff CF Medium | 12/16 | #B2B2B2 |
| Eyebrow / etiket | Greycliff CF Bold | 12/16, ls 0.08em | #FFC900 |
| Tür pill | Greycliff CF Bold | 12/16, sentence case | tam tür rengi, zemin %16 |

Fontlar (`scripts/_fonts/`, lisanslı — repoya konmaz): New Science SemiBold Extended + GreycliffCF. Önizleme `embed_fonts()` ile base64 gömer; canlı sitede fontlar dev tarafından yüklenir.

## Tür rozeti paleti (TÜM içerikte aynı renk — merkezi: `GENRE_BADGE_COLORS`, `badge_color_for()`)

Figma'dan birebir: Aksiyon `#FF5C5C` · Macera `#FF9F43` · Korku `#F472B6` · RPG `#818CF8` · FPS `#FB7185` · MMO `#E879F9` · MMORPG `#2DD4BF` · Spor `#FACC15` · Simülasyon `#38BDF8` · Strateji `#5B8DEF` · Gerçek Zamanlı Strateji `#60A5FA` · Bağımsız `#A3E635` · Roguelike `#A78BFA` · Bulmaca `#C084FC` · Aile `#34D399` · Hayatta Kalma `#4ADE80` · Parti `#FBBF24` · Co-op `#22D3EE`.
Atananlar (tasarımda yoktu): Yarış `#FB923C` · Dövüş `#E11D48` · Platform `#F59E0B` · Arcade `#FBBF24` · MOBA `#14B8A6` · Basit Eğlence `#86EFAC` · Oynaması Ücretsiz `#FCD34D` · Demo `#94A3B8` · Soulslike `#A3A3A3` · Metroidvania `#D8B4FE` · JRPG `#8B5CF6` · Gizlilik `#22C55E`.
Pill: zemin renk %16, metin tam renk, r6, 4x10px, kenarlıksız, sentence case; çoklu pill flex-wrap 6x8px boşluk (üst üste binmez).

## Efektler ve ikonlar
- **Dönen glow (`gp-conic`, `--gp-glow`):** TLDR + CTA Paketler/Oyunlar + End CTA + Öne Çıkan Oyun + **Ubisoft+ CTA**.
  Renk `--gp-glow` ile verilir: GFN bloklarında `#FFC900`, Ubisoft+ CTA'da `#0061FF`.
- İkonlar: TLDR + Editör Notu → doküman (SVG_DOC); Hatırlatma → ampul (SVG_BULB); Öne Çıkan eyebrow → **gamepad**; CTA eyebrow'ları (Paketler / Oyunlar / End / Ubisoft+) → **sparkle** (`SVG_SPARKLE`, 4 uçlu yıldız). Sparkle `fill="currentColor"`, yani eyebrow rengini miras alır (GFN'de sarı, Ubisoft+'ta mavi). **★ karakteri hiçbir yerde kullanılmaz.**
- **TLDR okuma süresi:** başlığın sağında, 20px boşlukla, dikeyde ortalı gri "N dk okuma" (`render_tldr(items, reading_time=...)`; süre `estimate_reading_time(body)` ile gövdeden hesaplanır, sabit yazılmaz).
- İlgili yazı kartları: gerçek kapak görseli (`img` alanı = og:image) + koyu gradient overlay + GFN THURSDAY etiketi.
- Linkler: **alt çizgi yok, renk değişimi yeterli.** Dış platform linki: `color:inherit` + ↗ ikon (SVG_EXT_LINK).
- **Mağaza linkleri yeni sekmede:** oyun adı ve Platform/Çıkış sütunundaki tüm mağaza linkleri `target="_blank" rel="noopener noreferrer"` taşır (`rel` güvenlik için zorunlu). Arka planda mı ön planda mı açılacağına tarayıcı karar verir; HTML bunu zorlayamaz.

## Mobil (<=700px)
- Tablo başlıkları hücreye **ortalı** (`text-align:center !important`), hücreler dikeyde ortalı; sütun genişlikleri sütun sayısına göre (3 sütunda 40/32/28). 375px'te ölçüldü: 9/9 başlıkta sapma 0px.
- Yatay kaydırma yok (`overflow-x:visible`, `table-layout:fixed`), punto 0.76em.
- **İçindekiler** (<=900px) `bottom:16px`'e iner (masaüstünde `top:120px` sağda). Bu kural f-string kaçış hatası yüzünden bir süre üretilmiyordu; `verify_output` artık çıktıda `{{`/`}}` kalırsa FAIL verir.

## v10.3 ince ayarlar (16 Temmuz örneğinde onaylandı, skille işlendi)
- **Başlık ölçekleri** yukarıdaki tabloda (masaüstü + mobil). ANIMATED_BORDER_STYLE'da `!important` ile; renk atanmaz (CMS verir).
- **Gövde paragrafı 16/24** (mobil 15/22); inline-stilli callout/CTA paragrafları etkilenmez.
- **"Hızlı Özet" başlığı artık `<div>`** (SEO: başlık outline'ından çıkar; İçindekiler'e zaten girmiyordu). Boyut 19px (mobil 16), iç padding 15/18, madde arası 8px.
- **CTA başlıkları** en fazla H2 kadar, responsive (End 21/17, Paketler-Oyunlar-Öne Çıkan 19/16); CTA sınıflarına scoped, info-card 24px değerlerine dokunmaz.
- **CTA yüksekliği mobilde kısaldı:** eyebrow altı 24->8, açıklama altı 24->12 + satır aralığı sıkı, başlık altı 8->4, buton yüksekliği (padding 12->9), iç boşluk 15->14; eyebrow 12->11, açıklama/buton 16->15. **End CTA'nın iki butonu mobilde YAN YANA** (12.5px, sarma serbest, ortalı) -> alt alta 2 satır yerine tek sıra. Toplam: End CTA ~378px -> ~287px (%24 kısa, 375px).
- **info-card / gp-cell** mobilde 2 kolon `minmax(0,1fr)`, değer 19→17px / etiket 13→12px (≤700/≤400).
- **Tablolar mobilde:** başlık satırı KALIR (thead görünür), hücreler dikey ortalı, içerik responsive; GFN-özel düzen (oyun adı 14/13, platform 11/10, tür ortalı, platform oku `nowrap` = kelimeye bitişik) **3 sütunlu tabloya scoped** (`:first-child:nth-last-child(3)`), 2/4-sütun karşılaştırma tabloları etkilenmez.
- **Yumuşak kaydırma:** `html{scroll-behavior:smooth}` + başlıklara `scroll-margin-top:28px` (saf CSS, JS yok). NOT: scroll-reveal (fade-in) animasyonu skile EKLENMEDİ.

## GA4 tıklama id'leri (statik — her yazıda aynı)
`packages-button` · `games-button` · `end-packages-button` · `end-games-button` · `featured-game-button` · `ubisoft-packages-button`

## v10.5 — floating ToC: CLS düzeltmesi + CMS uyumlu davranış + H1 maddesi

**1. CLS (0.125 -> 0).** `.floating-toc` kuralları eskiden elemandan SONRAKİ ayrı bir stil bloğundaydı.
Mobilde (`max-width:900px`) konum `top:120px` -> `bottom:16px` değiştiği için tarayıcı elemanı önce
üstte boyayıp sonra ~626px aşağı taşıyordu. Kurallar artık **`ANIMATED_BORDER_STYLE` içinde**, yani
eleman parse edilmeden önce uygulanıyor; ilk boyama doğru konumda (ölçülen sıçrama: 0px).
**Konum/boyut stilleri inline yazılmaz.**

**2. CMS inline `onclick`'i siliyor.** Canlıda doğrulandı: `.gp-toptop` ve ToC linklerinde `onclick`
özniteliği yok (bu yüzden başa-dön butonu çalışmıyordu). `<script>` bloğu ise çalışıyor. Tüm davranışlar
(başa dön, link tıklayınca kapat, scroll/dışarı tıklama ile kapat) artık `addEventListener` ile bağlanır.
Başa-dön'de güvenlik ağı var: smooth animasyon başlamazsa 400 ms sonra anında başa alınır.

**3. H1 ToC'nin ilk maddesi.** `inject_heading_ids` artık H1'i de toplar (level 1) ve ToC'nin ilk maddesi
yazı başlığı olur (yukarı-ok işaretli). Hedefi başa-dön butonuyla aynıdır.
`render_floating_toc(items)` çağrısında items'ı `l == 2` diye filtreleme; `l in (1, 2)` kullan.

**4. Başa dön hedefi: sayfa başı DEĞİL, yazının ilk başlığı (v10.20).** Canlıda ölçüldü
(`/blog/yapay-zeka-oyunlari-nasil-degistiriyor-unity-7-ve-ai-npc-ler`): script çalışıyordu, ancak
`window.scrollTo({top:0})` kullanıcıyı yazı başlığının ~370-670px üstüne, site menüsü ve hero
görselinin olduğu alana bırakıyordu. `basaDonHedefi()` sırayla şuna bakar: İçindekiler ilk maddesinin
çapası -> `.gp-content` içindeki ilk `h1, h2` -> sayfadaki `h1`. Hedef `getBoundingClientRect().top +
pageYOffset - 28` ile hesaplanır (28px, başlıkların `scroll-margin-top` değeriyle aynı). Güvenlik ağı
korunur: 400 ms sonra hiç hareket olmamışsa anında hedefe atlanır. Ölçüm: hangi noktadan tıklanırsa
tıklansın başlık ekranın 16-28px altında duruyor.

**Script yayındaki yazılara geriye dönük gitmez** - her yazının gövdesinde kendi kopyası var.
Mevcut çıktıları güncellemek için: `python3 scripts/basa_don_yamasi.py <dosya...>` (eski script
bloğunu bulup güncel bloğuyla değiştirir, zaten güncel olanı atlar).

## v10.6 / v10.7 - CSS izolasyonu, sınıf tabanlı bileşenler, tipografi

Frontend ekibi (3 Ağustos 2026) blog gövdesinden site tipografisini kaldırdı. İçerik artık **kendi
kendine yeterli olmak zorunda**: kendi stilini kendi taşır, siteden bir şey ummaz, siteye de taşmaz.

**1. `.gp-content` sarmalayıcı (v10.6).** Build'in EN SON adımı `wrap_gp_content(...)`. Gövdedeki tüm
CSS seçicileri bu sınıfa bağlıdır; çıplak `h2 {}`, `p {}`, `ul li::marker {}` YAZILMAZ (bunlar sol
menüyü ve footer'ı da boyuyordu). `html {}` kuralı hiç kullanılmaz - yumuşak kaydırma JS ile yapılır.

**2. Renkler gövdeden gelir (v10.6).** Site CSS'i çekildiği için gövde artık kendi renklerini taşır:
`p #B2B2B2` · `h1-h4 #fff` · `a #FFC900` · `a:hover #ffd94d`. **İç linkler altı çizgisizdir**
(`text-decoration: none`); verilmezse Bootstrap varsayılanı altını çizer. `a:hover` ayrıca yazılır:
sitenin `a:hover{color:inherit}` kuralı (0,1,1) yalnız `.gp-content a:hover` (0,2,1) ile aşılır.

**3. Sınıf tabanlı bileşenler (v10.7).** Tüm inline stiller sınıflara taşındı; `.gp-content` öneki
specificity'yi yükselttiği için `!important` gerekmiyor (211 -> 6). Dinamik değerler inline kalır:
tür renkleri, `--gp-glow`, `--row-c`, `--gp-bw` (card-table rozet sütunu), `--gp-thumb` (kapak görseli).

| Bileşen | Sınıflar |
|---|---|
| TLDR | `.tldr-block` `.gp-tldr-title` `.gp-tldr-rt` `.gp-tldr-bullet` `.gp-tldr-text` |
| info-card | `.info-card` `.gp-cell` `.gp-cell-value` `.gp-cell-label` `.gp-check-row` |
| Not kutuları | `.editor-note` `.highlight-box` `.gp-note-bar` `.gp-note-eyebrow` |
| CTA | `.gp-cta-eyebrow` `.gp-cta-title` `.gp-cta-desc` `.gp-cta-actions` `.gp-btn` + `.gp-btn-solid` / `.gp-btn-outline` / `.gp-btn-lg` `.gp-cta-compact-main` `.gp-cta-compact-tagline` |
| CTA renk varyantı | `.cta-ubisoft` yalnızca `--gp-accent: #0061FF` ve `--gp-btn-fg: #FFFFFF` tanımlar. Eyebrow rengi, sparkle fill'i, dolu buton zemini ve kontur buton rengi bu iki token'dan okunur; yeni bir marka rengi gerekirse aynı desenle tek satırlık bir sınıf eklenir. |
| Tablo | `.table-wrap` `.gp-table-scroll` `.gp-row-feat` `.gp-tg-link` `.gp-tg-meta` `.gp-ext` |
| Tür rozeti | `.gp-genres` `.gp-genre` |
| Card-table | `.card-table-wrap` `.gp-ct-head` `.gp-ct-title` `.gp-card-rows` `.card-row` `.gp-badge` `.gp-badge-link` `.gp-name` `.gp-meta` |
| Oyun başlığı | `.gp-game-head` `.gp-game-badge` `.gp-game-badge-link` `.gp-game-name` `.gp-game-meta` |
| SSS | `.faq-block` `.faq-item` `.faq-icon` `.faq-q` |
| Gövde listesi | `.gp-list` `.gp-list-dot` `.gp-list-check` |
| İçindekiler | `.floating-toc` `.gp-toc-num` `.gp-toc-gap` `.gp-toc-top` `.gp-toptop` |
| Önceki haftalar | `.prev-weeks-grid` `.gp-prev-week` `.gp-pw-thumb` `.gp-pw-scrim` `.gp-pw-tag` `.gp-pw-body` `.gp-pw-date` `.gp-pw-title` `.gp-pw-more` |

**Kural sırası önemli:** taban bileşen kuralları TÜM `@media` bloklarından ÖNCE gelir. `!important`
kalktığı için sonradan gelen taban kural mobil ölçüyü ezer.

**Kalan 6 `!important` (bilinçli):**
- `.gp-yt-wrap` ve `iframe` (5) - gömme işaretlemesi yazardan/CMS'ten geliyor, skill üretmiyor; normalize etmek gerekiyor.
- `.faq-item[open] .faq-icon { transform }` (1) - ikon üzerinde `gp-pulse-plus` animasyonu var; CSS animasyonları normal bildirimleri ezer, `!important` olmadan 45° dönüş uygulanmaz.

**4. Tek stil bloğu.** Hiçbir renderer ayrı `<style>` üretmez (`render_prev_weeks_cards`'ınki kaldırıldı).
İkinci stil bloğu CLS'e ve CMS'te sıra sorunlarına yol açıyordu.

**5. Tipografi (referans repo `game--yeni-blog-ornegi-2026-temmuz` head CSS'i esas alındı).**

| | Masaüstü | Mobil (<=700) |
|---|---|---|
| Gövde / p | 20 / 24 | 16 / 24 |
| H1 | 40 / 48 | 30 / 1.15 |
| H2 | 28 / 36 | 22 / 1.2 |
| H3 | 24 / 32 | 19 / 1.25 |
| H4 | 20 / 28 | 17 / 1.3 |

**6. İçindekiler numaralandırma.** İlk madde (H1) `01`, sonraki H2'ler `02`, `03`... tek dizi.
Başa-dön butonundaki ok daireye tam ortalıdır (simetrik SVG + `line-height:0`).

**7. Font adı.** Başlıklar `'New Science'` adıyla çağrılır; frontend `global.scss`'te bu adla alias
`@font-face` tanımladı. **İsim değiştirilmez.** Font dosyaları gövdeye GÖMÜLMEZ (lisans).

## v10.8 - Marka "Font Kullanım Rehberi" + tablo yatay kaydırma (4 Ağustos 2026)

Tasarım ekibinden gelen **Font Kullanım Rehberi** (masaüstü + mobil 360 px) esas alındı. Kurallar
`ANIMATED_BORDER_STYLE`'ın **EN SONUNDA** ayrı bir "v10.8" bloğunda; önceki tüm ölçüleri bilinçli ezer.
Yeni bileşen eklerken ölçüyü BU bloğa yaz, yoksa eski kurallar sonradan gelip ezer.

| Öğe | Masaüstü | Mobil (<=700) |
|---|---|---|
| H1 | 40/48 #fff | 24/32 |
| H2 | 32/40 #fff | 21/28 |
| H3 | 28/36 **#FFC900** | 24/32 |
| H4 | 24/32 #fff | 24/32 |
| Gövde paragraf | 16/24 #B2B2B2 | 16/24 |
| Hızlı Özet başlığı | 24/32 #fff | 20/24 |
| Özet maddesi | 16/24 #B2B2B2 | 16/24 |
| İçindekiler kutu başlığı | 24/32 #fff | 20/26 |
| İçindekiler madde + numara | 16/20 | 12/16 |
| İstatistik sayısı | 27/35 #FFC900 (v10.12; rehber 28/36) | 17/23 |
| İstatistik etiketi | 16/24 #B2B2B2 | 13/17 |
| Editör Notu / Hatırlatma | 16/22 #fff | 15/22 |
| CTA başlığı (compact + end) | 32/40 #fff | 19/25 |
| CTA metni | 16/20 #B2B2B2 | 16/20 |
| Buton | 16/20 #131313 | 16/20 |
| Tablo sütun başlığı | 16/20 #FFC900 | 16/20 |
| Tablo hücresi | 16/20 #B2B2B2 | 16/20 |
| Tablo oyun adı | 16/20 **#fff** | 16/20 |
| İlgili yazı kartı başlığı | 20/24 #fff | 20/24 |
| Küçük metin (eyebrow, meta, tarih, tür etiketi, stüdyo·yıl) | 12/16 | 12/16 |

**Rehberden bilinçli ayrışmalar:**
- **Tablo oyun adı beyaz** (rehber #FFC900 diyor) - marka tasarım görselinde beyaz; sütun başlıkları sarı kalıyor.
- **Tür etiketi kendi tür renginde** (rehber #FFC900 diyor) - tür-renk taksonomisi korunuyor, yalnız boyut 12/16'ya çekildi.
- **Editör Notu / Hatırlatma** rehberde 20/32; kullanıcı 16/22 (masaüstü) ve 15/22 (mobil) istedi.
- **Eyebrow** rehberde iki ayrı satırda çelişiyor (20/24 "Alt Başlık Regular" vs 12/16 "Etiket Bold · eyebrow"); 12/16 seçildi.

**Tablo mobilde SIKIŞTIRILMAZ, yana kaydırılır:**
- Hücreler `white-space: nowrap`, tür rozetleri tek satır; tablo `.gp-table-scroll` içinde yatay kayar.
- **İlk sütun (Oyun) 170 px sabit + `white-space: normal`** - uzun oyun adı alt satıra sarar, böylece
  Tür sütunu ekrana girer ve tablonun kaydırılabilir olduğu görülür.
- **Kaydırma çubuğu HER genişlikte gizli** (`scrollbar-width: none` + `::-webkit-scrollbar{display:none}`);
  kaydırılabilirliği `render_table`'ın bastığı **"Tabloyu yana kaydır ->"** ipucu anlatır
  (`.gp-table-hint`, 12/16 medium #B2B2B2, masaüstünde `display:none`).
- Eski `.table-wrap > div { overflow-x: visible }` kuralı daha yüksek specificity'ye sahip olduğundan
  kaydırma kabı `.table-wrap > div.gp-table-scroll` seçicisiyle hedeflenir.

**İç linkler altı çizgisizdir** (`.gp-content a { text-decoration: none }`); renk yeterli.

## v10.9 - Tablolar tek yapıda: card-table gerçek tabloya çevrildi (4 Ağustos 2026)

**Sorun:** "En İyi N / Çıkış Sırası" listesi (card-table) CSS grid'di; GFN oyun tablosu ise gerçek
`<table>`. İkisi ayrı ayrı stillendiği için tipografi, hover ve kaydırma davranışı tutmuyordu.

**Çözüm:** `render_card_table` artık `render_table`'ı çağırıyor. Çıktı: `.table-wrap` + `<thead>`
(**Oyun · Tür · Stüdyo · Yıl**) + `.gp-table-scroll` + "Tabloyu yana kaydır ->" ipucu. Kupa ikonlu
gradient başlık tablonun ÜSTÜNDE kalıyor. Oyun adı `anchor` verilirse `.gp-tg-link` ile yazı
içindeki bölüme bağlanıyor; tür rozeti `.gp-genres` / `.gp-genre` (GFN tablosuyla aynı bileşen).
Eski grid kuralları (`.card-row`, `.gp-name`, `.gp-badge`, `--gp-bw`) geriye dönük uyumluluk için durur.

**Üç tablo tipi:**

| Tip | Sarmalayıcı | Ne zaman |
|---|---|---|
| Oyun tablosu (GFN) | `table-wrap gp-table` | ilk sütun geniş (oyun adı) |
| Sıralama tablosu | `table-wrap gp-table gp-table-rank` | ilk sütun KISA (<=4 karakter: sıra no) - `render_table` otomatik algılar |
| Card-table | `card-table-wrap` + içinde oyun tablosu | `render_card_table` |

**Sıralama tablosu (`gp-table-rank`) farkları:**
- Hücreler beyaz + 600 (card-table'daki oyun adı görünümü).
- Başlık ve hücreler SOLA yaslı; yalnız `gp-col-num` sütunu ortalı.
- Hover / seçili satırda **tüm hücreler** #FFC900 olur. Genel hover kuralı yalnız `td:first-child`'ı
  boyar; orada sıra numarası olduğu için oyun adları beyaz kalıyordu.
- Mobilde iki sıra sütunu %44/%44, sıra-no %12; hücreler sarar (`white-space: normal`).

**Sıra numarası sütunu (`gp-col-num`):** `width:1%`, `nowrap`, ortalı, iki yanda eşit dolgu
(masaüstü 20 px, mobil 14 px). Mobildeki 170 px'lik ilk-sütun kuralı `:not(.gp-col-num)` ile bunu atlar.

**Tür rozeti genişliği:** card-table rozet sütunu EN UZUN tür adından hesaplanır
(`round(9.6*len)+22`); sabit taban yok. "FPS" -> 51 px, "Macera" -> 80 px.

**Specificity tuzağı (not):** eski GFN 3-sütun kuralı
`tr > :first-child:nth-last-child(3) ~ :nth-child(2)` (0,5,1) ağırlığında ve 2. sütunu ortalıyor.
`.gp-table-rank tr td` (0,4,2) ile aşılamaz; aynı desen `.gp-table-rank` önekiyle tekrarlanıp
(0,6,1) yapılmalıdır.

## Oyun açıklamaları: başlık -> fragman -> açıklama

`move_game_descriptions(html, game_names)` - sıralamayı tablo olarak verdiğimiz yazılarda
"Oyun Adı: açıklama" paragraflarını ilgili oyunun başlık + fragman bloğunun altına taşır ve
baştaki "Oyun Adı:" önekini kaldırır. Adlar UZUNDAN KISAYA denenir ve paragraf "sahiplenilir"
(yoksa "Halo 3", "Halo 3: ODST: ..." paragrafını kapar). Başlık eşleşmesi `.gp-game-name` içinde
TAM ad üzerinden yapılır. Karşılığı olmayan paragraf yerinde bırakılır.

## v10.10 - Kupa ikonu kaldırıldı, tablo başlığı h-tag değil, oyun adları bold değil

- **Kupa ikonu (trophy) ARTIK KULLANILMIYOR.** `render_card_table` çıktısında yok; `SVG_TROPHY`
  sabiti geriye dönük uyumluluk için duruyor ama DEPRECATED - yeni içerikte çağırma.
- **Tablo üstü başlık h-tag DEĞİL.** `<h3>` yerine `<div class="gp-ct-title">`; SEO başlık
  outline'ına girmiyor ama **H2 tipografisinde** görünüyor: masaüstü 32/40, mobil 21/28,
  New Science 600, düz `#FFC900` (gradient kaldırıldı), sola yaslı.
- **Tüm tablolarda oyun adları BOLD DEĞİL** (font-weight 400). Kalın yazı tabloda gereksiz yer
  kaplıyordu; hiyerarşi zaten renk (beyaz) ve sütun başlığıyla kuruluyor. Hem GFN oyun tablosunda
  hem sıralama tablosunda geçerli.

## v10.11 - İçindekiler: bölümler + TABLO ÜSTÜ BAŞLIKLAR; azalan mobil başlık ölçeği

**İçindekiler'e ne girer:**

| Öğe | ToC'de | İşaret |
|---|---|---|
| H1 (yazı başlığı) | ilk madde | **küçük nokta** (numaralarla aynı renk, #FFC900) |
| H2 (bölümler) | var | 01, 02, 03 ... |
| H3 oyun başlıkları | **yok** | - |
| H4 | **yok** | - |
| Tablo üstü başlıklar | **yok** | (id alırlar, bağlantı verilebilir) |

Alt numaralandırma (2.1 / 3.1) denendi ve VAZGEÇİLDİ - liste sadeliğini bozuyordu.
SSS bölümü tek satırdır (sorular `<summary>` olduğu için zaten başlık sayılmaz).

**Tablo üstü başlık (`.gp-ct-title`):** h-tag DEĞİL (SEO outline'ına girmez) ama **H3 ile aynı
renk ve ölçü**: masaüstü 28/36 beyaz, mobil 19/26. `render_card_table` her zaman basar;
`render_table(..., title="...")` ile normal tablolara da eklenebilir. Otomatik `id` alır ve
`inject_heading_ids` tarafından ToC'ye level 3 olarak toplanır.

**Tüm tablolarda sütunlar SOLA yaslı** (yalnız `.gp-col-num` sıra-no sütunu ortalı). Eski GFN
kuralı 2. sütunu ortalıyordu (`tr > :first-child:nth-last-child(3) ~ :nth-child(2)`, (0,5,1));
aynı desen sonra tekrarlanarak aşılır. Tür rozetleri de `justify-content: flex-start`.

**Mobil başlık ölçeği AZALAN:** h1 24/32 > h2 21/28 > h3 19/26 > h4 17/24. Oyun başlığı kendi
seviyesinin ölçüsünü kullanır (h3 ise h3 gibi); bu yüzden ölçeğin azalan olması şart.

**Karşılaştırma tablosunda sıra:** çıkış sırası yazının başında zaten verildiyse karşılaştırma
tablosunda ÖNCE hikaye (kronolojik) sırası gelir, sonra çıkış sırası. Tablonun üstüne ne olduğunu
anlatan bir başlık konur.

## Çıktıda yorum YOK

CMS'e giden HTML'de CSS/JS yorumu bulunmaz. Kaynakta yorumlar KALIR (bakım için gerekli):
`_STYLE_KAYNAK` ham stil bloğudur, `ANIMATED_BORDER_STYLE = _yorumsuz(_STYLE_KAYNAK)` ile
temizlenmiş hali üretilir. `render_floating_toc` da `<script>` bloğunu aynı süzgeçten geçirir.

`_yorumsuz(kod)`: `/* ... */` bloklarını atar, satır sonu boşluklarını siler, 3+ boş satırı tek
boş satıra indirir. Yeni kural yazarken yorumu rahatça ekleyebilirsin - çıktıya düşmez.

Etki: stil bloğu 44.993 -> 36.115 karakter; tipik yazı ~9.000 karakter küçüldü.

## v10.12 - İstatistik kartlarında ortalama + tablo ipucu tablonun dışına (6 Ağustos 2026)

Marka geri bildirimi. Kurallar `ANIMATED_BORDER_STYLE`'ın **EN SONUNDAKİ "v10.12" bloğunda**;
v10.8 dahil önceki tüm `.gp-cell` / `.gp-table-hint` ölçülerini bilinçli ezer. Yeni kural yazarken
ölçüyü BU bloğa yaz.

**1. İstatistik kartları (`.gp-cell`) yatayda ve dikeyde ortalı.** Kartlar grid öğesi olduğu için
`stretch` ile eşit yükseklik alıyordu, içerik ise kutunun üstüne yapışıyordu. Çözüm:

```css
.gp-content .gp-cell { display: flex; flex-direction: column;
  align-items: center; justify-content: center; text-align: center; }
.gp-content .gp-cell > * { width: 100%; }
```

Değer iki satıra sardığında da (ör. "Battlefield 6 S4") kart dengeli kalıyor. Masaüstü ve mobilde
üst/alt boşluk eşit ölçüldü (masaüstü 39/39 px, mobil 15/15 px).

**2. Sarı değer masaüstünde 1 punto küçültüldü: `28/36` -> `27/35`.** Mobil ölçüler (17/23, <=400 px
dahil) değişmedi. Rehberdeki 28/36'dan bilinçli ayrışma.

**3. "Tabloyu yana kaydır ->" ipucu artık `.table-wrap`'in DIŞINDA, hemen ÜSTÜNDE.** Eskiden kabın
içindeydi ve tablo çerçevesinin içine taşıyordu. Ölçü aynı (12/16 medium #B2B2B2), sola tablo
kabıyla hizalı. `render_table` çıktısı:

```html
<div class="gp-ct-title">...</div>          <!-- varsa -->
<div class="gp-table-hint">Tabloyu yana kaydır &rarr;</div>
<div class="table-wrap gp-table">
  <div class="gp-table-scroll"><table>...</table></div>
</div>
```

**Boşluk mantığı (dikkat):** ipucu görünürken üstteki 24 px'i O taşır, `.table-wrap`'in üst boşluğu
sıfırlanır; ipucu gizliyken kap 24 px'ini geri alır. Bu yüzden gizleme JS'te `display` ile DEĞİL
`.gp-hint-off` sınıfıyla yapılır - kardeş seçici (`.gp-table-hint:not(.gp-hint-off) + .table-wrap`)
sınıfı görebilsin diye. `display:none` ile gizlenseydi kardeş seçici yine eşleşir ve masaüstünde
tablo bir önceki paragrafa yapışırdı.

`render_floating_toc`'un `ipucuGuncelle` fonksiyonu ipucunu `.table-wrap`'in
`previousElementSibling`'i olarak arar; bulamazsa eski (kap içi) yerleşime düşer.

## v10.13 - Fırsatlar linki kaldırıldı, iki doküman hatası düzeltildi (18 Ağustos 2026)

**1. `/firsatlar` yönlendirmesi kalktı (marka kararı).** `render_end_cta`'nın ikinci buton
varsayılanı `"Güncel Fırsatlar" -> /firsatlar` iken **`"GeForce NOW Oyunları" -> /gfn/oyunlar`**
oldu. Kural ve hedef tablosu: `content-rules.md` -> Kural 19.

**2. `SVG_CHECK_GREEN` -> `SVG_CHECK`.** Sabitin adı yanıltıcıydı: içindeki `stroke` değeri
`#FFC900`, yani ikon yeşil değil SARI basıyor. `SVG_CHECK_GREEN` geriye dönük uyumluluk için
takma ad olarak duruyor (DEPRECATED), yeni kodda `SVG_CHECK` kullanılır. Kullanıldığı yerler:
`render_list(marker="check")` ve `render_info_card(style="checkmark")`.

**3. Hızlı Özet madde işareti = SARI `•`, tik DEĞİL.** `SKILL.md`'deki "✓ tikli maddeler" yorumu
v9'dan kalma yanlış bir nottu; `render_tldr` her zaman `<span class="gp-tldr-bullet">&bull;</span>`
basar ve CSS rengi `#FFC900`'dür. Kategori skill'iyle bu noktada fark YOKTUR.

**4. Kural 18'in tetikleyicisi düzeltildi.** Kontrol `'cta-ubisoft' in final_html` idi; bu sınıf
PAYLAŞILAN stil bloğunda da geçtiği için her yazıda tetikleniyordu. Artık yalnızca gövdeye bakıyor:
`final_html.split('</style>')[-1]`. Sınıf adına göre "bu bir Ubisoft yazısı mı" kararı verirken
stil bloğunu daima dışarıda bırak.

**Yeni safeguard'lar (`verify_output`):**

| Kontrol | Tip | Ne yakalar |
|---|---|---|
| Fırsatlar linki yok | FAIL | gövdede `gameplus.com.tr/firsatlar` |
| CTA bloğu içi çakışma yok | FAIL | kapanış CTA'sının iki butonu aynı adrese gidiyor |
| CTA hedefi sayfada tekrarlamıyor | UYARI | aynı hedef birden çok CTA id'sinde (hangi id'ler olduğunu yazar) |

## v10.14 - Gövde içi kategori linkleri (18 Ağustos 2026)

**1. Sayfa geneli CTA tekrar uyarısı KALDIRILDI.** Marka kararı: farklı CTA bloklarının aynı hedefe
gitmesi sorun değil. Tek kural, **aynı bloğun iki butonunun aynı adrese gitmemesi** (FAIL olarak
duruyor).

**2. `CATEGORY_ANCHORS` + `auto_link_categories` / `link_categories`.** Gövde paragraflarında doğal
geçen kategori ifadelerini GFN kategori sayfalarına bağlar (Kural 20). Anchor'lar Google Ads TR
arama hacmiyle sıralı; her kategori için çekim varyantları tanımlı ("FPS oyunu", "yarış oyunlarına").

**Linklenmeyen yerler:** başlık, tablo, liste, CTA metni, Hızlı Özet, Editör Notu, Hatırlatma ve
lisans/mağaza sayımı içeren cümleler. **Mağaza kategorileri** (Steam, Xbox, Epic Games, EA App,
Ubisoft Connect, GOG, Diğer) otomatik seçimden hariç - bu adlar gövdede mağaza bağlamında geçtiği
için otomatik link yanlış yere düşüyordu.

**Safeguard:** "Kategori linki 1-2 arası" (3'ü aşarsa FAIL) + "Gövde içi kategori linki" (0 ise UYARI).

## v10.17 - Link politikası (Kural 21)

Dış linkler `rel="nofollow noopener noreferrer"`, iç linkler `rel="noopener noreferrer"` (nofollow
YOK), ikisi de `target="_blank"`. Sayfa içi çapalar (`#bolum`) dokunulmaz - aksi halde İçindekiler
her tıklamada yeni sekme açar. Uygulama `apply_link_policy(body)`; üç otomatik kontrolle denetlenir.

## v10.18 - DOM genişliği: bileşenler `<section>` altında (Kural 22)

Sitebulb taraması iki blog sayfasında **"Avoid excessive DOM width"** uyarısı verdi. Hint'in eşiği
**bir ebeveynde 60'tan fazla çocuk düğüm**, önem derecesi **Low**. Ölçümde eşiği aşan tek eleman
`.gp-content` çıktı: cozy-games 67 element / 135 çocuk düğüm, 26 Ağustos GFN 52 element / 105 düğüm.
Sitenin kendi elemanları en fazla 5-13 çocuk taşıyor, yani genişlik tamamen bizim kabımızdan geliyordu.
(Sitebulb "child nodes" saydığı için bileşenler arasındaki satır sonları da sayıma giriyor.)

**Çözüm:** `group_into_sections(body)` - `wrap_gp_content`ten hemen önce çağrılır. Her `<h2>` yeni bir
`<section class="gp-sec">` başlatır; eşiği (varsayılan 50) aşan bölüm kalırsa `<h3>`, gerekirse `<h4>`
ile kardeş alt bölümlere ayrılır. `<h1>`, `<style>`, en üst seviye `<script>` ve floating ToC bölüm
dışında kalır - ToC `position: fixed` olduğu için bir ata elemana transform gelmesi riskine girilmez.

**Neden CSS güvenli:** kütüphanede tek bir `.gp-content >` doğrudan-çocuk seçicisi yok; tüm kardeş ve
konum seçicileri (`.table-wrap`, `.gp-cell`, `.tldr-block`, `.gp-card-table-inner`) bölüm içinde kalıyor.
`.gp-table-hint:not(.gp-hint-off) + .table-wrap` çifti hiçbir zaman bölüm sınırında ayrılmıyor.
`.gp-content` düz blok (flex/grid değil), `<section>` de varsayılan kenar boşluğu taşımıyor.

**Ölçülen sonuç (27 Ağustos yazısı):** `.gp-content` 105 -> 19 çocuk düğüm, en büyük bölüm 29 düğüm,
maliyet +176 karakter / +5 düğüm. 1280 px ve 390 px'te 53 öğenin konum ve boyutu birebir aynı;
toplam yükseklik 7393 px ve 11115 px olarak değişmedi. 28 kategori sayfasında `.gp-content` ortalama
141 -> 35 düğüm; kategori sayfasında da 88 öğede fark sıfır.

**Kural 22 kontrolü:** `verify_output` ve `verify_category_output` içinde "DOM genişliği (Kural 22)";
60 çocuk düğümü aşarsa UYARI verir ve `group_into_sections` çağrılmasını hatırlatır.

**Ayrı hint - "Avoid excessive DOM size" (1500 element):** bizim yazılarımızı ilgilendirmiyor.
Blog sayfaları 615-702 element bandında; eşiği aşanlar site şablon sayfaları (`/blog` 2075, `/destek` 2008).

**Parser notu:** `_element_sonu` içinde `html.lower()` KULLANILMAZ. Türkçe `İ` küçültülünce iki karaktere
("i" + birleşik nokta) dönüşüp tüm indeksleri kaydırıyor; script kapanışı yanlış yerde bulunuyordu.
Büyük/küçük harf duyarsızlık `re.compile(..., re.I)` ile sağlanıyor.

## v10.19 - Yazım güvenlik ağı: Türkçe İ tuzağı (Kural 23)

Kategori skilinde (v12.3) "Indie" yazımı otomatik düzeltiliyor. Blogda yazarın metni
DEĞİŞTİRİLMEZ, bu yüzden aynı kural burada otomatik düzeltici olarak değil **iki uyarı**
olarak duruyor:

1. **"Yazım: İngilizce terimde Türkçe İ"** - gövdede `İndie`, `İntel`, `İnstagram`, `İnput`,
   `İnterface`, `İnventory`, `İtem`, `İndex`, `İnstall`, `İOS`, `İD` geçerse uyarır.
   İngilizce sözcükler Türkçe büyük İ ile yazılmaz. (`İnternet` Türkçeleşmiş sözcük olduğu
   için listede yoktur.)

2. **"Büyük harf tuzağı (lang=tr)"** - `.gp-gic-badge`, `.gp-note-eyebrow` ve `.gp-cta-eyebrow`
   CSS'te `text-transform: uppercase` taşır. Sayfa `lang="tr"` olduğu için tarayıcı `i` harfini
   Türkçe kuralıyla `İ`ye çevirir: kaynakta `Indie` yazan etiket ekranda **INDİE** görünür
   (tarayıcıda doğrulandı). Bu yüzden CSS ile büyütülen etiketlerin metninde küçük `i`
   bulunmamalı; etiket kaynakta doğru büyük harfle yazılır (İngilizce terim düz I, Türkçe İ).

Mevcut çıktılarda ikisi de temiz; kontroller ileride bozulmaması için var.
