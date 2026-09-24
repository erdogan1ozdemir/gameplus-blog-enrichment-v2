# -*- coding: utf-8 -*-
"""The Blood of Dawnwalker incelemesi -> v10.23 enriched HTML + doc (metin + HTML).

Kaynaklar (hepsi 24 Eylul 2026'da dogrulandi):
- Steam magaza sayfasi ve inceleme ozeti (appid 3751260): gelistirici, cikis, diller, sistem
  gereksinimleri, 25.851 inceleme / %87 olumlu, Turkce 517 inceleme / %93 olumlu.
- OpenCritic (game/20499): Top Critic Average 84, elestirmenlerin %94'u tavsiye, 152 inceleme.
- Metacritic: 83 (70 elestirmen), kullanici 8.3 (1.274 oy).
- Wikipedia: yapim, 30 gun sistemi, Rebel Wolves ve Konrad Tomaszkiewicz, 3 gunde 1 milyon satis.
- HowLongToBeat (game/144338): ana hikaye 21,5 saat; yan gorevlerle 34,5 saat; %100 icin 50 saat.
- NVIDIA blog (3 Eylul 2026): oyun cikis gunu GeForce NOW kutuphanesine eklendi.
- YouTube TR inceleme yorumlari: 30 gun sistemi ve Turkce dil destegi etrafindaki oyuncu tepkisi.
- Gomulu video: Bandai Namco resmi kanalindaki genel bakis videosu (_U88fNicSPg). Cikis fragmani
  (pNTT7lknCE0) YAS KISITLI; gomulu oynatilamiyor, tarayicida dogrulandi.
"""
import os
import re
import sys

SKILL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts")
sys.path.insert(0, SKILL)
from gameplus_blog_components import *  # noqa: F401,F403

OUT = os.environ.get("GAMEPLUS_OUT", os.getcwd())
TITLE = "The Blood of Dawnwalker İncelemesi: 30 Günde Vampir Olmak"
SLUG = "the-blood-of-dawnwalker-incelemesi"

# ---------------------------------------------------------------- gövde metni
P = []          # (tip, metin) - tip: h1 | h2 | p | yt


def h1(t): P.append(("h1", t))
def h2(t): P.append(("h2", t))
def p(t): P.append(("p", t))
def yt(vid, baslik): P.append(("yt", (vid, baslik)))


h1(TITLE)

p("Veba Avrupa'yı kırıp geçirirken, savaşlar da köyleri boşaltmış durumda. Vampirler tam olarak bu "
  "boşluğu bekliyordu. <strong>The Blood of Dawnwalker</strong> seni bu karanlığın ortasına bırakıyor "
  "ve gündüz insan, gece vampir olan Coen'in yerine koyuyor. Elinde ailesini kurtarmak için sadece "
  "30 gün var.")

p("Oyunu yapan ekip de en az konusu kadar dikkat çekici. Rebel Wolves'un kadrosunda The Witcher 3: "
  "Wild Hunt'ın yönetmeni Konrad Tomaszkiewicz ve CD Projekt RED'den ayrılan başka isimler bulunuyor. "
  "Stüdyonun ilk oyunu 3 Eylül 2026'da çıktı ve ilk üç günde bir milyondan fazla sattı. Peki ortaya "
  "çıkan iş, arkasındaki isimlerin gölgesinde kalıyor mu, yoksa kendi kimliğini kurmayı başarıyor mu?")

h2("The Blood of Dawnwalker Nedir?")
p("The Blood of Dawnwalker, 14. yüzyıl Avrupası'nda geçen açık dünya aksiyon rol yapma oyunu. "
  "Bandai Namco tarafından yayınlanıyor, Unreal Engine 5 ile geliştirilmiş ve PC'nin yanı sıra "
  "PlayStation 5 ile Xbox Series X|S'te de oynanabiliyor. Oyun, Karpatlar'da vampirlerin kontrolüne "
  "geçmiş kurgusal bir vadide, Vale Sangora'da geçiyor.")
