import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import datetime
import re  #formatlı plaka kontrolü için

# Mevcut dizini bul
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Bir üst klasöre çık ve veritabani klasörüne gir
# /AracKiralamaProjesi/veritabani/data.json
VERI_DOSYASI = os.path.normpath(
    os.path.join(BASE_DIR, "..", "veritabani", "data.json")
)

GECMIS_DOSYASI = os.path.normpath(
    os.path.join(BASE_DIR, "..", "veritabani", "gecmis.json")
)

#RENKLER
RENK_ARKA = "#F5F7FA"
RENK_PANEL = "#FFFFFF"
RENK_BUTON_EKLE = "#4A90E2"     
RENK_BUTON_FILTRE = "#5CC689"  
RENK_BUTON_TEMIZLE = "#E57373"  
RENK_BUTON_ISLEM = "#78909C"    
RENK_BASLIK = "#2C3E50"

RENK_EKLE_ALAN = "#EAF2FF"
RENK_ENTRY_ARKA = "#F8FAFF"

RENK_SATIR_MUSAIT = "#C8E6C9"  
RENK_SATIR_KIRADA = "#FFCDD2"   

RENK_FILTRE_ALAN = "#EAF2FF"

#markalar listesi checkbox ile seçilecek 
MARKALAR = ["Hyundai", "Audi", "BMW", "Chery", "Citroen", "Dacia", "Fiat", "Renault", "Ford", "Honda","KIA"]

def marka_normalize(marka: str) -> str:#normalize aynı markanın farklı yazımlarını tek formata indirgiyor
    m_in = (marka or "").strip()
    for m in MARKALAR:#Tanımlı markalar içinde ara
        if m_in.casefold() == m.casefold(): # casefold() karşılaştırması (büyük/küçük harf duyarsız)
            return m  #listede varsa oradaki halini göndüürür
    return ilk_harf_buyuk(m_in)

