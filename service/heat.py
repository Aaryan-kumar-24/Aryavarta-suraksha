import cv2
import numpy as np
import time
from datetime import datetime
import pytz
import os

# ===== TIMEZONE =====
LOCAL_TZ = pytz.timezone("Asia/Kolkata")

# ===== SETTINGS =====
DECAY = 0.94
GAIN = 35
HIGH_THRESHOLD = 0.30   # alert start
LOW_THRESHOLD = 0.10    # alert stop (ONLY visual)

# ===== ALERT FILE =====
ALERT_FILE = "service/heat_alerts.txt"


def load_alerts():
    if not os.path.exists(ALERT_FILE):
        return []
    with open(ALERT_FILE, "r") as f:
        return [line.strip() for line in f.readlines()][-10:]


alerts = load_alerts()


def save_alerts():
    global alerts
    alerts = alerts[-10:]
    with open(ALERT_FILE, "w") as f:
        for a in alerts:
            f.write(a + "\n")


def update_settings(decay=None, gain=None, high=None, low=None):
    global DECAY, GAIN, HIGH_THRESHOLD, LOW_THRESHOLD

    if decay:
        DECAY = float(decay)
    if gain:
        GAIN = float(gain)
    if high:
        HIGH_THRESHOLD = float(high)
    if low:
        LOW_THRESHOLD = float(low)


def generate_frames():
    global alerts

    cap = cv2.VideoCapture(0)

    ret, prev_frame = cap.read()
    if not ret:
        return

    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    heatmap = np.zeros_like(prev_gray, dtype=np.float32)

    activity_score = 0.0
    alert_active = False
    pulse_phase = 0
    prev_time = time.time()
    last_alert_time = None

    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
        frame = cv2.flip(frame, 1) 
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # FPS
        current_time = time.time()
        fps = 1 / (current_time - prev_time)
        prev_time = current_time

        # Motion
        diff = cv2.absdiff(prev_gray, gray)
        _, motion_mask = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

        motion_strength = np.mean(diff)
        motion_area_ratio = np.sum(motion_mask > 0) / motion_mask.size
        activity = motion_strength * motion_area_ratio
        activity_score = 0.9 * activity_score + 0.1 * activity

        # Heatmap
        heatmap[:] = heatmap * DECAY + (motion_mask / 255.0) * GAIN
        heatmap[:] = np.clip(heatmap, 0, 255)

        heat_display = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

        red = np.zeros_like(frame)
        red[:, :, 2] = heat_display
        blended = cv2.addWeighted(frame, 1.0, red, 0.6, 0)

        h, w = blended.shape[:2]

        # ===== ALERT STATE MACHINE =====
        if activity_score > HIGH_THRESHOLD:
            alert_active = True
        elif activity_score < LOW_THRESHOLD:
            alert_active = False

        status = "ACTIVE" if alert_active else "CALM"
        color = (0, 0, 255) if alert_active else (0, 255, 0)

        # Dashboard
        panel = blended.copy()
        cv2.rectangle(panel, (10, 10), (430, 190), (0, 0, 0), -1)
        blended = cv2.addWeighted(panel, 0.45, blended, 0.55, 0)

        y = 55
        cv2.putText(blended, f"Activity: {activity_score:.2f}", (25, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 3)

        y += 40
        cv2.putText(blended, f"Motion Strength: {motion_strength:.2f}", (25, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (220, 220, 220), 3)

        y += 35
        cv2.putText(blended, f"Motion Area: {motion_area_ratio*100:.1f}%", (25, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (220, 220, 220), 3)

        y += 35
        cv2.putText(blended, f"Heat Level: {np.mean(heatmap):.2f}", (25, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (220, 220, 220), 3)

        cv2.putText(blended, f"FPS: {fps:.1f}", (w - 220, 55),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 3)

        cv2.putText(blended, f"Status: {status}", (w - 260, 110),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 3)

        # ===== VISUAL ALERT =====
        if alert_active:
            pulse_phase += 0.2
            glow = int((np.sin(pulse_phase) + 1) * 40)

            box_w, box_h = 520, 110
            x1 = (w - box_w) // 2
            y1 = h - box_h - 30

            cv2.rectangle(blended, (x1, y1), (x1 + box_w, y1 + box_h),
                          (0, 0, 180 + glow), -1)
            cv2.rectangle(blended, (x1, y1), (x1 + box_w, y1 + box_h),
                          (255, 255, 255), 4)

            cv2.putText(blended, "DANGER DETECTED", (x1 + 60, y1 + 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.3, (255, 255, 255), 4)

            timestamp = datetime.now(LOCAL_TZ).strftime("%H:%M:%S")

            if last_alert_time != timestamp:
                alerts.append(timestamp)
                if len(alerts) > 10:
                    alerts.pop(0)
                save_alerts()
                last_alert_time = timestamp

        prev_gray = gray.copy()

        _, buffer = cv2.imencode(".jpg", blended)
        yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n")
