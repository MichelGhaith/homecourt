from django.contrib import admin

# Register your models here.

from .models import Level,Challenge,Drill,LevelChallenge,Program,DrillExercise,FinishedProgram

admin.site.register(Level)
admin.site.register(Challenge)
admin.site.register(Drill)
admin.site.register(LevelChallenge)
admin.site.register(Program)
admin.site.register(DrillExercise)
admin.site.register(FinishedProgram)