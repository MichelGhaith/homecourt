from channels.generic.websocket import AsyncWebsocketConsumer
import reactivex.operators as ops
from reactivex import just
import numpy as np
import json
import visioncore.ballhandlingdrill as bh
import visioncore.reactiondrill as rd
import cv2
from . import models
from datetime import datetime
import asyncio
from .observers import BallHandlingObserver,ReactionDrillObserver,AgilityDrillObserver
from reactivex.scheduler import ThreadPoolScheduler
from skimage.exposure import is_low_contrast

class BallHandlingConsumer(AsyncWebsocketConsumer):
    #'ws://127.0.0.1:8000/ballhandling/'
    async def websocket_connect(self, message):
        self.channel_name = self.channel_name
        self.pool_scheduler = ThreadPoolScheduler(8)  
        self.previous = None
        self.flag = False
        await self.accept()

    async def force_close(self, event):
        if self.levelchallengeid % 2 == 0: #quantitymatter
            count = event['count']
        else:
            finishedTime = event["finishedTime"]
        if self.customWorkout == False:
            program = await models.Program.objects.aget(id = self.programid)
            profile = await models.Profile.objects.aget(id = self.profileid)
            finishedProgram,created= await models.FinishedProgram.objects.aget_or_create(program = program, player = profile)
            if created:
                if self.levelchallengeid % 2 == 0:
                    finishedProgram.highScoreQuantity = count
                else:
                    finishedProgram.highScoreTime = finishedTime
                finishedProgram.highScoreDate = datetime.now()
                finishedProgram.lastTryDate = datetime.now()
                await finishedProgram.asave()
            else :
                finishedProgram.numberOfTries = finishedProgram.numberOfTries + 1
                finishedProgram.lastTryDate = datetime.now()
                if self.levelchallengeid % 2 != 0 :
                    if finishedProgram.highScoreTime > finishedTime:
                        finishedProgram.highScoreTime = finishedTime
                        finishedProgram.highScoreDate = datetime.now()
                else:
                    if finishedProgram.highScoreQuantity < count:
                        finishedProgram.highScoreQuantity = count
                        finishedProgram.highScoreDate = datetime.now()
                await finishedProgram.asave()
        if self.levelchallengeid % 2 == 0:
            await self.send(
                    text_data= json.dumps({
                        'state' : "Program is Finished",
                        'count' : count
                    }))
        else:
            await self.send(
                    text_data= json.dumps({
                        'state' : "Program is Finished",
                        'finishedTime' : finishedTime
                    }))

    def apply_clahe(self,frame):
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2Lab)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        cl = clahe.apply(l)
        img = cv2.merge((cl, a, b))
        final = cv2.cvtColor(img, cv2.COLOR_Lab2BGR)
        return final
        

    async def websocket_receive(self, message):
        if isinstance(message.get('text'), str):
            data = json.loads(message['text'])
            if data['startOfProgramTime'] == 0:
                informations = data['program']       
                self.programid = data['programid']  
                self.profileid = data['profileid']
                self.levelchallengeid = data['levelchallengeid']
                self.customWorkout = data['customWorkout']
                self.observer = BallHandlingObserver(self.channel_name,self.levelchallengeid,informations)
            else:
                startOfProgramTime = datetime.fromisoformat(data['startOfProgramTime'])
                self.observer.ballHandlingDrill.startTimeOfProgram = startOfProgramTime
        elif isinstance(message.get('bytes'), bytes):
            frame = cv2.imdecode(np.frombuffer(message['bytes'], dtype=np.uint8), cv2.IMREAD_COLOR)
            frame = cv2.resize(frame,(720,480))
            frame = cv2.flip(frame , 1)
            

            #frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
            just(frame, scheduler= self.pool_scheduler).subscribe(self.observer)
    
    
    async def dribble_evaluation(self, event):
        if event['state'] == "Pose is not detected yet" or event['state'] == "Pose is Lost":
            await self.send(
                text_data= json.dumps({
                    'state' : event['state']
                })
            )
        else:
            if self.levelchallengeid % 2 == 0 :
                await self.send(text_data= json.dumps({
                "state" : event["state"],
                    "dribblecount" : event["dribblecount"],
                    'drill' : event['drill']
                }))

            else:
                await self.send(text_data= json.dumps({
                "state" : event["state"],
                "count" : event["count"],
                'drill' : event['drill']

                }))
