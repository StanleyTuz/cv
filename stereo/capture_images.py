import cv2
import glob
import numpy as np
import time
import matplotlib.pyplot as plt
import os

FOLDER = "checkerboard"
os.makedirs(FOLDER, exist_ok=True)

# Open cameras
cam_l = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam_r = cv2.VideoCapture(1, cv2.CAP_DSHOW)

if not cam_l.isOpened() or not cam_r.isOpened():
    raise RuntimeError("Couldn't open webcams.")

# Set matching resolutions and FPS in order to reduce drift between cameras
for cam in (cam_l, cam_r):
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cam.set(cv2.CAP_PROP_FPS, 30)

# Warm up the webcams
for _ in range(20):
    cam_l.read()
    cam_r.read()


idx = 0

print("Press SPACE to save a stereo pair")
print("Press q to quit")

while True:
    ts = time.time()

    ret_r, frame_r = cam_r.read()
    ret_l, frame_l = cam_l.read()

    if not ret_r or not ret_l:
        print("capture failed")
        continue

    # Show both feeds
    cv2.imshow("Right", frame_r)
    cv2.imshow("Left", frame_l)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

    if key == ord(" "):
        # Save frames
        cv2.imwrite(f"{FOLDER}/right_{idx}.jpg", frame_r)
        cv2.imwrite(f"{FOLDER}/left_{idx}.jpg", frame_l)

        print(f"Saved pair {idx}")

        idx += 1

cam_l.release()
cam_r.release()

cv2.destroyAllWindows()