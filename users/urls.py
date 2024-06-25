from django.urls import path
from . import views

urlpatterns = [
    path("", views.profiles, name= "profiles"),
    path('profile=<str:pk>/editprofile/' , views.editAccount , name = "editprofile"),
    path("profile=<str:pk>/" , views.profile, name= "profile"),
    path('useraccount/' , views.userAccount , name= "useraccount"),
    path('previousclubsfor=<str:pk>/' , views.previousClubsForUser , name= "previousclubs" ),
    path('positionsof=<str:pk>/', views.playerPositions, name ="playerpositions"),
    path("clubs/" , views.clubs, name = 'clubs'),
    path("club=<str:pk>/", views.club, name = "club"),
    path("usersbyclub=<str:pk>/" , views.usersByClub , name ="usersbyclub"),
    path('positions/', views.positions , name="positions"),
    path('login/' , views.loginUser, name ="login"),
    
]
