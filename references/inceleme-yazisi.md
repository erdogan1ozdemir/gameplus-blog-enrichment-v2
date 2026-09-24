# Yeni içerik yazımı: yapı, dil, SEO/GEO ve doğrulama (v10.25)

Tek bir oyunu değerlendiren yazılar için. Marka onayıyla oturan tarz, ilk olarak
**The Blood of Dawnwalker İncelemesi** (24 Eylül 2026) ile uygulandı; üretim dosyası
`examples/build-inceleme-reference.py`.

Bu dosya yalnız inceleme için değil, **listicle, rehber ve derleme dahil her yeni blog içeriği** için geçerlidir:
sayı yuvarlama, topluluk ifadeleri, öneri dili ve kaynak doğrulama maddeleri her yazıda uygulanır.

> **Kapsam uyarısı.** Buradaki tarz kuralları **yeni içerik yazarken** geçerlidir. Kullanıcı hazır
> bir taslak ilettiğinde yazarın metnine dokunulmaz: sayı yuvarlanmaz, kelime değiştirilmez, cümle
> yumuşatılmaz (content-rules kural 1). Tarz o durumda yalnız bizim eklediğimiz parçalara
> (Hızlı Özet, editör notu, hatırlatma, CTA metinleri, SSS yanıtları) uygulanır.

## 1. Bölüm akışı

Sıra sabit değil ama bu iskelet onaylandı:

1. **Başlıksız giriş (2 paragraf).** İlk paragraf oyunu tek cümlede kurar (kim, nerede, ne yapıyor);
   ikinci paragraf stüdyoyu, çıkış tarihini ve varsa satış/ilgi verisini verir ve yazının sorusunu koyar.
2. **`{Oyun} Nedir?`** - tür, yayıncı, motor, platformlar, stüdyo geçmişi. Fragman bu bölümde.
3. **`{Oyun} Hikayesi Neyi Anlatıyor?`** - kurulum, ton, anlatı yapısı. Spoiler yok.
4. **Oyunun en çok tartışılan sistemi** - ne olduğu, nasıl işlediği (madde listesi), eleştirmen
   ve oyuncu tarafının nasıl ayrıştığı. Editör notu buraya girer.
5. **`{Oyun}'da Dövüş Nasıl İşliyor?`** - mekanikler, ilerleme, eleştiriler.
6. **`{Oyun} Puanları: Metacritic ve OpenCritic`** - puan tablosu + yorum. İlk cümle puanı tarihle
   verir, tablonun başlığında da **ölçüm tarihi** bulunur ("Puan Tablosu (24 Eylül 2026)").
7. **`{Oyun} Türkçe mi, Kaç Saat Sürüyor?`** - Türkçe dil desteği, süre, donanımın iki cümlelik özeti.
8. **`{Oyun} Alınır mı?`** - ilk cümle doğrudan cevap; ardından "tam sana göre" (tikli) ve
   "beklentini ayarla" (noktalı) diye **iki ayrı liste**. Olumlu ve uyarı maddeleri aynı tikli
   listede durmaz; işaret ile içerik çelişir.
9. **`Genel Değerlendirme`** - iki paragraf: ne iyi, ne eksik. Kendi puanımızı vermeyiz.
10. **`{Oyun} GeForce NOW'da Oynanır mı?`** - **tek paragraf**, "Evet, ..." ile açılır (bkz. 4).
11. **SSS** - 6-8 soru, arama talebinden (bkz. 9).

Listicle ve rehberde bölüm akışı içeriğe göre değişir; **7-11. bölümlerdeki SEO/GEO kuralları
her yeni içerikte aynen geçerlidir.**

Zorunlu bileşenler değişmez: Hızlı Özet (3-6 madde), info-card (4 metrik), İçindekiler, CTA Paketler,
Editör Notu, Hatırlatma, tercih edilen kaynak kartı, kapanış CTA'sı, FAQ akordiyonu + FAQ şeması.

