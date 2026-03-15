# 🚗 Araç Kiralama Otomasyon Sistemi

[cite_start]Bu proje, Marmara Üniversitesi **Bilgisayar Programlama II** dersi kapsamında geliştirilmiş; modüler yapıda ve Nesne Yönelimli Programlama (OOP) prensiplerini temel alan bir masaüstü yazılımıdır[cite: 4, 18, 196].

[cite_start]Uygulama, bir araç kiralama ofisinin tüm envanter yönetimini ve kiralama süreçlerini dijital ortama taşıyarak operasyonel verimliliği artırmayı amaçlar[cite: 47, 48].

## 🛠️ Öne Çıkan Teknik Özellikler

Projenin teknik altyapısı, sürdürülebilir ve hatasız bir çalışma deneyimi sunmak üzere tasarlanmıştır:

* 🏗️ **Modüler Mimari:** Proje; [cite_start]`main`, `arayuz`, `islemler` ve `veritabani` olmak üzere 4 ana katmana ayrılmıştır[cite: 23, 24, 93, 97].
* [cite_start]📦 **Dinamik Veri Yönetimi:** Veritabanı olarak JSON formatı (`data.json` ve `gecmis.json`) tercih edilerek uygulamanın taşınabilir olması sağlanmıştır[cite: 20, 29, 63, 64].
* [cite_start]🔍 **Regex ile Veri Doğrulama:** Türkiye standartlarına uygun plaka kontrolü, düzenli ifadeler (Regex) ile sistem seviyesinde yapılmaktadır[cite: 21, 65, 67, 131].
* [cite_start]💰 **Akıllı Ücret Hesaplama:** `datetime` modülü kullanılarak, kiralama ve iade tarihleri arasındaki gün farkı üzerinden maliyet hesaplamaları otomatik olarak gerçekleştirilir[cite: 35, 136, 140].

## 💻 Kullanıcı Deneyimi

Kullanıcı dostu arayüz elemanları ile sistem yönetimi kolaylaştırılmıştır:

* [cite_start]🎨 **Renk Kodlu Takip:** Treeview üzerinde müsait araçlar **yeşil**, kiradaki araçlar ise **kırmızı** renkle vurgulanarak görsel takip kolaylığı sağlanmıştır[cite: 39, 150, 151, 152].
* [cite_start]⚡ **Anlık Filtreleme:** Kullanıcı arama kutusuna yazı yazdığı anda liste `KeyRelease` olayı ile eş zamanlı olarak güncellenir[cite: 40, 153, 154].
* [cite_start]⚠️ **Hata Yönetimi:** Geçersiz veri girişleri (negatif ücret, hatalı plaka formatı vb.) `try-except` blokları ve `messagebox` uyarıları ile engellenmiştir[cite: 41, 42, 178, 179].

## 📂 Proje Yapısı

Sistem, yazılım mühendisliği standartlarına uygun olarak modüler bir katmanlı mimari ile çalışır:

* [cite_start]**`main/`**: Uygulamanın giriş noktası ve ana döngünün yönetimi[cite: 25, 99, 103].
* [cite_start]**`islemler/`**: İş mantığı; araç ekleme, silme ve kiralama hesaplamaları[cite: 26, 100, 105, 106].
* [cite_start]**`arayuz/`**: Görsel tasarım, formlar ve kullanıcı etkileşimi[cite: 27, 101, 110, 112].
* [cite_start]**`veritabani/`**: JSON veri yönetimi ve dosya okuma/yazma (I/O) işlemleri[cite: 28, 102, 113, 114].