yt("_U88fNicSPg", "The Blood of Dawnwalker Genel Bakış Videosu")
p("Rebel Wolves 2022'de kuruldu ve Dawnwalker'ı tek seferlik bir yapım olarak değil, Coen'in "
  "farklı dönemlerde geçen kendi içinde kapalı hikayelerinden oluşan bir serinin ilk halkası olarak "
  "tasarladı. Çıkıştan bir hafta sonra stüdyonun devam oyunu için ilan vermeye başlaması da bu planın "
  "işlediğini gösteriyor. Oyun tamamen tek kişilik; çok oyunculu bir mod bulunmuyor, kontrolcü desteği "
  "tam ve stüdyo oyunu gamepad ile oynamayı öneriyor.")
p("Ana karakter Coen, köylü bir genç iken vampir kanıyla dönüşüme uğruyor ve iki tarafın arasında "
  "sıkışıyor: gündüz insan kalıyor, gece vampir güçlerine kavuşuyor. Bu ikili yapı yalnızca bir "
  "hikaye detayı değil, oyunun bütün sistemlerinin üzerine kurulduğu temel.")

h2("Hikaye: Vale Sangora'da Geçen 30 Gün")
p("Coen'in derdi dünyayı kurtarmak değil, ailesini vampir lordu Brencis'in elinden almak. Oyun bu "
  "hedefi bir zaman sınırına bağlıyor ve sana 30 oyun günü veriyor. Klasik anlamda çizgisel bir ana "
  "görev zinciri yok; hikaye senin hangi görevi hangi sırayla aldığına, kimi dinlediğine ve neyi "
  "atladığına göre şekilleniyor.")
p("Oyunun tonu baştan sona karanlık. Vebanın kol gezdiği köyler, kendi arasında bölünmüş bir "
  "vadi ve gece olunca kapıların sürgülendiği bir dünya var. Rebel Wolves bunu \"anlatı temelli "
  "açık dünya\" olarak tarifliyor: masaüstü rol yapma oyunlarındaki gibi, bir görevi kimin lehine "
  "çözdüğün sonraki kapıları açıyor ya da kapatıyor. Aynı göreve gündüz insan olarak gitmekle gece "
  "vampir olarak gitmek çoğu zaman iki ayrı çözüm anlamına geliyor.")
p("Yazım tarafı, incelemelerde en çok övülen yan oldu. RPG Site ve RPGFan gibi kaynaklar yan "
  "karakterlerin yazımını ve diyalogların kalitesini türün son yıllardaki en iyileri arasında "
  "gösterdi. GameSpot ise seslendirme ve senaryonun, başka bir oyunda sıradan kalabilecek açık dünya "
  "içeriğini bile ilgi çekici hale getirdiğini yazdı. Eurogamer, oyunu bir ilk yapım için fazlasıyla "
  "iddialı buldu ve The Witcher 3'ün çıtasına yaklaştığını söyledi. PC Gamer ise oyunu son yılların "
  "en iyi büyük bütçeli aksiyon rol yapma yapımlarından biri olarak gösterdi.")
p("Karşılaştırma kaçınılmaz olsa da her inceleme aynı yere varmıyor. TheGamer'ın değerlendirmesinde, "
  "iki oyunun ortak noktasının ortaçağ atmosferi ve benzer bir kahramandan ibaret olduğu, "
  "Dawnwalker'ın yapı olarak kendi yolunu çizdiği söyleniyor. Pratikte de öyle: haritadaki soru "
  "işaretlerini tek tek temizlediğin bir düzen yok, oyun seni neyi bırakacağına karar vermeye zorluyor.")

h2("30 Günlük Zaman Sistemi Nasıl İşliyor?")
p("Oyunun en çok konuşulan tarafı bu. Zaman, sen açık dünyada gezerken ilerlemiyor. Yani ormanda "
  "dolaşmak, eşya toplamak ya da bir mağarayı keşfetmek gününden bir şey götürmüyor. Takvim yalnızca "
  "hikayeyi etkileyen adımlar attığında ilerliyor:")
