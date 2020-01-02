from django.contrib import admin

# Register your models here.
from .models import Question, Replacers, ExcersiseTemplate, SavedPrimer, Exercise

admin.site.register(Question)
admin.site.register(Exercise)
admin.site.register(ExcersiseTemplate)
admin.site.register(Replacers)
admin.site.register(SavedPrimer)
