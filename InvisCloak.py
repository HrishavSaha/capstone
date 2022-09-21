import cv2
import time
import numpy as np

fcc = cv2.VideoWriter_fourcc(*"XVID")
output = cv2.VideoWriter("output.avi", fcc, 20.0, (640, 480))

VCO = cv2.VideoCapture(0)
time.sleep(2)
bg = 0

for i in range(60):
    ret,bg = VCO.read()

bg = np.flip(bg, 1)

while (VCO.isOpened()):
    i=1
    print(i)
    i+=1
    ret, img = VCO.read()
    if not ret:
        print('break called')
        break
    img = np.flip(img, 1)
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    lred = np.array([0,120,50])
    ured = np.array([10,255,255])
    mask1 = cv2.inRange(hsv,lred,ured)
    lred = np.array([170,120,70])
    ured = np.array([180,255,255])
    mask2 = cv2.inRange(hsv,lred, ured)

    mask1 = mask1 + mask2

    mask1 = cv2.morphologyEx(mask1,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    mask1 = cv2.morphologyEx(mask1,cv2.MORPH_DILATE,np.ones((3,3),np.uint8))

    mask2 = cv2.bitwise_not(mask1)
    res1 = cv2.bitwise_and(img,img,mask=mask2)
    res2 = cv2.bitwise_and(bg, bg, mask=mask1)

    fOutput = cv2.addWeighted(res1,1,res2,1,0)
    output.write(fOutput)

    cv2.imshow("Magic",fOutput)
    cv2.waitKey(1)
    VCO.release()
    fOutput.release()
    cv2.destroyAllWindows()