P.append(("liste", [
    "<strong>Görevler:</strong> ana hikayeyi ve önemli yan hatları ilerleten adımlar günün bir "
    "bölümünü harcıyor.",
    "<strong>Yetenek yatırımları:</strong> karakterini geliştirmek de zaman maliyetiyle geliyor, "
    "yani her yeni güç bir bedel.",
    "<strong>Gündüz ve gece tercihi:</strong> bir işi hangi vakitte hallettiğin hem çözüm yolunu "
    "hem de elindeki süreyi değiştiriyor.",
]))
p("Eleştirmenler bu sistemde ikiye ayrıldı. IGN, zamanı bir kaynak gibi harcatmanın oyunun her "
  "alanını güçlendirdiğini savundu ve sistemi yılın en cesur tasarım tercihlerinden biri olarak "
  "gösterdi. PC Gamer ise baskının pratikte sandığı kadar hissedilmediğini, sınırın çoğu zaman "
  "kağıt üzerinde kaldığını yazdı. Game Informer tarafında ise ters yönde bir eleştiri var: "
  "sınır yüzünden oyunu gereğinden fazla temkinli oynadığını belirtti.")
p("Oyuncu tarafında da tablo benzer. Yerli oyuncu topluluklarının yorumlarında 30 günün \"aceleye getirdiği\" "
  "yönünde sitemler var; buna karşılık ikinci kez oynamayı bu sınır sayesinde anlamlı bulanlar da "
  "az değil. Pratikte tek cümleyle özetlemek gerekirse: her görevi toplayıp sonra tek tek bitirme "
  "alışkanlığın varsa bu oyun o alışkanlığı bozuyor.")

p("Sistem pratikte şuna benziyor: bir görev zincirine girdiğinde saatler ilerliyor, gece oluyor, "
  "vampir tarafın açılıyor ve o sırada elindeki başka bir işin şartları değişiyor. Bu yüzden "
  "\"önce şu bölgeyi temizleyeyim, sonra ana göreve dönerim\" mantığı burada her zaman işlemiyor. "
  "İlk oynayışta bunu bir eksik gibi değil, hikayeyi kendi yolundan okumanın bedeli gibi düşünmek "
  "daha sağlıklı.")

h2("Gündüz İnsan, Gece Vampir: Dövüş ve Oynanış")
p("Gündüz Coen bir insan. Kılıçla, yön tabanlı bir dövüş sistemiyle savaşıyor; köylülerle konuşup "
  "işleri kan dökmeden çözme ihtimali de daha yüksek. Gece ise vampir tarafı devreye giriyor: "
  "pençeler, ısırık saldırıları ve gündüz çıkamadığın yerlere tırmanmanı sağlayan hareket kabiliyeti.")
p("Vampir tarafının bir de faturası var. Gece boyunca kan susuzluğunu yönetmen gerekiyor; "
  "beslenmezsen bunun bedelini çevrendeki insanlar ödüyor. Görev veren bir karakteri ya da bir "
  "tüccarı kaybetmek mümkün, bu da o hikaye kolunu tamamen değiştiriyor. Karakter gelişimi üç ayrı "
  "yetenek ağacına dağılmış durumda, dolayısıyla insan ve vampir taraflarından hangisine yatırım "
  "yapacağın kendi başına bir tercih.")
p("Dövüş, incelemelerde genel olarak olumlu karşılandı ama eleştirisiz değil. Birkaç eleştirmen "
  "ilk saatlerdeki öğrenme eğrisinin sert olduğunu, insan ve vampir dövüşünün zamanla birbirine "
  "benzediğini yazdı. Steam yorumlarında da benzer bir sitem var: yön tabanlı savuşturma bir süre "
  "sonra tekrara düşebiliyor ve düşman çeşitliliği yeterli bulunmuyor.")

h2("Eleştirmenler ve Oyuncular Ne Dedi?")
p("Oyun, çıkışından üç hafta sonra hem basın hem oyuncu tarafında olumlu bir tabloya sahip. "
  "Aşağıdaki değerler 24 Eylül 2026 itibarıyla geçerli:")
