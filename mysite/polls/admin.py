from django.contrib import admin
from django.contrib.auth.models import Group
# Register your models here.
from .models import Replacers, ExcersiseTemplate, SavedPrimer, Exercise, TrainingApparatus, ExerciseTypes, TrainingTest

admin.site.site_header = 'Тренажер СИТШ'
admin.site.register(Exercise)
#admin.site.register(ExcersiseTemplate)
#admin.site.register(Replacers)
#admin.site.register(SavedPrimer)
admin.site.register(ExerciseTypes)
admin.site.register(TrainingApparatus)
admin.site.register(TrainingTest)


