#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  camera_pi.py
#
#  Debian-compatible version using OpenCV instead of picamera

import time
import socket
import cv2

class Camera:
    def __init__(self, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index)
        if not self.cap.isOpened():
            raise IOError("Cannot open camera")
        
        # Optionally, set resolution
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            raise IOError("Failed to capture frame")
        # Encode to JPEG for transmission
        _, buffer = cv2.imencode('.jpg', frame)
        return buffer.tobytes()

    def release(self):
        self.cap.release()

# UDP setup
server_address = ('127.0.0.2', 8001)
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

camera = Camera()

def get_f():
    global camera, client
    try:
        image = camera.get_frame()
        print(f"Captured frame size: {len(image)} bytes")
        client.sendto(image, server_address)
    except Exception as e:
        print(f"Error: {e}")

def read_send_image():
    while True:
        get_f()
        time.sleep(0.05)  # ~20 FPS

if __name__ == '__main__':
    try:
        read_send_image()
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        camera.release()
        client.close()