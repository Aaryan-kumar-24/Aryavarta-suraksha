import cv2
import pickle
import os


def run():
    """
    Draw waiting-zone boxes and save to service/box
    Left click:
        - Delete box if clicked inside
        - Otherwise create new box
    Press 'a' to exit
    """

    file_path = "service/box"

    # delete old boxes on start
    if os.path.exists(file_path):
        os.remove(file_path)

    posList = []
    cap = cv2.VideoCapture(0)

    # fixed box size
    box_w, box_h = 200, 200

    def mouseClick(event, x, y, flags, params):
        nonlocal posList, img_shape

        if event == cv2.EVENT_LBUTTONDOWN:
            img_h, img_w = img_shape[:2]

            # 🔴 delete if click inside existing box
            for i, pos in enumerate(posList):
                x1, y1, w1, h1 = pos
                abs_x = int(x1 * img_w)
                abs_y = int(y1 * img_h)
                abs_w = int(w1 * img_w)
                abs_h = int(h1 * img_h)

                if abs_x < x < abs_x + abs_w and abs_y < y < abs_y + abs_h:
                    posList.pop(i)
                    with open(file_path, "wb") as f:
                        pickle.dump(posList, f)
                    return

            # 🟢 create new box
            posList.append((x / img_w, y / img_h, box_w / img_w, box_h / img_h))

            with open(file_path, "wb") as f:
                pickle.dump(posList, f)

    cv2.namedWindow("Wait Zone Selector")
    cv2.setMouseCallback("Wait Zone Selector", mouseClick)

    while True:
        success, img = cap.read()
        if not success:
            continue

        img_shape = img.shape

        # draw boxes
        for pos in posList:
            x_rel, y_rel, w_rel, h_rel = pos
            x = int(x_rel * img_shape[1])
            y = int(y_rel * img_shape[0])
            w = int(w_rel * img_shape[1])
            h = int(h_rel * img_shape[0])

            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

        cv2.putText(
            img,
            "Left Click: Create/Delete | Press 'A' to Exit",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 0),
            2,
        )

        cv2.imshow("Wait Zone Selector", img)

        if cv2.waitKey(1) & 0xFF == ord("a"):
            break

    cap.release()
    cv2.destroyAllWindows()


# 🔥 Django-safe guard
if __name__ == "__main__":
    run()
