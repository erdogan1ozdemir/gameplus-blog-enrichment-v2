# -*- coding: utf-8 -*-
"""Kısa Hikayeli Oyunlar: ham docx -> v10.22 enriched (metin KORUNUR, sadece EKLENİR).
Stüdyo · Yıl verileri Steam Store API'den doğrulandı (uydurma yok).
v10.22 denemesi: tercih edilen kaynak kartı + satır içi oyun başlığı hizası."""
import sys, os, re, zipfile
import xml.etree.ElementTree as ET
from docx import Document

SKILL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts")
sys.path.insert(0, SKILL)
from gameplus_blog_components import *

OUT = os.environ.get("GAMEPLUS_OUT", os.getcwd())
DOCX = sys.argv[1] if len(sys.argv) > 1 else "Kısa Hikayeli Oyunlar_ Bir Oturuşta Bitirebileceğin Kısa Oyunlar.docx"
TITLE = "Kısa Hikayeli Oyunlar: Bir Oturuşta Bitirebileceğin Kısa Oyunlar"
SLUG = "kisa-hikayeli-oyunlar-bir-oturusta-bitirebilecegin-kisa-oyunlar"

NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
def Wt(t): return '{%s}%s' % (NS['w'], t)
def Rt(t): return '{%s}%s' % (NS['r'], t)

z = zipfile.ZipFile(DOCX)
rels = {rel.get('Id'): rel.get('Target') for rel in ET.fromstring(z.read('word/_rels/document.xml.rels'))}

def esc(t): return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def run_html(r):
    txt = ''.join(n.text or '' for n in r.iter(Wt('t')))
    if not txt: return ''
    rpr = r.find(Wt('rPr'))
    b = rpr is not None and rpr.find(Wt('b')) is not None
    i = rpr is not None and rpr.find(Wt('i')) is not None
    h = esc(txt)
    if b: h = '<strong>%s</strong>' % h
    if i: h = '<em>%s</em>' % h
    return h

def para_html(p):
    parts = []
    for ch in p._p:
        tag = ch.tag.split('}')[-1]
        if tag == 'r':
            parts.append(run_html(ch))
        elif tag == 'hyperlink':
            url = rels.get(ch.get(Rt('id')), '')
            inner = ''.join(run_html(r) for r in ch.findall(Wt('r')))
            parts.append('<a href="%s">%s</a>' % (url, inner) if url else inner)
    return re.sub(r'</strong><strong>', '', ''.join(parts))

d = Document(DOCX)
blocks = []
for p in d.paragraphs:
    txt = p.text.strip()
    if not txt: continue
    kind = {'Heading 1': 'h1', 'Heading 2': 'h2', 'Heading 3': 'h3'}.get(p.style.name, 'p')
    html = para_html(p).strip()
    if kind == 'p' and re.match(r'^https?://(www\.)?youtube\.com/watch', txt):
        kind, html = 'yt', txt
    elif kind == 'p' and p._p.pPr is not None and p._p.pPr.numPr is not None:
        kind = 'li'
    blocks.append((kind, html, txt))

# Kaynak metin (doğrulama için) - YouTube URL satırları hariç
original_body = "\n".join(
    f'<{k if k in ("h1","h2","h3") else "p"}>{h}</{k if k in ("h1","h2","h3") else "p"}>'
    for (k, h, t) in blocks if k != 'yt')

# ---------------- Oyun verileri (Steam Store API ile doğrulandı) ----------------
# (rozet, Stüdyo · Yıl, çapa). Rozetler GFN kategorileri: Macera, Aksiyon-Macera, Platform.
GAMES = {
    'Little Nightmares':           ('Macera', 'Tarsier Studios &middot; 2017', 'little-nightmares'),
    'Little Nightmares II':        ('Macera', 'Tarsier Studios &middot; 2021', 'little-nightmares-ii'),
    '11-11 Memories Retold':       ('Macera', 'DigixArt, Aardman Animations &middot; 2018', '11-11-memories-retold'),
    'Hellblade II: Senua’s Saga':  ('Aksiyon-Macera', 'Ninja Theory &middot; 2024', 'hellblade-ii-senuas-saga'),
    'South of Midnight':           ('Aksiyon-Macera', 'Compulsion Games &middot; 2025', 'south-of-midnight'),
    '9 Years of Shadows':          ('Platform', 'Halberd Studios &middot; 2023', '9-years-of-shadows'),
}
# Ana hikaye süreleri YAZARIN metninden (paragraflarda geçen değerler)
SURE = {
    'Little Nightmares': '3.5-4 saat',
    'Little Nightmares II': '5.5-6 saat',
    '11-11 Memories Retold': 'Yaklaşık 5 saat',
    'Hellblade II: Senua’s Saga': '7-8 saat',
    'South of Midnight': '6-8 saat',
    '9 Years of Shadows': '6-7 saat',
}

