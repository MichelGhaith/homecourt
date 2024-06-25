from django.db import models
import uuid
from users.models import Profile

# Create your models here.

class Level(models.Model):
    
    name = models.CharField(max_length= 50,null= False , blank= False)

    def __str__(self):
        return self.name


class Challenge(models.Model):
    
    Challenge_Type = (
        ('TimeMatter', 'Time Matter'),
        ('QuantityMatter', 'Quantity Matter'),
    )
    type = models.TextField(max_length= 50 , choices= Challenge_Type)
    
    def __str__(self):
        return self.type


class LevelChallenge(models.Model):
    #1 Easy TimeMatter
    #2 Easy QuantityMatter
    #3 Medium TimeMatter
    #4 Medium QuantityMatter
    #5 Hard TimeMatter
    #6 Hard QuantityMatter
    level = models.ForeignKey(Level, on_delete= models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete= models.CASCADE)
    
    def __str__(self):
        return "{} - {}".format(self.level,self.challenge)
    

class Drill(models.Model):

    name = models.CharField(max_length= 50)

    def __str__(self) -> str:
        return self.name


class Program(models.Model):
    Program_Type = (
        ('Reaction' , 'Reaction'),
        ('BallHandling' , 'BallHandling'),
        ('Agility' , 'Agility')
    )
    levelchallenge = models.ForeignKey(LevelChallenge, on_delete= models.CASCADE)
    owner = models.ForeignKey(Profile, on_delete= models.CASCADE)
    created = models.DateTimeField(auto_now_add= True)
    id = models.UUIDField(default = uuid.uuid4,unique = True, primary_key = True , editable = False)
    type = models.TextField(max_length= 50 , choices= Program_Type)
    def __str__(self) -> str:
        return "owner by : {} levelchallenge : {} type: {}".format(self.owner,self.levelchallenge,self.type)

    


class DrillExercise(models.Model):

    id = models.UUIDField(default = uuid.uuid4,unique = True, primary_key = True , editable = False)
    program = models.ForeignKey(Program, on_delete= models.CASCADE)
    drill = models.ForeignKey(Drill, on_delete= models.CASCADE)
    repetition = models.PositiveIntegerField(default= 0, null = True , blank= True, )
    endTime = models.PositiveIntegerField(default= 0, null= True, blank= True )
    numberOfDrill = models.PositiveIntegerField(default= 1)

    def __str__(self) -> str:
        return "{} : {}".format(self.drill,self.repetition)
    
    class Meta:
        ordering = ['numberOfDrill']


class FinishedProgram(models.Model):

    id = models.UUIDField(default = uuid.uuid4,unique = True, primary_key = True , editable = False)
    program = models.ForeignKey(Program,on_delete= models.CASCADE)
    player = models.ForeignKey(Profile, on_delete= models.CASCADE)
    numberOfTries = models.IntegerField(default= 1)
    highScoreQuantity = models.IntegerField(null= True , blank= True)
    highScoreTime = models.IntegerField(null= True, blank= True)
    highScoreDate = models.DateTimeField(null = True,blank= True)
    lastTryDate = models.DateTimeField(auto_now= True)
    #uploaded video