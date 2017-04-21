from django.contrib import admin

# Register your models here.
from .models import Question, Primer, Replacers, ExcersiseTemplate

admin.site.register(Question)
admin.site.register(Primer)
admin.site.register(ExcersiseTemplate)
admin.site.register(Replacers)
