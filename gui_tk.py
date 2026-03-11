import threading
import webbrowser
import subprocess
import sys
import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Projenin kök dizinini çalışma dizini olarak ayarlıyoruz
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

from calibrate import calibrate_eye_position
from gaze_tracking import gaze_tracking_loop
from voice_control import start_voice_recognition

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Temassız Kontrol Merkezi")
        self.geometry("640x480")
        # Koyu gri arka plan daha modern
        self.configure(bg="#2E2E2E")

        # Durum etiketi
        self.status_var = tk.StringVar(value="📷 Kalibrasyon bekleniyor...")
        status_label = tk.Label(
            self,
            textvariable=self.status_var,
            font=("Segoe UI", 12, 'bold'),
            fg="#FFFFFF",
            bg="#2E2E2E"
        )
        status_label.pack(pady=10)

        # Resources klasörü
        default_dir = os.path.join(script_dir, "resources")
        if os.path.isdir(default_dir):
            self.res_dir = default_dir
        else:
            print(f"UYARI: resources klasörü bulunamadı, ikonlar script klasöründen yüklenecek.")
            self.res_dir = script_dir

        # İkon dosyaları
        icon_map = {
            "Acil Yardım": "acil.png",
            "Ayarlar": "ayarlar.png",
            "Google": "google.png",
            "Klavye": "klavye.png",
            "E-Posta": "mail.png",
            "YouTube": "youtube.png",
            "Yemek": "yemek.png",
            "Diğer": "diğer.png"
        }
        self.icons = {}
        for name, fname in icon_map.items():
            path = os.path.join(self.res_dir, fname)
            try:
                img = Image.open(path).convert("RGBA")
                # Beyaz arka planı şeffaf yap
                datas = img.getdata()
                newData = []
                for item in datas:
                    if item[0] > 240 and item[1] > 240 and item[2] > 240:
                        newData.append((255, 255, 255, 0))
                    else:
                        newData.append(item)
                img.putdata(newData)
                img = img.resize((50, 50), Image.LANCZOS)
                self.icons[name] = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Icon yüklenemedi: {fname}, {e}")
                self.icons[name] = None

        # Buton renk paleti (Material tarzı)
        color_map = {
            "Acil Yardım": "#E53935",  # Kırmızı
            "Ayarlar": "#1E88E5",     # Mavi
            "Google": "#FDD835",      # Sarı
            "Klavye": "#43A047",      # Yeşil
            "E-Posta": "#8E24AA",     # Mor
            "YouTube": "#D32F2F",     # Koyu kırmızı
            "Yemek": "#FB8C00",       # Turuncu
            "Diğer": "#546E7A"        # Gri-mavi
        }

        # Buton çerçevesi
        frame = tk.Frame(self, bg="#2E2E2E")
        frame.pack(expand=True, fill="both", padx=20, pady=10)

        # Buton tanımları (metin, komut)
        actions = [
            ("Acil Yardım", lambda: webbrowser.open("tel:112")),
            ("Ayarlar", lambda: subprocess.Popen("start ms-settings:", shell=True)),
            ("Google", lambda: webbrowser.open("https://www.google.com")),
            ("Klavye", lambda: subprocess.Popen("osk", shell=True)),
            ("E-Posta", lambda: webbrowser.open("mailto:")),
            ("YouTube", lambda: webbrowser.open("https://www.youtube.com")),
            ("Yemek", lambda: webbrowser.open("https://www.yemeksepeti.com")),
            ("Diğer", lambda: messagebox.showinfo("Diğer", "Ek seçenekler yakında..."))
        ]

        # Grid düzeni ve buton stili
        for idx, (text, cmd) in enumerate(actions):
            icon = self.icons.get(text)
            btn = tk.Button(
                frame,
                text=text,
                image=icon,
                compound=tk.TOP,
                command=cmd,
                font=("Segoe UI", 11, 'bold'),
                fg="#FFFFFF",
                bg=color_map.get(text, "#424242"),
                activebackground="#FFFFFF",
                activeforeground=color_map.get(text, "#424242"),
                bd=0,
                relief=tk.RAISED,
                padx=10,
                pady=8
            )
            btn.grid(row=idx//4, column=idx%4, padx=10, pady=10, sticky="nsew")

        # Grid yeniden boyutlandırma
        for r in range(2):
            frame.grid_rowconfigure(r, weight=1)
        for c in range(4):
            frame.grid_columnconfigure(c, weight=1)

        # Sistem başlatma thread
        threading.Thread(target=self.initialize_system, daemon=True).start()

    def initialize_system(self):
        try:
            calibrate_eye_position()
            self.status_var.set("✅ Kalibrasyon tamamlandı!")
        except Exception as e:
            messagebox.showerror("Kalibrasyon Hatası", str(e))
            sys.exit(1)

        threading.Thread(target=start_voice_recognition, daemon=True).start()
        threading.Thread(target=gaze_tracking_loop, daemon=True).start()

if __name__ == "__main__":
    app = App()
    app.mainloop()
