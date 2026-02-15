import cv2
import face_recognition
import os
import numpy as np
from datetime import datetime
import pytz

IMG_PATH = "service/ImagesAttendance"
ATT_FILE = "service/Attendance.csv"
LOCAL_TZ = pytz.timezone("Asia/Kolkata")


# ===== LOAD ENCODINGS =====
def load_encodings():
    os.makedirs(IMG_PATH, exist_ok=True)

    images, names = [], []

    for file in os.listdir(IMG_PATH):
        img = cv2.imread(f"{IMG_PATH}/{file}")
        if img is not None:
            images.append(img)
            names.append(os.path.splitext(file)[0])

    encodes = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        e = face_recognition.face_encodings(img)
        if e:
            encodes.append(e[0])

    return encodes, names


# ===== MARK ATTENDANCE (IST TIME) =====
def mark_attendance(name):
    os.makedirs("service", exist_ok=True)

    if not os.path.exists(ATT_FILE):
        open(ATT_FILE, "w").close()

    now = datetime.now(LOCAL_TZ).strftime("%H:%M:%S")

    lines = []
    updated = False

    with open(ATT_FILE, "r") as f:
        lines = f.readlines()

    with open(ATT_FILE, "w") as f:
        for line in lines:
            entry = line.strip().split(",")

            if entry[0] == name:
                f.write(f"{name},{now}\n")
                updated = True
            else:
                f.write(line)

        if not updated:
            f.write(f"{name},{now}\n")


# ===== READ FOR HTML =====
def get_attendance():
    if not os.path.exists(ATT_FILE):
        return []

    data = []
    with open(ATT_FILE, "r") as f:
        for line in f:
            name, time = line.strip().split(",")
            data.append({"name": name, "time": time})

    return data


# ===== VIDEO STREAM =====
def generate_frames():
    cap = cv2.VideoCapture(0)

    known_encodes, names = load_encodings()

    while True:
        ret, img = cap.read()
        if not ret:
            break

        # SHOW CAMERA EVEN IF NO FACE REGISTERED
        if len(known_encodes) == 0:
            cv2.putText(img, "No faces registered",
                        (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 0, 255), 2)
        else:
            small = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            small = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

            faces = face_recognition.face_locations(small)
            encodes = face_recognition.face_encodings(small, faces)

            for enc, loc in zip(encodes, faces):
                dist = face_recognition.face_distance(known_encodes, enc)
                idx = np.argmin(dist)

                name = "UNKNOWN"
                if dist[idx] < 0.5:
                    name = names[idx].upper()
                    mark_attendance(name)

                y1, x2, y2, x1 = [v * 4 for v in loc]

                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img, name, (x1, y2 - 6),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        _, buffer = cv2.imencode(".jpg", img)
        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" +
               buffer.tobytes() + b"\r\n")
