import cv2
import pickle
import numpy as np
from datetime import datetime
import pytz
import time
import os

FILE_PATH = "service/box2"
THRESHOLD_FILE = "service/threshold.pkl"

alerts = []
cooldown = 2
last_alert_time = 0

# CONFIG MODE FLAG
CONFIG_MODE = False


def load_config():
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "rb") as f:
            boxes = pickle.load(f)
    else:
        boxes = []

    if os.path.exists(THRESHOLD_FILE):
        with open(THRESHOLD_FILE, "rb") as f:
            threshold, bw, bh = pickle.load(f)
    else:
        threshold, bw, bh = 50, 0.2, 0.2

    return boxes, threshold, bw, bh


def save_config(boxes, threshold, bw, bh):
    with open(FILE_PATH, "wb") as f:
        pickle.dump(boxes, f)

    with open(THRESHOLD_FILE, "wb") as f:
        pickle.dump((threshold, bw, bh), f)


def generate_frames():
    global last_alert_time

    cap = cv2.VideoCapture(0)

    while True:
        ret, img = cap.read()
        if not ret:
            continue

        boxes, threshold, bw, bh = load_config()

        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
        imgThresh = cv2.adaptiveThreshold(
            imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV, 25, 16
        )

        alert_flag = False
        h, w = img.shape[:2]

        # Draw rectangles only in normal mode
        if not CONFIG_MODE:
            for pos in boxes:
                x = int(pos[0] * w)
                y = int(pos[1] * h)
                box_w = int(bw * w)
                box_h = int(bh * h)

                crop = imgThresh[y:y+box_h, x:x+box_w]
                white = cv2.countNonZero(crop)

                if white > threshold:
                    alert_flag = True
                    cv2.rectangle(img, (x, y), (x+box_w, y+box_h), (0, 0, 255), 4)
                else:
                    cv2.rectangle(img, (x, y), (x+box_w, y+box_h), (0, 255, 0), 2)

        # Save alert time (IST)
        if alert_flag and time.time() - last_alert_time > cooldown:
            ist = pytz.timezone("Asia/Kolkata")
            alerts.append(datetime.now(ist).strftime("%H:%M:%S"))
            del alerts[:-10]
            last_alert_time = time.time()

        # ===== CENTER-BOTTOM ALERT MESSAGE =====
        if alert_flag:

            text = "⚠ ALERT DETECTED"
            font = cv2.FONT_HERSHEY_SIMPLEX
            scale = 1.4
            thickness = 3

            # Get text size for centering
            (text_w, text_h), _ = cv2.getTextSize(text, font, scale, thickness)

            # Position → center horizontally, near bottom
            x_pos = (w - text_w) // 2
            y_pos = h - 30

            # Semi-transparent black bar behind text
            overlay = img.copy()
            cv2.rectangle(
                overlay,
                (x_pos - 20, y_pos - text_h - 15),
                (x_pos + text_w + 20, y_pos + 10),
                (0, 0, 0),
                -1
            )

            # Blend overlay for transparency
            alpha = 0.6
            img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

            # Draw bright orange-red alert text
            cv2.putText(
                img,
                text,
                (x_pos, y_pos),
                font,
                scale,
                (0, 140, 255),  # 🔥 orange-red warning color
                thickness,
                cv2.LINE_AA
            )

        # Encode frame for streaming
        _, buffer = cv2.imencode(".jpg", img)
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" +
            buffer.tobytes() +
            b"\r\n"
        )
