import sys
sys.path.insert(1, 'D:/graduationproject/backendpart/swishserver/visioncore')
import cv2
import numpy as np
class HoughCircle():

    def __init__(self) -> None:
        self.previousFrame = []
        self.flag = False
        self.ballColor = None
        self.currentCenter = (None,None)
        self.previousCenter = (None,None)
        self.direction = None
        self.radius = None

    def getCircles(self,image, handX, handY):
        x = handX -70
        y = handY -70
        w = h = 140
        mask = np.zeros(image.shape[:2],np.uint8)
        mask[y:y+h,x:x+w] = 255
        res = cv2.bitwise_and(image,image,mask = mask)
        gray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
        bilateral_filtered_image = cv2.bilateralFilter(gray, 3, 25,25 )
        circles = cv2.HoughCircles(bilateral_filtered_image,cv2.HOUGH_GRADIENT,1,image.shape[1]/8,param1= 15,param2=25,minRadius=20,maxRadius=30)
        return circles
    
    def setBallMinThresholdMaxThreshold(self,image, circles):
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                # 2za dfet 3lparameter l2wal bimshi 3limin
                center = (i[0],i[1])
                radius = i[2]
                mask = np.zeros(image.shape[:2],dtype= np.uint8)
                mask = cv2.circle(mask,center, radius , 255, -1)
                image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                mean_hsv = cv2.mean(image_hsv, mask= mask)
                h,s,v = cv2.split(image_hsv)
                self.lower_threshold = (mean_hsv[0]-10, mean_hsv[1]-50, mean_hsv[2]-50)
                self.upper_threshold = (mean_hsv[0]+10, mean_hsv[1]+50, mean_hsv[2]+50)
                self.flag = True
    


    def ballMask(self,frame):
        frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        dst= cv2.inRange(frame_HSV,self.lower_threshold,self.upper_threshold)
        contours,_ = cv2.findContours(dst, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) != 0:
            maxContour = max(contours, key = cv2.contourArea)
            self.currentCenter,self.radius = cv2.minEnclosingCircle(maxContour)

    

    def drawBallContour(self,image):
        if self.currentCenter == None:
            cv2.imshow("image" , image)
            cv2.waitKey(1)
        image_copy = image.copy()
        cv2.circle(image_copy, (int(self.currentCenter[0]), int(self.currentCenter[1])), int(self.radius), (0, 255, 0), 2)
        cv2.imshow("contour" , image_copy)
        cv2.waitKey(1)
    
    def drawCenterOfBall(self,image):
        if self.currentCenter == None:
            return image
        image_copy = image.copy()
        cv2.circle(image_copy, (int(self.currentCenter[0]), int(self.currentCenter[1])), 1, (0, 255, 0), -1)
        return image_copy
    
    def detectDirection(self):
        if(self.currentCenter != None):
            _,currentY = self.currentCenter
        if self.previousCenter != None:
            _,previousY = self.previousCenter
        if previousY != None and currentY != None:
            if previousY < currentY:
                self.direction = "Down"
            elif previousY > currentY:
                self.direction = "Up"
            else:
                self.direction = "Unknown"
        else:
            self.direction = None

    def ballHSVFinder(self,current,leftHand,rightHand):
        self.previousFrame = current
        if leftHand == None and rightHand == None:
            return
        leftHandX,leftHandY = leftHand
        rightHandX,rightHandY = rightHand
        circlesL= self.getCircles(current,handX=leftHandX,handY=leftHandY)
        circlesR = self.getCircles(current,handX=rightHandX,handY=rightHandY)
        if circlesL is not None :
            #mmken ifidni lcenter b3den broi
            self.setBallMinThresholdMaxThreshold(current,circles=circlesL) 
        elif circlesR is not None:
            self.setBallMinThresholdMaxThreshold(current,circles=circlesR)           

    def ballFinder(self,current):
        diff = cv2.absdiff(current, self.previousFrame)
        self.previousFrame = current
        self.previousCenter = self.currentCenter
        gray = cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray,(5,5),0)
        _,threshold = cv2.threshold(blur,20,255,cv2.THRESH_BINARY)
        colored = cv2.bitwise_and(current, current , mask= threshold)
        self.ballMask(colored)