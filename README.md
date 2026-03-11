# 💎 Instagram Activity Manager PRO

![Logo](logo.png)

**Developer:** Muhammed Emir Çeliksu  
**License:** MIT

## 📝 Proje Açıklaması
**Instagram Activity Manager**, Instagram dijital ayak izinizi profesyonelce temizlemeniz için tasarlanmış, modüler ve yüksek hızlı bir otomasyon aracıdır. Beğeniler, kaydedilen gönderiler ve yorumlar üzerinde tam kontrol sağlar. Artık tek bir dosya yerine, geliştirilmeye açık modüler bir yapıya sahiptir.

---

## ✨ Özellikler
*   **🌍 AI Dinamik Çeviri:** Arapça, Rusça, Fransızca dahil tüm dilleri saniyeler içinde anlar.
*   **🚀 Turbo Beğeni Süpürme:** API tabanlı sistemle binlerce beğeniyi dakikalar içinde kaldırır.
*   **📦 Kaydedilenler Temizliği:** "Tüm Gönderiler" koleksiyonunu tek tıkla boşaltır.
*   **💬 Tarayıcı Tabanlı Yorum Silme:** Güvenli otomasyon ile eski yorumlarınızı tarihe gömer.
*   **🛡️ Gölge Profil (Shadow Mode):** Tarayıcınız açık olsa bile profil kilitlenmesi yaşamadan çalışır.
*   **🤖 Otomatik Kurulum:** Eksik modülleri ve sanal ortamı (venv) kendisi hazırlar.
*   **📁 Arşivleme:** Silinen her öğenin URL'sini zaman damgasıyla `logs/` altına kaydeder.

---

## 🛠️ Kurulum

### 1. Gereksinimler
*   Python 3.8+
*   Sisteminizde yüklü bir tarayıcı (Zen, Chrome, Brave, Firefox veya Edge)

### 2. Başlatma
Sadece ana klasöre girin ve dosyayı çalıştırın; gerisini sistem halleder:
```bash
python3 instagram_manager.py
```

---

## 🚀 Kullanım
1.  Uygulamayı çalıştırdığınızda dil tercihinizi yapın (`tr`, `en` vb.).
2.  Ana menüden yapmak istediğiniz işlemi seçin:
    *   **1:** Sadece Beğenileri temizler.
    *   **2:** Sadece Kaydedilen gönderileri temizler.
    *   **3:** Yorumları temizlemek için güvenli bir tarayıcı penceresi açar.
    *   **4:** Hepsini birden temizler.
3.  Oturum bilgileri, bilgisayarınızda açık olan tarayıcı profilinden **şifrenize ihtiyaç duymadan** saniyeler içinde çekilir.

---

## 🏗️ Proje Yapısı
```
instagram-manager/
├── instagram_manager.py (Ana Giriş)
├── requirements.txt
├── README.md
├── LICENSE
├── logo.png
├── modules/
│   ├── likes.py (Beğeni & Kaydetme Mantığı)
│   ├── comments.py (Yorum Silme Mantığı)
│   └── cleaner.py (Ortak Temizlik Altyapısı)
└── utils/
    └── language.py (Çeviri & Dil Yönetimi)
```

---

## 📜 Lisans
Bu proje **MIT Lisansı** ile lisanslanmıştır. **Muhammed Emir Çeliksu** tarafından geliştirilmiştir.

---
*Not: Bu araç sadece kişisel kullanım içindir. Sorumlu kullanım ve Instagram kullanım koşullarına uyulması önerilir.*
