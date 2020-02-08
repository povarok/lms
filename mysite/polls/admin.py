from django.contrib import admin

# Register your models here.
from .models import Replacers, ExcersiseTemplate, SavedPrimer, Exercise, TrainingApparatus, ExerciseTypes, TrainingTest

admin.site.register(Exercise)
#admin.site.register(ExcersiseTemplate)
#admin.site.register(Replacers)
#admin.site.register(SavedPrimer)
admin.site.register(ExerciseTypes)
admin.site.register(TrainingApparatus)
admin.site.register(TrainingTest)

