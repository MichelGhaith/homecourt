import reactivex as rx
import sys
sys.path.insert(1, 'D:/graduationproject/backendpart/homecourt/')
from visioncore.ballhandlingdrill import BallHandlingDrill
from visioncore.reactiondrill import ReactionDrill
from visioncore.agilitydrill import AgilityDrill
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from datetime import datetime

class BallHandlingObserver(rx.Subject):
    def __init__(self,channel_name,levelchallenge,informations) -> None:
        self.channel_name = channel_name
        self.channel_layer = get_channel_layer()
        self.ballHandlingDrill = BallHandlingDrill(levelchallenge=levelchallenge,informations=informations)

    
    def on_next(self, frame):
        #"Program is Finished" "Pose is Detected For First Time" "Pose is not detected yet" "Ball Not Found" "Human pose is not detected yet" "Ball direction is unknown"
        #"the ball is not hitting the ground" "Hand under the ball" "not finished yet" True False
        #mmken hon 2za kan is finished 2b3at ltime mshan sajlo
        state = self.ballHandlingDrill.process(frame)
        print(state)
        if state == "Pose is not detected yet" or state == "Pose is Lost":
            async_to_sync(self.channel_layer.send)(self.channel_name,{
                    "type":"dribble.evaluation",
                    "state" : state,
            })
        elif state == "not finished yet":
            return
        elif(state == "Program is Finished"):
            if self.ballHandlingDrill.levelchallenge % 2 == 0:
                count = self.ballHandlingDrill.dribblecount
                self.ballHandlingDrill.resetProgram()
                async_to_sync(self.channel_layer.send)(self.channel_name,{
                        "type":"force.close",
                        "count" : count
                    })
                
            else :
                finishedTime = (datetime.now() - self.ballHandlingDrill.startTimeOfProgram).seconds
                self.ballHandlingDrill.resetProgram()
                async_to_sync(self.channel_layer.send)(self.channel_name,{
                        "type":"force.close",
                            "finishedTime" : finishedTime
                        })
        else :

            if self.ballHandlingDrill.levelchallenge % 2 == 0:

                async_to_sync(self.channel_layer.send)(self.channel_name,{
                    "type":"dribble.evaluation",
                    "state": state,
                    "dribblecount" : self.ballHandlingDrill.dribblecount,
                    'drill' : self.ballHandlingDrill.drill
                    })
            else:   
                count = self.ballHandlingDrill.program[0]['repetition']
                drill = self.ballHandlingDrill.program[0]['excercise']
                async_to_sync(self.channel_layer.send)(self.channel_name,{
                    "type":"dribble.evaluation",
                    "state": state,
                    "count" : count,
                    'drill' : drill
                })


