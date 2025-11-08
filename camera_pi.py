#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# camera_pi.py — Updated for Raspberry Pi OS Bookworm
#
import time
import threading
import socket
import cv2
from picamera2 import Picamera2

class Camera(object):
    thread = None          # background thread that reads frames
    frame = None           # current frame as JPEG bytes
    last_access = 0        # time of last client access
    picam2 = None          # global camera instance

    def initialize(self):
        if Camera.thread is None:
            # Start background thread
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()

            # Wait until a frame is available
            while self.frame is None:
                time.sleep(0.1)

    def get_frame(self):
        Camera.last_access = time.time()
        self.initialize()
        return self.frame

    @classmethod
    def _thread(cls):
        # Initialize camera
        cls.picam2 = Picamera2()

        # Create a video configuration
        config = cls.picam2.create_video_configuration(main={"size": (640, 480)})
        cls.picam2.configure(config)
        cls.picam2.start()

        print("Camera streaming started...")

        while True:
            # Capture frame as a NumPy array
            frame = cls.picam2.capture_array()

            # Encode as JPEG
            ret, jpeg = cv2.imencode('.jpg', frame)
            if not ret:
                continue

            cls.frame = jpeg.tobytes()

            # Stop thread if no client access for >10s
            if time.time() - cls.last_access > 10:
                print("No client access in 10s — stopping camera thread.")
                break

        cls.picam2.stop()
        cls.thread = None
        print("Camera thread stopped.")

camera = Camera()
server_address = ('127.0.0.2', 8001)
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def get_f():
    image = camera.get_frame()
    print(f"Sending image ({len(image)} bytes)")
    try:
        client.sendto(image, server_address)
    except Exception as e:
        print("Error sending frame:", e)

def read_send_image():
    while True:
        get_f()
        time.sleep(0.05)

if __name__ == '__main__':
    read_send_image()