def ytid(u):
    m = re.search(r'v=([A-Za-z0-9_-]{11})', u)
    return m.group(1) if m else ''

def yt(vid, t=""):
    return (f'<div class="gp-yt-wrap" style="max-width:720px;margin:1.6em auto;">'
            f'<iframe src="https://www.youtube.com/embed/{vid}" title="{esc(t)}" frameborder="0" '
            f'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" '
            f'allowfullscreen loading="lazy" style="display:block;width:100%;aspect-ratio:16/9;height:auto;'
            f'border:0;border-radius:12px;box-shadow:0 4px 14px rgba(0,0,0,0.5);"></iframe></div>')

n = len(blocks)
game_idx = [i for i in range(n) if blocks[i][0] == 'h3' and blocks[i][2] in GAMES]
game_names = [blocks[i][2] for i in game_idx]
assert len(game_names) == 6, game_names
first_game = game_idx[0]

# ---------------- Bileşenler ----------------
card_table = render_card_table("Listedeki Kısa Hikayeli Oyunlar", [
    {'name': nm, 'badge': GAMES[nm][0], 'badge_color': badge_color_for(GAMES[nm][0]),
     'meta': GAMES[nm][1], 'anchor': GAMES[nm][2]} for nm in game_names])

sure_table = render_table(
    ["Oyun", "Ana Hikaye Süresi", "Anlatım Tarzı"],
    [["Little Nightmares", SURE['Little Nightmares'], "Diyalogsuz, atmosfer odaklı gerilim"],
     ["Little Nightmares II", SURE['Little Nightmares II'], "İki karakterli karanlık yolculuk"],
     ["11-11 Memories Retold", SURE['11-11 Memories Retold'], "Tablo benzeri görsellerle savaş hikayesi"],
     ["Hellblade II: Senua’s Saga", SURE['Hellblade II: Senua’s Saga'], "Sinematik, çizgisel, psikolojik"],
     ["South of Midnight", SURE['South of Midnight'], "Folklor esintili, stop-motion görünümlü"],
     ["9 Years of Shadows", SURE['9 Years of Shadows'], "2D piksel sanatlı Metroidvania"]],
    title="Kısa Hikayeli Oyunlar: Ortalama Bitirme Süreleri")

cta_paketler = render_cta_paketler(
    "Kısa bir hikayeye başlamak için kurulum bekleme",
    "GeForce NOW ile kütüphanendeki desteklenen oyunları güçlü bir bilgisayara ihtiyaç duymadan "
    "buluttan açabilir, bir akşamlık maceraya hemen başlayabilirsin.")

end_cta = render_end_cta(
    "Bu akşamın hikayesini seçtin mi?",
    "Performance ve Ultimate paketleri, sahip olduğun GeForce NOW destekli oyunları güçlü bir ekran kartı "
    "olmadan çalıştırmanı sağlar. Paketleri karşılaştırıp sana uyanı seçebilirsin.")

editor_note = render_editor_note(
    "Little Nightmares serisine yeni başlıyorsan ilk oyundan başlamanı öneririz. İkinci oyunda yolu "
    "kesişen Six, ilk oyunun kahramanı; iki yapımı arka arkaya oynamak hikayeyi daha bütünlüklü "
    "okumanı sağlıyor.")

hatirlatma = render_highlight(
    "GeForce NOW oyun satmaz, sahip olduğun oyunları bulutta çalıştırır. Bir yapımı buluttan açabilmen için "
    "o oyuna Steam, Epic Games Store, Xbox, Ubisoft Connect, GOG, EA App veya Battle.net gibi desteklenen "
    "bir platformda sahip olman gerekir.")

