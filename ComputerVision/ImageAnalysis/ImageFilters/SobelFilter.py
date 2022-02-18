#  Copyright (c) 2022. Oskar "Bocian" Możdżeń
#  All rights reserved.

import numpy as np
from scipy.ndimage import filters

def sobelFiltering(image_gray, mode='x'):
    image_array = np.array(image_gray)

    image_x = image_y = np.zeros(image_array.shape)

    filters.sobel(image_array, 1, image_x)
    filters.sobel(image_array, 0, image_y)

    if mode == 'y':
        image = image_y
    elif mode == 'x':
        image = image_x
    else:
        image = np.sqrt(image_x ** 2 + image_y ** 2)

    return image
