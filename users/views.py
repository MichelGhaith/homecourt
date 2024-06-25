from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import Profile,PreviousClub,PositionPlayer,Club,Position
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from . import serializers
from django.core.serializers import serialize
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.

"""class BB(ModelViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = None
    serializer_class = ProfileSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)()
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)"""


def loginUser(request):
    if request.user.is_authenticated :
        return HttpResponse(
            'already login'
        )
    if request.method == 'POST':    
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username = username)
        except :
            return Response('User is not found')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user = user)
            return HttpResponse('is authenticate')
        else:
            return HttpResponse('username or password is incorrect')
        

def logoutUser(request):
    logout(request)
    #redirect('login')

@api_view(['GET'])
def profiles(request):
    profiles = Profile.objects.all()
    serializer = serializers.ProfileSerializer(profiles , many = True)
    return Response(serializer.data)
    #data = serialize("json", profiles)
    #return HttpResponse(data , content_type = 'application/json')
    
@api_view(['GET'])
def profile(request, pk):
    profile = Profile.objects.get(id = pk)
    serializer = serializers.ProfileSerializer(profile,many = False)
    return Response(serializer.data)
    """mmken jib ldata ili bdi iaha mslan
    previousClubs = PreviousClub.objects.filter(player = profile)
    positions = PositionPlayer.objects.filter(player = profile)
    context={
    'profile': profile,
    'previousClubs': previousClubs,
    'positions' : positions
    }
     
    """

@api_view(['GET'])
def previousClubsForUser(request, pk):
    previousClubs = PreviousClub.objects.filter(player = pk)
    serializer = serializers.PreviousClubSerializer(previousClubs,many = True)
    return Response(serializer.data)

@api_view(['GET'])
def playerPositions(request, pk):
    positions = PositionPlayer.objects.filter(player = pk)
    serializer = serializers.PositionPlayerSerializer(positions,many = True)
    return Response(serializer.data)

@api_view(['GET'])
@login_required(login_url="login")
def userAccount(request):
    profile = request.user.profile
    serializer = serializers.ProfileSerializer(profile, many = False)
    return Response(serializer.data)
    #same as profile


@api_view(['GET'])
def club(request,pk):
    club = Club.objects.get(id = pk)
    serializer = serializers.ClubSerializer(club, many = False)
    return Response(serializer.data)

@api_view(['GET'])
def usersByClub(request , pk):
    profiles = Profile.objects.filter(currentClub = pk)
    serialize = serializers.ProfileSerializer(profiles , many = True)
    return Response(serialize.data)

@api_view(['GET'])
def clubs(request):
    clubs = Club.objects.all()
    serializer = serializers.ClubSerializer(clubs, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def positions(request):
    allpositions = Position.objects.all()
    serializer = serializers.PositionSerializer(allpositions,many = True)
    return Response(serializer.data)

@api_view(['PUT'])
@login_required()
def editAccount(request):
    data = request.data
    profile = request.user.Profile
    profile.firstName = data['firstName']
    profile.lastName = data['lastName']
    profile.email = data['email']
    profile.username = data['username']
    profile.proffesional = data['proffesional']
    profile.height = data['height']
    profile.weight = data['weight']
    #profile.birthday = data['birthday']
    profile.bio = data['bio']
    #profile.profile_image = data['profile_image']
    profile.social_facebook = data['social_facebook']
    profile.social_instagram = data['social_instagram']
    profile.social_youtube = data['social_youtube']
    profile.currentClub = data['currentClub']
    profile.save()
    serializer = serializers.ProfileSerializer(profile,many = False)
    return Response(serializer.data)