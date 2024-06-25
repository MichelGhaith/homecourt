from django.contrib import admin
from .models import Profile,Position,PositionPlayer,Club,PreviousClub
# Register your models here.

admin.site.register(Profile)
admin.site.register(Position)
admin.site.register(PositionPlayer)
admin.site.register(Club)
admin.site.register(PreviousClub)