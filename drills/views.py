from .models import Program ,Drill, DrillExercise , FinishedProgram , LevelChallenge , Challenge , Level
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProgramSerializer,ChallengeSerializer,LevelSerializer,DrillSerializer,DrillExcerciseSerializer,FinishedProgramSerializer , LevelChallengeSerializer
from django.http import HttpResponse
from django.core.serializers import serialize
from rest_framework.views import APIView
# Create your views here.
@api_view(['GET'])
def programs(request):
    programs = Program.objects.all()
    serializer = ProgramSerializer(programs, many = True)
    return Response(serializer.data)

class b1(APIView):
    def get(self,req,*args,**kw):
        pass
    def podt(self,req,*args,**ks):
        pass

# @api_view(['GET'])
class programexercises(APIView):
    def get(self,req,*args,**kw):
    # def programexercises(request,pk):
        pk = kw["pk"]
        exercises = DrillExercise.objects.filter(program = pk)
        serializer = DrillExcerciseSerializer(exercises, many =True)
        return Response(serializer.data)

@api_view(['GET'])
def program(request,pk):
    program = Program.objects.get(id = pk)
    serializer = ProgramSerializer(program, many = False)
    return Response(serializer.data)

@api_view(['GET'])
def levelchallengeprograms(request,pk):
    #pk = 1 easy timematter
    #pk =  2 easy quantitymatter
    #pk = 3 medium timematter
    #pk = 4 medium quantitymatter
    #pk = 5 hard timematter
    #pk = 6 hard quantity matter
    programs = Program.objects.filter(levelchallenge = pk)
    serializer = ProgramSerializer(programs, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def programsforspecifictypeandspecificlevelchallenge(request,programtype,levelchallengeid):
    programs = Program.objects.filter(levelchallenge = levelchallengeid,type = programtype)
    serializer = ProgramSerializer(programs, many = True)
    return Response(serializer.data)
#lazem order by date
@api_view(['GET'])
def finishedprogramsforspecificplayer(request,pk):
    finishedPrograms = FinishedProgram.objects.filter(player=pk)
    serializer = FinishedProgramSerializer(finishedPrograms, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def levelchallenges(request):
    levelchallenges = LevelChallenge.objects.all()
    serializer = LevelChallengeSerializer(levelchallenges, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def drills(request):
    drills = Drill.objects.all()
    serializer = DrillSerializer(drills, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def levels(request):
    levels = Level.objects.all()
    serializer = LevelSerializer(levels, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def challenges(request):
    challenges = Challenge.objects.all()
    serializer = ChallengeSerializer(challenges, many = True)
    return Response(serializer.data)

def level(request,pk):
    level = Level.objects.get(id = pk)
    return HttpResponse(level.name)

def challenge(request,pk):
    challenge = Challenge.objects.get(id = pk)
    return HttpResponse(challenge.type)



#not tried yet
def highscoresforspecificprogram(request,pk):
    print('1')
    program = Program.objects.get(id = pk)
    print('2')
    levelchallengeId = program.levelchallenge
    print(levelchallengeId)
    print('3')
    levelchallenge = LevelChallenge.objects.get(id = levelchallengeId)
    print('4')
    challengeId = levelchallenge.challenge
    print('5')
    challenge = Challenge.objects.get(id = challengeId)
    print('6')
    if challenge.type == 'TimeMatter':
        orderbyValue = 'HighScoreQuantity'
        print('7')
    else:
        orderbyValue = 'HighScoreTime'
        print('7')
    finishedprograms= FinishedProgram.objects.filter(program= pk).order_by(orderbyValue)
    print('8')
    serializer = FinishedProgramSerializer(finishedprograms,many = True)
    return Response(serializer.data)
    #return HttpResponse("finished ones for specific program")