P.append(("puan_tablo", None))
p("Yerli oyuncu toplulukları için ayrı bir not düşmek gerekiyor: Steam'deki Türkçe yorumların büyük bölümü "
  "olumlu ve bunların önemli bir kısmı doğrudan Türkçe dil desteğine teşekkür ediyor. Bu ölçekteki "
  "bir yapımda Türkçe arayüz ve altyazının çıkışta hazır olması, yorumlarda puanı yukarı çeken "
  "belirgin bir etken.")
p("Globaldeki oyuncu topluluklarında olumsuz yorumların öne çıkan başlıkları ise performans dalgalanmaları, gamepad ile hareket "
  "kontrollerinin ilk günlerdeki tuhaflığı ve yukarıda değindiğimiz zaman baskısı. Oyunun ilk "
  "haftasında çıkan yamalar bazı kontrol sorunlarını çözdü, ancak optimizasyon hâlâ yorumlarda "
  "tartışılan bir konu.")

h2("Teknik Taraf: Türkçe Dil, Süre ve Donanım")
p("Oyun Türkçe arayüz ve altyazı desteğiyle geliyor; Türkçe seslendirme bulunmuyor. Süre tarafında "
  "HowLongToBeat verileri şöyle: ana hikayeye odaklanırsan 20 saatin üzerinde bir süre, yan "
  "görevlerle birlikte 35 saat civarı, her şeyi görmek istersen 50 saate yakın bir oynayış. Zaman sınırı nedeniyle tek bir "
  "oynayışta her şeyi görmek zaten mümkün değil.")
p("Oyunda 46 Steam başarımı, tam kontrolcü desteği ve DualSense uyumu bulunuyor. Tek kişilik bir "
  "yapım olduğu için çevrimiçi bir mod aramana gerek yok. Kayıtlar Steam Cloud ile senkronize "
  "ediliyor, bu da bilgisayar ile bulut arasında geçiş yapan oyuncular için pratik bir ayrıntı.")
p("Donanım tarafında minimum listede GTX 1060 seviyesi bir ekran kartı yeterli görülüyor; "
  "önerilen liste RTX 4060 sınıfına çıkıyor. Kurulum için 60 GB boş alan ve SSD isteniyor.")

h2("Kimler Sevecek, Kimler İki Kez Düşünmeli?")
p("Oyunun neyi iyi yaptığı kadar kime hitap ettiği de net. Kısa bir değerlendirme:")
P.append(("liste2", [
    "<strong>Hikaye odaklı RPG sevenler:</strong> yazım ve karakterler oyunun en güçlü tarafı, "
    "The Witcher 3'ten sonra benzer bir doygunluk arayan oyuncular burada karşılığını buluyor.",
    "<strong>İkinci kez oynamaya niyetli olanlar:</strong> 30 gün sınırı her oynayışta farklı bir "
    "hikaye kolu görmeni sağlıyor.",
    "<strong>Acelesiz keşif isteyenler:</strong> her görevi sırayla bitirmeyi seviyorsan zaman "
    "sistemi seni rahatsız edebilir.",
    "<strong>Yoğun aksiyon bekleyenler:</strong> dövüş tatmin edici ama temposu ölçülü; hızlı ve "
    "sürekli çatışma arıyorsan beklentini buna göre ayarla.",
]))

h2("Genel Değerlendirme")
p("The Blood of Dawnwalker, bir ilk oyun için beklenenin üzerinde bir iş. Yazım ve karakterler "
  "türün üst sınıfında; gece ve gündüz ayrımı yalnızca görsel bir tema değil, oynanışı gerçekten "
  "ikiye bölen bir sistem. Zaman sınırı ise oyunu sevip sevmeyeceğini belirleyen ana etken: bir "
  "kısıtlama olarak görürsen sinir bozucu, bir kural olarak kabul edersen her kararı anlamlı kılan "
  "bir tasarım.")
