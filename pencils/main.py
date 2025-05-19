import matplotlib.pyplot as plt
import numpy as np
from skimage.filters import sobel, threshold_otsu
from skimage.measure import label, regionprops
from skimage.morphology import binary_closing, binary_dilation
from collections import defaultdict


c = defaultdict(lambda: 0)
for i in range(1, 13):
    image = plt.imread(f'./images/img ({i}).jpg')[:, :, :-1].mean(axis=2)
    s = sobel(image)
    threshold = threshold_otsu(s)
    s[s < threshold] = 0
    s[s >= threshold] = 1
    
    for _ in range(5):
        s = binary_dilation(s)

    labeled = label(s)
    regions = regionprops(labeled)

    for r in regions:
        c_area = r.convex_area
        e = r.eccentricity
        
        if 0.997 < e < 0.999 and c_area > 20000: # Параметры подбирал вручную
            c[i] += 1


for k in range(1, 13):
    print(f'На изображении {k}: {c[k]} карандашей')
print(f'Всего карандашей: {sum(c.values())}')