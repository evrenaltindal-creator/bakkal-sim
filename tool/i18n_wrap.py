#!/usr/bin/env python3
"""index.html içindeki Türkçe metinleri tx('...') çağrılarına sarar ve anahtarları çıkarır.

Bir kez çalıştırılmak için yazıldı (oyunu çok dilli yapmak için). Kaynak dil Türkçedir: anahtar,
metnin Türkçesidir; i18n.js her dil için çevirisini tutar. Şablonlardaki ${...} ifadeleri {0}, {1}
yer tutucularına dönüşür, böylece çeviride kelime sırası değişebilir.

Kullanım:
  python3 tool/i18n_wrap.py index.html            # dosyayı yerinde dönüştürür
  python3 tool/i18n_wrap.py index.html --keys     # yalnızca tx('...') anahtarlarını listeler (JSON)
"""
import json
import re
import sys

LETTER = r'[A-Za-zÇĞİÖŞÜçğıöşüâÂ]'
TR_CHAR = r'[ÇĞİÖŞÜçğıöşüâÂ]'
EXCLUDE = {'Rubik', 'Bungee', 'Space', 'Arial Black', 'Impact', 'Ayşe', 'Mehmet', 'Zeynep', 'Murat', 'Elif', 'Emre', 'Fatma', 'Can',
           'Selin', 'Hasan', 'Derya', 'Kemal', 'Büşra', 'Oğuz', 'AudioContext', 'use strict'}
PUNCT_ONLY = re.compile(r'^[\s\W\d₺×·★⇄✓✗%]*$')


def translatable(s):
    st = s.strip()
    if st in EXCLUDE or len(re.findall(LETTER, st)) < 2:
        return False
    if re.search(r"px\b|#[0-9a-fA-F]{3}|rgba|var\(|=>|\(\)|\.(mp3|png|woff2|js|html)\b|bakkal\.|sans-serif|^'|', |^[a-z0-9_\-]+$|^[a-z]+[A-Z]\w*$|^\w+\.\w+$", st):
        return False
    return (' ' in st or bool(re.search(TR_CHAR, st)) or bool(re.match(r'^[A-ZÇĞİÖŞÜ][a-zçğıöşüâ]+[.!]?$', st))
            or (st.isupper() and len(st) > 2))


def js_quote(s):
    return "'" + s.replace('\\', '\\\\').replace("'", "\\'").replace('\n', ' ') + "'"


def cook(raw):
    return re.sub(r'\\(.)', lambda m: {'n': '\n', 't': '\t'}.get(m.group(1), m.group(1)), raw)


class Scanner:
    def __init__(self, src):
        self.s = src

    def read_string(self, i):
        q = self.s[i]
        j = i + 1
        while self.s[j] != q:
            j += 2 if self.s[j] == '\\' else 1
        return self.s[i + 1:j], j + 1

    def read_template(self, i):
        """i: açan ` konumu. Döner: (parçalar, bitiş). Parça: ('text', ham) | ('expr', kod)."""
        parts, j, buf = [], i + 1, ''
        while True:
            c = self.s[j]
            if c == '\\':
                buf += self.s[j:j + 2]; j += 2; continue
            if c == '`':
                parts.append(('text', buf)); return parts, j + 1
            if c == '$' and self.s[j + 1] == '{':
                parts.append(('text', buf)); buf = ''
                k, depth = j + 2, 1
                while depth:
                    ch = self.s[k]
                    if ch in '\'"':
                        _, k = self.read_string(k); continue
                    if ch == '`':
                        _, k = self.read_template(k); continue
                    if ch == '{': depth += 1
                    elif ch == '}': depth -= 1
                    k += 1
                parts.append(('expr', self.s[j + 2:k - 1])); j = k; continue
            buf += c; j += 1


