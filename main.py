# main.py

import threading
from calibrate import calibrate_eye_position
from gaze_tracking import gaze_tracking_loop
from voice_control import start_voice_recognition

def main():
    # 1️⃣ Kalibrasyon: iris merkez koordinatlarını al
    iris_center = calibrate_eye_position()  # returns (avg_x, avg_y)

    # 2️⃣ Sesli komut dinleyicisini arka planda başlat
    stop_listening = start_voice_recognition()

    # 3️⃣ Gaze takibi: kalibrasyon verisini geçir
    #    Bu fonksiyon bloklayıcıdır, programı burada takip eder
    gaze_tracking_loop(iris_center)

    # 4️⃣ Gerekirse dinlemeyi sonlandır
    stop_listening(wait_for_stop=False)

if __name__ == "__main__":
    main()

import speech_recognition as sr # type: ignore
import pyautogui
import subprocess

def voice_callback(recognizer, audio):
    try:
        cmd = recognizer.recognize_google(audio, language="tr-TR").lower()
        print(f"🗣️ Komut: {cmd}")
        if "sağ tık" in cmd:
            pyautogui.click(button='right')
        elif "sol tık" in cmd:
            pyautogui.click(button='left')
        elif "çift tık" in cmd:
            pyautogui.doubleClick()
        elif "enter" in cmd:
            pyautogui.press('enter')
        elif "chrome" in cmd:
            print("🌐 Chrome açılıyor...")
            subprocess.Popen("start chrome", shell=True)
        elif "klavyeyi aç" in cmd:
            print("⌨️ Ekran klavyesi açılıyor...")
            subprocess.Popen("osk", shell=True)
        elif "çık" in cmd or "kapat" in cmd:
            print("🔴 Uygulama sonlandırılıyor.")
            raise KeyboardInterrupt()
    except sr.UnknownValueError:
        print("❓ Anlaşılamadı.")
    except sr.RequestError:
        print("🌐 Google servisine ulaşılamadı.")

def start_voice_recognition():
    r = sr.Recognizer()
    mic = sr.Microphone()
    with mic as src:
        r.adjust_for_ambient_noise(src)
    # Arka planda dinleme başlat, stop_listening fonksiyonunu döner
    stop_listening = r.listen_in_background(mic, voice_callback)
    print("🎙️ Sesli komut dinleme başladı.")
    return stop_listening
