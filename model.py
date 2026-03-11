import cv2
import pyautogui

def pressEnter(frame, landmarks, frame_w, frame_h):
    left_pupil = [landmarks[145], landmarks[468]]
    right_pupil = [landmarks[374], landmarks[473]]
    if (left_pupil[0].y - left_pupil[1].y >= 0.014) and (right_pupil[0].y - right_pupil[1].y >= 0.014):
        print("enter")
        pyautogui.press('enter')

def back_n_forth(frame, landmarks, frame_w, frame_h):
    left_pupil = [landmarks[133], landmarks[468]]
    right_pupil = [landmarks[263], landmarks[473]]
    if (left_pupil[0].x - left_pupil[1].x <= 0.018) and (right_pupil[0].x - right_pupil[1].x <= 0.018):
        print("forth")
        pyautogui.hotkey('ctrl', 'right')
    elif (left_pupil[0].x - left_pupil[1].x >= 0.028) and (right_pupil[0].x - right_pupil[1].x >= 0.028):
        print("back")
        pyautogui.hotkey('ctrl', 'left')
    else:
        print("center")

def smile(frame, landmarks, frame_w, frame_h):
    left = landmarks[61]
    right = landmarks[291]
    if abs(left.x - right.x) > 0.10:
        print("You smiled")
        pyautogui.scroll(-10)

def eyebrows(frame, landmarks, frame_w, frame_h):
    left = [landmarks[66], landmarks[69]]
    right = [landmarks[296], landmarks[299]]
    if (abs(left[0].y - left[1].y) < 0.040) and (abs(right[0].y - right[1].y) < 0.040):
        print("both eyebrows raised")
        pyautogui.scroll(10)

def left_eyebrow(frame, landmarks, frame_w, frame_h):
    left = [landmarks[66], landmarks[69]]
    if abs(left[0].y - left[1].y) < 0.040:
        print("left eyebrow raised")

def right_eyebrow(frame, landmarks, frame_w, frame_h):
    right = [landmarks[296], landmarks[299]]
    if abs(right[0].y - right[1].y) < 0.040:
        print("right eyebrow raised")

def mouth_open(frame, landmarks, frame_w, frame_h, isOpen: bool):
    mouth = [landmarks[13], landmarks[14]]
    if isOpen:
        pyautogui.press('esc')
        return True
    else:
        if abs(mouth[0].y - mouth[1].y) > 0.1:
            print("mouth open")
            pyautogui.press('ctrl', presses=2)
            return True
    return False

def right_wink(frame, landmarks, frame_w, frame_h):
    eye = [landmarks[386], landmarks[374]]
    if abs(eye[0].y - eye[1].y) < 0.02:
        print("right wink")
        pyautogui.click()
