#Load Library Dependencies
pip install opencv-python mediapipe screen_brightness_control numpy
pip install --upgrade jax==0.4.30

#Import the libraries
import cv2
import numpy as np
from math import hypot
import screen_brightness_control as sbc
from mediapipe.python.solutions import hands as mp_hands
from mediapipe.python.solutions import drawing_utils as mp_drawing

#cpature the video from camera
hands = mp_hands.Hands()
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

# Marking Landmarks on Hand 
if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            lm_list = []
            h, w, _ = frame.shape
            for id, lm in enumerate(hand_landmarks.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append((cx, cy))

            if len(lm_list) >= 9:
                x1, y1 = lm_list[4]  # Thumb tip
                x2, y2 = lm_list[8]  # Index tip

                cv2.circle(frame, (x1, y1), 10, (255, 0, 0), -1)
                cv2.circle(frame, (x2, y2), 10, (255, 0, 0), -1)
                cv2.line(frame, (x1, y1), (x2, y2), (255, 255, 0), 2)

                length = hypot(x2 - x1, y2 - y1)
                brightness = int(np.interp(length, [30, 200], [0, 100]))
                sbc.set_brightness(brightness)
                cv2.putText(frame, f'Brightness: {brightness}%', (10, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Brightness Control", frame)

# Exit form running shell
if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
