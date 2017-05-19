from django.db import models
from django.utils.encoding import python_2_unicode_compatible
import datetime
from django.utils import timezone
from django import forms
import re
from django.forms import ModelForm
from django.http import HttpResponseRedirect, Http404


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
    your_name = forms.CharField(label='кол-во вариантов', max_length=100, required=True)
    fieldn = forms.CharField(label='кол-во заданий в варианте', max_length=100, required=True)
class AnotherForm(forms.Form):
    field = forms.CharField(label='', max_length=100, required=False)
    # ModelMultipleChoiceField(**kwargs)






class ExcersiseTemplate(models.Model):
    text = models.TextField (max_length=1000)
    name = models.CharField (max_length=200)
    correctAnswer = models.CharField (max_length=200)
    type = models.CharField (max_length=200)
    grade = models.IntegerField ()
    subject = models.CharField (max_length=200, default = "Null")

    def get_subs(self):
         return re.findall(r'{{\s*([a-z]+)(\d+)\s*}}', self.text)

    def get_answer(self):
         return re.findall(r'{{\s*([a-z]+)(\d+)\s*}}', self.correctAnswer)

    def __str__(self):
        return self.name

class TemplateForm(ModelForm):
    class Meta:
        model = ExcersiseTemplate
        fields = ['text', 'name', 'correctAnswer', 'type', 'grade', 'subject']

class ChoiseForm(forms.Form):
    field = forms.ModelChoiceField(queryset=ExcersiseTemplate.objects.all(), empty_label="Случайная задача", required=False)

class Replacers(models.Model):
    type = models.CharField (max_length=200)
    value = models.CharField (max_length=200)
    def __str__(self):
        return self.type

# перенесена функция получения сгенерированного варианта из отдельных страниц во views, чтобы не прописывать для каждой страницы
def templates(filter):
        if filter != '':
            template = ExcersiseTemplate.objects.filter(name=filter).order_by('?').first()
        else:
            template = ExcersiseTemplate.objects.order_by('?').first()
        subs = template.get_subs()
        answer = template.get_answer ()
        temp_text=template.text
        temp_answer = template.correctAnswer
        for name, number in subs:
            replacer = Replacers.objects.filter(type=name).order_by("?").first().value
            temp_text = temp_text.replace("{{"+name+number+"}}", replacer)
            # print (temp_text)
            # print(name,  number, replacer)
            for nameAns, numberAns in answer:
                if name == nameAns and number == numberAns:
                    temp_answer = temp_answer.replace ("{{"+nameAns+numberAns+"}}", replacer)

    #temp_answer = eval(temp_answer)
        temp_answer = float("{0:.2f}".format(eval(temp_answer)))

        temp_name = template.name
        return temp_text, temp_answer, temp_name

