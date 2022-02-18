#  Copyright (c) 2022. Oskar "Bocian" Możdżeń
#  All rights reserved.

import numpy as np
from cv2 import cv2


def harrisCorners(image, block_size=2, k_size=5, k=0.1, threshold=0.01, iters=2, corner_color=(0, 0, 255)):
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_gray = np.float32(image_gray)

    dst = cv2.cornerHarris(image_gray, block_size, k_size, k)
    dst = cv2.dilate(dst, None, iterations=iters)

    image[dst > threshold * dst.max()] = corner_color

    cv2.imshow('Image', image)
    cv2.waitKey(0)
