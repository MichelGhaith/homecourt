from rest_framework.serializers import ModelSerializer
from .models import Program,Level,Challenge,Drill,DrillExercise,FinishedProgram,LevelChallenge

class ProgramSerializer(ModelSerializer):
    class Meta:
        model = Program
        fields = '__all__'

class DrillExcerciseSerializer(ModelSerializer):
    class Meta:
        model = DrillExercise
        fields = ['drill' , 'repetition' , 'endTime']

class FinishedProgramSerializer(ModelSerializer):
    class Meta:
        model = FinishedProgram
        fields = '__all__'

class LevelChallengeSerializer(ModelSerializer):
    class Meta:
        model = LevelChallenge
        fields = '__all__'

class DrillSerializer(ModelSerializer):
    class Meta:
        model = Drill
        fields = '__all__'

class LevelSerializer(ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'

class ChallengeSerializer(ModelSerializer):
    class Meta:
        model = Challenge
        fields = '__all__'