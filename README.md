# Hand Gesture Controlled Screen Brightness Adjuster

This project allows you to **control your screen brightness** using **hand gestures** captured by your webcam. 
It uses **MediaPipe** for hand tracking, **OpenCV** for camera feed, **Tkinter** for a simple GUI interface, and **Screen Brightness Control** for adjusting the display brightness in real-time.

---

## Features

- Detects hand gestures using webcam
- Measures distance between thumb and index finger
- Dynamically adjusts screen brightness based on gesture
- Simple GUI built using Tkinter
- MediaPipe-based hand landmark detection

---

## 📦 Requirements

Make sure you have the following installed:

**How It Works**
The application captures webcam frames.

MediaPipe identifies hand landmarks.

It calculates the Euclidean distance between the thumb and index finger.

Based on this distance, the screen brightness is increased or decreased proportionally.

**How to Run**

python main_inti.py
Once running:

->Show your hand to the webcam.

->Pinch your thumb and index finger to adjust the brightness.

->Use the GUI buttons to start/stop the webcam.
