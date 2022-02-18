#  Copyright (c) 2022. Oskar "Bocian" Możdżeń
#  All rights reserved.

from cv2 import cv2
from SobelFilter import sobelFiltering
from GaussianFilter import gaussianFilter

path = ""
image = cv2.imread(path)
image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

sobel_image = sobelFiltering(image_gray)

gaussian_image = gaussianFilter(image_gray, sigma=3)

cv2.imshow('Sobel image', sobel_image)
cv2.waitKey(0)
cv2.imshow('Gaussian image', gaussian_image)
cv2.waitKey(0)
