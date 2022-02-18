#  Copyright (c) 2022. Oskar "Bocian" Możdżeń
#  All rights reserved.

from cv2 import cv2
import numpy as np

def opticalFlow(capture_src=0, step=16):
    cap = cv2.VideoCapture(capture_src)

    _, image = cap.read()
    prev_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    while 1:
        _, image = cap.read()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        prev_gray = gray

        cv2.imshow('Optical flow', drawFlow(gray, flow, step))
        if cv2.waitKey(10) == 27:
            cv2.destroyAllWindows()
            break


def drawFlow(image, flow, step):
    h, w = image.shape[:2]
    y, x = np.mgrid[step/2:h:step, step/2:w:step].reshape(2, -1)
    y = y.astype(np.int32)
    x = x.astype(np.int32)
    fx, fy = flow[y, x].T

    lines = np.vstack([x, y, x+fx, y+fy]).T.reshape(-1, 2, 2)
    lines = np.int32(lines)

    vis = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    for (x1, y1), (x2, y2) in lines:
        cv2.line(vis, (x1, y1), (x2, y2), (0, 255, 0), 1)
        cv2.circle(vis, (x1, y1), 1, (0, 255, 0), -1)
    return vis
