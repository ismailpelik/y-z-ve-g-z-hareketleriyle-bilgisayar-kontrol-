import cv2
import numpy as np
import time

def calibrate_eye_position(cam, face_mesh, iris_landmarks):
    """
    Basit kalibrasyon fonksiyonu.
    Kullanıcıdan kameraya bakması istenir,
    göz iris koordinatlarının ortalaması hesaplanır.
    """

    print("Kalibrasyon başlıyor. Lütfen kameraya düz bakın...")
    time.sleep(2)

    positions = []

    for _ in range(30):  # 30 kare topla
        ret, frame = cam.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = face_mesh.process(rgb_frame)

        if result.multi_face_landmarks:
            landmarks = result.multi_face_landmarks[0].landmark
            avg_x = np.mean([landmarks[i].x for i in iris_landmarks])
            avg_y = np.mean([landmarks[i].y for i in iris_landmarks])
            positions.append((avg_x, avg_y))

    if not positions:
        print("Kalibrasyon başarısız oldu. Yüz tespit edilemedi.")
        return None

    avg_pos = np.mean(positions, axis=0)
    print(f"Kalibrasyon tamamlandı. Ortalama göz pozisyonu: {avg_pos}")
    return avg_pos
