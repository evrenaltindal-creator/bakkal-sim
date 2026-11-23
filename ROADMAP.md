# Yol haritası

## Faz 1: Bakkal'ı App Store'a hazırla (2D piksel, iPhone)

| # | Adım | Durum |
| --- | --- | --- |
| – | Müzik (sabah, gün içi, akşam) | ✅ |
| – | 12 ürün simgesi, raflar, manav, vitrin, kasa, depo, zemin | ✅ |
| – | Uygulama simgesi: `icon/app-icon-1024.png` (orijinal) | ✅ |
| 1 | Depoya taşıma, internetsiz çalışma, denge panelini gizleme | ✅ |
| 2 | Ses efektleri (kasa, kapı zili, kamyon kornası, motorcu, poşet, kızgın müşteri, seviye) | ✅ |
| 3 | Hırsız: 4. gün ilk (siyah kapüşonlu, öğretici), 5–9 günde 1, 10+ normal kıyafetli ve davranışından anlaşılan, 15+ ara sıra iki kişilik ekip. Yanlış kişiyi durdurmak itibarı sert düşürür | ✅ |
| 4 | Hedefler ve mahalle seviyesi (günde 3 hedef, 10 seviye, para ve kalıcı avantaj ödülleri) | ✅ |
| 5 | Oyun sonu: 30.000 ₺ + itibar 80 + seviye 10 olunca "Mahallenin efsanesi" ekranı. Seçenekler: yeni mahallede baştan başla (★ esnaf yıldızı: toptancı indirimi, başlangıç parası ve itibarı) ya da devam et. **İkinci şube** ilk güncellemeye kaldı. | 🟡 |
| 6 | İsim: **Little Bakkal** + 7 dil: tr, en, de, es, pt-BR, ru, ar | ⬜ |
| 7 | iOS paketi (WKWebView/Capacitor, internetsiz) → TestFlight, 5–10 kişi bir hafta Ses oturumu `ambient` olmalı: oyuncu kendi müziğini (Spotify vb.) dinlerken oyun onu durdurmamalı, efektler üstüne çalmalı. | ⬜ |
| 8 | Düzeltmeler → gizlilik sayfası, ekran görüntüleri → App Store | ⬜ |

## Sonrası

Little Bakkal kendi başına bitmiş, satılan bir oyun olacak. Büyük vizyon (bakkal → zincir → market → holding,
bakkal ve depo oyuncularının ortak pazarda buluşması) ayrı ve daha büyük bir proje olarak, aynı mekaniklerle 2.5D yapılacak.


- **Faz 2:** Android / Google Play (aynı kod)
- **Faz 3:** Unity ile 2.5D sürüm (Steam + mobil), aynı mekaniklerle
- **Faz 4:** Depo aşaması (oyun içinde tedarikçilik)
- **Faz 5:** Online ortak pazar (sunucu, hesaplar, hileye karşı koruma; serbest sohbet yerine
  hazır mesajlar, çünkü Apple kullanıcılar arası yazışmada şikâyet/engelleme/filtre ister)

## Bilinen denge notları

- Oyuncu 5–6 saatte her şeyi açıyor (iki kasa, manav, şarküteri, 3 eleman). Hedefler ve şube
  bu noktadan sonrasını taşımalı; zorluk sert bir duvar olmamalı.
- Üç elemanın maaşı (~940 ₺/gün) ilk zamanlarda kârı eksiye çekebiliyor; bilinçli bir karar.