class ReactionDrillObserver(rx.Subject):
    def __init__(self,channel_name,levelchallengeid,data) -> None:
        self.channel_name = channel_name
        self.channel_layer = get_channel_layer()
        self.reactionDrill = ReactionDrill(levelchallenge=levelchallengeid,data = data)
    
    def on_next(self, frame):
        state = self.reactionDrill.process(frame)
        levelchallenge = self.reactionDrill.levelchallenge
        if state == "Pose is not detected yet" or state == "Pose is Lost":
            async_to_sync(self.channel_layer.send)(self.channel_name,{
                    "type":"is.hitted",
                    "state" : state,
            })
        
        elif state == "nothing":
            return
        elif state == "Program is Finished":
            if levelchallenge % 2 == 0:
                score = self.reactionDrill.score
                self.reactionDrill.resetProgram()
                async_to_sync(self.channel_layer.send)(self.channel_name,{
                            "type":"force.close",
                             "score" : score
                    })
            else:
                finishedTime = (datetime.now()- self.reactionDrill.startTime).seconds
                self.reactionDrill.resetProgram()
                async_to_sync(self.channel_layer.send)(self.channel_name,{
                            "type":"force.close",
                             "finishedTime" : finishedTime})
        else:
            right = 0
            wrong = 0
            if self.reactionDrill.rightwa7edimin != None:
                rightone = self.reactionDrill.rightwa7edimin
                right = right + 1
            if self.reactionDrill.rightwa7edisar != None:
                rightone = self.reactionDrill.rightwa7edisar
                right = right + 1
            if self.reactionDrill.righttnenimin != None :
                righttwo = self.reactionDrill.righttnenimin
                right = right + 1
            if self.reactionDrill.righttnenisar != None :
                righttwo = self.reactionDrill.righttnenisar
                right = right + 1
            if self.reactionDrill.wrongimin != None :
                wrongone = self.reactionDrill.wrongimin
                wrong = wrong + 1
            if self.reactionDrill.wrongisar != None:
                wrongone = self.reactionDrill.wrongisar
                wrong = wrong + 1
            if right == 2:
                async_to_sync(self.channel_layer.send)(self.channel_name,{
                        "type":"is.hitted",
                        "state" : state,
                        "numberOfRightGoals" : right,
                        "numberOfWrongGoals" : wrong,
                        'rightone' : rightone,
                        'righttwo' : righttwo,
                        "score" : self.reactionDrill.score,
                        })
            elif right == 1 and wrong == 1 :
                async_to_sync(self.channel_layer.send)(self.channel_name,{
                        "type":"is.hitted",
                        "state" : state,
                        "numberOfRightGoals" : right,
                        "numberOfWrongGoals" : wrong,
                        'rightone' : rightone,
                        'wrong' : wrongone,
                        "score" : self.reactionDrill.score
                        })
            elif right == 1 and wrong == 0:
                async_to_sync(self.channel_layer.send)(self.channel_name,{
                        "type":"is.hitted",
                        "state" : state,
                        "numberOfRightGoals" : right,
                        "numberOfWrongGoals" : wrong,
                        'rightone' : rightone,
                        "score" : self.reactionDrill.score
                        })
         

class AgilityDrillObserver(rx.Subject):
    def __init__(self,channel_name,levelchallengeid,data) -> None:
        self.channel_name = channel_name
        self.channel_layer = get_channel_layer()
        self.agilityDrill = AgilityDrill(levelchallenge=levelchallengeid,data = data)
    
    def on_next(self, frame):
        state = self.agilityDrill.process(frame)
        levelchallenge = self.agilityDrill.levelchallenge
        if state == "Pose is not detected yet" or state == "Pose is Lost":
            async_to_sync(self.channel_layer.send)(self.channel_name,{
                    "type":"is.hitted",
                    "state" : state,})
        elif state == "nothing":
            return
        elif state == "Program is Finished":
            if levelchallenge % 2 == 0:
                numberOfHits = self.agilityDrill.numberOfHits
                self.agilityDrill.resetProgram()
                async_to_sync(self.channel_layer.send)(self.channel_name,{
                            "type":"force.close",
                             "score" : numberOfHits
                    })
            else:
                finishedTime = (datetime.now()- self.agilityDrill.startTime).seconds
                self.agilityDrill.resetProgram()
                async_to_sync(self.channel_layer.send)(self.channel_name,{
                            "type":"force.close",
                             "finishedTime" : finishedTime
                    })
        elif state == "Has To Go To Middle":
                async_to_sync(self.channel_layer.send)(self.channel_name,{
                        "type":"is.hitted",
                        "state" : state,
                        "score" : self.agilityDrill.numberOfHits,
                        })
        elif state == "Backed To Middle" or state == "Pose is Detected For First Time" :
            if self.agilityDrill.leftCone != None:
                async_to_sync(self.channel_layer.send)(self.channel_name,{
                    "type":"is.hitted",
                    "state" : state,
                    "cone" : self.agilityDrill.leftCone,
                    'score' : self.agilityDrill.numberOfHits})
            elif self.agilityDrill.rightCone != None:
                async_to_sync(self.channel_layer.send)(self.channel_name,{
                    "type":"is.hitted",
                    "state" : state,
                    "cone" : self.agilityDrill.rightCone,
                    'score' : self.agilityDrill.numberOfHits})

            
         