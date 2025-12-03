"""Script to quickly capture images """

import argparse
import cv2
import pathlib
import time
import os

def capture_images(dst_dir: pathlib.Path):
    
    # Create the destination location
    os.makedirs(dst_dir, exist_ok=False)
    print(f"Writing images to {str(dst_dir.resolve())}.")

    # Open cameras
    cam = cv2.VideoCapture(1, cv2.CAP_DSHOW)

    if not cam.isOpened():
        raise RuntimeError("Couldn't open webcam.")

    # Set resolution and FPS
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cam.set(cv2.CAP_PROP_FPS, 30)

    # Warm up the webcam
    for _ in range(20):
        cam.read()


    idx = 0

    print("Press SPACE to save an image")
    print("Press q to quit")

    try:
        while True:
            # Capture frame
            ret, frame = cam.read()
            
            if not ret:
                print("capture failed")
                continue

            # Show feed
            cv2.imshow("Webcam", frame)

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

            if key == ord(" "):
                # If user presses SPACE, save frames
                dst = str(dst_dir / f"img_{idx:02}.jpg")
                cv2.imwrite(dst, frame)

                print(f"Saved image {idx}")

                idx += 1
    finally:
        cam.release()
        cv2.destroyAllWindows()


def cleanup_empty_dst_path(dst_dir: pathlib.Path):
    """If no images were recorded, delete the destination folder
    to keep things clean.
    """
    if dst_dir.is_dir() and not any(dst_dir.iterdir()):
        dst_dir.rmdir()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--dirname',
        type=pathlib.Path,
        help='Name of folder to store images'
    )
    args = parser.parse_args()

    dirname = args.dirname or str(int(time.time()))
    dst_dir = pathlib.Path('data') / dirname
    
    # Start capture loop
    try:
        capture_images(
            dst_dir=dst_dir,
        )
    finally:
        # If no images were captured, clean up the folder
        cleanup_empty_dst_path(dst_dir)

