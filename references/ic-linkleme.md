# İç linkleme yöntemi (v10.30)

Yeni yazılan her blog içeriğinde (inceleme, listicle, rehber) uygulanır. Kaynak: markanın 2025-2026
blog brief tablosu (90+ yazının iç link ve anchor listesi) ve canlı yazılardaki kullanım. Hazır gelen
taslakta yazarın metnine dokunulmaz; orada yalnız bizim eklediğimiz parçalara (SSS, notlar) link girer.

## 1. Hedef: yazı başına 7-11 gövde içi iç link

CTA düğmeleri ve tercih edilen kaynak kartı sayılmaz. Linkler gövde paragraflarına dağıtılır;
başlıkta, Hızlı Özet'te, tabloda ve CTA metninde iç link olmaz.

| Grup | Adet | Hedef | Marka anchor'u (tablodaki kullanım) |
|---|---|---|---|
| Sabit üçlü | 3 | `/gfn` · `/gfn/paketler` · `/gfn/oyunlar` | "GeForce NOW" · "GeForce NOW fiyat" · "GeForce NOW oyunları" |
| GFN kategori | 1-2 | `/gfn/oyunlar/<kategori>` | "aksiyon oyunları", "macera oyunları", "rol yapma oyunları", "fps oyunları", "strateji oyunları" |
| İlgili blog yazıları | 2-4 | `/blog/<slug>` | aranan kelime biçiminde, küçük harf: "açık dünya oyunları", "souls like oyunlar", "en iyi hikayeli oyunlar", "remake oyunlar" |
| GFN Thursday | 1 | oyunun buluta geldiği haftanın yazısı | "3 Eylül 2026 tarihli GFN Thursday yazısında" |

Sabit üçlü markanın neredeyse her yazısında var (tabloda 89 / 88 / 73 kez). Yerleşim, canlı
yazılardaki gibi GFN bölümünün sonunda tek cümlede: "Güncel **GeForce NOW fiyat** bilgisine ve
kütüphanedeki diğer **GeForce NOW oyunlarına** de göz atabilirsin." `/gfn` linki GFN bölümünün
ilk cümlesindeki "GeForce NOW" ifadesine verilir.

## 2. İlgili blog yazısı seçimi

1. Aday havuzu: `https://gameplus.com.tr/sitemap-blog.xml` + marka tablosundaki URL'ler.
2. Seçim ölçütü: yazının bir bölümüyle doğrudan bağ (aynı seri, aynı tür, sorulan soru).
   Örnekler: Dawnwalker → The Witcher 3 incelemesi ve The Witcher serisi (aynı ekip);
   Onimusha → remake nedir ("remake mi?" sorusu), souls like oyunlar ("Sekiro gibi mi?"),
   Assassin's Creed Shadows (feodal Japonya); Türkçe bölümü → Türkçe dublajlı ve altyazılı oyunlar.
3. **Her URL canlıda doğrulanır:** gameplus.com.tr olmayan blog adresine de 200 döndürür (soft 404).
   Sayfadaki `"headline"` JSON'u okunur; yoksa link verilmez (ör. `dlss-ve-ray-tracing-nedir`
   tabloda geçiyor ama yayında değil).
4. İçeriği bizim yazımızla ilgisiz olan listeye "beklenen oyunlar" diye link verilmez: hedef
   yazıda oyun geçmiyorsa bağ kurulmaz (2026 takvimi yazılarında Control/Onimusha yoktu).

## 3. Anchor kuralları

- Anchor, hedef sayfanın arandığı kelimedir; cümle içinde doğal akar. "tıklayın", "bu yazı" yok.
- Marka tablosundaki anchor önceliklidir; daha doğal ya da arama değeri daha yüksek bir
  karşılık varsa o kullanılır ("GeForce Now oyunlar" yerine Türkçe çekimli "GeForce NOW oyunları").
- Yazım: "GeForce NOW" (büyük NOW), kelime anchor'ları küçük harf, oyun adları özgün yazımıyla.
- Aynı URL'ye bir yazıda tek link (CTA düğmesi hariç). Aynı kategoriye iki link verilmez;
  `auto_link_categories(..., haric=(...))` ile elle verilen kategori dışarıda tutulur.
- Bağlantı cümlesi öneri dilinde kurulur: "listemize de bakabilirsin", "yazımıza da göz atabilirsin",
  "iyi bir sonraki durak olabilir".

## 4. Build notları

- `auto_link_categories` içinde link olan paragrafı atlar; elle link eklenen paragraftaki kategori
  ifadesi otomatik bağlanmaz. Kategori linkleri bu yüzden gerekiyorsa elle yazılır.
- Paragraf metni değişince, bileşen yerleşimi için kullanılan `veri.startswith(...)` tetikleri
  kontrol edilir (link eklenen cümle başı tetiği bozar; Hatırlatma bloğu düşebilir).
- Brief Excel'inin "Link Verilecek Sayfalar" sütunu bu tabloya göre doldurulur: iç linkler anchor ile,
  dış linkler (OpenCritic, Metacritic, HowLongToBeat) ayrı satırda.
