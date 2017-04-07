from django.contrib import admin
from .models import Teplate

@admin.register(Teplate)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('text', 'hidden')
