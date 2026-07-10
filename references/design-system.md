# Tasarım Sistemi — v10.1 "Game+ UI" (Figma: Blog Detail / GFN Thursday)

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
| H1 (yazı başlığı — gövde H1 ile başlar) | New Science SemiBold Extended | 40/48 | #fff |
| H2 (bölüm) | New Science SemiBold Ext | 28/36 | #fff |
| H3 | New Science SemiBold Ext | 24/32 | #fff |
| H4 | New Science SemiBold Ext | 20/28 | #fff |
| Stat değeri (karosel, ortalı) | New Science SemiBold Ext | 24/32 | **#FFC900** |
| Gövde paragraf | Greycliff CF Regular | 20/24 (mobil 16/24) | #B2B2B2 |
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
- **Dönen sarı glow (`gp-conic`, `--gp-glow:#FFC900`):** TLDR + CTA Paketler/Oyunlar + End CTA + Öne Çıkan Oyun.
- İkonlar: TLDR + Editör Notu → doküman (SVG_DOC); Hatırlatma → ampul (SVG_BULB); Öne Çıkan eyebrow → **gamepad** (sarı stroke; yıldız değil).
- İlgili yazı kartları: gerçek kapak görseli (`img` alanı = og:image) + koyu gradient overlay + GFN THURSDAY etiketi.
- Linkler: **alt çizgi yok, renk değişimi yeterli.** Dış platform linki: `color:inherit` + ↗ ikon (SVG_EXT_LINK).

## GA4 tıklama id'leri (statik — her yazıda aynı)
`packages-button` · `games-button` · `end-packages-button` · `end-games-button` · `featured-game-button` · `ubisoft-packages-button`
