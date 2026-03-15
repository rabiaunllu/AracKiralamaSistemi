import os
import json
from xml.etree.ElementTree import indent


def veri_yukle():

    #data.json dosyasi yoksa yeni dosya olusturur
    #encoding="utf-8" ile turkce karalter kullanimina izin verilir
    if not os.path.exists("data.json"):
        with open("data.json","w",encoding="utf-8") as f:
            f.write("[]")
        return []

    #data.json dosyasi varsa acilabilme durumunu kontrol eder ve acar
    #eger dosya bozuksa bos liste doner
    with open("data.json","r",encoding="utf-8") as f:
        try:
            veri= json.load(f)
            return veri
        except:
            return []

def veri_kaydet(arac_listesi):
    with open("data.json","w",indent=3,encoding="utf-8") as f:
        json.dump(arac_listesi,f,ensure_ascii=False, indent=3)
        # arac listesi json formatina cevrilir ve dosyaya (f) kaydedilir
        #ensure_ascii=False ile turkce karakter kullanimi icin
        #indent=3 json dosyasini hizali sekilde daha okunabilir gosterir