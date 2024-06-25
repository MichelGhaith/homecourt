import numpy as np
import cv2 as cv
from cvzone.ColorModule import ColorFinder
from skimage.exposure import is_low_contrast

class ballTracker():
    def __init__(self):
        self.myColorFinder = ColorFinder(False)
        self.hsvVals = {'hmin': 147, 'smin': 23, 'vmin': 98, 'hmax': 180, 'smax': 113, 'vmax': 240}
        self.ballContour = None
        self.currentCenter = (None,None)
        self.previousCenter = (None,None)
        self.direction = None
        self.previousFrame = None
        self.flag = False

    def apply_clahe(self,frame):
        lab = cv.cvtColor(frame, cv.COLOR_BGR2Lab)
        l, a, b = cv.split(lab)
        clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        cl = clahe.apply(l)
        img = cv.merge((cl, a, b))
        final = cv.cvtColor(img, cv.COLOR_Lab2BGR)
        return final
    
    def motion_detection(self,current,inversePoseMask):
        diff = cv.absdiff(self.previousFrame, current)
        grayscale = cv.cvtColor(diff, cv.COLOR_BGR2GRAY)
        _, threshold = cv.threshold(grayscale, 25, 255, cv.THRESH_BINARY)
        temp = cv.bitwise_and(current,current,mask=threshold)
        #mov
        min_HSV = np.array([110, 9, 55], dtype = "uint8")
        max_HSV = np.array([155, 113, 197], dtype = "uint8")
        #orange
        #min_HSV = np.array([115, 0, 0], dtype = "uint8")
        #max_HSV = np.array([167, 255, 255], dtype = "uint8")
        #2sfar
        #min_HSV = np.array([77, 0, 0], dtype = "uint8")
        #max_HSV = np.array([133, 255, 255], dtype = "uint8")
        #diff_threshold = cv.inRange(justBall, min_HSV, max_HSV)
        diff_threshold = cv.inRange(temp, min_HSV, max_HSV)
        diff_threshold = cv.morphologyEx(diff_threshold,cv.MORPH_CLOSE,(5,5))
        #diff_threshold = cv.morphologyEx(justBall,cv.MORPH_CLOSE,(5,5))
        return diff_threshold
    
    def ballFinder(self,current,inversePoseMask):
        if is_low_contrast(current):
            current = self.apply_clahe(current)
        current = cv.GaussianBlur(current, (5,5), 0)
        if self.flag == True:
            motion = self.motion_detection(current,inversePoseMask)

            self.previousFrame = current
            contours, _ =cv.findContours(motion,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
            if len(contours) > 0:
                cnt = max(contours,key= lambda x : cv.contourArea(x))
                self.ballContour = cnt   
        else :
            self.previousFrame = current
            self.flag = True
            
    def detectCenterOfBall(self):
        ballContour = self.ballContour
        M = cv.moments(ballContour)
        self.previousCenter = self.currentCenter
        if M['m00'] != 0:
            cy =  int(M['m10']/M['m00'])
            cx = int(M['m01']/M['m00'])
            self.currentCenter = (cx,cy)  
        else :
            self.currentCenter = (None,None)  

    def detectDirection(self):
        if(self.currentCenter != None):
            currentX,currentY = self.currentCenter
        if self.previousCenter != None:
            previousX,previousY = self.previousCenter
        if previousX != None and currentX != None:
            if previousX < currentX:
                self.direction = "Down"
            elif previousX > currentX:
                self.direction = "Up"
            else:
                self.direction = "Unknown"
        else:
            self.direction = None
    
    def drawBallContour(self,image):
        image_copy = image.copy()
        image_copy =cv.drawContours(image_copy,[self.ballContour],-1,(0,255,0),10)
        return image_copy
    
    def drawCenterOfBall(self,image):
        image_copy = image.copy()
        x ,y = self.currentCenter
        image_copy = cv.circle(image_copy,(y,x),5,(255,0,255),-1)
        return image_copy


