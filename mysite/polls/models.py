from django.db import models
from django.utils.encoding import python_2_unicode_compatible
import datetime
from django.utils import timezone
from django import forms


# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
    

class Primer (models.Model):
    sl = models.CharField(max_length=200)
    sll = models.CharField(max_length=200)
    summ = models.CharField(max_length=200)
    znak = models.CharField(max_length=200)

class NameForm(forms.Form):
    your_name = forms.CharField(label='Answer', max_length=100)

class ExcersiseTemplate(models.Model):
    text = models.TextField (max_length=1000)
    name = models.CharField (max_length=200)
    correctAnswer = models.CharField (max_length=200)
    type = models.CharField (max_length=200)
    grade = models.IntegerField ()

class Replacers(models.Model):
    type = models.CharField (max_length=200)
    value = models.CharField (max_length=200)




