from django.urls import path
from . import views

urlpatterns = [
    path("programexercises/<str:pk>/" , views.programexercises.as_view() , name = "programexercises"),
    path("programs/" , views.programs, name= "programs"),
    path("program=<str:pk>/" , views.program , name ="program"),
    path('lv=<str:pk>/programs/',views.levelchallengeprograms, name= "levelchallengeprograms"),
    path('lv=<str:levelchallengeid>/andtype=<str:programtype>/programs/', views.programsforspecifictypeandspecificlevelchallenge, name="specifictypeandlevelchallenge"),
    path("pl=<str:pk>/finishedprograms/" , views.finishedprogramsforspecificplayer, name= "finishedforaplayer"),
    path('level/<str:pk>/', views.level, name= "level"),
    path('challenge/<str:pk>/', views.challenge, name="challenge"),
    path('highscores/program=<str:pk>/' , views.highscoresforspecificprogram, name= "programhighscores"),
    path('drills/', views.drills , name = 'drills'),
    path('levels/' , views.levels , name ='levels'),
    path('challenges/' , views.challenges , name ="challenges"),
    path('levelchallenges/' , views.levelchallenges , name = "levelchallenge")
]