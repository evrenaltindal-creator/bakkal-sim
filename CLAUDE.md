# CLAUDE.md: Bakkal Sim için çalışma kuralları

Kullanıcıyla Türkçe konuş. Oyun 7 dildedir: tr (kaynak), en, de, es, pt (Brezilya), ru, ar (sağdan sola).

## Yapı

- Oyunun tamamı `index.html` içindedir: kurallar (`step`, müşteri, eleman, kamyon, paket),
  çizim (`draw`, `renderBg`), arayüz (sabah ekranı, rapor, ayarlar). Derleme yok.
- Görseller `art/`, müzik `music/`, yazı tipleri `fonts/` altındadır ve göreli yolla yüklenir.
  **İnternetten hiçbir şey yüklenmez** (App Store 4.2: uygulama web sitesi gibi davranmamalı).
  Yeni bir dış bağlantı ekleme.
- Mantıksal tuval 400×720'dir; ölçek ekrana göre hesaplanır.
- **Şubeler:** etkin dükkânın alanları `S` içindedir (`STORE_KEYS`), diğer dükkân `S.branches` içinde durur;
  `switchStore` yer değiştirir. Kasa, gün, seviye, hedefler, kredi ortaktır. Oyun kuralı yazarken gün için
  `S.day` değil dükkânın yaşı `sAge()` kullanılır (yeni şube sıfırdan büyür). Sen yokken şube `simBranch` ile
  sayılarla hesaplanır.

- **iPhone uygulaması** `ios/` altındadır: Xcode projesi `ios/project.yml`'dan XcodeGen ile üretilir (depoya
  girmez). Oyun dosyaları `ios/build_www.sh` ile `ios/www`'ye kopyalanıp uygulamaya gömülür ve WKWebView'da
  `bakkal://game/` adresinden açılır (`GameViewController.swift`, internet yok). Ses oturumu `ambient`'tir.
  Oyuna yeni bir klasör/dosya türü eklersen `build_www.sh`'a ve gerekirse MIME tablosuna ekle.
  Derleme ve TestFlight yüklemesi `.github/workflows/ios-testflight.yml` ile (elle başlatılır). Paket kimliği
  `com.vardiox.littlebakkal`; değiştirilirse iş akışı ve App Store Connect kaydı da değişir.

## Kurallar

- **Kayıt uyumu:** oyun `localStorage` içinde `bakkal.save.v2` anahtarıyla saklanır ve her
  güncellemeden sonra kaldığı yerden açılır. Durum (`S`) alanı eklerken eski kayıtta o alanın
  olmayabileceğini düşün (`S.x = S.x || ...`). Uyumsuz bir değişiklik gerekiyorsa `S.v`'yi artır
  ve eski kaydı dönüştür; oyuncunun ilerlemesini silme.
- **Görseller elle düzenlenmez.** Kaynak `art/source/` altındadır; `tool/key_art.py` ile
  yeniden üretilir. Yeşil parçası olan ürün (domates, elma) mor zeminde üretilir.
- Kullanıcı görselleri Google Flow (Nano Banana Pro), müzikleri Google Lyria ile üretir.
  Sohbette yanıt sürerken araya gönderilen görseller dosya olarak kaydedilmez; kullanıcıdan
  yeni bir mesajda göndermesini iste.
- Denge paneli yalnızca `#dev` ile açılır; oyuncu "Ayarlar"ı (müzik, yeni oyun) görür.
- **Çeviri:** oyuncuya görünen her metin `tx('Türkçe metin', [değerler])` ile yazılır; Türkçe metin anahtardır,
  değişkenler `{0}`, `{1}` yer tutucularıdır (dize birleştirme yapma, dillerde kelime sırası değişir).
  Yeni ya da değişen metni `i18n/src/keys.json` sonuna ekle, her dilin `i18n/src/<dil>.txt` dosyasına
  aynı numarayla çevirisini yaz ve `python3 tool/build_i18n.py` çalıştır (`i18n/<dil>.js` elle düzenlenmez;
  betik yer tutucuları denetler, çevirisi olmayan metni bildirir). Sayılar `fmt`/`fmtD`/`pct` ile yazılır.
  Arapçada hareke kullanma (yazı tipi harfi düşürüyor). Yerleşimde `left/right` yerine `inline-start/end`.
- Değişiklikten sonra `node tests/smoke.js` çalıştır (yedi dilde oynatır, çevrilmemiş Türkçeyi yakalar); hata varsa düzelt.
- Oyunun yayında bir önizlemesi vardır (claude.ai artifact). Güncellerken aynı adrese yayınla.
