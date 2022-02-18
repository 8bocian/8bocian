#  Copyright (c) 2022. Oskar "Bocian" Możdżeń
#  All rights reserved.

from cv2 import cv2
from CornerDetector import harrisCorners

path = ""
image = cv2.imread(path)
image = harrisCorners(image)
cv2.imshow('Image', image)
cv2.waitKey(0)
