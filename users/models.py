from django.contrib.auth.models import User
from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User , on_delete= models.CASCADE)
    firstName = models.CharField(max_length= 50 , blank= True , null= True)
    lastName = models.CharField(max_length= 50 , blank= True , null= True)
    email = models.EmailField(max_length= 500 , blank= True , null = True)
    username = models.CharField(max_length= 200 , blank= True, null = True)
    proffesional = models.BooleanField(default= False)
    height = models.IntegerField(null= True, blank= True)
    weight = models.IntegerField(null = True, blank = True)
    birthday = models.DateField(null = True, blank= True)
    currentClub = models.ForeignKey('Club', on_delete= models.SET_NULL, null= True , blank= True)
    bio = models.TextField(blank=True, null= True)
    profile_image = models.ImageField(null= True , blank= True , upload_to= 'profiles/' , default= 'profiles/image.jpg')
    social_facebook = models.CharField(max_length= 200 , blank= True , null= True)
    social_instagram = models.CharField(max_length= 200 , blank= True , null= True)
    social_youtube = models.CharField(max_length= 200 , blank= True , null= True)
    created = models.DateTimeField(auto_now_add= True)
    id = models.UUIDField(default = uuid.uuid4,unique = True, primary_key = True , editable = False)

    def __str__(self) -> str:
        return self.user.username


class Position(models.Model):

    number = models.PositiveIntegerField()
    name = models.CharField(max_length= 50)
    
    def __str__(self) -> str:
        return self.name


class PositionPlayer(models.Model):

    id = models.UUIDField(default = uuid.uuid4,unique = True, primary_key = True , editable = False)
    player = models.ForeignKey(Profile, on_delete= models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    description = models.TextField(null= True, blank = True)

    def __str__(self):
        return "{} {}".format(self.player.username, self.position.number)


class Club(models.Model):

    id = models.UUIDField(default = uuid.uuid4,unique = True, primary_key = True , editable = False)
    name = models.CharField(max_length= 200)
    location = models.CharField(max_length= 500,)

    def __str__(self) -> str:
        return self.name


class PreviousClub(models.Model):

    id = models.UUIDField(default = uuid.uuid4,unique = True, primary_key = True , editable = False)
    player = models.ForeignKey(Profile, on_delete= models.CASCADE)
    club = models.ForeignKey(Club,on_delete= models.CASCADE)
    joinDate = models.DateField()
    endDate = models.DateField()
    def __str__(self) -> str:
        return "{} : {} ".format(self.player, self.club)

