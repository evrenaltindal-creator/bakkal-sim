# CLAUDE.md: Bakkal Sim için çalışma kuralları

Kullanıcıyla Türkçe konuş. Oyundaki her metin şimdilik Türkçedir (7 dil ROADMAP'te).

## Yapı

- Oyunun tamamı `index.html` içindedir: kurallar (`step`, müşteri, eleman, kamyon, paket),
  çizim (`draw`, `renderBg`), arayüz (sabah ekranı, rapor, ayarlar). Derleme yok.
- Görseller `art/`, müzik `music/`, yazı tipleri `fonts/` altındadır ve göreli yolla yüklenir.
  **İnternetten hiçbir şey yüklenmez** (App Store 4.2: uygulama web sitesi gibi davranmamalı).
  Yeni bir dış bağlantı ekleme.
- Mantıksal tuval 400×720'dir; ölçek ekrana göre hesaplanır.

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
- Değişiklikten sonra `node tests/smoke.js` çalıştır; hata varsa düzelt.
- Oyunun yayında bir önizlemesi vardır (claude.ai artifact). Güncellerken aynı adrese yayınla.