"""if is_low_contrast(frame):
                frame = self.apply_clahe(frame)
            if self.flag == False:
                self.previous = frame
                self.flag = True
            #diff_threshold = cv2.inRange(frame, (147, 23, 98), (180, 113, 240))
            #in moudaraj
            else: 
                #cv2.imshow("frame" , frame)
                #cv2.waitKey(1)
                diff = cv2.absdiff(self.previous, frame)
                grayscale = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                _, threshold = cv2.threshold(grayscale, 25, 255, cv2.THRESH_BINARY)
                temp = cv2.bitwise_and(frame,frame,mask=threshold)
                temp = cv2.cvtColor(temp,cv2.COLOR_BGR2HSV)
                #diff_threshold = cv2.inRange(temp, (38, 47, 126), (101, 172, 255))
                #mov
                #min_HSV = np.array([110, 9, 55], dtype = "uint8")
                #max_HSV = np.array([155, 113, 197], dtype = "uint8")
                #orange
                #min_HSV = np.array([115, 0, 0], dtype = "uint8")
                #max_HSV = np.array([167, 255, 255], dtype = "uint8")
                #2sfar
                min_HSV = np.array([77, 0, 0], dtype = "uint8")
                max_HSV = np.array([133, 255, 255], dtype = "uint8")
                diff_threshold = cv2.inRange(temp, min_HSV, max_HSV)
                diff_threshold = cv2.morphologyEx(diff_threshold,cv2.MORPH_CLOSE,(5,5))
                self.previous = frame
                contours, _ =cv2.findContours(diff_threshold,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                if len(contours) > 0:
                    cnt = max(contours,key= lambda x : cv2.contourArea(x))
                    ballContour = cnt  
                    temp = frame.copy()
                    temp =cv2.drawContours(temp,[ballContour],-1,(255,0,0),2)
                    cv2.imshow("temp" , temp)
                    cv2.waitKey(1)"""

class ReactionDrillConsumer(AsyncWebsocketConsumer):
    #'ws://127.0.0.1:8000/reaction/'
    async def websocket_connect(self,message):
        self.channel_name = self.channel_name
        self.pool_scheduler = ThreadPoolScheduler(8)     
        await self.accept()
        
    async def websocket_receive(self, message):
        if isinstance(message.get('text'), str):
            if isinstance(message.get('text'), str):
                data = json.loads(message['text'])
                if data['startOfProgramTime'] == 0:
                    self.programid = data['programid']  
                    self.profileid = data['profileid']
                    self.levelchallengeid = data['levelchallengeid']
                    if(self.levelchallengeid % 2 == 0) : #quantity matter
                        #programTime = datetime.fromisoformat(data['programTime'])
                        self.observer = ReactionDrillObserver(self.channel_name,self.levelchallengeid,data['programTime'])
                    else : #timematter
                        self.observer = ReactionDrillObserver(self.channel_name,self.levelchallengeid,data['fullHitsNumber'])
                else:
                    startOfProgramTime = datetime.fromisoformat(data['startOfProgramTime'])
                    self.observer.reactionDrill.startTime = startOfProgramTime
                    self.observer.reactionDrill.startTimeOfAGoal = startOfProgramTime
                    #self.observer.reactionDrill.generateNewGoal()
        elif isinstance(message.get('bytes'), bytes):
            frame = cv2.imdecode(np.frombuffer(message['bytes'], dtype=np.uint8), cv2.IMREAD_COLOR)
            frame = cv2.resize(frame,(720,480))
            frame = cv2.flip(frame,1)
            just(frame, scheduler= self.pool_scheduler).subscribe(self.observer)

    async def force_close(self, event):
        if self.levelchallengeid % 2 == 0: #quantitymatter
            score = event['score']
        else:
            finishedTime = event["finishedTime"]
        program = await models.Program.objects.aget(id = self.programid)
        profile = await models.Profile.objects.aget(id = self.profileid)
        finishedProgram,created= await models.FinishedProgram.objects.aget_or_create(program = program, player = profile)
        if created:
            if self.levelchallengeid % 2 == 0:
                finishedProgram.highScoreQuantity = score
            else:
                finishedProgram.highScoreTime = finishedTime
            finishedProgram.highScoreDate = datetime.now()
            finishedProgram.lastTryDate = datetime.now()
            await finishedProgram.asave()
        else :
            finishedProgram.numberOfTries = finishedProgram.numberOfTries + 1
            finishedProgram.lastTryDate = datetime.now()
            if self.levelchallengeid % 2 != 0 :
                if finishedProgram.highScoreTime > finishedTime:
                    finishedProgram.highScoreTime = finishedTime
                    finishedProgram.highScoreDate = datetime.now()
            else:
                if finishedProgram.highScoreQuantity < score:
                    finishedProgram.highScoreQuantity = score
                    finishedProgram.highScoreDate = datetime.now()
            await finishedProgram.asave()
        if self.levelchallengeid % 2 == 0:
            await self.send(
                    text_data= json.dumps({
                        'state' : "Program is Finished",
                        'count' : score
                    }))
        else:
            await self.send(
                    text_data= json.dumps({
                        'state' : "Program is Finished",
                        'finishedTime' : finishedTime
                    }))
      
    async def is_hitted(self, event):
        if event['state'] == "Pose is not detected yet" or event['state'] == "Pose is Lost":
            await self.send(
                text_data= json.dumps({
                    'state' : event['state']
                })
            )
        else :
            right = event['numberOfRightGoals']
            wrong = event['numberOfWrongGoals']
            if right == 2 :
                """rightOnePercent = self.convertGoalPositionToFlutter(event['rightone'])
                rightTwoPercent = self.convertGoalPositionToFlutter(event['rightone'])"""
                await self.send(text_data= json.dumps({
                "state" : event['state'],
                "numberOfRightGoals" : right,
                "numberOfWrongGoals" : wrong,
                'rightOnePercent' : event['rightone'],
                'rightTwoPercent' : event['righttwo'],
                "score" : event['score'],
                }))
            elif right == 1 and wrong == 1:
                """rightPercent = self.convertGoalPositionToFlutter(event['rightone'])
                wrongPercent = self.convertGoalPositionToFlutter(event['wrong'])"""
                await self.send(text_data=json.dumps({
                    "state" : event['state'],
                    "numberOfRightGoals" : right,
                    "numberOfWrongGoals" : wrong,
                    'rightPercent' : event['rightone'],
                    'wrongPercent' : event['wrong'],
                    "score" : event['score']
                }))
            elif right == 1 and wrong == 0:
                #rightPercent = self.convertGoalPositionToFlutter(event['rightone'])
                await self.send(text_data=json.dumps({
                    "state" : event['state'],
                    "numberOfRightGoals" : right,
                    "numberOfWrongGoals" : wrong,
                    'rightPercent' : event['rightone'],
                    "score" : event['score']
                }))


