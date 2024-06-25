from rest_framework.serializers import ModelSerializer
from . import models
from django.contrib.auth.models import User

class ProfileSerializer(ModelSerializer):
    class Meta:
        model = models.Profile
        fields = '__all__'

class PreviousClubSerializer(ModelSerializer):
    class Meta:
        model = models.PreviousClub
        fields = '__all__'

class PositionPlayerSerializer(ModelSerializer):
    class Meta:
        model = models.PositionPlayer
        fields = '__all__'

class ClubSerializer(ModelSerializer):
    class Meta:
        model = models.Club
        fields = '__all__'

class PositionSerializer(ModelSerializer):
    class Meta:
        model = models.Position
        fields = '__all__'

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username' , 'password']