# ---------------- Yerleştirme ----------------
out = []
i = 0
h2_count = 0
while i < n:
    k, html, txt = blocks[i]

    if k == 'h1':
        out.append(f'<h1>{html}</h1>'); i += 1; continue

    if k == 'h2':
        h2_count += 1
        if 'Sıkça Sorulan' in txt:                       # End CTA -> SSS'den ÖNCE, FAQ accordion
            pairs = []; j = i + 1
            while j < n and blocks[j][0] != 'h2':
                if blocks[j][0] == 'h3' and j + 1 < n and blocks[j + 1][0] == 'p':
                    pairs.append((blocks[j][2], blocks[j + 1][1])); j += 2
                else:
                    j += 1
            out.append(end_cta)
            out.append(f'<h2>{html}</h2>')
            out.append(render_faq_accordion(pairs))
            out.append(render_faq_schema(pairs))
            i = j; continue
        if h2_count == 2:                                 # CTA Paketler -> 2. H2'den önce
            out.append(cta_paketler)
        out.append(f'<h2>{html}</h2>'); i += 1; continue

    if k == 'h3' and i in game_idx:                       # oyun başlığı + fragman
        if i == first_game:
            out.append(card_table)
        nm = txt
        badge, meta, anchor = GAMES[nm]
        out.append(render_game_h3_inline(anchor, html, badge, badge_color_for(badge), meta, level="h3"))
        if i + 1 < n and blocks[i + 1][0] == 'yt':
            out.append(yt(ytid(blocks[i + 1][1]), nm)); i += 2
        else:
            i += 1
        continue

    if k == 'yt':
        out.append(yt(ytid(html))); i += 1; continue

    if k == 'li':                                          # yazarın numaralı maddeleri -> madde listesi
        items = []
        while i < n and blocks[i][0] == 'li':
            items.append(blocks[i][1]); i += 1
        out.append(render_list(items, marker="dot"))
        out.append(sure_table)                             # öneri listesinin ardından süre tablosu
        continue

    if k == 'h3':
        out.append(f'<h3>{html}</h3>'); i += 1; continue

    out.append(f'<p>{html}</p>')
    if txt.startswith('İlk oyunun yakaladığı atmosferi genişleten'):
        out.append(editor_note)
    elif txt.startswith('Üstelik bu listedeki yapımları deneyimlemek'):
        out.append(hatirlatma)
    i += 1

body = "\n".join(out)
body, toc_items = inject_heading_ids(body)
body = shrink_youtube_embeds(body)

rt = estimate_reading_time(body)
tldr = render_tldr([
    "<strong>6 kısa hikayeli oyun:</strong> Little Nightmares serisinden South of Midnight ve 9 Years of Shadows'a kadar.",
    "<strong>Süreler 3.5 ile 8 saat arasında:</strong> çoğu yapım tek akşamda ya da bir hafta sonunda bitiyor.",
    "<strong>Gerilim arıyorsan:</strong> Little Nightmares serisi; sinematik anlatım için Hellblade II: Senua’s Saga.",
    "<strong>2D keşif sevenlere:</strong> piksel sanatlı Metroidvania 9 Years of Shadows.",
], reading_time=rt)

info = render_info_card([
    ("Listedeki Oyun", "6 Yapım"),
    ("Ana Hikaye Süresi", "3.5-8 Saat"),
    ("Odak", "Hikaye Anlatımı"),
    ("Oynanış", "Tek Oyunculu"),
])

toc = render_floating_toc(toc_items)

m = re.search(r'</h1>', body)
assert m, "H1 bulunamadı"
body = body[:m.end()] + "\n" + toc + "\n" + tldr + "\n" + info + "\n" + body[m.end():]

_mevcut = set(re.findall(r'href="(https://gameplus\.com\.tr/gfn/oyunlar/[a-z-]+)"', body))
body, _kat_linkler = auto_link_categories(body, max_links=2, haric=tuple(_mevcut))   # Kural 20
body, ps_bilgi = insert_preferred_source(body)                                       # v10.22
body, _link_sayac = apply_link_policy(body)                                          # Kural 21
body = ensure_leading_h1(body)
final_body = wrap_gp_content(ANIMATED_BORDER_STYLE + group_into_sections(body))      # Kural 22

# ---------------- Doğrulama ----------------
print("=" * 60)
res = verify_output(final_body, blog_type="general", n_games=6, expect_faq=True)
ok = print_report(res, label="Kısa Hikayeli Oyunlar")
print("-" * 60)
src_ok = print_source_report(original_body, final_body)
print("=" * 60)
print("tercih edilen kaynak:", ps_bilgi)

# ---------------- Çıktı ----------------
open(os.path.join(OUT, f"{SLUG}-html.txt"), "w", encoding="utf-8").write(final_body)
onizleme = embed_fonts(PAGE_HEAD.replace("__TITLE__", TITLE) + final_body + PAGE_FOOT)
open(os.path.join(OUT, f"onizleme-{SLUG}.html"), "w", encoding="utf-8").write(onizleme)
print(f"\nkelime: {len(re.sub(r'<[^>]+>',' ', body).split())} | okuma: {rt} dk | oyun: {len(game_names)} "
      f"| boyut: {len(final_body)} karakter")
print("TESLİM EDİLEBİLİR" if (ok and src_ok) else "!!! DÜZELTME GEREKLİ !!!")
