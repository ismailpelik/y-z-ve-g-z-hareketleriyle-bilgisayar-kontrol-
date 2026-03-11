import cv2
import mediapipe as mp # type: ignore
import pyautogui
import numpy as np
import time
import threading
import speech_recognition as sr # type: ignore
import sys

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = False

def voice_commands():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
    print("🎙️ Sesli komut sistemi aktif...")

    while True:
        try:
            with mic as source:
                audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio, language="tr-TR").lower()
            print(f"🗣️ Komut: {command}")

            if "sağ tık" in command:
                pyautogui.click(button='right')
            elif "sol tık" in command:
                pyautogui.click(button='left')
            elif "çift tık" in command:
                pyautogui.doubleClick()
            elif "enter" in command:
                pyautogui.press('enter')
            elif "çık" in command or "kapat" in command:
                print("🔴 Uygulama sonlandırılıyor (sesli komut).")
                sys.exit()

        except sr.WaitTimeoutError:
            continue
        except sr.UnknownValueError:
            print("❓ Anlaşılamadı.")
        except sr.RequestError:
            print("🌐 Google servisine ulaşılamadı.")

def gaze_tracking_loop():
    cam = cv2.VideoCapture(0)
    face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True, max_num_faces=1)

    screen_w, screen_h = pyautogui.size()
    last_blink_time = 0
    last_action_time = 0
    action_cooldown = 1.0
    base_nose = None

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)

        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0].landmark
            h, w, _ = frame.shape

            left_eye = (landmarks[159].y - landmarks[145].y)
            right_eye = (landmarks[386].y - landmarks[374].y)
            left_closed = left_eye < 0.02
            right_closed = right_eye < 0.02
            now = time.time()

            if right_closed and not left_closed and (now - last_action_time > action_cooldown):
                pyautogui.click(button='right')
                print("Sağ göz kırpma → Sağ tık")
                last_action_time = now
            elif left_closed and not right_closed and (now - last_action_time > action_cooldown):
                pyautogui.click(button='left')
                print("Sol göz kırpma → Sol tık")
                last_action_time = now
            elif left_closed and right_closed:
                if now - last_blink_time < 1.0:
                    pyautogui.doubleClick()
                    print("İki gözle çift kırpma → Çift tıklama")
                    last_blink_time = 0
                    last_action_time = now
                elif now - last_action_time > action_cooldown:
                    pyautogui.click()
                    print("İki gözle tek kırpma → Tek tıklama")
                    last_blink_time = now
                    last_action_time = now

            # Burunla fare kontrolü
            nose_tip = landmarks[1]
            nose_x = int(nose_tip.x * w)
            nose_y = int(nose_tip.y * h)

            if base_nose is None:
                base_nose = (nose_x, nose_y)

            dx = nose_x - base_nose[0]
            dy = nose_y - base_nose[1]

            # Hızlandırılmış kalibrasyon
            move_x = np.interp(dx, [-60, 60], [-50, 50])
            move_y = np.interp(dy, [-40, 40], [-35, 35])
            curr_mouse = pyautogui.position()
            pyautogui.moveTo(curr_mouse.x + move_x, curr_mouse.y + move_y)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("🔴 Klavyeden çıkış yapıldı.")
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Sesli komutlar için ayrı thread
    threading.Thread(target=voice_commands, daemon=True).start()
    # Göz ve kafa takip sistemi
    gaze_tracking_loop()
