import cv2
import math
import numpy as np
import pyautogui


def preprocess(action_frame):
    blur = cv2.GaussianBlur(action_frame, (3, 3), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_RGB2HSV)


    lower_color = np.array([108, 23, 82])
    upper_color = np.array([179, 255, 255])

    mask = cv2.inRange(hsv, lower_color, upper_color)
    blur = cv2.medianBlur(mask, 5)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 8))
    hsv_d = cv2.dilate(blur, kernel)

    return hsv_d


def findLargestContour(contours):
    max_area = -10000
    c_index = 0

    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])
        if (area > max_area):
            max_area = area
            c_index = i

    largest_contour = contours[c_index]

    return c_index, largest_contour


def getCountDefect(action_frame, largest_contour, defects):
    finger_count = 0

    for i in range(defects.shape[0]):
        s, e, f, d = defects[i, 0]
        start = tuple(largest_contour[s][0])
        end = tuple(largest_contour[e][0])
        far = tuple(largest_contour[f][0])

        # optional to plot these lines
        cv2.line(action_frame, start, end, [255, 0, 0], 2)
        cv2.line(action_frame, start, far, [255, 0, 0], 2)
        cv2.line(action_frame, far, end, [255, 0, 0], 2)
        cv2.circle(action_frame, far, 5, [0, 255, 0], -1)

        a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
        b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
        c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)

        # cosine rule to find angle of the far point from the start and end point
        angle = (math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 180) / 3.14

        # if angle <= 90 ,consider it a finger and plot far point

        if angle <= 90:
            finger_count += 1
            # print(finger_count)
            cv2.circle(action_frame, far, 1, [0, 0, 0], 4)

    return finger_count


cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()

    if (not ret):
        print("Dude !! Frame not captured!")
        continue

    cv2.rectangle(frame, (200, 200), (500, 500), (0, 255, 255), 2)
    action_frame = frame[200:500, 200:500]

    preprocessed_frame = preprocess(action_frame)

    # get contours
    contours, hierarchy = cv2.findContours(preprocessed_frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  #  _, contours, _ = cv2.findContours(preprocessed_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE, )

    try:
        c_index, largest_contour = findLargestContour(contours)

        # get convex hull or largest contour
        hull = cv2.convexHull(largest_contour)

        # draw contours
        spot = np.zeros(action_frame.shape, np.uint8)
        cv2.drawContours(spot, largest_contour, c_index, (255, 0, 255), 2)
        cv2.drawContours(spot, [hull], -1, (0, 255, 255), 2)


        # defect[i] = [start_point, ,end_point, farthest_point, distance_From_farthest_point]
        hullIndices = cv2.convexHull(largest_contour, returnPoints=False)
        defects = cv2.convexityDefects(largest_contour, hullIndices)

        defect_count = getCountDefect(action_frame, largest_contour, defects)

        # Motion Jump time!
        if defect_count > 3:
            pyautogui.press('space')
            cv2.putText(frame, "Motion Jump", (80, 80), cv2.FONT_ITALIC, 2, 2, 2)

        cv2.imshow("Spot", spot)

    except:
        pass

    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()