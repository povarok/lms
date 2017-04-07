from django.db import models

# Create your models here.

class Teplate(models.Model):
    text = models.TextField()
    hidden = models.BooleanField(default=False)
