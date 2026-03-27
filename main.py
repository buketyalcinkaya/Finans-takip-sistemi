import tkinter as tk
from tkinter import messagebox
import json
import datetime
import os


class FinansAsistani:
    def __init__(self, pencere):
        self.pencere = pencere
        self.pencere.title("Finans Takipçisi")
        self.pencere.geometry("450x600")

        try:
            self.pencere.iconbitmap("wallet.ico")
        except:
            pass
        self.pencere.configure(bg="#f8f9fa")

        self.dosya_adi = "harcamalar.json"
        self.veriler = self.verileri_yukle()

        self.arayuz_hazirla()

    def arayuz_hazirla(self):
        # Başlık Bölümü
        tk.Label(self.pencere, text="💰 Finans Asistanım", font=("Segoe UI", 18, "bold"), bg="#f8f9fa",
                 fg="#2c3e50").pack(pady=20)

        # Giriş Alanları
        giris_cerceve = tk.Frame(self.pencere, bg="#f8f9fa")
        giris_cerceve.pack(pady=10)

        tk.Label(giris_cerceve, text="Harcama Tutarı (TL):", bg="#f8f9fa", font=("Segoe UI", 10)).grid(row=0, column=0,
                                                                                                       sticky="w",
                                                                                                       pady=5)
        self.miktar_entry = tk.Entry(giris_cerceve, font=("Segoe UI", 10), width=20)
        self.miktar_entry.grid(row=0, column=1, pady=5, padx=10)

        tk.Label(giris_cerceve, text="Harcama Notu:", bg="#f8f9fa", font=("Segoe UI", 10)).grid(row=1, column=0,
                                                                                                sticky="w", pady=5)
        self.not_entry = tk.Entry(giris_cerceve, font=("Segoe UI", 10), width=20)
        self.not_entry.grid(row=1, column=1, pady=5, padx=10)

        # Kategori Seçimi
        tk.Label(self.pencere, text="Kategori Seçiniz", bg="#f8f9fa", font=("Segoe UI", 10, "bold")).pack(pady=10)
        self.kat_var = tk.StringVar(value="Diğer")

        kat_cerceve = tk.Frame(self.pencere, bg="#f8f9fa")
        kat_cerceve.pack()

        kategoriler = [("Mutfak", "#ff7675"), ("Ulaşım", "#74b9ff"), ("Eğitim", "#55efc4"), ("Eğlence", "#a29bfe"),
                       ("Diğer", "#dfe6e9")]

        for metin, renk in kategoriler:
            tk.Radiobutton(kat_cerceve, text=metin, variable=self.kat_var, value=metin,
                           indicatoron=0, width=8, bg=renk, selectcolor="#636e72").pack(side="left", padx=2)

        # Kaydet Butonu
        tk.Button(self.pencere, text="KAYDET", command=self.kaydet, bg="#2ecc71", fg="white",
                  font=("Segoe UI", 11, "bold"), width=25, height=2, bd=0).pack(pady=30)

        # Özet Butonları
        tk.Button(self.pencere, text="📅 Yıllık Genel Bakış", command=self.yillik_pencere,
                  bg="#34495e", fg="white", bd=0, width=20).pack(pady=5)

        # Alt Toplam Bilgisi
        self.toplam_etiket = tk.Label(self.pencere, text="", font=("Segoe UI", 13, "bold"), bg="#f8f9fa", fg="#e74c3c")
        self.toplam_etiket.pack(side="bottom", pady=40)
        self.toplam_hesapla()

    def verileri_yukle(self):
        if os.path.exists(self.dosya_adi):
            with open(self.dosya_adi, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def kaydet(self):
        try:
            miktar = float(self.miktar_entry.get())
            not_metni = self.not_entry.get()
            kategori = self.kat_var.get()
            tarih = datetime.datetime.now().strftime("%Y-%m-%d")

            yeni_harcama = {"miktar": miktar, "kategori": kategori, "not": not_metni, "tarih": tarih}
            self.veriler.append(yeni_harcama)

            with open(self.dosya_adi, "w", encoding="utf-8") as f:
                json.dump(self.veriler, f, ensure_ascii=False, indent=4)

            messagebox.showinfo("Başarılı", "Harcama listeye eklendi!")
            self.miktar_entry.delete(0, tk.END)
            self.not_entry.delete(0, tk.END)
            self.toplam_hesapla()
        except ValueError:
            messagebox.showerror("Hata", "Lütfen geçerli bir sayı girin!")

    def toplam_hesapla(self):
        su_an = datetime.datetime.now().strftime("%Y-%m")
        aylik_toplam = sum(h['miktar'] for h in self.veriler if h['tarih'].startswith(su_an))
        self.toplam_etiket.config(text=f"Bu Ayki Toplam: {aylik_toplam:.2f} TL")

    def yillik_pencere(self):
        yeni = tk.Toplevel(self.pencere)
        yeni.title("Yıllık Takvim Özeti")
        yeni.geometry("350x450")

        tk.Label(yeni, text="2026 Yılı Harcama Özeti", font=("Segoe UI", 12, "bold")).pack(pady=10)

        metin_alani = tk.Text(yeni, width=35, height=18, font=("Courier", 10))
        metin_alani.pack(pady=10)

        aylar = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım",
                 "Aralık"]
        aylik_veriler = {f"{i + 1:02d}": 0 for i in range(12)}

        for h in self.veriler:
            yil, ay, gun = h['tarih'].split("-")
            if yil == "2026":
                aylik_veriler[ay] += h['miktar']

        for i, (ay_no, toplam) in enumerate(aylik_veriler.items()):
            metin_alani.insert(tk.END, f"{aylar[i]:<10}: {toplam:>10.2f} TL\n")

        metin_alani.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    uygulama = FinansAsistani(root)
    root.mainloop()