import sys
import os

# main.py'nin olduğu klasörden bir üst klasöre (proje ana dizinine) çıkıyoruz.
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

try:
    from arayuz import arayuz
except ImportError as e:
    print("Hata: Arayüz dosyası bulunamadı. Klasör yapısını kontrol edin.")
    print(f"Hata detayı: {e}")