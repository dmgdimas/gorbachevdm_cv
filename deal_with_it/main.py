import cv2
import numpy as np
cv2.namedWindow('Camera', cv2.WINDOW_NORMAL)
glasses=cv2.imread("deal-with-it.png")

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_AUTO_EXPOSURE,1)
capture.set(cv2.CAP_PROP_EXPOSURE,-3)

def censore(image,size=(5,5)):
    result=np.zeros_like(image)
    stepy=result.shape[0]//size[0]
    stepx=result.shape[1]//size[1]
    for y in range(0,image.shape[0],stepy):
        for x in range(1,image.shape[1],stepx):
            for c in range(0,image.shape[2]):
                result[y:y+stepy,x:x+stepx,c]=np.mean(image[y:y+stepy,x:x+stepx,c])
    return result

face_cascade = cv2.CascadeClassifier("haarcascade-frontalface-default.xml")
eye_cascade = cv2.CascadeClassifier("haarcascade-eye.xml")
eye_glasses = cv2.CascadeClassifier("haarcascade-eye-tree-eyeglasses.xml")

glasses,transparent=glasses[:,:,:3],glasses[:,:,-1]
glasses=cv2.resize(glasses,(glasses.shape[1]//6,glasses.shape[0]//6))
transparent=cv2.resize(transparent,(transparent.shape[1]//6,transparent.shape[0]//6))

glasses_gray=cv2.cvtColor(glasses,cv2.COLOR_BGR2GRAY)
ret,mask=cv2.threshold(glasses_gray,10,255,cv2.THRESH_BINARY_INV)
mask=transparent


while capture.isOpened():
    
    ret, frame = capture.read()
    blurred = cv2.GaussianBlur(frame, (11,11), 0)
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    faces = eye_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=7)
    print(faces)
    print(len(faces))
    eyes=[]
    for x,y,w,h in faces:
        eyes.append((x,y,w,h))
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        new_w=w#int(w*1.5)
        new_h=h#int(h*1.5)
        x-=w//6
        y-=h//6
        try:
            roi=frame[y:y+new_h,x:x+new_w]
            censored=censore(roi,(10,10))
            frame[y:y+new_h,x:x+new_w]=censored
        except ValueError:
            pass
    
    if len(faces)==2:
        x1, y1, w1, h1 = eyes[0]
        x2, y2, w2, h2 = eyes[1]

        combined_x = min(x1, x2)
        combined_y = min(y1, y2)
        mask = cv2.inRange(glasses, np.array([1, 1, 1]), np.array([255, 255, 255]))
        roi=frame[combined_y:combined_y+glasses.shape[0],combined_x:combined_x+glasses.shape[1]]
        bg = cv2.bitwise_and(roi, roi, mask=mask)
        fg = cv2.bitwise_and(glasses, glasses, mask=cv2.bitwise_not(mask))
        combined=cv2.add(bg,fg)
        frame[combined_y:combined_y + combined.shape[0], combined_x:combined_x + combined.shape[1]] = combined
    key = chr(cv2.waitKey(1) & 0xFF)
    if key == "q":
        break
    cv2.imshow("Camera", frame)
capture.release()
cv2.destroyAllWindows()