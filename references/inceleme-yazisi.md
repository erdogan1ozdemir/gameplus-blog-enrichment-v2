# İnceleme yazısı: yapı, dil ve doğrulama (v10.24)

Tek bir oyunu değerlendiren yazılar için. Marka onayıyla oturan tarz, ilk olarak
**The Blood of Dawnwalker İncelemesi** (24 Eylül 2026) ile uygulandı; üretim dosyası
`examples/build-inceleme-reference.py`.

Bu dosya yalnız inceleme için değil, **genel blog yazılarının dili** için de geçerlidir:
sayı yuvarlama, topluluk ifadeleri, öneri dili ve kaynak doğrulama maddeleri her yazıda uygulanır.

## 1. Bölüm akışı

Sıra sabit değil ama bu iskelet onaylandı:

1. **Başlıksız giriş (2 paragraf).** İlk paragraf oyunu tek cümlede kurar (kim, nerede, ne yapıyor);
   ikinci paragraf stüdyoyu, çıkış tarihini ve varsa satış/ilgi verisini verir ve yazının sorusunu koyar.
2. **`{Oyun} Nedir?`** - tür, yayıncı, motor, platformlar, stüdyo geçmişi. Fragman bu bölümde.
3. **Hikaye** - kurulum, ton, anlatı yapısı. Spoiler yok.
4. **Oyunun en çok tartışılan sistemi** - ne olduğu, nasıl işlediği (madde listesi), eleştirmen
   ve oyuncu tarafının nasıl ayrıştığı. Editör notu buraya girer.
5. **Oynanış ve dövüş** - mekanikler, ilerleme, eleştiriler.
6. **`Eleştirmenler ve Oyuncular Ne Dedi?`** - puan tablosu + yorum. Tablonun başlığında **ölçüm
   tarihi** bulunur ("Puan Tablosu (24 Eylül 2026)").
7. **Teknik taraf** - Türkçe dil desteği, süre, donanımın iki cümlelik özeti.
8. **`Kimler Sevecek, Kimler İki Kez Düşünmeli?`** - madde listesi, dürüst ayrım.
9. **`Genel Değerlendirme`** - iki paragraf: ne iyi, ne eksik. Kendi puanımızı vermeyiz.
10. **GeForce NOW bölümü** - **tek paragraf** (bkz. 4).
11. **SSS** - 5 soru.

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
- Eleştiri aktarılırken kaynak belirtilir ("IGN'e göre", "PC Gamer tarafında"), yargı markaya
  mal edilmez.
- Olumsuz bulgular saklanmaz; "eksik taraflar da var" paragrafı yazının parçasıdır.
- Em dash yok, klişe açılış yok, hype yok (content-rules kural 16).

## 4. GeForce NOW bölümü ve sistem gereksinimleri

- **GFN bölümü tek paragraf.** Şunları taşır: oyunun kütüphanede olup olmadığı (kaynağıyla),
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
| Eleştirmen ortalaması, tavsiye oranı, tek tek puanlar | OpenCritic oyun sayfası |
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
