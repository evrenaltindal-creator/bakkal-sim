#!/usr/bin/env bash
# Oyunun dosyalarını uygulamanın içine gömülecek ios/www klasörüne kopyalar.
# Yalnızca oyunun çalışırken yüklediği dosyalar girer (kaynak görseller, araçlar, testler girmez).
set -euo pipefail
cd "$(dirname "$0")"
rm -rf www
mkdir -p www/art
cp ../index.html www/
cp -R ../i18n www/ && rm -rf www/i18n/src
cp -R ../art/icons ../art/scene www/art/
cp -R ../music ../fonts www/
echo "www hazır: $(find www -type f | wc -l | tr -d ' ') dosya"