p("Eksik taraflar da var. Dövüş uzun oynayışlarda tekrara düşebiliyor, düşman çeşitliliği "
  "beklentinin altında kalıyor ve performans hâlâ yama bekleyen bir konu. Yine de 84 ortalama ve "
  "Steam'deki %87 olumlu oran, bu eksiklerin oyunun bütününü gölgelemediğini gösteriyor. Türe yakın "
  "başka yapımlar arıyorsan GeForce NOW kütüphanesindeki macera oyunları iyi bir başlangıç noktası.")

h2("The Blood of Dawnwalker'ı GeForce NOW ile Bulutta Oynamak")
p("Oyun, çıkış günü GeForce NOW kütüphanesine eklendi. 60 GB'lık kurulumu beklemeden buluttan "
  "başlatabiliyor, önerilen listedeki ekran kartına sahip olmasan da oynayabiliyorsun; işi senin "
  "bilgisayarın yerine bulut tarafındaki RTX destekli sunucular yapıyor ve kayıtların Steam "
  "hesabında durduğu için kaldığın yerden devam ediyorsun.")

h2("Sıkça Sorulan Sorular")

FAQ = [
    ("The Blood of Dawnwalker Türkçe dil desteği var mı?",
     "Evet. Oyun Türkçe arayüz ve altyazı desteğiyle çıktı, Türkçe seslendirme bulunmuyor. Steam'deki "
     "Türkçe yorumların çoğunluğu olumlu ve birçoğu doğrudan bu dil desteğine değiniyor."),
    ("The Blood of Dawnwalker kaç saatte bitiyor?",
     "HowLongToBeat verilerine göre ana hikaye 20 saatin üzerinde, yan görevlerle birlikte 35 saat "
     "civarında sürüyor. Her şeyi görmeyi hedefleyen oyuncular 50 saate yakın bir süreden söz ediyor."),
    ("30 günlük süre sistemi tam olarak nasıl işliyor?",
     "Zaman, açık dünyada gezerken ilerlemiyor. Yalnızca hikayeyi etkileyen görevler ve yetenek "
     "yatırımları günün bir bölümünü harcıyor. Ana hedefini bu 30 günlük takvim içinde tamamlaman "
     "gerekiyor, bu yüzden hangi görevi alacağın bir tercihe dönüşüyor."),
    ("The Blood of Dawnwalker GeForce NOW'da oynanabiliyor mu?",
     "Evet, oyun çıkış günü GeForce NOW kütüphanesine eklendi. Oynayabilmen için oyuna Steam gibi "
     "desteklenen bir mağazada sahip olman gerekiyor; GeForce NOW oyunu satmaz, senin kütüphanendeki "
     "oyunu bulutta çalıştırır."),
    ("The Witcher 2 sevenler The Blood of Dawnwalker'ı sever mi?",
     "The Witcher serisinin karanlık tonunu ve seçim ağırlıklı anlatımını sevdiysen bu oyun tanıdık "
     "gelir; ekipte The Witcher 3'ün yönetmeni yer alıyor ve incelemelerde iki seri sık sık yan yana "
     "anılıyor. Ancak Dawnwalker'ın 30 günlük zaman sınırı ve gece/gündüz döngüsü, oyunu daha planlı "
     "oynamanı gerektiren farklı bir deneyim haline getiriyor."),
]

# ---------------------------------------------------------------- bileşenler
puan_tablo = render_table(
    ["Kaynak", "Puan", "Kapsam"],
    [["OpenCritic", "84 (Top Critic Average)", "152 eleştirmen, %94 tavsiye ediyor"],
     ["Metacritic", "83", "70 eleştirmen incelemesi"],
     ["Metacritic kullanıcı", "8.3", "1.200'den fazla oy"],
     ["Steam", "%87 olumlu (Çok Olumlu)", "25 binden fazla inceleme"],
     ["Steam Türkçe yorumlar", "%93 olumlu", "500'den fazla inceleme"]],
    first_col_strong=False,
    title="The Blood of Dawnwalker Puan Tablosu (24 Eylül 2026)")

editor_note = render_editor_note(
    "Zaman sistemine ilk oynayışında çok takılmadan ilerleyebilirsin. Takvim yalnızca görevlerle ve "
    "yetenek yatırımlarıyla ilerlediği için keşfe ayırdığın saatler cebinden çıkmıyor. İlgini çeken "
    "yan hikayeleri rahatça takip edebilirsin; 30 gün, ana hedefi tamamlamak için yeterli bir süre.")

