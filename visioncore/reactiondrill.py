import sys
sys.path.insert(1, 'D:/graduationproject/backendpart/swishserver/visioncore')
import posetracker as pt
import cv2
import math
import numpy as np
from datetime import datetime
import random

class ReactionDrill():
    def __init__(self,levelchallenge,data) -> None:
        self.levelchallenge = levelchallenge
        self.drillPoseTracker = pt.poseTracker(False,0.5,1)
        if levelchallenge == 1 or levelchallenge == 2:
            self.waitTime = 5
        elif levelchallenge == 3 or levelchallenge == 4:
            self.waitTime = 3
        elif levelchallenge == 5 or levelchallenge == 6:
            self.waitTime = 2
        if levelchallenge % 2 == 0 :
            self.programTime = data    
        else:
            self.fullHitsNumber = data
        self.score = 0
        self.numberOfTimeOut = 0
        self.numberOfHits = 0
        self.numberOfMiss = 0
        self.poseIsDetected = False
        self.numberOfLost = 0
        self.startTime = None
        self.rightwa7edimin = None
        self.rightwa7edisar = None
        self.righttnenimin = None
        self.righttnenisar = None
        self.wrongimin = None
        self.wrongisar =None
        self.poseMask = None
        self.iIsInitialize = False
        self.previousI = None

    def resetProgram(self):
        self.drillPoseTracker = None
        self.waitTime = 0
        self.levelchallenge = None
        self.numberOfHits = None
        self.numberOfMiss = None
        self.score = None
        self.startTime = None
        self.channel_name = None
        self.startTimeOfAGoal = None
        self.fullHitsNumber = None
        self.programTime = None
        self.numberOfTimeOut = None
        self.poseIsDetected = False
        self.numberOfLost = 0
        self.rightwa7edimin = None
        self.rightwa7edisar = None
        self.righttnenimin = None
        self.righttnenisar = None
        self.wrongimin = None
        self.wrongisar =None
        self.poseMask = None
            
    def checkIsHittedUsingPoseMask(self,mask):
        hitNumber = 0
        missNumber = 0
        if self.rightwa7edimin != None:
            x,y = self.rightwa7edimin
            if mask [x][y] == 1.0:
                hitNumber = hitNumber + 1 
        if self.rightwa7edisar != None :
            x,y = self.rightwa7edisar
            if mask [x][y] == 1.0:
                hitNumber = hitNumber + 1 
        if self.righttnenimin != None:
            x,y = self.righttnenimin
            if mask [x][y] == 1.0:
                hitNumber = hitNumber + 1 
        if self.righttnenisar != None:
            x,y = self.righttnenisar
            if mask [x][y] == 1.0:
                hitNumber = hitNumber + 1 
        if self.wrongimin != None :
            x,y = self.wrongimin
            if mask [x][y] == 1.0:
                x,y = self.wrongimin
                missNumber = missNumber + 1 
        if self.wrongisar != None:
            x,y = self.wrongisar
            if mask [x][y] == 1.0:
                x,y = self.wrongisar
                missNumber = missNumber + 1
        if hitNumber == 2 :
            return "double hit"
        elif hitNumber == 1 and missNumber == 1:
            return "one hit one miss"
        elif hitNumber == 1 and missNumber == 0:
            return "one hit"
        elif hitNumber == 0 and missNumber == 1:
            return "one miss"
        else:
            return "nothing"
    # left 15 to 85            170 to 245 right         up and down 15 to 240
    def generateNewGoal(self):
        leftPosition = (150,210)
        rightPosition = (150,470)
        #(540,210)
        #(160,210)
        mask = self.poseMask 
        i = random.randint(0,2)
        if self.iIsInitialize == False:
            self.iIsInitialize = True
            self.previousI = i
        else:
            while i == self.previousI:
                i = random.randint(0,2)
            self.previousI = i
        if i == 0 : #one right and one wrong
            j = random.randint(0,1)
            if j == 0: # 25dar imin 27mar isar
                """rightiminx = random.randint(100,180)
                rightiminy = random.randint(170,245)
                wrongisarx = random.randint(100,180)
                wrongisary = random.randint(15,85)
                while mask[rightiminx][rightiminy] == 1.0 or mask[wrongisarx][wrongisary] == 1.0 :#or math.dist((rightiminx,rightiminy),(wrongisarx,wrongisary)) < 50 :
                    rightiminx = random.randint(100,180)
                    rightiminy = random.randint(170,245)
                    wrongisarx = random.randint(100,180)
                    wrongisary = random.randint(15,85)"""
                #self.rightwa7edimin = (rightiminx,rightiminy)
                self.rightwa7edimin = rightPosition
                self.rightwa7edisar = None
                self.righttnenimin = None
                self.righttnenisar = None
                self.wrongimin = None
                #self.wrongisar =(wrongisarx,wrongisary)
                self.wrongisar = leftPosition
                
            else: #25dar isar 27mar imin
                """wrongiminx = random.randint(100,180)
                wrongiminy = random.randint(170,245)
                rightisarx = random.randint(100,180)
                rightisary = random.randint(15,85)
                while mask[rightisarx][rightisary] == 1.0 or mask[wrongiminx][wrongiminy] == 1.0:
                    wrongiminx = random.randint(100,180)
                    wrongiminy = random.randint(170,245)
                    rightisarx = random.randint(100,180)
                    rightisary = random.randint(15,85)"""
                self.rightwa7edimin = None
                #self.rightwa7edisar = (rightisarx,rightisary)
                self.rightwa7edisar = leftPosition
                self.righttnenimin = None
                self.righttnenisar = None
                #self.wrongimin = (wrongiminx,wrongiminy)
                self.wrongimin = rightPosition
                self.wrongisar =None
                
        elif i == 1: #one right only
            j = random.randint(0,1)
            if j == 0: # rightGoal 3l imin bs
                """rightiminx = random.randint(100,180)
                rightiminy = random.randint(170,245)
                while mask[rightiminx][rightiminy] == 1.0:
                    rightiminx = random.randint(100,180)
                    rightiminy = random.randint(170,245)"""
                #self.rightwa7edimin = (rightiminx,rightiminy)
                self.rightwa7edimin = rightPosition
                self.rightwa7edisar = None
                self.righttnenimin = None
                self.righttnenisar = None
                self.wrongimin = None
                self.wrongisar =None
                
            else: #right goal 3lisar bs
                """rightisarx = random.randint(100,180)
                rightisary = random.randint(15,85)
                while mask[rightisarx][rightisary] == 1.0:
                    rightisarx = random.randint(100,180)
                    rightisary = random.randint(15,85)"""
                self.rightwa7edimin = None
                #self.rightwa7edisar = (rightisarx,rightisary)
                self.rightwa7edisar = leftPosition
                self.righttnenimin = None
                self.righttnenisar = None
                self.wrongimin = None
                self.wrongisar =None         
        else : #two right
            """firstrightx = random.randint(100,180)
            firstrighty = random.randint(170,245)
            secondrightx = random.randint(100,180)
            secondrighty = random.randint(15,85)
            while mask[firstrightx][firstrighty] == 1.0 or mask[secondrightx][secondrighty] == 1.0 :
                firstrightx = random.randint(100,180)
                firstrighty = random.randint(170,245)
                secondrightx = random.randint(100,180)
                secondrighty = random.randint(15,85)"""
            #self.rightwa7edimin = (firstrightx,firstrighty)
            self.rightwa7edimin = rightPosition
            self.rightwa7edisar = None
            self.righttnenimin = None
            #self.righttnenisar = (secondrightx,secondrighty)
            self.righttnenisar = leftPosition
            self.wrongimin = None
            self.wrongisar =None
        self.startTimeOfAGoal = datetime.now()
   
    def process(self,image_copy):
        self.drillPoseTracker.poseFinder(image_copy)
        if self.poseIsDetected == False:
            if self.drillPoseTracker.isFullPoseInImage():
                self.poseIsDetected = True
                self.poseMask = self.drillPoseTracker.posemask()
                self.generateNewGoal()
                if self.startTime == None:
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
            else:
                self.poseMask = self.drillPoseTracker.posemask()
                self.numberOfLost = 0
        
        state = self.checkIsHittedUsingPoseMask(self.poseMask)
        #diff = self.programTime - (datetime.now() - self.startTime).seconds
        #if ((self.levelchallenge % 2 == 0) and ( diff <= 0 )):
        #    return "Program is Finished"
        if state == "double hit":
            self.numberOfHits = self.numberOfHits + 2
            self.score = self.score + 4
            if self.levelchallenge % 2 != 0 and self.numberOfHits >= self.fullHitsNumber:
                return "Program is Finished"
            self.generateNewGoal()
            return "hit" 
        elif state == "one hit one miss":
             self.numberOfHits = self.numberOfHits + 1
             if self.levelchallenge % 2 != 0 and self.numberOfHits >= self.fullHitsNumber:
                return "Program is Finished"
             self.generateNewGoal()
             return "hit" 
        elif state == "one hit":
            self.score = self.score + 1
            self.numberOfHits = self.numberOfHits + 1
            if self.levelchallenge % 2 != 0 and self.numberOfHits >= self.fullHitsNumber:
                return "Program is Finished"
            self.generateNewGoal()
            return "hit"
        elif state == "one miss":
            self.score = self.score - 1
            self.numberOfMiss = self.numberOfMiss + 1 
            self.generateNewGoal()
            return "miss"
       
        diff = (datetime.now() - self.startTimeOfAGoal).seconds
        if diff >= self.waitTime:
            self.generateNewGoal()
            self.numberOfTimeOut = self.numberOfTimeOut + 1
            return "TimedOut"
        return "nothing"


    