## 2. Sayılar: yuvarla, ham bırakma

Marka kararı: gövdede ham büyük sayı durmaz, okunur biçimde yuvarlanır.

| Ham veri | Yazıda |
|---|---|
| 25.851 inceleme | **25 binden fazla inceleme** |
| 517 inceleme | **500'den fazla inceleme** |
| 1.274 oy | **1.200'den fazla oy** |
| ana hikaye 21,5 saat | **20 saatin üzerinde** / info-card'da **20 Saat+** |
| yan görevlerle 34,5 saat | **35 saat civarı** |

Yuvarlama **aşağı** yapılır, abartılmaz. Puanların kendisi (84, 83, 8.3, %87) ve eleştirmen sayısı
gibi küçük kesin değerler (152, 70) olduğu gibi kalır. Tarih ve sürüm numaraları yuvarlanmaz.

## 3. Dil

- **"Türk oyuncular" denmez.** Yerel tepki için **"yerli oyuncu toplulukları"**, uluslararası tepki
  için **"globaldeki oyuncu toplulukları"** kullanılır. Veri etiketi olarak "Steam Türkçe yorumlar"
  tablo satırında kalabilir.
- **Editör notu ve öneriler yumuşak kurulur.** "Fazla kafa yorma" gibi buyurgan ya da küçümser
  ifadeler yerine olanak dili: "**çok takılmadan ilerleyebilirsin**", "rahatça takip edebilirsin".
- **Basın/yayın adı verilmez (v10.26).** İncelemeler araştırılır, bulgular derlenip genel bir
  inceleme gibi yazılır. "IGN'e göre", "GameSpot 9 verdi", "RPGFan'ın ifadesiyle" yazılmaz.

| Yazılmaz | Yazılır |
|---|---|
| "RPG Site ve RPGFan gibi kaynaklar yan karakterlerin yazımını türün en iyileri arasında gösterdi." | "The Blood of Dawnwalker'da yan karakterlerin yazımı ve diyalogların kalitesi türün son yıllardaki en iyi örnekleri arasında gösteriliyor." |
| "IGN sistemi yılın en cesur tercihi olarak gösterdi, PC Gamer baskının hissedilmediğini yazdı." | "Bir kesim eleştirmen sistemi yılın en cesur tasarım tercihlerinden biri olarak görüyor; diğerleri baskının pratikte sanıldığı kadar hissedilmediğini söylüyor." |
| "GameSpot'un ölçümüne göre 30 saat" | "Eleştirmenlerin oynama sürelerine göre 30 saat civarı" |
| Puan tablosunda GameSpot 9/10, IGN 8/10 satırları | "Eleştirmen puan aralığı: 3/5 ile 9/10 arası" |

  Anılabilenler: toplayıcılar (OpenCritic, Metacritic), HowLongToBeat, mağazalar, geliştirici ve
  yayıncı açıklamaları. `verify_output(..., yeni_icerik=True)` basın adında FAIL verir.
- Olumsuz bulgular saklanmaz; "eksik taraflar da var" paragrafı yazının parçasıdır.
- Em dash yok, klişe açılış yok, hype yok (content-rules kural 16).

## 4. GeForce NOW bölümü ve sistem gereksinimleri

- **GFN bölümü tek paragraf.** Oyunun kütüphaneye eklendiği bilgisi doğrudan yazılır
  ("NVIDIA'nın duyurusuna göre" gibi atıf yapılmaz, paket şartı yazılmaz). Paragraf şunları taşır:
  oyunun kütüphanede olup olmadığı,
  indirme boyutunu beklemeden başlama, donanımın bulutta kalması, kayıtların mağaza hesabında
  durması. Ardından **Hatırlatma** bloğu (lisans) gelir.
- **Oyun detay sayfası henüz yayında olmadığı için o sayfaya link verilmez.** Açıldığında bu kural
  güncellenir.
