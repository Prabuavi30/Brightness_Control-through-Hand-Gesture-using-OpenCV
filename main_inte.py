#Load the libraries
pip install opencv-python mediapipe screen-brightness-control pillow

# Main class integerated GUI with brightness control code
import cv2
from mediapipe.python.solutions import hands as mp_hands
from mediapipe.python.solutions import drawing_utils as mp_drawing
import numpy as np
from math import hypot
import screen_brightness_control as sbc
from tkinter import *
from PIL import Image, ImageTk

class BrightnessControllerApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Hand Gesture Brightness Control")
        self.window.geometry("800x600")

        self.video_running = False
        self.label = Label(self.window)
        self.label.pack()

        self.start_button = Button(self.window, text="Start Camera", command=self.start_camera, bg="green", fg="white")
        self.start_button.pack(side=LEFT, padx=20, pady=20)

        self.stop_button = Button(self.window, text="Stop Camera", command=self.stop_camera, bg="red", fg="white")
        self.stop_button.pack(side=RIGHT, padx=20, pady=20)

        self.mpHands = mp_hands
        self.hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
        self.mpDraw = mp_drawing

    def start_camera(self):
        self.cap = cv2.VideoCapture(0)
        self.video_running = True
        self.update_frame()

    def stop_camera(self):
        self.video_running = False
        self.cap.release()
        self.label.config(image='')

    def update_frame(self):
        if self.video_running:
            success, frame = self.cap.read()
            if not success:
                return
            
            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb)

            if results.multi_hand_landmarks:
                for handLms in results.multi_hand_landmarks:
                    lmList = []
                    for id, lm in enumerate(handLms.landmark):
                        h, w, c = frame.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        lmList.append((cx, cy))

                    if len(lmList) >= 9:
                        x1, y1 = lmList[4]   # Thumb tip
                        x2, y2 = lmList[8]   # Index finger tip
                        cv2.circle(frame, (x1, y1), 10, (255, 0, 255), -1)
                        cv2.circle(frame, (x2, y2), 10, (255, 0, 255), -1)
                        cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

                        length = hypot(x2 - x1, y2 - y1)
                        brightness = np.interp(length, [15, 220], [0, 100])
                        try:
                            sbc.set_brightness(int(brightness))
                        except:
                            pass

                        cv2.putText(frame, f'Brightness: {int(brightness)}%', (10, 50),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

                    self.mpDraw.draw_landmarks(frame, handLms, self.mpHands.HAND_CONNECTIONS)

            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            imgtk = ImageTk.PhotoImage(image=img)
            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)
            self.window.after(10, self.update_frame)

root = Tk()
app = BrightnessControllerApp(root)
root.mainloop()
