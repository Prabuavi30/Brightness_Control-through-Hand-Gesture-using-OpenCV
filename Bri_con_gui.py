#Import required libraries to create a gui
import cv2
from tkinter import *
from PIL import Image, ImageTk

#Execution
class App:
    def __init__(self, window):
        self.window = window
        self.window.title("Webcam Feed with Exit Button")
        self.window.geometry("700x500")
        self.video_running = False

        self.label = Label(self.window)
        self.label.pack()

        self.start_button = Button(self.window, text="Start Camera", command=self.start_camera)
        self.start_button.pack(side=LEFT, padx=10)

        self.stop_button = Button(self.window, text="Stop Camera", command=self.stop_camera)
        self.stop_button.pack(side=RIGHT, padx=10)

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
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.label.imgtk = imgtk
                self.label.configure(image=imgtk)
            self.window.after(10, self.update_frame)

root = Tk()
app = App(root)
root.mainloop()
