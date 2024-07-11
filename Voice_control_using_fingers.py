import cv2
import mediapipe as mp
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import time

# إعدادات mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils

# إعدادات pycaw
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volume_range = volume.GetVolumeRange()
min_vol = volume_range[0]
max_vol = volume_range[1]

# تشغيل كاميرا الويب
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 15)

def draw_volume_bar(image, vol, min_vol, max_vol):
    bar_height = 300
    bar_x_start = 50
    bar_y_start = 50
    bar_width = 30
    vol_perc = int((vol - min_vol) / (max_vol - min_vol) * 100)
    
    # خلفية الشريط
    cv2.rectangle(image, (bar_x_start, bar_y_start), 
                  (bar_x_start + bar_width, bar_y_start + bar_height), 
                  (255, 255, 255), 3)
    
 
    # الشريط المتقدم
    filled_height = int((vol_perc / 100) * bar_height)
    cv2.rectangle(image, (bar_x_start, bar_y_start + (bar_height - filled_height)), 
                  (bar_x_start + bar_width, bar_y_start + bar_height), 
                  (0, 255, 0), cv2.FILLED)
    
    # عرض النسبة المئوية
    cv2.putText(image, f'{vol_perc}%', (bar_x_start + 40, bar_y_start + bar_height - filled_height + 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

def draw_instructions(image):
    instructions = [
        "Use your thumb and index finger to control the volume.",
        "Bring them closer to reduce the volume.",
        "Separate them to increase the volume.",
        "Press 'q' to exit."
    ]
    
    y0, dy = 20, 30
    for i, line in enumerate(instructions):
        y = y0 + i * dy
        cv2.putText(image, line, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2, cv2.LINE_AA)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = hands.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    draw_instructions(image)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            landmarks = hand_landmarks.landmark
            thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            h, w, _ = image.shape
            thumb_tip_coords = (int(thumb_tip.x * w), int(thumb_tip.y * h))
            index_tip_coords = (int(index_tip.x * w), int(index_tip.y * h))

            cv2.circle(image, thumb_tip_coords, 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(image, index_tip_coords, 10, (0, 255, 0), cv2.FILLED)
            cv2.line(image, thumb_tip_coords, index_tip_coords, (255, 255, 255), 2)

            distance = np.linalg.norm(np.array(thumb_tip_coords) - np.array(index_tip_coords))
            vol = np.interp(distance, [50, 300], [min_vol, max_vol])
            volume.SetMasterVolumeLevel(vol, None)

            draw_volume_bar(image, vol, min_vol, max_vol)

    cv2.imshow('Gesture Volume Control', image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
