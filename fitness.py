import cv2
import cvzone
from cvzone import PoseModule
import numpy as np
import os
from typing import List, Tuple


def function_init_header() -> List[List[int]]:
    folderPath = "header"
    list_header = os.listdir(folderPath)
    overlayList = []
    for imPath in list_header:
        image = cv2.imread(f'{folderPath}/{imPath}')
        overlayList.append(image)
    return overlayList


def function_init_var() -> Tuple[int, int, str, str, List[List[int]], List[int]]:
    count = 0
    direction = 0
    exercise = 'squat'
    previous_exercise = 'squat'
    overlayList = function_init_header()
    header = overlayList[0]
    return count, direction, exercise, previous_exercise, overlayList, header


def function_init_webcam() -> cv2.VideoCapture:
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)
    cap.set(10, 150)
    return cap


def function_bar_text(bar, percentage, color):
    # Bar
    cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)
    cv2.rectangle(img, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
    cv2.putText(img, f'{int(percentage)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4, color, 4)

    # Count
    cv2.rectangle(img, (0, 450), (400, 750), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15, (255, 0, 0), 25)


def function_exercise(exercise: str, previous_exercise: str, angle_min: int, angle_max: int, p1: int, p2: int, p3: int,
                      count: float, direction: int) -> Tuple[str, float, int]:
    if previous_exercise != exercise:
        count = 0
        direction = 0
    ## RIGHT LEG
    angle = detector.findAngle(img, p1, p2, p3)
    percentage = np.interp(angle, (angle_min, angle_max), (100, 0))
    bar = np.interp(angle, (angle_min, angle_max), (100, 650))

    color = (255, 0, 255)
    if percentage == 100:
        color = (0, 255, 0)
        if direction == 0:
            count += 0.5
            direction = 1
    if percentage == 0:
        color = (0, 255, 0)
        if direction == 1:
            count += 0.5
            direction = 0

    function_bar_text(bar, percentage, color)
    previous_exercise = exercise

    return previous_exercise, count, direction


if __name__ == '__main__':
    count, direction, exercise, previous_exercise, overlayList, header = function_init_var()
    cap = function_init_webcam()
    detector = cvzone.PoseModule.PoseDetector()

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, False)

        if len(lmList[0]) != 0:

            ### MENU
            x1, y1 = lmList[0][19][1:]
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            if y1 < 125:
                if 170 < x1 < 420:
                    header = overlayList[0]
                    exercise = 'squat'
                elif 460 < x1 < 660:
                    header = overlayList[1]
                    exercise = 'curl'
                elif 700 < x1 < 965:
                    header = overlayList[2]
                    exercise = 'lateral_raise'
                elif 1085 < x1 < 1280:
                    header = overlayList[3]
                    exercise = 'eraser'

            ### EXERCISE
            if exercise == 'curl':
                previous_exercise, count, direction = function_exercise("curl", previous_exercise, 60, 150, 15, 13,
                                                                        11, count, direction)

            elif exercise == 'squat':
                previous_exercise, count, direction = function_exercise("squat", previous_exercise, 60, 150, 23, 25,
                                                                        27, count, direction)

            elif exercise == 'lateral_raise':
                previous_exercise, count, direction = function_exercise("lateral_raise", previous_exercise, 280, 330, 23, 11,
                                                                        13, count, direction)

            elif exercise == 'eraser':
                count = 0
                direction = 0

        img[0:125, 0:1280] = header
        cv2.imshow("Image", img)
        cv2.waitKey(1)
