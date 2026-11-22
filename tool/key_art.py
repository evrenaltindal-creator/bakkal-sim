#!/usr/bin/env python3
"""Google Flow'dan gelen görselin düz zeminini siler, kırpar ve oyuna uygun boyuta getirir.

Kullanım:
  python3 tool/key_art.py art/source/16-ekmek.jpg art/icons/ekmek.png --bg green --size 48
  python3 tool/key_art.py art/source/24-domates.jpg art/icons/domates.png --bg magenta --size 48
  python3 tool/key_art.py art/source/06-raf.jpg art/scene/raf.png --bg green --width 400

Zemin rengi:
  green   -> düz yeşil (#00FF00). Yeşil parçası olan ürünlerde kullanma: yaprak da silinir.
  magenta -> düz mor-pembe (#FF00FF). Domates, elma gibi yeşil sapı olan ürünler için.

Görselleri elle düzenleme; kaynağı art/source/ altında tut ve bu betikle yeniden üret.
Gerekli: pip install Pillow
"""
import argparse
from PIL import Image


def key(im, bg):
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if bg == 'green':
                if g > 150 and g > r + 60 and g > b + 60:
                    px[x, y] = (0, 0, 0, 0)
                elif g > r + 25 and g > b + 25 and g > 140:  # kenardaki yeşil saçak
                    px[x, y] = (r, max(r, b), b, a)
            else:
                if r > 150 and b > 120 and g < 110:
                    px[x, y] = (0, 0, 0, 0)
                elif r > g + 50 and b > g + 50:  # kenardaki mor saçak
                    px[x, y] = (r, g, min(b, g + 20), a)
    return im


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src')
    ap.add_argument('dst')
    ap.add_argument('--bg', choices=['green', 'magenta'], default='green')
    ap.add_argument('--size', type=int, help='ürün simgesi: en uzun kenar (ör. 48)')
    ap.add_argument('--width', type=int, help='sahne görseli: genişlik (ör. 400)')
    a = ap.parse_args()
    im = key(Image.open(a.src).convert('RGBA'), a.bg)
    im = im.crop(im.getbbox())
    if a.size:
        im.thumbnail((a.size, a.size), Image.BOX)
    elif a.width:
        im = im.resize((a.width, round(im.height * a.width / im.width)), Image.BOX)
    im.save(a.dst)
    print(a.dst, im.size)


if __name__ == '__main__':
    main()
