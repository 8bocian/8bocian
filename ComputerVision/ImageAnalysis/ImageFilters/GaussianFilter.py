#  Copyright (c) 2022. Oskar "Bocian" Możdżeń
#  All rights reserved.

import numpy as np
from scipy.ndimage import filters

def gaussianFilter(image_gray, mode='x', sigma=5):
    # sigma - standard deviation

    image_array = np.array(image_gray)
    image_d = np.zeros(image_array.shape)

    if mode == 'x':
        d = (0, 1)
    else:
        d = (1, 0)

    filters.gaussian_filter(image_array, (sigma, sigma), d, image_d)
    return image_d