def transform(code, mode='text'):
    sc = Scanner(code)
    out, i, prev = [], 0, ''
    n = len(code)
    while i < n:
        c = code[i]
        if code.startswith('//', i):
            j = code.find('\n', i); j = n if j < 0 else j
            out.append(code[i:j]); i = j; continue
        if code.startswith('/*', i):
            j = code.index('*/', i) + 2
            out.append(code[i:j]); i = j; continue
        if c == '/' and (prev in '(,=:[!&|?{};+-*%<>~^' or prev == '' or re.search(r'(return|typeof)\s*$', ''.join(out[-3:]))):
            j = i + 1; inclass = False
            while True:
                ch = code[j]
                if ch == '\\': j += 2; continue
                if ch == '[': inclass = True
                elif ch == ']': inclass = False
                elif ch == '/' and not inclass: break
                j += 1
            j += 1
            while j < n and code[j].isalpha(): j += 1
            out.append(code[i:j]); i = j; prev = '/'; continue
        if c in '\'"':
            raw, j = sc.read_string(i)
            lit = code[i:j]
            if mode == 'text' and translatable(cook(raw)):
                txt = cook(raw); core = txt.strip(); lead = txt[:len(txt) - len(txt.lstrip())]; trail = txt[len(txt.rstrip()):]
                w = 'tx(' + js_quote(core) + ')'
                if lead or trail:
                    w = '(' + (js_quote(lead) + ' + ' if lead else '') + w + (' + ' + js_quote(trail) if trail else '') + ')'
                out.append(w)
            else:
                out.append(lit)
            i = j; prev = 'a'; continue
        if c == '`':
            parts, j = sc.read_template(i)
            out.append(template(parts, mode)); i = j; prev = 'a'; continue
        out.append(c)
        if not c.isspace():
            prev = c if not (c.isalnum() or c in '_$') else 'a'
        i += 1
    return ''.join(out)


def template(parts, mode):
    if mode == 'code':
        return '`' + ''.join(p if k == 'text' else '${' + transform(p, 'code') + '}' for k, p in parts) + '`'
    out = []
    unit = []  # ('text', ham) | ('expr', kod)
    in_tag = False

    def flush():
        if not unit:
            return
        static = ''.join(cook(p) for k, p in unit if k == 'text')
        exprs = [p for k, p in unit if k == 'expr']
        key, n = '', 0
        for k, p in unit:
            if k == 'text':
                key += cook(p)
            else:
                key += '{%d}' % n; n += 1
        if len(re.findall(LETTER, static)) >= 2 and not PUNCT_ONLY.match(static) and translatable(key):
            norm = re.sub(r'\s+', ' ', key)
            lead = norm[:len(norm) - len(norm.lstrip())]; trail = norm[len(norm.rstrip()):]
            args = '' if not exprs else ', [' + ', '.join(transform(e, 'text') for e in exprs) + ']'
            out.append(lead + '${tx(' + js_quote(norm.strip()) + args + ')}' + trail)
        else:
            for k, p in unit:
                out.append(p if k == 'text' else '${' + transform(p, 'text') + '}')
        unit.clear()

    for k, p in parts:
        if k == 'expr':
            if in_tag:
                out.append('${' + transform(p, 'code') + '}')
            else:
                unit.append(('expr', p))
            continue
        buf = ''
        for ch in p:
            if not in_tag and ch == '<':
                if buf: unit.append(('text', buf)); buf = ''
                flush(); in_tag = True; buf = '<'
            elif in_tag and ch == '>':
                buf += '>'; out.append(buf); buf = ''; in_tag = False
            else:
                buf += ch
        if buf:
            if in_tag: out.append(buf)
            else: unit.append(('text', buf))
    flush()
    return '`' + ''.join(out) + '`'


def main():
    path = sys.argv[1]
    src = open(path, encoding='utf-8').read()
    a = src.index('<script>') + len('<script>')
    b = src.rindex('</script>')
    if '--keys' in sys.argv:
        keys = []
        for m in re.finditer(r"\btx\('((?:[^'\\]|\\.)*)'", src[a:b]):
            k = cook(m.group(1))
            if k not in keys: keys.append(k)
        print(json.dumps(keys, ensure_ascii=False, indent=1))
        return
    new = src[:a] + transform(src[a:b]) + src[b:]
    open(path, 'w', encoding='utf-8').write(new)
    print('dönüştürüldü')


if __name__ == '__main__':
    main()
