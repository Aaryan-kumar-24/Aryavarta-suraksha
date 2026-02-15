import cv2
import os

IMG_PATH = "service/ImagesAttendance"
ATT_FILE = "service/Attendance.csv"


def register(name):
    os.makedirs(IMG_PATH, exist_ok=True)

    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()

    if ret:
        cv2.imwrite(f"{IMG_PATH}/{name}.jpg", frame)

    cap.release()

    # create attendance file if not exists
    if not os.path.exists(ATT_FILE):
        open(ATT_FILE, "w").close()
