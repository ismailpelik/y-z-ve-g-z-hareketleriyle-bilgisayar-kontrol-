
#voice

import speech_recognition as sr  # type: ignore
import pyautogui              # type: ignore
import subprocess
import os

def run_app(command):
    # — Uygulama açma komutları —
    if command in ["google chrome aç", "chrome aç", "chrome başlat"]:
        subprocess.Popen("start chrome", shell=True)
    elif command in ["klavye aç", "ekran klavye aç"]:
        subprocess.Popen("osk", shell=True)
    elif command in ["hesap makinesi aç", "calculator aç"]:
        subprocess.Popen("calc", shell=True)
    elif command == "not defteri aç":
        subprocess.Popen("notepad", shell=True)
    elif command == "paint aç":
        subprocess.Popen("mspaint", shell=True)
    elif command == "wordpad aç":
        subprocess.Popen("write", shell=True)
    elif command == "excel aç":
        subprocess.Popen("start excel", shell=True)
    elif command in ["tarayıcı aç", "browser aç"]:
        subprocess.Popen("start \"\" \"%ProgramFiles%\\Internet Explorer\\iexplore.exe\"", shell=True)
    elif command in ["outlook aç", "mail aç", "e posta aç"]:
        subprocess.Popen("start \"\" \"%ProgramFiles%\\Microsoft Office\\root\\Office16\\OUTLOOK.EXE\"", shell=True)
    elif command in ["ayarlar aç", "ayarları aç"]:
        subprocess.Popen("start ms-settings:", shell=True)
    elif command in ["dosyaları aç", "dosyalar aç", "file explorer aç"]:
        subprocess.Popen("explorer", shell=True)
    elif command in ["masaüstü aç", "masaüstünü göster", "show desktop"]:
        pyautogui.hotkey('win', 'd')

    # — Uygulama kapatma komutları —
    elif command in ["chrome kapat", "google chrome kapat"]:
        subprocess.Popen("taskkill /im chrome.exe /f", shell=True)
    elif command in ["hesap makinesi kapat", "calculator kapat"]:
        subprocess.Popen("taskkill /im Calculator.exe /f", shell=True)
    elif command == "not defteri kapat":
        subprocess.Popen("taskkill /im notepad.exe /f", shell=True)
    elif command == "paint kapat":
        subprocess.Popen("taskkill /im mspaint.exe /f", shell=True)
    elif command == "wordpad kapat":
        subprocess.Popen("taskkill /im wordpad.exe /f", shell=True)
    elif command == "excel kapat":
        subprocess.Popen("taskkill /im excel.exe /f", shell=True)
    elif command in ["tarayıcı kapat", "browser kapat"]:
        subprocess.Popen("taskkill /im iexplore.exe /f", shell=True)
    elif command in ["outlook kapat", "mail kapat", "e posta kapat"]:
        subprocess.Popen("taskkill /im outlook.exe /f", shell=True)

    else:
        return False
    return True

def voice_callback(recognizer, audio):
    try:
        cmd = recognizer.recognize_google(audio, language="tr-TR").lower()
        print(f"🗣️ Komut: {cmd}")

        # Fare tıklamaları
        if "sağ tık" in cmd:
            pyautogui.click(button='right'); return
        if "sol tık" in cmd:
            pyautogui.click(button='left'); return
        if "çift tık" in cmd:
            pyautogui.doubleClick(); return

        # Uygulama açma/kapama
        if run_app(cmd):
            return

        # Uygulamayı tamamen durdurma
        if "programı durdur" in cmd or "uygulamayı durdur" in cmd:
            print("🛑 Program kapatılıyor…")
            stop_listening(wait_for_stop=False)
            os._exit(0)

        print("❓ Tanınmayan komut.")

    except sr.UnknownValueError:
        print("❓ Anlaşılamadı.")
    except sr.RequestError:
        print("🌐 Google servisine ulaşılamadı.")

def start_voice_recognition():
    r = sr.Recognizer()
    mic = sr.Microphone()
    with mic as src:
        r.adjust_for_ambient_noise(src)
    global stop_listening
    stop_listening = r.listen_in_background(mic, voice_callback)
    print("🎙️ Sesli komut dinleme başladı.")
    return stop_listening

if __name__ == "__main__":
    try:
        stop = start_voice_recognition()
        import time
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("🛑 Sesli komut uygulaması kapatıldı.")
