import sys
sys.path.insert(1, 'D:/graduationproject/backendpart/swishserver/visioncore')
import posetracker as pt
sys.path.insert(1, 'D:/graduationproject/backendpart/swishserver/visioncore')
import balltracker as bt
sys.path.insert(1, 'D:/graduationproject/backendpart/swishserver/visioncore')
import houghcircles as hc
import math
import numpy as np
from datetime import datetime
import cv2 
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
class BallHandlingDrill():
    def __init__(self,levelchallenge,informations) -> None:
        self.levelchallenge = levelchallenge
        if(self.levelchallenge % 2 == 0) : #quantity matter
            self.programTime = informations['programTime']
            self.drill = informations['drill']
        else : #timematter
            self.program = informations
        self.drillPoseTracker = pt.poseTracker(False,0.5,1)
        #self.drillBallTracker = hc.HoughCircle()
        self.drillBallTracker = bt.ballTracker()
        self.xPositions = []
        self.yPositions = []
        self.currentSituation = None
        self.previousSituation = None
        self.situationQueue = []
        self.dribblecount = 0
        self.startTimeOfProgram = None
        self.ballNotFound = 0
        self.directionIsNotDetected = 0
        self.poseIsLost = 0
        self.poseIsDetected = False
    
    def linearRegression(self):
        a,b = np.polyfit(self.xPositions,self.yPositions,1)
        return a,b

    def quadraticRegression(self):
        a,b,c = np.polyfit(self.xPositions,self.yPositions,2)
        return a,b,c
        
    def crossoverEvaluation(self):
        situations = self.situationQueue
        first = situations[0]
        second = situations[1]
        third = situations[2]
        situationCheck = False
        if first == "DownRight" and second == "Up" and third == "DownLeft":
            situationCheck = True
        if first == "DownLeft" and second == "Up" and third == "DownRight":
            situationCheck = True
        if situationCheck == False:
            return False
        else:
            #functionCheck (check the values of a b c)
            # then it has to be both of checks true to be a cross over
            return situationCheck
            


    def rightVShapeEvaluation(self):
            situations = self.situationQueue
            first = situations[0]
            second = situations[1]
            third = situations[2]
            situationCheck = False
            if first == "DownRight" and second == "Up" and third == "DownRight":
                situationCheck = True
            if situationCheck == False:
                return False
            else:
                #functionCheck (check the values of a b c)
                # then it has to be both of checks true to be a cross over
                return situationCheck
        
    def leftVShapeEvaluation(self):
            situations = self.situationQueue
            first = situations[0]
            second = situations[1]
            third = situations[2]
            situationCheck = False
            if first == "DownLeft" and second == "Up" and third == "DownLeft":
                situationCheck = True
            if situationCheck == False:
                return False
            else:
                #functionCheck (check the values of a b c)
                # then it has to be both of checks true to be a cross over
                return situationCheck
        
    def rightDribbleEvaluation(self,a , b):
            situations = self.situationQueue
            first = situations[0]
            second = situations[1]
            third = situations[2]
            situationCheck = False
            if first == "DownRight" and second == "Up" and third == "DownRight":
                situationCheck = True
            if situationCheck == False:
                return False
            else:
                if ( -0.2 < a and a < 0.2):
                    return True
                else:
                    return False
                #functionCheck (check the values of a b c)
                # then it has to be both of checks true to be a cross over
                #return situationCheck
        
    def leftDribbleEvaluation(self,a , b):
            situations = self.situationQueue
            first = situations[0]
            second = situations[1]
            third = situations[2]
            situationCheck = False
            if first == "DownLeft" and second == "Up" and third == "DownLeft":
                situationCheck = True
            if situationCheck == False:
                return False
            else:
                #functionCheck (check the values of a b c)
                # then it has to be both of checks true to be a cross over
                if -0.2 < a and a < 0.2:
                    return True
                else:
                    return False
                #return situationCheck

    def drillEvaluation(self):
            if self.levelchallenge % 2 == 0:
                drillName = self.drill
            else:
                drillInformation = self.program[0]
                drillName = drillInformation['excercise']
            if drillName == 'Left  Dribble':
                a,b = self.linearRegression()
                #image_copy = self.drawLinearFunction(image,a,b)
                #cv2.imshow("image" , image_copy)
                #cv2.waitKey(1)
                return self.leftDribbleEvaluation(a,b)
                
            elif drillName == 'Right Dribble':
                a,b = self.linearRegression()
                #image_copy = self.drawTheFunction(image,a,b)
                #cv2.imshow("image" , image_copy)
                #cv2.waitKey(1)
                
                #print("right dribble a " + str(a))
                #print("right dribble b " + str(b))
                
                return  self.rightDribbleEvaluation(a,b)
                
            elif drillName == 'Left V Dribble':
                #a , b , c = self.quadraticRegression()
                #image_copy = self.drawQuadraticFunction(image,a,b,c)
                #cv2.imshow("image" , image_copy)
                #cv2.waitKey(1)
                return self.leftVShapeEvaluation()
        
            elif drillName == 'Right V Dribble':
                #a , b , c = self.quadraticRegression()
                return self.rightVShapeEvaluation()
        
            else :
                #a , b , c = self.quadraticRegression()
                return self.crossoverEvaluation()
    
    def resetProgress(self):
        self.currentSituation = None
        self.previousSituation = None
        self.xPositions = []
        self.yPositions = []
        self.situationQueue = []
        self.ballNotFound = 0
        self.directionIsNotDetected = 0
        self.poseIsLost = 0

    def resetProgram(self):
        self.resetProgress()
        self.channel_name = None
        self.drillPoseTracker = None
        self.drillBallTracker = None
        self.program= []
        self.startTimeOfProgram = None
        self.levelchallenge = None
        self.dribblecount = None
        self.programTime = None
        self.drill = None
        self.poseIsDetected = False

    def detectWhichHand(self,ball,rightHand,leftHand):
            d1 = math.dist(ball,rightHand)
            d2 = math.dist(ball,leftHand)
            if d1 > d2:
                return "Left"
            else :
                return "Right"
            
    def drawLinearFunction(self,image,a,b):
        image_copy = image.copy()
        xList = [item for item in range(0,480)]
        for x in xList:
            y = int (a*x + b )
            image_copy = cv2.circle(image_copy,(y,x), 5 , (255,0,255),-1)
        return image_copy
    
    def drawQuadraticFunction(self,image,a,b,c):
        image_copy = image.copy()
        xList = [item for item in range(0,480)]
        for x in xList:
            y = int ( (a*x * x ) + (b * x )+ c)
            image_copy = cv2.circle(image_copy,(y,x), 5 , (255,0,255),-1)
        return image_copy
          
    def updateState(self,current):
        #height bidel 3la x nizami
        #width bidel 3la y nizami
        height,width,z = current.shape
        self.drillPoseTracker.landmarksDetector(height,width)
        self.drillBallTracker.ballFinder(current,None) #self.inversePoseMask
        self.drillBallTracker.detectCenterOfBall()
        ball = self.drillBallTracker.currentCenter
        leftHand = self.drillPoseTracker.landmarkByItsIndex(20)
        #x , y = leftHand
        #cv2.circle(current,(y,x),10,(255,0,0),-1)
        #cv2.imshow("frame" , current)
        #cv2.waitKey(1)
        rightHand = self.drillPoseTracker.landmarkByItsIndex(19)
        leftHip = self.drillPoseTracker.landmarkByItsIndex(24)
        rightHip = self.drillPoseTracker.landmarkByItsIndex(23)
        if ball == (None,None):
            self.ballNotFound += 1
            if self.ballNotFound == 10 :
                return "Ball Not Found"
        else:
            self.ballNotFound = 0
        if leftHand == None and rightHand == None: #lazem ma 3ad ifout 3hal shrt b7iato
            return "not finished yet"
        self.drillBallTracker.detectDirection()
        direction = self.drillBallTracker.direction
        if direction == None or direction == "Unknown" :
            self.directionIsNotDetected +=1
            if self.directionIsNotDetected == 10 :
                return "Ball direction is unknown"
        else:
            self.directionIsNotDetected = 0
        hand = self.detectWhichHand(ball,rightHand,leftHand)
        #landmarks = self.drillPoseTracker.drawLandMarks(current)
        """contour = self.drillBallTracker.drawBallContour(current)
        center = self.drillBallTracker.drawCenterOfBall(contour)
        cv2.imshow("landmarks" , center)
        cv2.waitKey(1)"""
        if (self.currentSituation != None and self.previousSituation == None) or (self.currentSituation == "Up" and self.previousSituation != None) or (self.currentSituation != None and self.previousSituation == "Up"):
            currentX , currentY = ball
            self.xPositions.append(currentX)
            self.yPositions.append(currentY)

        if direction == "Down" and self.previousSituation == None and self.currentSituation == None:    
            if hand == "Left":
                """_,leftHandY = leftHand
                _, currentBallY = ball"""
                self.currentSituation = "DownLeft"
                self.situationQueue.append("DownLeft")
                """if leftHandY < currentBallY:                        
                    self.currentSituation = "DownLeft"
                    self.situationQueue.append("DownLeft")
                else :
                    # the wrong here is the hand under the ball
                    self.resetProgress()
                    print("left hand under the ball from first sitation")
                    return "Hand under the ball"
                    """
            else:
                """_,rightHandY = rightHand
                _, currentBallY = ball"""
                self.currentSituation = "DownRight"
                self.situationQueue.append("DownRight")
                """if rightHandY < currentBallY:
                    self.currentSituation = "DownRight"
                    self.situationQueue.append("DownRight")
                else :
                    # the wrong here is the hand under the ball
                    self.resetProgress()
                    print("right hand under the ball from first situation")
                    return "Hand under the ball"
                    """
                
        if direction == "Up" and self.currentSituation != None and self.previousSituation == None:
            currentBallX, currentBallY = ball
            LeftHipX,leftHipY = leftHip
            rightHipX,rightHipY = rightHip
            # bltl3a ltabe 2jbari t7t lhip (2wal ma ttla3) w 7ta kman t7t lrkbe 2jbari
            if LeftHipX < currentBallX or rightHipX < currentBallX:
                self.previousSituation = self.currentSituation
                self.currentSituation = "Up"
                self.situationQueue.append("Up")
            else :
                #the wrong here ltabe ma 3m ttej bl2red
                self.resetProgress()
                return "the ball is not hitting the ground"
        if direction == "Down" and self.currentSituation == "Up" and self.previousSituation != None:
            if hand == "Left":
                """_,leftHandY = leftHand
                _, currentBallY = self.drillBallTracker.currentCenter"""
                self.situationQueue.append("DownLeft")
                isValid = self.drillEvaluation()
                self.resetProgress()
                return isValid
                """if leftHandY  < currentBallY:
                    self.situationQueue.append("DownLeft")
                    isValid = self.drillEvaluation()
                    #image_copy = self.drawTheFunction(640,image_copy)
                    self.resetProgress()
                    return isValid
                else: 
                    # the wrong here is the hand under the ball
                    self.resetProgress()
                    print("left hand under the ball from second phase")
                    return "Hand under the ball"
                """
            else:
                """_,rightHandY = rightHand
                _, currentBallY = ball"""
                self.situationQueue.append("DownRight")
                isValid = self.drillEvaluation()
                self.resetProgress() 
                return isValid
                """if rightHandY  < currentBallY:
                    self.situationQueue.append("DownRight")
                    isValid = self.drillEvaluation()
                    self.resetProgress() 
                    return isValid
                else:
                    # the wrong here is the hand under the ball
                    self.resetProgress()
                    print("right hand under the ball from second phase")

                    return "Hand under the ball"       
                 """
        return "not finished yet"
            
    def validDribble(self):
            drillInformation = self.program[0]
            count = drillInformation['repetition']
            if count == 1:
                self.program.pop(0)
            else:
                drillInformation['repetition'] = drillInformation['repetition'] - 1

    """def process(self,image_copy):
        print("inside process")
        if self.levelchallenge % 2 == 0 and (datetime.now()- self.startTimeOfProgram).seconds > self.programTime:
            return "Program is Finished"
        if self.drillBallTracker.flag == False:
            self.drillPoseTracker.poseFinder(image_copy)
            self.drillPoseTracker.landmarksDetector(image_copy.shape)
            leftHand = self.drillPoseTracker.landmarkByItsIndex(19)
            rightHand = self.drillPoseTracker.landmarkByItsIndex(20)
            self.drillBallTracker.ballHSVFinder(image_copy,leftHand,rightHand)
            return "Ball is not detected yet"
        else:
            self.drillPoseTracker.poseFinder(image_copy)
            self.drillPoseTracker.landmarksDetector(image_copy.shape)
            self.drillBallTracker.ballFinder(image_copy)
            self.drillBallTracker.drawBallContour(image_copy)
            isValid = self.updateState()
            if isValid == True:
                print("valid")
                if self.levelchallenge % 2 == 0:
                    self.dribblecount = self.dribblecount + 1
                else:  
                    self.validDribble()
                    if len(self.program) == 0 :
                        return "Program is Finished"
                return True
            else:
                return isValid"""
    
    def process(self,image_copy):
        self.drillPoseTracker.poseFinder(image_copy)
        if self.poseIsDetected == False:
            if self.drillPoseTracker.isFullPoseInImage():
                self.poseIsDetected = True
                self.poseMask = self.drillPoseTracker.posemask()
                #self.inversePoseMask = self.drillPoseTracker.inverseBinaryPoseMask()
                if self.startTimeOfProgram == None:
                    return "Pose is Detected For First Time"
            else :
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
                #self.inversePoseMask = self.drillPoseTracker.inverseBinaryPoseMask()
                self.numberOfLost = 0
        isValid = self.updateState(image_copy)
        #if self.levelchallenge % 2 == 0 and (datetime.now()- self.startTimeOfProgram).seconds > self.programTime:
        #    return "Program is Finished"
        if isValid == True:
            if self.levelchallenge % 2 == 0:
                self.dribblecount = self.dribblecount + 1
            else:  
                self.validDribble()
                if len(self.program) == 0 :
                    return "Program is Finished"
            return True
        else:
            return isValid
    