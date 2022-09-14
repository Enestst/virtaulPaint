#virtual main project with opencv
import cv2 as cv
import numpy as np

# parameters of the color, calculated with color detection and used directly in the project

colors = [[100,60,60,140,255,255], # for blue, if will be added more colors should add for loop in findColor func
        ]


capture = cv.VideoCapture(0) # default webcam of machine

capture.set(3, 640) # width of frame
capture.set(4, 480) # height of frame
capture.set(10,100) # braightness of frame

drawPoints = []
# finding color and its mask
def findColor(image, colorlist):
    # creatinng HSV format of the image
    imgHsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    
    lower = np.array(colorlist[0][:3]) # lower bound of blue
    upper = np.array(colorlist[0][3:]) # upper bound of blue
    # creating mask with inRange
    mask = cv.inRange(imgHsv, lower, upper)
    
    # finding blue color points and adding final drawing list
    x, y = getContours(mask)
    if x!= 0 and y != 0:
        drawPoints.append([x,y])
    
# getting contour function
def getContours(img):
    x,y,w,h = 0,0,0,0
    contours,hierarchy = cv.findContours(img,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)
    
    for cnt in contours:
        if cv.contourArea(cnt)>100: 
            cv.drawContours(imgResult, cnt, -1, (0, 0, 0), 3) # drawing contour of the shape
            #approximate the corners of shape
            arcl = cv.arcLength(cnt,True)
            appr = cv.approxPolyDP(cnt,0.02*arcl,True)
            x, y, w, h = cv.boundingRect(appr)
            
    return x+w // 2 , y # finding the top center of contour


# drawing function
def draw(drawPoints):
    for point in drawPoints:
        cv.circle(imgResult, (point[0], point[1]), 10, (255,0,0), cv.FILLED)
  
# DISPLAYING loop
while True:
    suc, img = capture.read()
    
    imgResult = img.copy()
    # calling functions to detecting blue color and draw it
    findColor(img, colors)
    
    draw(drawPoints)       
    
    if img is None: # if can not connect to webcam
        break
    
    cv.imshow("webcam", imgResult)
    
    if cv.waitKey(1) & 0xFF == ord("x"): #press x to quit
        break

# Cleanup code
capture.release()
cv.destroyAllWindows()



