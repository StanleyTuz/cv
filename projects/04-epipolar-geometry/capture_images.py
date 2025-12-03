import argparse
import cv2
import pathlib
import time
import os

def capture_images(dst_path: pathlib.Path):
    
    # Create the destination location
    os.makedirs(dst_path, exist_ok=False)
    print(f"Writing images to {str(dst_path.resolve())}.")

    # Open cameras
    cam_l = cv2.VideoCapture(1, cv2.CAP_DSHOW)  # Left camera
    cam_r = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Right camera

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
        # Capture frame
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
            # If user presses SPACE, save frames
            dst_l = str(dst_path / f"left_{idx}.jpg")
            dst_r = str(dst_path / f"right_{idx}.jpg")
            cv2.imwrite(dst_l, frame_l)
            cv2.imwrite(dst_r, frame_r)

            print(f"Saved pair {idx}")

            idx += 1

    cam_l.release()
    cam_r.release()

    cv2.destroyAllWindows()


def cleanup_empty_dst_path(dst_path: pathlib.Path):
    """If no images were recorded, delete the destination folder
    to keep things clean.
    """
    if dst_path.is_dir() and not any(dst_path.iterdir()):
        dst_path.rmdir()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--dirname',
        type=pathlib.Path,
        help='Name of folder to store images'
    )
    args = parser.parse_args()

    dirname = args.dirname or str(int(time.time()))
    dst_path = pathlib.Path('data') / dirname
    
    # Start capture loop
    try:
        capture_images(
            dst_path=dst_path,
        )
    finally:
        # If no images were captured, clean up the folder
        cleanup_empty_dst_path(dst_path)

