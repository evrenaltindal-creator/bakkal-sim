#!/usr/bin/env python3
"""Çevirileri i18n/<dil>.js dosyalarına derler.

Kaynak: i18n/src/keys.json (Türkçe anahtarlar, sıralı) ve i18n/src/<dil>.txt
("numara<TAB>çeviri" satırları). Her çevirinin yer tutucuları ({0}, {1}) ve HTML etiketleri
Türkçesiyle aynı olmalı; değilse hata verir. index.html'deki tx('...') anahtarlarından
çevirisi olmayan varsa uyarır (yeni metin eklenmiş demektir).

Kullanım: python3 tool/build_i18n.py
"""
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANGS = ['en', 'de', 'es', 'pt', 'ru', 'ar']


def sig(s):
    return sorted(re.findall(r'\{\d+\}', s)), sorted(re.findall(r'</?[a-z]+[^>]*>', s))


def main():
    keys = json.load(open(os.path.join(ROOT, 'i18n/src/keys.json'), encoding='utf-8'))
    current = json.loads(subprocess.check_output([sys.executable, os.path.join(ROOT, 'tool/i18n_wrap.py'),
                                                  os.path.join(ROOT, 'index.html'), '--keys']))
    missing = [k for k in current if k not in keys]
    for k in missing:
        print('UYARI: çevirisi yok:', k)
    errors = 0
    for lang in LANGS:
        rows = {}
        for ln in open(os.path.join(ROOT, f'i18n/src/{lang}.txt'), encoding='utf-8'):
            ln = ln.rstrip('\n')
            if not ln.strip():
                continue
            n, _, tr = ln.partition('\t')
            rows[int(n)] = tr
        out = {}
        for i, k in enumerate(keys):
            if i not in rows:
                print(f'HATA {lang}: {i} eksik ({k})'); errors += 1; continue
            if sig(rows[i]) != sig(k):
                print(f'HATA {lang} {i}: yer tutucu/etiket farklı\n  {k}\n  {rows[i]}'); errors += 1
            out[k] = rows[i]
        extra = set(rows) - set(range(len(keys)))
        if extra:
            print(f'HATA {lang}: fazla satır {sorted(extra)}'); errors += 1
        js = ('// tool/build_i18n.py ile üretilir; elle düzenleme (kaynak: i18n/src/%s.txt).\n'
              'window.L10N = window.L10N || {};\nwindow.L10N.%s = %s;\n') % (lang, lang, json.dumps(out, ensure_ascii=False, indent=0))
        open(os.path.join(ROOT, f'i18n/{lang}.js'), 'w', encoding='utf-8').write(js)
    unused = [k for k in keys if k not in current]
    if unused:
        print(f'not: {len(unused)} anahtar artık kullanılmıyor')
    if errors:
        sys.exit(1)
    print('tamam:', ', '.join(LANGS), f'({len(keys)} anahtar)')


if __name__ == '__main__':
    main()