class AgilityDrillConsumer(AsyncWebsocketConsumer):
    #'ws://127.0.0.1:8000/agility/'
    async def websocket_connect(self,message):
        self.channel_name = self.channel_name
        self.pool_scheduler = ThreadPoolScheduler(8)     
        await self.accept()
        
    async def websocket_receive(self, message):
        if isinstance(message.get('text'), str):
            if isinstance(message.get('text'), str):
                data = json.loads(message['text'])
                if data['startOfProgramTime'] == 0:
                    self.programid = data['programid']  
                    self.profileid = data['profileid']
                    self.levelchallengeid = data['levelchallengeid']
                    if(self.levelchallengeid % 2 == 0) : #quantity matter
                        self.observer = AgilityDrillObserver(self.channel_name,self.levelchallengeid,data['programTime'])
                    else : #timematter
                        self.observer = AgilityDrillObserver(self.channel_name,self.levelchallengeid,data['fullHitsNumber'])
                else:
                    startOfProgramTime = datetime.fromisoformat(data['startOfProgramTime'])
                    self.observer.agilityDrill.startTime = startOfProgramTime
                    #self.observer.reactionDrill.generateNewGoal()
        elif isinstance(message.get('bytes'), bytes):
            frame = cv2.imdecode(np.frombuffer(message['bytes'], dtype=np.uint8), cv2.IMREAD_COLOR)
            frame = cv2.resize(frame,(720,480))
            frame = cv2.flip(frame , 1)    
            """cv2.circle(frame , (125,300), 10 , (255,0,0),-1)
            cv2.circle(frame , (605,300), 10 , (0,255,0),-1)
            cv2.imshow("frame" , frame)
            cv2.waitKey(1)"""
            just(frame, scheduler= self.pool_scheduler).subscribe(self.observer)
    


    async def force_close(self, event):
        if self.levelchallengeid % 2 == 0: #quantitymatter
            score = event['score']
        else:
            finishedTime = event["finishedTime"]
        program = await models.Program.objects.aget(id = self.programid)
        profile = await models.Profile.objects.aget(id = self.profileid)
        finishedProgram,created= await models.FinishedProgram.objects.aget_or_create(program = program, player = profile)
        if created:
            if self.levelchallengeid % 2 == 0:
                finishedProgram.highScoreQuantity = score
            else:
                finishedProgram.highScoreTime = finishedTime
            finishedProgram.highScoreDate = datetime.now()
            finishedProgram.lastTryDate = datetime.now()
            await finishedProgram.asave()
        else :
            finishedProgram.numberOfTries = finishedProgram.numberOfTries + 1
            finishedProgram.lastTryDate = datetime.now()
            if self.levelchallengeid % 2 != 0 :
                if finishedProgram.highScoreTime > finishedTime:
                    finishedProgram.highScoreTime = finishedTime
                    finishedProgram.highScoreDate = datetime.now()
            else:
                if finishedProgram.highScoreQuantity < score:
                    finishedProgram.highScoreQuantity = score
                    finishedProgram.highScoreDate = datetime.now()
            await finishedProgram.asave()
        if self.levelchallengeid % 2 == 0:
            await self.send(
                    text_data= json.dumps({
                        'state' : "Program is Finished",
                        'count' : score
                    }))
        else:
            await self.send(
                    text_data= json.dumps({
                        'state' : "Program is Finished",
                        'finishedTime' : finishedTime
                    }))
      
    async def is_hitted(self, event):
        if event['state'] == "Pose is not detected yet" or event['state'] == "Pose is Lost":
            await self.send(
                text_data= json.dumps({
                    'state' : event['state']
                })
            )
        elif event['state'] == 'Has To Go To Middle':
            await self.send(
                text_data=json.dumps({
                    'state' : event['state'],
                    'score' : event['score']
                })
            )
        elif event['state'] == 'Backed To Middle' or event['state'] == 'Pose is Detected For First Time' :
            await self.send(text_data= json.dumps({
            "state" : event['state'],
            "conePercent" : event['cone'],
            "score" : event['score'],
            }))
