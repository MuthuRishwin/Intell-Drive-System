import cv2
import numpy as np
from matplotlib import pyplot as plt


def roi(image, vertices):
    mask = np.zeros_like(image)
    mask_color = 255
    cv2.fillPoly(mask, vertices, mask_color)
    cropped_img = cv2.bitwise_and(image, mask)
    return cropped_img


def draw_lines(image, hough_lines):
    for line in hough_lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    return image


def process(img):
    height = img.shape[0]
    width = img.shape[1]
    roi_vertices = [
        (0, 650),
        (2 * width / 3, 2 * height / 3),
        (width, 1000)
    ]

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_img = cv2.dilate(gray_img, kernel=np.ones((3, 3), np.uint8))

    canny = cv2.Canny(gray_img, 130, 220)

    roi_img = roi(canny, np.array([roi_vertices], np.int32))

    lines = cv2.HoughLinesP(roi_img, 1, np.pi / 180, threshold=10, minLineLength=15, maxLineGap=2)

    if lines is None:
        return img

    final_img = draw_lines(img, lines)

    return final_img


cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if ret:
        try:
            frame = process(frame)

            cv2.imshow("frame", frame)

            if cv2.waitKey(1) & 0xFF == 27:
                break

        except Exception as e:
            print("Error:", e)
            break
    else:
        print("Error: Could not capture frame")
        break

cap.release()
cv2.destroyAllWindows()