hatirlatma = render_highlight(
    "GeForce NOW oyun satmaz, sahip olduğun oyunları bulutta çalıştırır. The Blood of Dawnwalker'ı "
    "buluttan açabilmen için oyuna Steam, Epic Games Store, Xbox veya desteklenen diğer mağazalardan "
    "birinde sahip olman gerekir.")

cta_paketler = render_cta_paketler(
    "Vale Sangora'ya 60 GB indirme beklemeden gir",
    "GeForce NOW, kütüphanendeki desteklenen oyunları güçlü bir ekran kartına ihtiyaç duymadan "
    "bulut üzerinden çalıştırır. Paketleri karşılaştırıp sana uyanı seçebilirsin.")

end_cta = render_end_cta(
    "Coen'in 30 günü seni bekliyor",
    "Performance ve Ultimate paketleri, sahip olduğun GeForce NOW destekli oyunları güçlü bir "
    "bilgisayar olmadan çalıştırmanı sağlar. Paketleri inceleyip kütüphanendeki oyunlarla başlayabilirsin.")


def ytembed(vid, baslik):
    return (f'<div class="gp-yt-wrap" style="max-width:720px;margin:1.6em auto;">'
            f'<iframe src="https://www.youtube.com/embed/{vid}" title="{baslik}" frameborder="0" '
            f'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; '
            f'picture-in-picture; web-share" allowfullscreen loading="lazy" '
            f'style="display:block;width:100%;aspect-ratio:16/9;height:auto;border:0;'
            f'border-radius:12px;box-shadow:0 4px 14px rgba(0,0,0,0.5);"></iframe></div>')


# ---------------------------------------------------------------- yerleştirme
out, h2_no = [], 0
for tip, veri in P:
    if tip == "h1":
        out.append(f"<h1>{veri}</h1>")
    elif tip == "h2":
        h2_no += 1
        if h2_no == 2:
            out.append(cta_paketler)
        out.append(f"<h2>{veri}</h2>")
        if veri.startswith("Sıkça Sorulan"):
            out.insert(len(out) - 1, end_cta)
    elif tip == "p":
        out.append(f"<p>{veri}</p>")
        if veri.startswith("Oyuncu tarafında da tablo benzer"):
            out.append(editor_note)
        elif veri.startswith("Oyun, çıkış günü GeForce NOW kütüphanesine eklendi"):
            out.append(hatirlatma)
    elif tip == "yt":
        out.append(ytembed(*veri))
    elif tip == "liste":
        out.append(render_list(veri, marker="dot"))
    elif tip == "liste2":
        out.append(render_list(veri, marker="check"))
    elif tip == "puan_tablo":
        out.append(puan_tablo)

out.append(render_faq_accordion(FAQ))
out.append(render_faq_schema(FAQ))

body = "\n".join(out)
body, toc_items = inject_heading_ids(body)

rt = estimate_reading_time(body)
tldr = render_tldr([
    "<strong>Ne oynuyorsun:</strong> 14. yüzyıl Avrupası'nda geçen açık dünya aksiyon RPG; gündüz "
    "insan, gece vampir olan Coen'in ailesini kurtarma hikayesi.",
    "<strong>Ekip:</strong> The Witcher 3'ün yönetmeninin kurduğu Rebel Wolves'un ilk oyunu; ilk üç "
    "günde bir milyondan fazla sattı.",
    "<strong>Puanlar:</strong> OpenCritic 84, Metacritic 83, Steam'de %87 olumlu (25 binden fazla inceleme).",
    "<strong>En çok tartışılan yan:</strong> 30 günlük zaman sınırı. Keşif süreyi harcamıyor, "
    "yalnızca görevler ve yetenek yatırımları harcıyor.",
    "<strong>Türkçe:</strong> arayüz ve altyazı var, seslendirme yok. Oyun çıkış günü GeForce NOW "
    "kütüphanesine eklendi.",
], reading_time=rt)

