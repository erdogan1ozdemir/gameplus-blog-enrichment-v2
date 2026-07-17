# GA4 Tıklama Takibi — CTA id'leri

Blog gövdesindeki CTA butonları **sabit `id`** taşır. Id'ler her yazıda AYNI kalır (yazıya/tarihe göre değişmez), böylece tek bir GTM kuralı tüm blog arşivini kapsar. Id doğrudan `<a>` etiketinin üzerindedir.

## Tanımlı id'ler

| `id` | Bileşen | Buton | Hedef |
|---|---|---|---|
| `packages-button` | `render_cta_paketler` | GeForce NOW Paketleri → | `/gfn/paketler` |
| `games-button` | `render_cta_oyunlar` | GeForce NOW Oyunları → | `/gfn/oyunlar` |
| `end-packages-button` | `render_end_cta` (dolu sarı, birincil) | GeForce NOW Paketleri → | `/gfn/paketler` |
| `end-games-button` | `render_end_cta` (çerçeveli, ikincil) | değişken | genelde `/gfn/oyunlar` |
| `featured-game-button` | `render_compact_cta` (Öne Çıkan Oyun) | değişken | genelde `/gfn/paketler` |
| `ubisoft-packages-button` | `render_ubisoft_cta` | Ubisoft+ Paketlerini İncele | `/ubisoft/paketler` |

## Hangi yazıda hangileri
- **GFN Thursday:** `featured-game-button` + `end-packages-button` + `end-games-button`
- **Rehber / listicle:** `packages-button` + `end-packages-button` + `end-games-button` (`games-button` opsiyonel)
- **Ubisoft yazıları:** ek olarak `ubisoft-packages-button`

## GTM kurulumu (linkler aynı domaine gittiği için GA4 otomatik ölçmez)
1. **Değişken:** yerleşik `Click ID` aktif (Variables → Configure → Click ID).
2. **Tetikleyici:** Click - Just Links → *Some Link Clicks* → Click ID `matches RegEx`:
   ```
   ^(packages-button|games-button|end-packages-button|end-games-button|featured-game-button|ubisoft-packages-button)$
   ```
3. **Etiket:** GA4 Event, adı `blog_cta_click`, parametreler:

| Parametre | GTM değeri |
|---|---|
| `cta_id` | `{{Click ID}}` |
| `cta_url` | `{{Click URL}}` |
| `cta_text` | `{{Click Text}}` |
| `page_location` | `{{Page URL}}` |

4. **GA4:** Admin → Custom definitions'ta `cta_id`, `cta_url`, `cta_text` için custom dimension oluşturulmalı (yoksa raporda kırılım çıkmaz). İstenirse `blog_cta_click` key event olarak işaretlenebilir.

Çalışır örnek: `examples/ga4-cta-tracking-demo.html` (tarayıcıda aç, butona bas, GA4'e gidecek payload'ı gör).

## Sınır
Id'ler **sayfa başına tekil**dir; içerik kuralları her bloktan yazıda en fazla bir tane olmasını söyler. Bir yazıya ikinci bir aynı tip blok konursa id çakışır — `render_compact_cta(cta_id=...)` ile ayrı id verilebilir (örn. `featured-game-button-2`).
