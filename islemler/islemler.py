from datetime import datetime #tarihler arası farkı hesaplama için
from veritabani import data


class Araclar:
    def __init__(self):
        # aracları tutan bir listemiz olacak ve bu listenin içi sözlükten oluşacak. 
        self.arac_listesi = data.veri_yukle()

    def arac_ekle(self, plaka, marka, model, ucret):
        # plaka benzersiz
        # ücret sayı olacak
        # ücret 0 dan kucuk olmamalı
        
        for arac in self.arac_listesi:
            if arac["plaka"] == plaka:
                print("Plaka kayitli")
                return False 
        
        try:
            ucret = float(ucret) #ücret tipi hatalıysa
        except ValueError:
            print("Ücret sayisal olmali.")
            return False
        
        if ucret < 0: #kontrol yapıldıgı için if-else
            print("Ücret negatif olamaz")
            return False
        
        # her araç sözlük yapısında tutulacak çünkü json formatında kullanmanın en kolay yolu budur.
        arac = {
            "plaka": plaka,
            "marka": marka,
            "model": model,
            "ucret": ucret,
            "durum": "müsait",
            "kiralayan": "",
            "baslangic_tarihi": "",
            "bitis_tarihi": ""
        }
        
        self.arac_listesi.append(arac)
        data.veri_kaydet(self.arac_listesi)
        print("Arac basari ile eklendi.")
        return True 

    def arac_sil(self, plaka):
        # verilen plakaya ait aracı silecek
        # arac bulunamazsa hata mesajı
        for arac in self.arac_listesi:
            if arac["plaka"]==plaka: 
             self.arac_listesi.remove(arac)
             data.veri_kaydet(self.arac_listesi)
             print("Arac silindi")
             return True #fonksiyondan tamamen çıkar
        print("Araç bulunamadı!")
        return False
        
    def arac_duzenle(self, plaka, marka=None, model=None, ucret=None):
        for arac in self.arac_listesi:
            if arac["plaka"] != plaka:
                continue

            if marka is not None and marka != "":
                arac["marka"] = marka
            if model is not None and model != "":
                arac["model"] = model

            if ucret is not None and ucret != "":
                try:
                    ucret = float(ucret)
                except ValueError:
                    print("Ücret sayısal olmalı")
                    return False
                if ucret < 0:
                    print("Ücret negatif olamaz")
                    return False
                arac["ucret"] = ucret

            data.veri_kaydet(self.arac_listesi)
            print("Araç bilgileri düzenlendi")
            return True

        print("Araç bulunamadı")
        return False

        # Bir aracın ücret, model veya diğer bilgilerini günceller.
        # yeni_bilgiler = {"ucret": 900, "model": "Civic"}
        

    def kiralama_islemi(self, plaka, musteri, baslangic, bitis):
        # Araç müsait değilse kiralanamaz.
        # Tarih kontrlü (bitis > baslangic)
        # Toplam gün+ücret hesaplanır.
        tarih_fotmati="%Y-%m-%d"
        for arac in self.arac_listesi:
            if arac["plaka"]==plaka:
                if arac["durum"]!="müsait":
                    print("Araç kiralamaya uygun değil")
                    return False
                try:
                    d1=datetime.strptime(baslangic, tarih_fotmati)
                    d2=datetime.strptime(bitis, tarih_fotmati)

                    if d2<=d1:
                        print("Başlangıç tarihi bitiş tarihinden sonra olamaz. Geçerli tarih girişi yapınız.")
                        return False
                    
                    gun_sayisi=(d2-d1).days
                    toplam_ucret=gun_sayisi*arac["ucret"]

                    arac["durum"]="kirada"
                    arac["kiralayan"]=musteri
                    arac["baslangic_tarihi"]=baslangic
                    arac["bitis_tarihi"]=bitis

                    data.veri_kaydet(self.arac_listesi) #kiralama için kayıt işlemleri
                    print("Araç kiralandi\n")
                    print("Ödeme miktarı: ", toplam_ucret, "TL")
                    return True
                except ValueError:
                    print("Yıl-Ay-Gün formatında giriniz")
                    return False
            print("Araç bulunamadı")    
            return False

    def arac_iadesi(self, plaka):
        # Kirada olan bir aracın iadesini gerçekleştirir.
        # Durumu 'müsait' olarak değiştirir.
        for arac in self.arac_listesi:
            if arac["plaka"]==plaka:
                if arac["durum"]=="kirada":
                    arac["durum"]="müsait"
                    arac["kiralayan"]=""
                    arac["baslangic_tarihi"]=""
                    arac["bitis_tarihi"]=""

                    data.veri_kaydet(self.arac_listesi) #iade eildikten sonra araçın durumu değişiyor bunun için kayıt değişiyor.
                    print(plaka, "plakalı araç iade edildi")
                    return True
                else:
                    print("Bu araç kirada değil, başka araç seçiniz")
                    return False
        print("İade edilecek araç bulunamadı")
        return False


     
    