# -*- coding: utf-8 -*-
"""v10.21: uretilmis/yayindaki blog HTML'lerinde oyun basligi CSS'ini gunceller.
Isim artik tur rozetinin SAGINDAN baslar (uzun isimler rozeti yalniz birakmaz).
Kullanim: python3 oyun_basligi_yamasi.py <dosya1> [<dosya2> ...]"""
import io, sys

ESKI = ".gp-content .gp-game-name { font-weight: 700; letter-spacing: -0.01em; }"
YENI = ".gp-content .gp-game-name { flex: 1 1 0%; min-width: 0; font-weight: 700; letter-spacing: -0.01em; }"


def yamala(yol):
    s = io.open(yol, encoding="utf-8").read()
    if "flex: 1 1 0%; min-width: 0; font-weight: 700" in s:
        return f"  zaten guncel: {yol}"
    if ESKI not in s:
        return f"  atlandi (kural bulunamadi): {yol}"
    io.open(yol, "w", encoding="utf-8").write(s.replace(ESKI, YENI))
    return f"  guncellendi: {yol}"


if __name__ == "__main__":
    for y in sys.argv[1:]:
        print(yamala(y))
