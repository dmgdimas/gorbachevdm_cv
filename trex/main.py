import matplotlib.pyplot as plt
import pyautogui
import webbrowser
import time
import cv2 
import keyboard
from skimage.measure import label
webbrowser.open('https://chromedino.com')
time.sleep(4)
template = pyautogui.locateOnScreen('dino.png')
#координаты
n = template[0] 
m = template[1] 
n = int(n) 
m = int(m)   
jump = 0  #подсчет прыжков
slp = 0.14 #время первой паузы
k = 170    #дистанция до препятствия
speed = 150  #скорость дино
tm = 0.01
speed_counter = 400 #для изменения скорости
trex = pyautogui.screenshot("trex.png",
                            region=(n, m, k, 45)) 
image = cv2.imread("trex.png")
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
labeled = label(image) 
mx = labeled.max()            
pyautogui.press('Space') 
print(f"Dino побежал: {slp}")   
time.sleep(1)       
while True:      
    trex = pyautogui.screenshot("trex.png", 
                                region=(n, m, k, 45))
    image = cv2.imread("trex.png")    
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    labeled = label(image)
    if labeled.max() > mx:  
        pyautogui.press('up')
        time.sleep(slp) 
        pyautogui.keyDown('down')

        pyautogui.keyUp('down')
        time.sleep(0.02)
        jump += 10 
        print(f"{jump//10} Прыжок")
    if jump == speed:
        slp -=0.005
        k +=5
        print('Смена тайма')
        print(slp,k) 
        if jump ==240:
            tm = 0.02
        if slp < 0.01: 
            slp = 0.01
        
        speed += 100
        if speed>speed_counter:
            k +=8
            slp -=0.005
            speed_counter += 150
            print('Переключение  передачи')
            print(slp,k,tm) 
             