- **Sistem gereksinimleri tablosu blogda yer almaz.** Tam tablo oyun detay sayfasının işidir; blogda
  iki cümlelik özet kalır ("minimum listede GTX 1060 seviyesi, önerilen liste RTX 4060 sınıfı,
  kurulum için 60 GB SSD").
- **SSS'de GFN ve Türkçe dil soruları KALIR** (marka kararı): "GeForce NOW'da oynanabiliyor mu"
  ve "Türkçe dil desteği var mı" soruları blogda da karşılanır.

### Oyun detay sayfasıyla çakışmayı azaltmak

İkisi aynı oyunu anlatır; ayrım niyette kurulur. Blog "nasıl bir oyun, alayım mı", detay sayfası
"bu oyunu burada nasıl oynarım" sorusunu karşılar.

| Konu | Blog incelemesi | Oyun detay sayfası |
|---|---|---|
| Puanlar | Kendi bölümü + tablo + eleştirmen ayrışması | Girişte bir iki satır |
| Hikaye ve oynanış | Yorumlu, eleştirili | Spoilersız, sistem ve terim odaklı |
| GeForce NOW | Tek paragraf | Sayfanın omurgası (erişim, cihaz, kontrol, hız tablosu) |
| Sistem gereksinimleri | İki cümle | Tam tablo + "bulutta gerekmiyor" karşıtlığı |
| Kimler sevecek / genel değerlendirme | Var | Yok |
| SSS | Değerlendirme soruları + GFN ve Türkçe dil | Erişim soruları (kaç GB, hangi mağaza, kumanda) |

## 5. Kaynaklar ve doğrulama

İncelemede geçen her sayı kaynaklıdır. Kullanılan kaynak seti:

| Veri | Kaynak |
|---|---|
| Stüdyo, yayıncı, çıkış, diller, sistem gereksinimleri, başarım | Steam `appdetails` API |
| Oyuncu tepkisi ve inceleme sayısı | Steam `appreviews` API (`language=all` ve `language=turkish`) |
| Eleştirmen ortalaması, tavsiye oranı, puan aralığı (tek tek site puanları metne yazılmaz) | OpenCritic oyun sayfası |
| Metascore ve kullanıcı puanı | Metacritic oyun sayfası |
| Yapım geçmişi, sistemler, eleştiri özeti | Wikipedia |
| Süre (ana hikaye / yan görevler / %100) | HowLongToBeat |
| GFN kütüphanesinde olup olmadığı | NVIDIA GFN blog duyurusu (tarihli) |
| Topluluk tonu | Steam yorumları ve YouTube inceleme yorumları |

**Sayfanın gerçekten o oyuna ait olduğu doğrulanır.** OpenCritic gibi siteler URL'deki slug'ı yok
sayıp id'ye bakar: `opencritic.com/game/20364/the-blood-of-dawnwalker` adresi **Breath of Fire IV**
sayfasını açıyordu. Her sayfada `h1`/`<title>` okunur, oyun adı eşleşmiyorsa veri alınmaz; doğru
kayıt sitenin kendi aramasından bulunur.

**Doğrulanmayan teknoloji iddiası yazılmaz.** DLSS, ışın izleme, HDR ve Reflex yalnız oyunun mağaza
sayfasında ya da NVIDIA duyurusunda geçiyorsa yazılır.

## 6. Gömülü video: yaş kısıtlısı kullanılmaz

Yaş kısıtlı YouTube videoları gömülü oynatılmaz; okuyucu kartın yerinde
"Sorry, this content is age-restricted" uyarısı görür. Çıkış fragmanları sık sık kısıtlıdır
(Dawnwalker çıkış fragmanı `pNTT7lknCE0` örneği).

Kontrol tarayıcıda yapılır; `curl` ile güvenilir sonuç alınmaz (veri merkezi IP'lerinde YouTube her
videoyu kapılı gösteriyor). Yöntem:

```bash
python3 scripts/video_yas_testi.py <video_id_1> <video_id_2> ...   # test sayfası üretir
```

Üretilen sayfa tarayıcıda açılır, oynatıcıda uyarı çıkan adaylar elenir. Kısıtsız bir resmi video
bulunamazsa yayıncının genel bakış videosu ya da mağaza kanalının (GOG, PlayStation) fragmanı
tercih edilir; hiçbiri uygun değilse yazı videosuz yayınlanır.

## 7. Yazmadan önce: arama verisi (brief adımı)

Detay sayfalarında olduğu gibi blogda da metin, arama verisi toplandıktan sonra yazılır. Dawnwalker
ve CONTROL Resonant incelemelerinde bu adım atlandığı için SEO/GEO denetiminde 72-80 puan çıktı;
eksiklerin çoğu bu adımdan kaynaklandı.

DataForSEO ile (Türkiye `location_code` 2792, `language_code` "tr"):

| Ne | Endpoint | Neden |
|---|---|---|
| Hacim | `keywords_data/google_ads/search_volume/live` | Ana kelime, kısa ad, **alternatif ad**, niyet ekleri (inceleme, türkçe, kaç saat, sistem gereksinimleri, metacritic, çıkış tarihi) |
| SERP | `serp/google/organic/live/advanced` (`people_also_ask_click_depth: 1`) | PAA soruları, ilgili aramalar, Türkçe rakipler, bilgi paneli |

Yeni çıkan oyunda 12 aylık ortalama yanıltır; **çıkış ayının hacmi** ayrıca okunur (Dawnwalker:
ortalama 2.400, Ağustos 6.600; "metacritic" eki ortalama 50, Ağustos 590). Rakip analizinde Türkçe
inceleme olup olmadığına bakılır: Dawnwalker'da ilk 20'de hiç Türkçe inceleme yoktu (fırsat),
CONTROL Resonant'ta Oyungezer 12. sıradaydı.

### Brief Excel'i (v10.27)

Toplanan veri yazıya geçmeden önce **brief Excel'ine** bir satır olarak yazılır; sonraki yazılar da
aynı dosyaya eklenir. **Yalnız yeni içerik taleplerinde** brief yazılır; kullanıcı hazır taslak
ilettiğinde brief yok.

- Dosya: `Game+  copy/Game+ Blogları/Game+ Blog Briefleri.xlsx` (sayfa: `Blog Briefleri`).
- Script: `scripts/blog_brief_satiri.py` → `brief_yaz(yol, satir)`. Aynı "Oyun / Konu" satırı varsa
  güncellenir, yoksa eklenir. Meta Title 60, Meta Description 160 karakteri aşarsa uyarı verir.
- Sütunlar: A Tarih · B Oyun / Konu · C İçerik Tipi · D Main KW · E Main KW Hacim · F İkincil
  Kelimeler · G Alt Başlıklar (H2) · H İçerik Kurgusu · **I Listelemede gözükecek başlık (Title)** ·
  J Link Verilecek Sayfalar · K SSS'ler · L Yanıt Biçimi · **M Meta Title** · N Slug ·
  **O Meta Description** · P Durum. I, M, O konumları markanın kendi tablosuyla aynı.
- Hacim hücresine 12 aylık ortalama ile çıkış ayının hacmi birlikte yazılır ("1.000 (Ağustos 2026: 3.600)").
- Listeleme başlığı yazının H1'i olur; Meta Title ondan kısa ve arama odaklıdır ("... İncelemesi ve Rehberi").
- Meta Description soru ya da değer cümlesiyle açılır, "Gameplus'ta okuyabilirsin / keşfet" gibi
  öneri diliyle kapanır (markanın Dawnwalker ve Resonant örnekleri).

## 8. Başlık ve ilk cümle (answer-first)

- **Her H2'nin ilk cümlesi başlığın sorusunu yanıtlar.** Geçiş cümlesiyle açılmaz.

| Önce | Sonra |
|---|---|
| "Oyunun en çok konuşulan tarafı bu." | "Zaman, yalnızca hikayeyi etkileyen adımlar attığında ilerliyor; açık dünyada gezmek takvimden gün götürmüyor." |
| "Gündüz Coen bir insan." | "Dövüş, Coen'in o anki haline göre ikiye ayrılıyor: gündüz ... kılıçla, gece ... pençe ve ısırıkla." |
| "En büyük değişiklik burada." | "Dövüş, ilk oyundaki silah ve telekinezi ağırlıklı yapıdan yakın dövüşe geçti." |

- **H2'lerin çoğunda oyun adı geçer** ve başlık arama niyetini taşır ("Alınır mı?", "Türkçe mi,
  Kaç Saat Sürüyor?", "Puanları: Metacritic ve OpenCritic"). Hepsine zorla eklenmez.
- Başlık en fazla iki konu taşır.

## 9. SSS: arama talebinden

- Sıra: PAA ve ilgili aramalardaki sorular önce (alınır mı, kaç saat, platformlar, sistem
  gereksinimleri, çıkış tarihi, alternatif ad), ardından marka soruları.
- **Türkçe dil ve GeForce NOW soruları her yazıda kalır.**
- Doğrulanamayan soru yazılmaz (Dawnwalker PAA'sındaki "romance" sorusu kaynak bulunamadığı için
  alınmadı).
- 20-60 kelime, ilk cümle doğrudan cevap, gövdedeki cümleyi birebir tekrar etmez.

## 10. Zaman ifadeleri: tarihli yaz

Yayın tarihi belli olmadığı için göreli ifade yazılmaz; puanlar yine verilir ama tarihle.

| Yazılmaz | Yazılır |
|---|---|
| "bugün çıktı" | "24 Eylül 2026'da çıktı" |
| "Oyun bu yazı hazırlanırken yeni çıktığı için Steam'de kullanıcı incelemesi bulunmuyor" | Hiç yazılmaz: veri yoksa alan kaldırılır (bkz. aşağı) |
| "Oyun, çıkışından üç hafta sonra olumlu bir tabloya sahip" | "24 Eylül 2026 itibarıyla ... puana sahip" |
| "çıkıştan bir hafta sonra" | "çıkışı izleyen hafta içinde" |

### Veri yoksa alan yazılmaz (v10.28)

Oluşmamış bir metrik (çıkış gününde Steam kullanıcı incelemesi, Metacritic kullanıcı puanı "tbd")
tabloya "-" satırı olarak ya da metne "henüz oluşmamıştı" açıklaması olarak girmez; alan tamamen
çıkarılır ve yazı mevcut veriyle kurulur. Puan tablosu o durumda yalnız eleştirmen verisini taşır
(OpenCritic, Metacritic, puan aralığı). Marka kararı, CONTROL Resonant incelemesi (24 Eylül 2026).

## 11. Linkler

| Link | Durum | Not |
|---|---|---|
| OpenCritic, Metacritic, HowLongToBeat, SteamDB | **Verilir** | Puan ve süre cümlesinin içinde, kaynak adı anchor olur |
| Mağazalar, resmi geliştirici/yayıncı sitesi | Verilir | Gerekiyorsa |
| **Oyun basını / rakip yayınlar** (GameSpot, IGN, PC Gamer, Eurogamer, Oyungezer, Technopat ...) | **ASLA** | Metinde kaynak olarak anılır, link verilmez. `apply_link_policy` çözer, `verify_output` FAIL verir |
| İlgili GFN Thursday yazısı | Verilir (iç link) | GFN bölümünde bir kez; önce `headline` ile doğrulanır (site soft 404 veriyor) |
| GFN kategori sayfası | 1-2 (Kural 20) | Doğal geçiş varsa |

Dış linkler `nofollow noopener noreferrer` + yeni sekme alır; iç linkler `noopener noreferrer` +
yeni sekme (Kural 21, `apply_link_policy` otomatik).
