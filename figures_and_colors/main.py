import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
from skimage.color import rgb2hsv
from collections import defaultdict

def shadesDivision(colors):
    sorted_colors = sorted(colors.items(), key=lambda item: item[0])
    d = np.diff([k for k, v in sorted_colors])
    pos = np.where(d > np.std(d)*2)
    splits = np.split(sorted_colors, pos[0]+1)
    shades = defaultdict(lambda: 0)
    for i, split in enumerate(splits):
        shade = round(np.mean(split[:, 0]), 2)
        shades[shade] = int(sum(split[:, 1]))
    return(shades)

image = plt.imread('balls_and_rects.png')
gray = image.mean(axis=2)
binary = gray > 0

labeled = label(binary)
regions = regionprops(labeled)

colors_rects = defaultdict(lambda: 0)
colors_balls = defaultdict(lambda: 0)

for i, r in enumerate(regions):
    y, x = r.centroid
    hue = rgb2hsv(image[int(y), int(x)])[0]
    if r.area == r.image.shape[0]*r.image.shape[1]:
        colors_rects[hue] += 1
    else:
        colors_balls[hue] += 1

shades_rects = shadesDivision(colors_rects)
shades_balls = shadesDivision(colors_balls)
sorted_shades_rects = sorted(shades_rects.items(), key=lambda item: item[1])
sorted_shades_balls = sorted(shades_balls.items(), key=lambda item: item[1])


print(f'Всего фигур: {sum(colors_rects.values())+sum(colors_balls.values())}')
shades = shades_rects.keys() | shades_balls.keys() #Чтоб избежать повторения ключей
for shade in shades:
    print(f'{shades_rects[shade]+shades_balls[shade]} фигур оттенка {shade}')
print(f'Прямоугольников: {sum(colors_rects.values())}')
for k, v in sorted_shades_rects:
    print(f'{v} прямоугольников оттенка {k}')
print(f'Кругов: {sum(colors_balls.values())}')
for k, v in sorted_shades_balls:
    print(f'{v} кругов оттенка {k}')