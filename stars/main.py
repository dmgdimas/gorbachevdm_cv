import numpy as np
import matplotlib.pylab as plt
from skimage.measure import label
from skimage.morphology import (binary_dilation, binary_closing,
                                binary_erosion, binary_opening)
from collections import defaultdict

def neighbours4(y, x):
    return (y-1, x), (y+1, x), (y, x-1), (y, x+1)

def neighboursX(y, x):
    return (y-1, x+1), (y+1, x+1), (y+1, x-1), (y-1, x-1)

def neighbours8(y, x):
    return neighbours4(y, x) + neighboursX(y, x)

def boundaries(labeled, label, connectivity=neighbours8):
    pos = np.where(labeled==label)
    bounds = []
    for y, x in zip(*pos):
        for yn, xn in connectivity(y, x):
            if yn < 0 or yn > labeled.shape[0]-1:
                bounds.append((y, x))
                break
            elif xn < 0 or xn > labeled.shape[1]-1:
                bounds.append((y, x))
                break
            elif labeled[yn, xn] == 0:
                bounds.append((y, x))
                break
    return bounds

def centroid(labeled, label):
    pos_y, pos_x = np.where(labeled == label)
    cy = pos_y.mean()
    cx = pos_x.mean()
    return cy, cx

def distance(px1, px2):
    return ((px1[0] - px2[0])**2 + (px1[1] - px2[1])**2)**0.5

def std_radial(labeled, label, connectivity=neighbours4):
    r, c = centroid(labeled, label)
    bounds = boundaries(labeled, label, connectivity)
    K = len(bounds)
    sr = 0
    rd = radial_distance(labeled, label, connectivity)
    for rk, ck, in bounds:
        sr += (distance((r, c), (rk, ck)) - rd)**2
    return (sr / K) ** 0.5

def radial_distance(labeled, label, connectivity=neighbours4):
    r, c = centroid(labeled, label)
    bounds = boundaries(labeled, label, connectivity)
    K = len(bounds)
    rd = 0
    for rk, ck, in bounds:
        rd += distance((r, c), (rk, ck))
    return rd / K

stars = np.load('stars.npy')
labeled = label(stars)

groups = defaultdict(lambda: 0)
for i in range(1, np.max(labeled)+1):
    groups[std_radial(labeled, i)] += 1
keys = list(groups.keys())
print("Количество звёздочек:",groups[keys[1]] + groups[keys[2]])