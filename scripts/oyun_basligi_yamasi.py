# -*- coding: utf-8 -*-
"""Uretilmis/yayindaki blog HTML'lerinde oyun basligi yerlesimini gunceller (v10.23).

Yaptiklari:
1) Stil blogundaki oyun basligi kural grubunu (v10.20 / v10.21 / v10.22 bicimlerinden hangisiyse)
   guncel blokla degistirir. v10.22: satir ici akis - rozet ilk satirla ayni hizada, uzun isim alt
   satirda basligin sol kenarindan devam eder. v10.23: rozet optik merkeze 2 px kaldirildi.
2) Govdede rozet ile isim arasindaki bosluk karakterini siler (satir ici akista ~5px ek bosluk yapar).
3) --gfn verilirse basliklardaki TUR ROZETINI kaldirir (GFN Thursday kurali, content-rules 11).
   Baslik yalnizca oyun adi + "Studyo · Yil" ile kalir.

Kullanim:
    python3 oyun_basligi_yamasi.py <dosya1> [<dosya2> ...]
    python3 oyun_basligi_yamasi.py --gfn <gfn-thursday-dosyasi> ...
"""
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gameplus_blog_components import ANIMATED_BORDER_STYLE  # noqa: E402

ESKI_CSS = re.compile(
    r"\.gp-content \.gp-game-head \{.*?\.gp-content \.gp-game-meta \{[^}]*\}", re.S)
_yeni = ESKI_CSS.search(ANIMATED_BORDER_STYLE)
assert _yeni, "guncel oyun basligi CSS'i ANIMATED_BORDER_STYLE icinde bulunamadi"
YENI_CSS = _yeni.group(0)

ROZET_BOSLUK = re.compile(
    r'(<span class="gp-game-badge"[^>]*>.*?</span>(?:</a>)?)\s+(<span class="gp-game-name">)', re.S)
BASLIK = re.compile(r'<(h[1-6])([^>]*class="gp-game-head"[^>]*)>(.*?)</\1>', re.S)
ROZET = re.compile(
    r'\s*(?:<a class="gp-game-badge-link"[^>]*>)?<span class="gp-game-badge"[^>]*>.*?</span>'
    r'(?:</a>)?\s*', re.S)


def rozetleri_kaldir(html):
    """Yalniz oyun basliklarindaki tur rozetlerini siler; tablolardaki tur bilgisi korunur."""
    sayac = [0]

    def _bir(m):
        ic, n = ROZET.subn("\n  ", m.group(3), count=1)
        sayac[0] += n
        return f"<{m.group(1)}{m.group(2)}>{ic}</{m.group(1)}>"

    return BASLIK.sub(_bir, html), sayac[0]


def yamala(yol, gfn=False):
    s = io.open(yol, encoding="utf-8").read()
    if "gp-game-head" not in s:
        return f"  atlandi (oyun basligi yok): {yol}"
    yeni = ESKI_CSS.sub(lambda m: YENI_CSS, s)
    yeni, bosluk_n = ROZET_BOSLUK.subn(r"\1\2", yeni)
    rozet_n = 0
    if gfn:
        yeni, rozet_n = rozetleri_kaldir(yeni)
    if yeni == s:
        return f"  zaten guncel: {yol}"
    io.open(yol, "w", encoding="utf-8").write(yeni)
    ek = f", baslik rozeti kaldirildi {rozet_n}" if gfn else ""
    return f"  guncellendi (rozet boslugu {bosluk_n}{ek}): {yol}"


if __name__ == "__main__":
    arg = sys.argv[1:]
    gfn = "--gfn" in arg
    for y in [a for a in arg if not a.startswith("--")]:
        print(yamala(y, gfn=gfn))
