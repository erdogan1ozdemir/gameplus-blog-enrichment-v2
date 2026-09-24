# -*- coding: utf-8 -*-
"""Gomulecek YouTube videolarinin yas kisitli olup olmadigini tarayicida test etmek icin
tek sayfalik bir test dosyasi uretir.

Neden tarayici: `curl` ile guvenilir sonuc alinmiyor. Veri merkezi IP'lerinden YouTube her videoyu
"Sign in to confirm your age" isaretiyle donduruyor, yani kisitli olmayan video da kisitli gorunuyor.
Gomulu oynaticiyi tarayicida acmak tek kesin yontem: kisitli videoda oynatici yerinde
"Sorry, this content is age-restricted" uyarisi cikar, kisitsiz videoda kapak goruntusu ve oynat
dugmesi gorunur.

Kullanim:
    python3 video_yas_testi.py dQw4w9WgXcQ pNTT7lknCE0 ...
    python3 video_yas_testi.py --cikti /tmp/test.html <id...>

Ardindan dosya tarayicida acilir (yerel sunucu uzerinden), uyari cikan adaylar elenir.
"""
import io
import os
import sys

SABLON = """<!DOCTYPE html>
<html lang="tr"><head><meta charset="utf-8"><title>YouTube yas kisiti testi</title>
<style>
 body {{ background:#111; color:#eee; font-family:system-ui,sans-serif; margin:0; padding:16px; }}
 h1 {{ font-size:18px; margin:0 0 4px; }}
 p.alt {{ color:#9a9a9a; font-size:13px; margin:0 0 20px; }}
 .oge {{ margin-bottom:22px; }}
 .ad {{ font-size:14px; margin:0 0 6px; }}
 .ad b {{ color:#FFC900; }}
 iframe {{ width:min(520px, 100%); aspect-ratio:16/9; border:0; border-radius:8px; }}
</style></head><body>
<h1>YouTube yas kisiti testi</h1>
<p class="alt">Oynatici yerinde "Sorry, this content is age-restricted" yaziyorsa o video gomulemez.</p>
{govde}
</body></html>
"""


def sayfa(idler):
    parcalar = []
    for i, vid in enumerate(idler, 1):
        parcalar.append(
            f'<div class="oge"><p class="ad">{i}. <b>{vid}</b> '
            f'<a href="https://www.youtube.com/watch?v={vid}" target="_blank" '
            f'rel="noopener noreferrer" style="color:#9a9a9a">YouTube\'da ac</a></p>'
            f'<iframe src="https://www.youtube.com/embed/{vid}" loading="eager" '
            f'allowfullscreen></iframe></div>')
    return SABLON.format(govde="\n".join(parcalar))


if __name__ == "__main__":
    arg = sys.argv[1:]
    cikti = "video-yas-testi.html"
    if "--cikti" in arg:
        i = arg.index("--cikti")
        cikti = arg[i + 1]
        arg = arg[:i] + arg[i + 2:]
    idler = [a for a in arg if not a.startswith("--")]
    if not idler:
        print(__doc__.strip())
        sys.exit(1)
    io.open(cikti, "w", encoding="utf-8").write(sayfa(idler))
    print(f"{len(idler)} video icin test sayfasi yazildi: {os.path.abspath(cikti)}")
    print("Tarayicida ac (yerel sunucu uzerinden) ve uyari cikan adaylari ele.")
