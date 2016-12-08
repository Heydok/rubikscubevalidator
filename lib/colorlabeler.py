#!/usr/bin/env python2

from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np
import cv2

class ColorLabeler:
    def __init__(self):
        # Initialize the colors dictionary, containing the color name as
        # the key and the RGB tuple as the value.
        colors = OrderedDict({
        'red': (255,0,0),
        'green': (0,255,0),
        'blue': (0,0,255),
        'yellow': (255,255,0),
        'green': (60,255,0),
        'orange': (255, 141, 0)
        # 'light_blue': (110,50,50),
        # 'dark_blue': (130,255,255)
        })
    
        # Allocate memory for the L*a*b* image, then initialize the
        # color names list
        self.lab = np.zeros((len(colors), 1, 3), dtype='uint8')
        self.colorNames = []

        # Loop over colors
        for (i, (name, rgb)) in enumerate(colors.items()):
            # Update the L*a*b* array and the color names list
            self.lab[i] = rgb
            self.colorNames.append(name)

        # Convert the L*a*b* array from the RGB color space to L*a*b*
        self.lab = cv2.cvtColor(self.lab, cv2.COLOR_RGB2LAB)

    def label(self, image, c):
        # Construct a mask for the contour, then compute
        # the average L*a*b* value for the masked region
        mask = np.zeros(image.shape[:2], dtype='uint8')
        cv2.drawContours(mask, [c], -1, 255, -1)
        mask = cv2.erode(mask, None, iterations=2)
        mean = cv2.mean(image, mask=mask)[:3]

        # Initialize the minimum distance found thus far
        minDist = (np.inf, None)

        # Loop over the known L*a*b* color values
        for (i, row) in enumerate(self.lab):
            # Compute the distance between current L*a*b*
            # color value and the mean of the range.
            d = dist.euclidean(row[0], mean)

            # If the distance is smaller than the current dist.,
            # then update the bookkeeping variable
            if d < minDist[0]:
                minDist = (d, i)

        # Return the name of the color with the smallest distance
        return self.colorNames[minDist[1]]