# dosya kontrolü
def veri_yukle():
    if not os.path.exists(VERI_DOSYASI):
        return []
    try:
        with open(VERI_DOSYASI, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

#Dosya yoksa program çalışmaya devam etsin diye [] döndürüyoruz kayıtlar JSON formatında saklanıyor
def veri_kaydet(veri):
    with open(VERI_DOSYASI, "w", encoding="utf-8") as f:
        json.dump(veri, f, indent=4, ensure_ascii=False)


def gecmis_yukle():
    if not os.path.exists(GECMIS_DOSYASI):
        return []
    try:
        with open(GECMIS_DOSYASI, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def gecmis_kaydet(kayit):
    if "musteri" in kayit:
        kayit["musteri"] = isim_duzelt(kayit.get("musteri", ""))
    gecmis = gecmis_yukle()
    gecmis.append(kayit)
    with open(GECMIS_DOSYASI, "w", encoding="utf-8") as f:
        json.dump(gecmis, f, indent=4, ensure_ascii=False)


def ilk_harf_buyuk(text: str) -> str:
    text = (text or "").strip()
    if not text:
        return ""
    return " ".join(w[:1].upper() + w[1:].lower() for w in text.split())

# sisteme verileri yükleme
veriler = veri_yukle()
# Önce marka, sonra model, sonra plaka
print("DOSYA:", VERI_DOSYASI, "ARAC SAYISI:", len(veriler))
def verileri_sirala():
    veriler.sort(key=lambda a: ( #lambda, her araç için (marka, model, plaka) üçlüsünü üretir ve  sıralamayı soldan sağa yapar.
        str(a.get("marka", "")).casefold(),
        str(a.get("model", "")).casefold(),
        str(a.get("plaka", "")).casefold()
    ))
verileri_sirala()
# Eski kayıtlarda alan yoksa hata olmasın
for a in veriler: #set default ile sozlük yapısında değeer yoksa default deger ekler
    a.setdefault("durum", "Müsait")
    a.setdefault("kiralayan", "")
    a.setdefault("baslangic_tarihi", "")
    a.setdefault("bitis_tarihi", "")

degisiklik_var = False
for a in veriler:
    eski_marka = a.get("marka", "")
    eski_model = a.get("model", "")

    yeni_marka = marka_normalize(eski_marka)
    yeni_model = ilk_harf_buyuk(eski_model)

    if yeni_marka != eski_marka:
        a["marka"] = yeni_marka
        degisiklik_var = True
    if yeni_model != eski_model:
        a["model"] = yeni_model
        degisiklik_var = True

if degisiklik_var:
    veri_kaydet(veriler)

#Arayüz tasarımı
#pack ile hizalama yapıldı genişletilebilirliği kolaylaştırmak için sol sabit genişlik, sağ ise genişleyen panel
pencere = tk.Tk()
pencere.title("Araç Kiralama Sistemi")
pencere.geometry("1250x750")
pencere.configure(bg=RENK_ARKA)

sol_panel = tk.Frame(pencere, bg=RENK_PANEL, width=300)#frame ile düzenli olunması sağlandı
sol_panel.pack(side="left", fill="y", padx=15, pady=15)

# Araç ekleme arayüzü
frm_arac_ekle = tk.Frame(sol_panel, bg=RENK_EKLE_ALAN, bd=1, relief="solid")
frm_arac_ekle.pack(fill="x", pady=(10, 10))

tk.Label(
    frm_arac_ekle, text="Yeni Araç Ekle", bg=RENK_EKLE_ALAN, fg=RENK_BASLIK,
    font=("Segoe UI", 12, "bold")
).pack(pady=(10, 10))

def ilk_harf_buyuk(text: str) -> str:
    text = (text or "").strip()
    if not text:
        return ""
    return " ".join(w[:1].upper() + w[1:].lower() for w in text.split())


def entry_olustur(baslik, parent):
    tk.Label(parent, text=baslik, bg=RENK_EKLE_ALAN, font=("Segoe UI", 9)).pack(anchor="w", pady=(5, 0), padx=10)
    e = tk.Entry(parent, font=("Segoe UI", 9), bd=1, relief="solid", bg=RENK_ENTRY_ARKA)
    e.pack(fill="x", pady=2, padx=10)
    return e


entry_plaka = entry_olustur("Plaka (Örn: 34 ABC 123):", frm_arac_ekle)
entry_marka = entry_olustur("Marka:", frm_arac_ekle)
entry_model = entry_olustur("Model:", frm_arac_ekle)
entry_ucret = entry_olustur("Günlük Ücret (₺):", frm_arac_ekle)


def temizle_giris_alanlari():
    entry_plaka.delete(0, tk.END)
    entry_marka.delete(0, tk.END)
    entry_model.delete(0, tk.END)
    entry_ucret.delete(0, tk.END)

def plaka_kontrol(plaka):#plaka kntrolü rexes ile: sayı+harf+sayı
    plaka = (plaka or "").strip().upper()
    plaka = " ".join(plaka.split())  # fazla boşlukları teke indir

    patron = r"^(0[1-9]|[1-7][0-9]|8[01])\s+[A-Z]{1,3}\s+\d{2,5}$"
    return bool(re.match(patron, plaka))

def marka_normalize(marka: str) -> str:#normalize aynı markanın farklı yazımlarını tek formata indirgiyor
    m_in = (marka or "").strip()
    for m in MARKALAR:
        if m_in.casefold() == m.casefold():
            return m  
    return ilk_harf_buyuk(m_in)

def isim_duzelt(ad_soyad: str) -> str:
    s = (ad_soyad or "").strip()
    s = " ".join(s.split())
    if not s or s == "-":
        return s
    return " ".join(k.capitalize() for k in s.split(" "))

def arac_ekle():
    plaka = entry_plaka.get().strip().upper()
    marka = marka_normalize(entry_marka.get())
    model = ilk_harf_buyuk(entry_model.get())
    ucret = entry_ucret.get().strip()

    if not all([plaka, marka, model, ucret]):
        messagebox.showwarning("Eksik Bilgi", "Lütfen tüm alanları doldurun.")
        return

    if not plaka_kontrol(plaka):
        messagebox.showerror("Hatalı Plaka", "Plaka formatı geçersiz!")
        return

    for a in veriler:
        if a.get("plaka") == plaka:
            messagebox.showerror("Hata", "Bu plaka kayıtlı!")
            return

    try:
        ucret_f = float(ucret)
    except ValueError:
        messagebox.showerror("Hata", "Ücret sayısal olmalı.")
        return

    if ucret_f < 0:
        messagebox.showerror("Hata", "Ücret negatif olamaz.")
        return

    veriler.append({
        "plaka": plaka,
        "marka": marka,
        "model": model,
        "ucret": ucret_f,
        "durum": "Müsait",
        "kiralayan": "",
        "baslangic_tarihi": "",
        "bitis_tarihi": ""
    })
    verileri_sirala()
    veri_kaydet(veriler)
    tablo_guncelle()
    temizle_giris_alanlari()
    messagebox.showinfo("Başarılı", "Araç başarıyla eklendi.")


tk.Button(
    frm_arac_ekle, text="Araç Ekle", command=arac_ekle,
    bg=RENK_BUTON_EKLE, fg="white", font=("bold"), pady=5#pady yazı ile buton arası bosluk
).pack(fill="x", pady=(15, 15), padx=10)#pack ile butonnu yerleştirme

# geçmiş işlemleri gösterme
#win ana pencere üzerinde açılan kiralama geçmişini gösteren penceredir.
def gecmis_goster_penceresi():
    win = tk.Toplevel(pencere)#sayfa üstünde açılsın
    win.title("İşlem Geçmişi")
    win.geometry("720x460")

    filtre_frm = tk.Frame(win, pady=8)
    filtre_frm.pack(fill="x")

    tk.Label(filtre_frm, text="Başlangıç (GG-AA-YYYY):").pack(side="left", padx=(10, 5))
    e_bas = tk.Entry(filtre_frm, width=12)
    e_bas.pack(side="left")

    tk.Label(filtre_frm, text="Bitiş (GG-AA-YYYY):").pack(side="left", padx=(10, 5))
    e_bit = tk.Entry(filtre_frm, width=12)
    e_bit.pack(side="left")

    cols = ("Tarih", "İşlem", "Plaka", "Müşteri")
    tree = ttk.Treeview(win, columns=cols, show="headings")#tablo görnüm için treeview , show headings sadce columms için

    for c in cols:
        tree.heading(c, text=c)
        tree.column(c, width=170, anchor="center")

    tree.pack(fill="both", expand=True)#fill=both yatayda dikey doldur, expand=True pencere büyürse tablo da büyüuto

    #okunabilirkil için 
    tree.tag_configure("even", background="#FFFFFF")
    tree.tag_configure("odd", background="#F3F7FF")

    def listeyi_doldur(kayitlar):#en son yapılan işlem üstte görünecek
        tree.delete(*tree.get_children())
        for i, k in enumerate(kayitlar):
            tag = "even" if i % 2 == 0 else "odd"
            tree.insert(
                "",
                "end",
                values=(k.get("tarih"), k.get("islem"), k.get("plaka"), k.get("musteri")),
                tags=(tag,)
            )

    tum_kayitlar = list(reversed(gecmis_yukle()))
    degisti = False
    for k in tum_kayitlar:
        eski = k.get("musteri", "")
        yeni = isim_duzelt(eski)
        if yeni != eski:
            k["musteri"] = yeni
            degisti = True

    if degisti:
        with open(GECMIS_DOSYASI, "w", encoding="utf-8") as f:
            json.dump(list(reversed(tum_kayitlar)), f, indent=4, ensure_ascii=False)

    listeyi_doldur(tum_kayitlar)

    def filtrele():
        bas_str = e_bas.get().strip()
        bit_str = e_bit.get().strip()

        if not bas_str and not bit_str:
            listeyi_doldur(tum_kayitlar)
            return

        try:
            bas_dt = datetime.datetime.strptime(bas_str, "%d-%m-%Y") if bas_str else None
            bit_dt = datetime.datetime.strptime(bit_str, "%d-%m-%Y") if bit_str else None
        except:
            messagebox.showerror("Hata", "Tarih formatı GG-AA-YYYY olmalı.")
            return

        if bit_dt is not None:
            bit_dt = bit_dt.replace(hour=23, minute=59, second=59)

        filtreli = []
        for k in tum_kayitlar:
            t = k.get("tarih", "")
            try:
                kayit_dt = datetime.datetime.strptime(t, "%Y-%m-%d %H:%M")
            except:
                continue

            if bas_dt is not None and kayit_dt < bas_dt:
                continue
            if bit_dt is not None and kayit_dt > bit_dt:
                continue

            filtreli.append(k)

        listeyi_doldur(filtreli)

    def temizle():
        e_bas.delete(0, tk.END)
        e_bit.delete(0, tk.END)
        listeyi_doldur(tum_kayitlar)
    
    tk.Button(
        filtre_frm, text="Filtrele", command=filtrele,
        bg=RENK_BUTON_EKLE, fg="white", font=("bold"), pady=4
    ).pack(side="left", padx=10)

    tk.Button(
        filtre_frm, text="Temizle", command=temizle,
        bg=RENK_BUTON_EKLE, fg="white", font=("bold"), pady=4
    ).pack(side="left")

tk.Button(
    sol_panel, text="📜 Kiralama Geçmişi", command=gecmis_goster_penceresi,
    bg="#607D8B", fg="white", font=("bold"), pady=5
).pack(fill="x", pady=5)

# Filtreleme işlemleri
frm_filtre = tk.Frame(sol_panel, bg=RENK_FILTRE_ALAN, bd=1, relief="solid")
frm_filtre.pack(fill="x", pady=(10, 10))

tk.Label(
    frm_filtre, text="Filtreleme", bg=RENK_FILTRE_ALAN, fg=RENK_BASLIK,
    font=("Segoe UI", 12, "bold")
).pack(pady=(10, 5))

combo_durum = ttk.Combobox(frm_filtre, values=["Tümü", "Müsait", "Kirada"], state="readonly")
combo_durum.current(0)
combo_durum.pack(fill="x", pady=5, padx=10)
#Combobox, kullanıcıya önceden belirlenmiş seçeneklerden seçim yaptırmak için kullanılır. readonly ile yazı girişi engellenir

tk.Label(
    frm_filtre, text="Maksimum Günlük Ücret (₺):", bg=RENK_FILTRE_ALAN,
    font=("Segoe UI", 9, "bold")
).pack(anchor="w", pady=(10, 0), padx=10)

entry_maks_ucret = tk.Entry(frm_filtre, bd=1, relief="solid", bg="#FFFDF7")
entry_maks_ucret.insert(0, "15000")
entry_maks_ucret.pack(fill="x", pady=5, padx=10)

tk.Label(
    frm_filtre, text="Markalar:", bg=RENK_FILTRE_ALAN, font=("Segoe UI", 9, "bold")
).pack(anchor="w", pady=(10, 0), padx=10)#sola dayattık west

marka_vars = {}#seçilen maraklar burada tutlacak

frm_markalar_dis = tk.Frame(frm_filtre, bg=RENK_FILTRE_ALAN)
frm_markalar_dis.pack(fill="x", padx=10, pady=(5, 5))
#Frame canvas içine konur scroll için
canvas = tk.Canvas(frm_markalar_dis, bg=RENK_FILTRE_ALAN, highlightthickness=0, height=120)
scrollbar = tk.Scrollbar(frm_markalar_dis, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

frm_markalar = tk.Frame(canvas, bg=RENK_FILTRE_ALAN)
canvas.create_window((0, 0), window=frm_markalar, anchor="nw")


def _marka_scroll_guncelle(event=None):
    canvas.configure(scrollregion=canvas.bbox("all"))


frm_markalar.bind("<Configure>", _marka_scroll_guncelle)

for m in MARKALAR:
    var = tk.BooleanVar(value=0)
    tk.Checkbutton(frm_markalar, text=m, variable=var, bg=RENK_FILTRE_ALAN, anchor="w").pack(fill="x")
    marka_vars[m] = var

#mouse tekerleği ile canvasın kaydırılmasını ve sadece mouse canvas üzerindeyken aktif olmasını sağlar.
def _mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


def _bind_mousewheel(event):
    canvas.bind_all("<MouseWheel>", _mousewheel)


def _unbind_mousewheel(event):
    canvas.unbind_all("<MouseWheel>")


canvas.bind("<Enter>", _bind_mousewheel)
canvas.bind("<Leave>", _unbind_mousewheel)#canvas üzerindeyken işlevleştirmek için

#Filtreleme arayarak 
tk.Label(frm_filtre, text="Arama (plaka/marka/model):", bg=RENK_FILTRE_ALAN,
         font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(10, 0), padx=10)
#kullanıcı giriş
entry_ara = tk.Entry(frm_filtre, bd=1, relief="solid", bg="#FFFDF7")
entry_ara.pack(fill="x", pady=5, padx=10)

sag_panel = tk.Frame(pencere, bg=RENK_ARKA)
sag_panel.pack(fill="both", expand=True, padx=20, pady=20)

frm_stat = tk.Frame(sag_panel, bg="#E3F2FD", pady=10)
frm_stat.pack(fill="x", pady=(0, 10))

lbl_toplam = tk.Label(frm_stat, text="Araç: 0", bg="#E3F2FD", font=("bold"), padx=15)
lbl_toplam.pack(side="left")

lbl_kirada = tk.Label(frm_stat, text="Kirada: 0", bg="#E3F2FD", fg="red", font=("bold"), padx=15)
lbl_kirada.pack(side="left")

lbl_musait = tk.Label(frm_stat, text="Müsait: 0", bg="#E3F2FD", fg="green", font=("bold"), padx=15)
lbl_musait.pack(side="left")

tablo = ttk.Treeview(sag_panel, columns=("Plaka", "Marka", "Model", "Ücret", "Durum"), show="headings")
for c in ("Plaka", "Marka", "Model", "Ücret", "Durum"):
    tablo.heading(c, text=c)
    tablo.column(c, anchor="center")
tablo.pack(fill="both", expand=True)

tablo.tag_configure("musait", background=RENK_SATIR_MUSAIT)
tablo.tag_configure("kirada", background=RENK_SATIR_KIRADA)

alt_panel = tk.Frame(pencere, bg=RENK_ARKA)
alt_panel.pack(fill="x", pady=10)


def secili_arac_getir():#treeviewdan seçili aracı getirir
    s = tablo.selection()
    if not s:
        return None
    values = tablo.item(s[0]).get("values", [])
    return values[0] if values else None#plaka döndürür sadece


def arac_bul(plaka):
    for a in veriler:
        if a.get("plaka") == plaka:
            return a
    return None


def filtre_uygula():
    durum = combo_durum.get().strip().casefold()
    aranan = entry_ara.get().strip().casefold()#büyük küçük farkını kaldırır

    try:
        maks = float(entry_maks_ucret.get().strip()) if entry_maks_ucret.get().strip() else 15000
    except:
        messagebox.showerror("Hata", "Maksimum ücret sayısal olmalı.")
        return

    secili_markalar = [m for m, v in marka_vars.items() if v.get()]

    tablo.delete(*tablo.get_children())#treeviewdaki satırları ver. eski tabloyu sil, filtrelenmiş halini getirir
#* ile tüm satrı bilgisine ulaşılır tüm fonksiyonel

    kirada_sayisi = 0
    for a in veriler:
        a_durum = str(a.get("durum", "Müsait"))
        if durum != "tümü" and a_durum.casefold() != durum:
            continue

        if secili_markalar and a.get("marka") not in secili_markalar:
            continue

        try:
            if float(a.get("ucret", 0)) > maks:
                continue
        except:
            continue

        metin = f"{a.get('plaka','')} {a.get('marka','')} {a.get('model','')}".strip().casefold()
        if aranan and aranan not in metin:
            continue

        tag = "musait" if a_durum == "Müsait" else "kirada" if a_durum == "Kirada" else ""
        tablo.insert("", "end",
                     values=(a.get("plaka"), a.get("marka"), a.get("model"), a.get("ucret"), a_durum),
                     tags=(tag,))
        if a_durum == "Kirada":
            kirada_sayisi += 1

    lbl_toplam.config(text=f"🚗 Toplam: {len(veriler)}")
    lbl_kirada.config(text=f"❌ Kirada: {kirada_sayisi}")
    lbl_musait.config(text=f"✅ Müsait: {len(veriler) - kirada_sayisi}")


def filtre_temizle():
    combo_durum.current(0)#tümü müait kirada
    entry_maks_ucret.delete(0, tk.END)
    entry_maks_ucret.insert(0, "15000")
    for v in marka_vars.values():
        v.set(0)#checokbox temizlenşr
    entry_ara.delete(0, tk.END)#arama kısmı temzlenir
    tablo_guncelle()

# Butonlar
tk.Button(frm_filtre, text="🔍 Filtrele", command=filtre_uygula, bg=RENK_BUTON_FILTRE, fg="white", pady=5)\
    .pack(fill="x", pady=5, padx=10)

tk.Button(frm_filtre, text="🧹 Temizle", command=filtre_temizle, bg=RENK_BUTON_TEMIZLE, fg="white", pady=5)\
    .pack(fill="x", padx=10, pady=(0, 10))

# Enter ile ve yazdıkça filtre uygula
entry_ara.bind("<Return>", lambda e: filtre_uygula())
entry_ara.bind("<KeyRelease>", lambda e: filtre_uygula())#bind, kullanıcıdan gelen klavye olaylarına tepki vermek için kullanılır.
#<Return> Enter tuşunu, <KeyRelease> tuş bırakma olayını temsil eder

#Bilgileri getir butonu
def bilgileri_getir_penceresi_ac():
    plaka = secili_arac_getir()
    if not plaka:
        messagebox.showerror("Hata", "Bilgileri görmek için listeden bir araç seçmelisiniz.")
        return

    a = arac_bul(plaka)
    if not a:
        messagebox.showerror("Hata", "Seçili araç verilerde bulunamadı.")
        return

    win = tk.Toplevel(pencere)
    win.title(f"Araç Bilgileri: {plaka}")
    win.configure(bg="#F3F7FF")
    win.resizable(False, False)

    frm = tk.Frame(win, bg="#F3F7FF")
    frm.pack(padx=18, pady=18)

    tk.Label(frm, text="Araç Detayları", bg="#F3F7FF", fg=RENK_BASLIK,
             font=("Segoe UI", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 15))

    lbl_font = ("Segoe UI", 10, "bold")
    val_font = ("Segoe UI", 10)

    def satir(r, baslik, deger):
        tk.Label(frm, text=baslik, bg="#F3F7FF", font=lbl_font)\
            .grid(row=r, column=0, sticky="e", padx=(0, 10), pady=6)
        tk.Label(frm, text=deger, bg="#F3F7FF", font=val_font)\
            .grid(row=r, column=1, sticky="w", pady=6)

    satir(1, "Plaka:", a.get("plaka", "-"))
    satir(2, "Marka:", a.get("marka", "-"))
    satir(3, "Model:", a.get("model", "-"))
    satir(4, "Günlük Ücret (₺):", str(a.get("ucret", "-")))
    satir(5, "Durum:", a.get("durum", "-"))

    kiralayan = a.get("kiralayan") or "-"
    bas = a.get("baslangic_tarihi") or "-"
    bit = a.get("bitis_tarihi") or "-"
    satir(6, "Kiralayan:", kiralayan)
    satir(7, "Başlangıç Tarihi:", bas)
    satir(8, "Bitiş Tarihi:", bit)

    tk.Button(frm, text="Kapat", command=win.destroy, bg=RENK_BUTON_ISLEM, fg="white",
              font=("Segoe UI", 10, "bold"), pady=6)\
        .grid(row=9, column=0, columnspan=2, pady=(16, 0), ipadx=12)

# Güncelle butonu
def guncelle_penceresi_ac():
    plaka = secili_arac_getir()
    if not plaka:
        messagebox.showerror("Hata", "Güncellemek için listeden bir araç seçmelisiniz.")
        return

    a = arac_bul(plaka)
    if not a:
        messagebox.showerror("Hata", "Seçili araç verilerde bulunamadı.")
        return

    win = tk.Toplevel(pencere)
    win.title(f"Araç Güncelle: {plaka}")
    win.configure(bg="#F3F7FF")
    win.resizable(False, False)

    frm = tk.Frame(win, bg="#F3F7FF")
    frm.pack(padx=18, pady=18)

    tk.Label(frm, text="Araç Bilgilerini Güncelle", bg="#F3F7FF", fg=RENK_BASLIK,
             font=("Segoe UI", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 15))

    lbl_font = ("Segoe UI", 10, "bold")
    ent_font = ("Segoe UI", 10)
    entry_width = 28

    tk.Label(frm, text="Plaka:", bg="#F3F7FF", font=lbl_font)\
        .grid(row=1, column=0, sticky="e", padx=(0, 10), pady=6)
    e_plaka = tk.Entry(frm, font=ent_font, width=entry_width, bd=1, relief="solid", bg="#FFFFFF")
    e_plaka.grid(row=1, column=1, sticky="w", pady=6)
    e_plaka.insert(0, a.get("plaka", ""))
    e_plaka.config(state="disabled")

    tk.Label(frm, text="Marka:", bg="#F3F7FF", font=lbl_font)\
        .grid(row=2, column=0, sticky="e", padx=(0, 10), pady=6)
    e_marka = tk.Entry(frm, font=ent_font, width=entry_width, bd=1, relief="solid", bg="#FFFFFF")
    e_marka.grid(row=2, column=1, sticky="w", pady=6)
    e_marka.insert(0, a.get("marka", ""))

    tk.Label(frm, text="Model:", bg="#F3F7FF", font=lbl_font)\
        .grid(row=3, column=0, sticky="e", padx=(0, 10), pady=6)
    e_model = tk.Entry(frm, font=ent_font, width=entry_width, bd=1, relief="solid", bg="#FFFFFF")
    e_model.grid(row=3, column=1, sticky="w", pady=6)
    e_model.insert(0, a.get("model", ""))

    tk.Label(frm, text="Günlük Ücret (₺):", bg="#F3F7FF", font=lbl_font)\
        .grid(row=4, column=0, sticky="e", padx=(0, 10), pady=6)
    e_ucret = tk.Entry(frm, font=ent_font, width=entry_width, bd=1, relief="solid", bg="#FFFFFF")
    e_ucret.grid(row=4, column=1, sticky="w", pady=6)
    e_ucret.insert(0, str(a.get("ucret", "")))

    def kaydet():
        yeni_marka = marka_normalize(e_marka.get())
        yeni_model = ilk_harf_buyuk(e_model.get())
        yeni_ucret = e_ucret.get().strip()

        if not yeni_marka or not yeni_model or not yeni_ucret:
            messagebox.showerror("Hata", "Marka, model ve ücret boş bırakılamaz.")
            return

        try:
            yeni_ucret_f = float(yeni_ucret)
        except ValueError:
            messagebox.showerror("Hata", "Ücret sayısal olmalı.")
            return

        if yeni_ucret_f < 0:
            messagebox.showerror("Hata", "Ücret negatif olamaz.")
            return

        a["marka"] = yeni_marka
        a["model"] = yeni_model
        a["ucret"] = yeni_ucret_f

        verileri_sirala()
        veri_kaydet(veriler)
        tablo_guncelle()
        win.destroy()
        messagebox.showinfo("Başarılı", "Araç bilgileri güncellendi.")

    tk.Button(frm, text="💾 Güncelle", command=kaydet, bg="#26C6DA", fg="white",
              font=("Segoe UI", 10, "bold"), pady=6)\
        .grid(row=5, column=0, columnspan=2, pady=(16, 0), ipadx=10)

# Kiralama işlemleri 
def kiralama_yap():
    plaka = secili_arac_getir()
    if not plaka:
        messagebox.showwarning("Uyarı", "Lütfen listeden bir araç seçin.")
        return

    a = arac_bul(plaka)
    if not a:
        messagebox.showerror("Hata", "Seçili araç verilerde bulunamadı.")
        return

    if a.get("durum") == "Kirada":
        messagebox.showerror("Hata", "Araç zaten kirada.")
        return

    win = tk.Toplevel(pencere)
    win.title(f"Kiralama: {plaka}")
    win.configure(bg="#F3F7FF")
    win.resizable(False, False)

    frm = tk.Frame(win, bg="#F3F7FF")
    frm.pack(padx=18, pady=18)

    tk.Label(frm, text="Kiralama Bilgileri", bg="#F3F7FF", fg=RENK_BASLIK,
             font=("Segoe UI", 14, "bold"))\
        .grid(row=0, column=0, columnspan=2, pady=(0, 15))

    lbl_font = ("Segoe UI", 10, "bold")
    ent_font = ("Segoe UI", 10)
    entry_width = 26

    tk.Label(frm, text="Müşteri Adı Soyadı:", bg="#F3F7FF", font=lbl_font)\
        .grid(row=1, column=0, sticky="e", padx=(0, 10), pady=6)
    e_m = tk.Entry(frm, font=ent_font, width=entry_width, bd=1, relief="solid", bg="#FFFFFF")
    e_m.grid(row=1, column=1, sticky="w", pady=6)

    tk.Label(frm, text="Alış Tarihi (GG-AA-YYYY):", bg="#F3F7FF", font=lbl_font)\
        .grid(row=2, column=0, sticky="e", padx=(0, 10), pady=6)
    e_a = tk.Entry(frm, font=ent_font, width=entry_width, bd=1, relief="solid", bg="#FFFFFF")
    e_a.insert(0, datetime.datetime.now().strftime("%d-%m-%Y"))
    e_a.grid(row=2, column=1, sticky="w", pady=6)

    tk.Label(frm, text="İade Tarihi (GG-AA-YYYY):", bg="#F3F7FF", font=lbl_font)\
        .grid(row=3, column=0, sticky="e", padx=(0, 10), pady=6)
    e_i = tk.Entry(frm, font=ent_font, width=entry_width, bd=1, relief="solid", bg="#FFFFFF")
    e_i.grid(row=3, column=1, sticky="w", pady=6)

    def onayla():
        musteri = isim_duzelt(e_m.get())
        if not musteri:
            messagebox.showerror("Hata", "Müşteri adı boş olamaz.")
            return

        try:
            d1 = datetime.datetime.strptime(e_a.get().strip(), "%d-%m-%Y")
            d2 = datetime.datetime.strptime(e_i.get().strip(), "%d-%m-%Y")
        except:
            messagebox.showerror("Hata", "Format: GG-AA-YYYY olmalı!")
            return

        gun = (d2 - d1).days
        if gun <= 0:
            messagebox.showerror("Hata", "Tarih hatası! İade tarihi alış tarihinden sonra olmalı.")
            return

        try:
            tutar = gun * float(a.get("ucret", 0))
        except:
            messagebox.showerror("Hata", "Araç ücreti geçersiz.")
            return

        if messagebox.askyesno("Ödeme Onayı", f"Toplam: {tutar} ₺. Onaylıyor musunuz?"):
            a["durum"] = "Kirada"
            a["kiralayan"] = musteri
            a["baslangic_tarihi"] = e_a.get().strip()
            a["bitis_tarihi"] = e_i.get().strip()

            gecmis_kaydet({
                "tarih": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                "islem": f"Kiralama ({gun} Gün)",
                "plaka": plaka,
                "musteri": musteri
            })

            veri_kaydet(veriler)
            tablo_guncelle()
            win.destroy()
            messagebox.showinfo("Başarılı", "Kiralama işlemi başarılı.")

    tk.Button(frm, text="Kiralama Başlat", command=onayla, bg=RENK_BUTON_FILTRE, fg="white",
              font=("Segoe UI", 10, "bold"), pady=6)\
        .grid(row=4, column=0, columnspan=2, pady=(16, 0), ipadx=10)


def iade_al():
    plaka = secili_arac_getir()
    if not plaka:
        messagebox.showwarning("Uyarı", "Lütfen listeden bir araç seçin.")
        return

    a = arac_bul(plaka)
    if not a:
        messagebox.showerror("Hata", "Seçili araç verilerde bulunamadı.")
        return

    if a.get("durum") == "Müsait":
        messagebox.showinfo("Bilgi", "Bu araç zaten müsait durumda.")
        return

    a["durum"] = "Müsait"
    a["kiralayan"] = ""
    a["baslangic_tarihi"] = ""
    a["bitis_tarihi"] = ""

    gecmis_kaydet({
        "tarih": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "islem": "İade",
        "plaka": plaka,
        "musteri": "-"
    })

    veri_kaydet(veriler)
    tablo_guncelle()
    messagebox.showinfo("Başarılı", "İade işlemi başarılı.")


def sil():
    plaka = secili_arac_getir()
    if not plaka:
        messagebox.showwarning("Uyarı", "Lütfen listeden bir araç seçin.")
        return

    if messagebox.askyesno("Onay", "Silinsin mi?"):
        veriler[:] = [a for a in veriler if a.get("plaka") != plaka]

        verileri_sirala()
        veri_kaydet(veriler)
        tablo_guncelle()


def btn(t, c, b):#Aynı tip butonları tekrar tekrar yazmamak
    tk.Button(alt_panel, text=t, command=c, bg=b, fg="white", font=("bold"), padx=15, pady=5)\
        .pack(side="left", padx=10)


btn("🚗 Kiralama Başlat", kiralama_yap, RENK_BUTON_FILTRE)
btn("🔄 İade Al", iade_al, RENK_BUTON_EKLE)
btn("✏️ Bilgileri Getir", bilgileri_getir_penceresi_ac, "#FFB74D")
btn("💾 Güncelle", guncelle_penceresi_ac, "#26C6DA")
btn("🗑️ Sil", sil, RENK_BUTON_TEMIZLE)


def tablo_guncelle():
    verileri_sirala()
    tablo.delete(*tablo.get_children())
    kirada_sayisi = 0

    for a in veriler:
        durum = a.get("durum", "Müsait")
        tag = "musait" if durum == "Müsait" else "kirada" if durum == "Kirada" else ""

        tablo.insert("", "end",
                     values=(a.get("plaka"), a.get("marka"), a.get("model"), a.get("ucret"), durum),
                     tags=(tag,))

        if durum == "Kirada":
            kirada_sayisi += 1

    lbl_toplam.config(text=f"🚗 Toplam: {len(veriler)}")
    lbl_kirada.config(text=f"❌ Kirada: {kirada_sayisi}")
    lbl_musait.config(text=f"✅ Müsait: {len(veriler) - kirada_sayisi}")



tablo_guncelle()
pencere.mainloop()
