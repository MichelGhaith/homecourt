import sys
sys.path.insert(1, 'D:/graduationproject/backendpart/swishserver/visioncore')
import posetracker as pt
import math
import numpy as np
from datetime import datetime
import random
import cv2 

class AgilityDrill():
    def __init__(self,levelchallenge,data) -> None:
        self.levelchallenge = levelchallenge
        self.drillPoseTracker = pt.poseTracker(False,0.5,1)
        if levelchallenge % 2 == 0 :
            self.programTime = data
        else:
            self.fullHitsNumber = data
        self.numberOfHits = 0
        self.poseIsDetected = False
        self.startTime = None
        self.rightCone = None
        self.leftCone = None
        self.poseMask = None
        self.hasToGoToMiddle = False

    def resetProgram(self):
        self.drillPoseTracker = None
        self.levelchallenge = None
        self.numberOfHits = 0
        self.startTime = None
        self.channel_name = None
        self.fullHitsNumber = None
        self.programTime = None
        self.poseIsDetected = False
        self.rightCone = None
        self.leftCone = None
        self.poseMask = None
        self.hasToGoToMiddle = False
            
    def checkIsHittedUsingPoseMask(self,mask):
        if self.leftCone != None:
            x , y = self.leftCone
            if mask[x][y] == 1.0:
                return "hit"
        elif self.rightCone != None:
            x , y = self.rightCone
            if mask[x][y] == 1.0:
                return "hit"
        return "nothing"
    # left 15 to 85            170 to 245 right         up and down 15 to 240
    def generateNewCone(self):
        i = random.randint(0,1)
        if i == 0 : #left cone
            self.rightCone = None
            self.leftCone = (300,125)
        elif i == 1:
            self.leftCone = None
            self.rightCone = (300,605)
        
    def process(self,image_copy):
        self.drillPoseTracker.poseFinder(image_copy)
        if self.poseIsDetected == False:
            if self.drillPoseTracker.isFullPoseInImage() :
                self.poseIsDetected = True
                if self.startTime == None:
                    self.poseMask = self.drillPoseTracker.posemask()
                    self.generateNewCone()
                    self.hasToGoToMiddle = False
                    return "Pose is Detected For First Time"
            else:
                return "Pose is not detected yet"
        else :
            if not self.drillPoseTracker.isFullPoseInImage():
                self.numberOfLost = self.numberOfLost + 1
                if self.numberOfLost == 60:
                    self.poseIsDetected = False
                    self.numberOfLost = 0
                    return "Pose is Lost"
                #return "nothing"
            else:
                self.poseMask = self.drillPoseTracker.posemask()
                self.numberOfLost = 0
        column = self.poseMask[:,360]
        i = np.count_nonzero(column)
        if self.hasToGoToMiddle == True and i > 200:
            self.hasToGoToMiddle = False
            self.generateNewCone()
            return "Backed To Middle"
        if self.hasToGoToMiddle == False:
            #if self.levelchallenge % 2 == 0 and (datetime.now()- self.startTime).seconds > self.programTime:
            #    return "Program is Finished"     
            state = self.checkIsHittedUsingPoseMask(self.poseMask)
            if state == "hit":
                self.hasToGoToMiddle = True
                self.numberOfHits = self.numberOfHits + 1
                if self.levelchallenge % 2 != 0 and self.numberOfHits >= self.fullHitsNumber:
                    return "Program is Finished"
                return "Has To Go To Middle"
            else:
                return "nothing"
        else :
            return "nothing"
             
        


    

