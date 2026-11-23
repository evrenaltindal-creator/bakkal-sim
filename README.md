# Little Bakkal

2D piksel sanat bir mahalle bakkalı işletme oyunu. Tek başına küçük bir bakkalla başlarsın;
kamyonu karşılar, rafları dizer, kasada hesap alırsın. Aynı anda tek yerde olabildiğin için
oyunun kalbi "şimdi neye koşmalıyım?" kararıdır. Günler ilerledikçe müşteri artar; manav,
şarküteri, ikinci kasa açar, eleman alır, paket servis yaparsın.

## Çalıştırma

Oyun tek bir `index.html` dosyasıdır; derleme adımı yoktur. Tarayıcıda açman yeterli:

```bash
python3 -m http.server 8000
```

Sonra `http://localhost:8000/` adresini aç. Dosyaya çift tıklayıp açmak da çalışır.
İnternet gerekmez: yazı tipleri, görseller ve müzikler depodadır.

Denge ayarları paneli oyuncudan gizlidir; adresin sonuna `#dev` yazınca açılır
(`http://localhost:8000/#dev`).

## Test

```bash
node tests/smoke.js
```

Oyunu Chromium'da açar, otomatik bir oyuncuyla 5 gün oynatır; sayfada hata çıkarsa başarısız olur.
Playwright ve Chromium kurulu olmalıdır.

## Klasörler

| Klasör | İçerik |
| --- | --- |
| `index.html` | Oyunun tamamı (kurallar, çizim, arayüz) |
| `art/icons/` | 12 ürün simgesi (zemini silinmiş PNG) |
| `art/scene/` | Raf, manav standı, vitrin, kasa, zemin, palet, koli |
| `art/source/` | Google Flow'dan gelen orijinal görseller (kaynak) |
| `music/` | Sabah, gün içi ve akşam müzikleri (Google Lyria) |
| `fonts/` | Rubik ve Bungee (SIL Open Font License) |
| `icon/` | Uygulama simgesi (1024×1024) |
| `tool/key_art.py` | Görselin yeşil/mor zeminini silen, kırpıp boyutlandıran betik |
| `tests/smoke.js` | Duman testi |

## Yol haritası

Bkz. [ROADMAP.md](ROADMAP.md).
