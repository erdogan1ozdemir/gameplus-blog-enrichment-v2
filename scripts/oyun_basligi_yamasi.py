# -*- coding: utf-8 -*-
"""v10.22: uretilmis/yayindaki blog HTML'lerinde oyun basligi yerlesimini gunceller.

Ne degisti: tur rozeti ilk satirla ayni hizada durur; isim alt satira indiginde baslik hizasindan
(rozetin sol kenarindan) devam eder. v10.21 ve oncesindeki flex yerlesimi isim kutusunu rozetin
yaninda sariyor, rozeti de iki satirlik ismin dikey ortasina aliyordu.

Iki adim:
1) Stil blogundaki oyun basligi kurallari (v10.20 ya da v10.21 bicimi) guncel blokla degisir.
2) Govdede rozet ile isim arasindaki bosluk karakteri silinir (satir ici akista ~5px ek bosluk yapar).

Kullanim: python3 oyun_basligi_yamasi.py <dosya1> [<dosya2> ...]"""
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gameplus_blog_components import ANIMATED_BORDER_STYLE  # noqa: E402

ESKI_CSS = re.compile(
    r"\.gp-content \.gp-game-head \{ display: flex;.*?flex-basis: 100%; margin-top: -4px; \}", re.S)
_yeni = re.search(
    r"\.gp-content \.gp-game-head \{ display: block;.*?margin-top: 8px; \}", ANIMATED_BORDER_STYLE, re.S)
assert _yeni, "guncel oyun basligi CSS'i ANIMATED_BORDER_STYLE icinde bulunamadi"
YENI_CSS = _yeni.group(0)

ROZET_BOSLUK = re.compile(
    r'(<span class="gp-game-badge"[^>]*>.*?</span>(?:</a>)?)\s+(<span class="gp-game-name">)', re.S)


def yamala(yol):
    s = io.open(yol, encoding="utf-8").read()
    if "gp-game-head" not in s:
        return f"  atlandi (oyun basligi yok): {yol}"
    css_n = len(ESKI_CSS.findall(s))
    s2 = ESKI_CSS.sub(lambda m: YENI_CSS, s)
    s2, bosluk_n = ROZET_BOSLUK.subn(r"\1\2", s2)
    if s2 == s:
        return f"  zaten guncel: {yol}"
    io.open(yol, "w", encoding="utf-8").write(s2)
    return f"  guncellendi (css {css_n} blok, rozet boslugu {bosluk_n}): {yol}"


if __name__ == "__main__":
    for y in sys.argv[1:]:
        print(yamala(y))