info = render_info_card([
    ("Çıkış", "3 Eylül 2026"),
    ("OpenCritic", "84 Puan"),
    ("Ana Hikaye", "20 Saat+"),
    ("Süre Sınırı", "30 Oyun Günü"),
])

toc = render_floating_toc(toc_items)

m = re.search(r"</h1>", body)
body = body[:m.end()] + "\n" + toc + "\n" + tldr + "\n" + info + "\n" + body[m.end():]

body, _kat = auto_link_categories(body, max_links=2)                 # Kural 20
body, ps_bilgi = insert_preferred_source(body)                       # v10.22
body, _link = apply_link_policy(body)                                # Kural 21
body = ensure_leading_h1(body)
final_body = wrap_gp_content(ANIMATED_BORDER_STYLE + group_into_sections(body))   # Kural 22

print("=" * 62)
ok = print_report(verify_output(final_body, blog_type="general", expect_faq=True), label="Dawnwalker")
print("kategori linkleri:", [a for a, _ in _kat], "| tercih edilen kaynak:", ps_bilgi)

# ---------------------------------------------------------------- çıktılar
open(os.path.join(OUT, f"{SLUG}-html.txt"), "w", encoding="utf-8").write(final_body)
open(os.path.join(OUT, f"onizleme-{SLUG}.html"), "w", encoding="utf-8").write(
    embed_fonts(PAGE_HEAD.replace("__TITLE__", TITLE) + final_body + PAGE_FOOT))

# --- doc: once duz metin, sonra HTML (kullanicinin ornek dosyasindaki bicim) ---
from docx import Document
from docx.shared import Pt, RGBColor

doc = Document()
st = doc.styles["Normal"]
st.font.name = "Calibri"
st.font.size = Pt(11)
st.font.color.rgb = RGBColor(0x10, 0x33, 0x2F)

doc.add_heading(TITLE, level=1)
for tip, veri in P:
    if tip == "h1":
        continue
    if tip == "h2":
        doc.add_heading(veri, level=2)
    elif tip == "p":
        doc.add_paragraph(re.sub(r"<[^>]+>", "", veri))
    elif tip == "yt":
        doc.add_paragraph(f"https://www.youtube.com/watch?v={veri[0]}")
    elif tip in ("liste", "liste2"):
        for md in veri:
            doc.add_paragraph(re.sub(r"<[^>]+>", "", md), style="List Bullet")
    elif tip == "puan_tablo":
        doc.add_paragraph("Puan tablosu: OpenCritic 84 (152 eleştirmen, %94 tavsiye) | Metacritic 83 "
                          "(70 eleştirmen) | Metacritic kullanıcı 8.3 (1.200'den fazla oy) | Steam %87 olumlu "
                          "(25 binden fazla inceleme) | Steam Türkçe yorumlar %93 olumlu "
                          "(500'den fazla inceleme)")
doc.add_heading("Sıkça Sorulan Sorular", level=2)
for soru, cevap in FAQ:
    doc.add_heading(soru, level=3)
    doc.add_paragraph(re.sub(r"<[^>]+>", "", cevap))

doc.add_paragraph("")
doc.add_paragraph("HTML")
for satir in final_body.split("\n"):
    par = doc.add_paragraph()
    par.paragraph_format.space_after = Pt(0)
    par.paragraph_format.line_spacing = 1.0
    r = par.add_run(satir)
    r.font.name = "Courier New"
    r.font.size = Pt(7)
DOC_ADI = TITLE.replace(":", " -")   # macOS Finder iki noktayi bolu isareti gibi gosteriyor
doc.save(os.path.join(OUT, f"{DOC_ADI}.docx"))

kelime = len(re.sub(r"<[^>]+>", " ", "\n".join(
    v if isinstance(v, str) else "" for _, v in P)).split())
print(f"\nkelime (yazar metni): {kelime} | okuma: {rt} dk | boyut: {len(final_body)} karakter")
print("TESLİM EDİLEBİLİR" if ok else "!!! DÜZELTME GEREKLİ !!!")
