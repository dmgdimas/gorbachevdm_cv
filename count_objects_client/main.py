import cv2
import zmq
import numpy as np
from scipy.ndimage import binary_fill_holes
from skimage.measure import label, regionprops

address = "84.237.21.36"
port = 6002

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE, b"")
socket.connect(f"tcp://{address}:{port}")

cv2.namedWindow("Client", cv2.WINDOW_GUI_NORMAL)
while True:
    count = 0
    circle_count = 0
    message = socket.recv()
    frame = cv2.imdecode(np.frombuffer(message, np.uint8), -1)
    blurred = cv2.GaussianBlur(frame, (7, 7), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(hsv, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 90, 255, cv2.THRESH_BINARY)
    thresh = cv2.erode(thresh, np.ones((7, 7)), iterations=4)
    labeled_image = label(thresh)
    regions = regionprops(labeled_image)
    output_frame = frame.copy()
    
    for region in regions:
        area = region.area
        perimeter = region.perimeter
        if(area > 200):
            count+=1
        else: continue
        circularity = 4 * np.pi * area / (perimeter * perimeter) if perimeter > 0 else 0
        if circularity > 0.84 : 
            circle_count += 1
        elif circularity < 0.68:
            count+=1
    key = chr(cv2.waitKey(1) & 0xFF)
    if key == "q":
        break
    
    cv2.putText(frame, f"Count: {count}", (10,60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0,0))
    cv2.putText(frame, f"Count circles: {circle_count}", (10,80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0,0))
    cv2.putText(frame, f"Count squares: {count-circle_count}", (10,100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0,0))
    cv2.imshow("Client", frame)
