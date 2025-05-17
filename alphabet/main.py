import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label, regionprops
from skimage.morphology import binary_dilation
from skimage.segmentation import clear_border

def count_holes(region):
    shape = region.image.shape
    new_image = np.zeros((shape[0] + 2, shape[1] + 2))
    new_image[1:-1, 1:-1] = region.image
    new_image = np.logical_not(new_image)
    labeled = label(new_image)
    return np.max(labeled) - 1

def count_lr_vlines(region):
    x = region.image.mean(axis=0) == 1
    return np.sum(x[:len(x)//2]) > np.sum(x[len(x)//2:])

def count_vlines(region):
    return np.all(region.image, axis=0).sum()

def hole_area(region):
    inverted = ~region.image
    internal = clear_border(inverted)
    labeled = label(internal)
    regions = regionprops(labeled)
    return sum(region.area for region in regions)

def recognize(region):
    if np.all(region.image):
        return '-'
    else:
        holes = count_holes(region)
        if holes == 2: # B,8
            _, cx = region.centroid_local
            cx /= region.image.shape[1]
            if cx < 0.44:
                return 'B'
            return '8'
        elif holes == 1: # A,0,P,D
            if count_vlines(region) > 1: # P,D
                if hole_area(region) / region.area < 0.45:
                    return 'P' 
                else:
                    return 'D'
            else: # A,0
                cy, cx = region.centroid_local
                cx /= region.image.shape[1]
                cy /= region.image.shape[0]
                if abs(cx - cy) < 0.03:
                    return '0'
                return 'A'
        else: # 1,*,/,x,w
            if count_vlines(region) >= 3:
                return '1'
            else:
                if region.eccentricity < 0.45:
                    return '*'
                else:
                    inv_image = ~region.image
                    inv_image = binary_dilation(inv_image, np.ones((3, 3)))
                    labeled = label(inv_image, connectivity=1)
                    if np.max(labeled)==2:
                        return '/'
                    elif np.max(labeled)==4:
                        return 'X'
                    else:
                        return 'W'


symbols = plt.imread('symbols.png')
symbols = symbols[:, :, :-1]
gray = symbols.mean(axis=2)
binary = gray > 0

labeled = label(binary)
regions = regionprops(labeled)

result = {}


for region in regions:
    symbol = recognize(region)
    if symbol not in result:
        result[symbol] = 0
    result[symbol] += 1

for k, v in result.items():
    print(k, v)