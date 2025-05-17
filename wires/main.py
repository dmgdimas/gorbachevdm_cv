import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label
from skimage.morphology import (binary_closing,binary_opening,binary_dilation,binary_erosion)

for i in range(1,7):
    data=np.load(f"wires{i}npy.txt")
    labeled=label(data) #маркируем изображение
    nelems=np.max(labeled) #считаем кол-во объектов
    print(f"В {i} файле {nelems} проводов") 
    for j in range(1,nelems+1):
        result=binary_erosion(labeled==j,np.ones(3).reshape(3,1)) #разделить на части
        newlabeled=label(result)
        diff=np.max(newlabeled)-1
        if diff==0:
            print(f"{j} провод целый")
        elif diff<0:
            print(f"{j} провод полностью уничтожен")
        else:
            print(f"У {j} провода {diff} разрезов")
    print("")
