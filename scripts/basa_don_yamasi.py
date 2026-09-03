# -*- coding: utf-8 -*-
"""v10.20: yayindaki/uretilmis blog HTML'lerinde 'Basa don' script blogunu gunceller.
Buton artik sayfanin en ustune degil, yazinin ILK BASLIGINA gider.
Kullanim: python3 basa_don_yamasi.py <dosya1> [<dosya2> ...]"""
import io, re, sys

ESKI_BAS = "<script>\n(function(){\n  var t = document.querySelector('.floating-toc');"
DESEN = re.compile(r"<script>\s*\(function\(\)\{\s*var t = document\.querySelector\('\.floating-toc'\);.*?</script>", re.S)

sys.path.insert(0, "/Users/Erdo/.claude/skills/gameplus-blog-enrich-v2/scripts")
from gameplus_blog_components import render_floating_toc

_ornek = render_floating_toc([(1, "x", "x"), (2, "y", "y")])
YENI = DESEN.search(_ornek).group(0)


def yamala(yol):
    s = io.open(yol, encoding="utf-8").read()
    n = len(DESEN.findall(s))
    if not n:
        return f"  atlandi (ToC script yok): {yol}"
    if "basaDonHedefi" in s:
        return f"  zaten guncel: {yol}"
    io.open(yol, "w", encoding="utf-8").write(DESEN.sub(lambda m: YENI, s))
    return f"  guncellendi ({n} blok): {yol}"


if __name__ == "__main__":
    for y in sys.argv[1:]:
        print(yamala(y))
