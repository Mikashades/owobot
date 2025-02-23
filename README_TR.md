# Discord Owo Bot

Discord'da otomatik mesaj gönderimi için captcha algılama özellikli basit bir OwO botu.

## Özellikler

- Özel aralıklarla çoklu mesaj gönderimi
- Koyu tema arayüzü
- Captcha algılama sistemi
- Sesli ve görsel uyarılar
- Mesaj günlüğü
- Captcha algılandığında otomatik durma

## Gereksinimler

```
pip install pyautogui
pip install pywin32
```

## Kullanım

1. Her mesaj için metin ve zaman aralığını (saniye cinsinden) girin
2. Kopya sayısını ayarlayın (1-5 arası, önerilen: 3)
3. "Başlat" düğmesine tıklayın
4. Discord mesaj giriş alanına tıklayın
5. Bot otomatik olarak:
   - Belirtilen aralıklarla mesaj gönderir
   - Captcha kontrolü yapar
   - Captcha algılandığında durur
   - Uyarı ve bildirimleri gösterir

## Önemli Notlar
- Bot Windows işletim sistemi gerektirir
- Fare imlecini mesaj alanının üzerinde tutun
- Bot captcha algılandığında otomatik olarak durur
- İngilizce (main_en.py) ve Türkçe (main_tr.py) olarak mevcuttur
- En az bir mesaj ve zaman aralığı doldurulmalıdır
- Zaman aralıkları pozitif sayı olmalıdır
- Kopya sayısı 1-5 arasında olmalıdır
- Geçersiz girişler hata mesajları tetikler
- Bot herhangi bir kritik hatada otomatik olarak durur

## Uyarı

Kullanım sorumluluğu size aittir. Bu bot sadece eğitim amaçlıdır.

Mikashades© tarafından yapılmıştır 