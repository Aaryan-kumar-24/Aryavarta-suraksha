import cv2
import pickle
import numpy as np
import time
import os
from datetime import datetime
import pytz

BOX_FILE = "service/box_wait.pkl"
CONFIG_FILE = "service/wait_config.pkl"

alerts = []
occupied_start = {}

CONFIG_MODE = False
RESET_TRIGGER = False   # 🔥 NEW


def load_config():
    if os.path.exists(BOX_FILE):
        with open(BOX_FILE, "rb") as f:
            boxes = pickle.load(f)
    else:
        boxes = []

    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "rb") as f:
            threshold, wait_time, bw, bh = pickle.load(f)
    else:
        threshold, wait_time, bw, bh = 1500, 2, 0.2, 0.2

    return boxes, threshold, wait_time, bw, bh


def save_config(boxes, threshold, wait_time, bw, bh):
    with open(BOX_FILE, "wb") as f:
        pickle.dump(boxes, f)

    with open(CONFIG_FILE, "wb") as f:
        pickle.dump((threshold, wait_time, bw, bh), f)


def generate_frames():
    global RESET_TRIGGER

    cap = cv2.VideoCapture(0)

    while True:

        # 🔁 reopen camera if needed
        if not cap.isOpened():
            cap.release()
            time.sleep(1)
            cap = cv2.VideoCapture(0)
            continue

        ret, img = cap.read()
        img = cv2.flip(img, 1) 
        if not ret:
            continue

        # 🔥 RESET LOGIC
        if RESET_TRIGGER:
            occupied_start.clear()
            RESET_TRIGGER = False

        boxes, threshold, wait_time, bw, bh = load_config()

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 1)
        thresh = cv2.adaptiveThreshold(
            blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV, 25, 16
        )
        med = cv2.medianBlur(thresh, 5)
        dil = cv2.dilate(med, np.ones((3, 3), np.uint8), 1)

        h, w = img.shape[:2]
        alert_flag = False

        if not CONFIG_MODE:
            for i, pos in enumerate(boxes):
                x = int(pos[0] * w)
                y = int(pos[1] * h)
                box_w = int(bw * w)
                box_h = int(bh * h)

                crop = dil[y:y+box_h, x:x+box_w]
                count = cv2.countNonZero(crop)

                if count > threshold:
                    if i not in occupied_start:
                        occupied_start[i] = time.time()

                    if time.time() - occupied_start[i] > wait_time:
                        alert_flag = True

                        ist = pytz.timezone("Asia/Kolkata")
                        alerts.append(datetime.now(ist).strftime("%H:%M:%S"))
                        del alerts[:-10]

                        cv2.rectangle(img, (x, y), (x+box_w, y+box_h), (0, 0, 255), 3)
                    else:
                        cv2.rectangle(img, (x, y), (x+box_w, y+box_h), (0, 165, 255), 2)
                else:
                    occupied_start.pop(i, None)
                    cv2.rectangle(img, (x, y), (x+box_w, y+box_h), (0, 255, 0), 2)

        # ===== CENTER ALERT TEXT =====
        if alert_flag:
            text = "⏳ WAIT ALERT"
            font = cv2.FONT_HERSHEY_SIMPLEX
            scale = 1.3
            thickness = 3

            (tw, th), _ = cv2.getTextSize(text, font, scale, thickness)
            x_pos = (w - tw) // 2
            y_pos = h - 30

            overlay = img.copy()
            cv2.rectangle(
                overlay,
                (x_pos - 20, y_pos - th - 15),
                (x_pos + tw + 20, y_pos + 10),
                (0, 0, 0),
                -1
            )
            img = cv2.addWeighted(overlay, 0.6, img, 0.4, 0)

            cv2.putText(img, text, (x_pos, y_pos),
                        font, scale, (0, 255, 255), thickness, cv2.LINE_AA)

        _, buffer = cv2.imencode(".jpg", img)
        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" +
               buffer.tobytes() + b"\r\n")
