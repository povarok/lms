# !/usr/bin/python
# -*- coding: utf-8 -*-

from reportlab.lib.pagesizes import A4, letter
from django.contrib.postgres.fields import JSONField
from reportlab.platypus import Paragraph,SimpleDocTemplate
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.contrib.auth.models import User
from .helper import *

from django.db import models
from django import forms
import re
from django.forms import ModelForm
from django.http import HttpResponseRedirect, Http404, HttpResponse





# Create your models here.
class ExerciseTypes(models.Model):
    name = models.CharField(verbose_name="Тип примера", max_length=200)
    description = models.TextField(verbose_name="Описание", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'тип упражнения'
        verbose_name_plural = u'типы упражнения'

class Grades(models.Model):
    perfect = models.PositiveIntegerField(verbose_name="Отлично")
    good = models.PositiveIntegerField(verbose_name="Хорошо")
    satisfactory = models.PositiveIntegerField(verbose_name="Удовлетворительно")

    def __str__(self):
        return self.name
    class Meta:
        abstract = True

class TrainingApparatus(Grades):
    name = models.CharField(verbose_name=u"Название тренажера", max_length=200)
    description = models.TextField(verbose_name="Описание", max_length=1000, blank=True, null=True)
    exercises_type = models.ForeignKey(ExerciseTypes, verbose_name=u"Тип(ы) примеров", on_delete=models.SET_DEFAULT,
                                       default=None, blank=True, null=True, help_text=u"В РАЗРАБОТКЕ")
    exercises_amount = models.PositiveIntegerField(verbose_name=u"Количество примеров", default=0)
    allotted_time = models.CharField(verbose_name=u"Время на выполнение", max_length=9, default="00:00:00", help_text=u'Формат - "00:00:00"')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'тренажер'
        verbose_name_plural = u'тренажеры'

class TrainingTest(models.Model):
    apparatus = models.ForeignKey(TrainingApparatus, verbose_name=u"Тип тренажера", on_delete=models.SET_DEFAULT,
                                  default=None, blank=True, null=True)
    user = models.ForeignKey(User, verbose_name=u"Пользователь", on_delete=models.CASCADE, default=None, blank=True, null=True)
    grade = models.PositiveIntegerField(verbose_name=u"Оценка")
    solved_exercises = models.PositiveIntegerField(verbose_name=u"Количество решенных примеров", default=0)
    correct_answers = models.PositiveIntegerField(verbose_name=u"Количество верных ответов", default=0)
    time_start = models.DateTimeField(verbose_name=u"Время начала тестирования", auto_now=False, auto_now_add=True, blank=True, null=True)
    time_spent = models.CharField(verbose_name=u"Потраченное время на решение", max_length=10, blank=True, null=True)

    def __str__(self):
        return self.apparatus.name + ' - ' + str(self.pk) + ', ' + str(self.user)

    class Meta:
        verbose_name = u'выполненный тест'
        verbose_name_plural = u'выполненные тесты'

class Exercise(models.Model):
    type = models.ForeignKey(ExerciseTypes, verbose_name=u"Тип упражнения", on_delete=models.CASCADE, default=None, blank=True, null=True)
    test = models.ForeignKey(TrainingTest, verbose_name=u"Тест", related_name="exercises", on_delete=models.CASCADE, default=None, blank=True, null=True)
    time_spent = models.CharField(verbose_name=u"Потраченное время на решение", blank=True, null=True, max_length=12)
    correct_answer = models.CharField(verbose_name=u"Верный ответ", max_length=200)
    given_answer = models.CharField(verbose_name=u"Данный пользователем ответ", max_length=200)
    answer_is_correct = models.BooleanField(verbose_name=u"Проверка ответа")
    text = models.TextField(verbose_name=u"Текст упражнения", max_length=1000)
    exercise_index = models.PositiveIntegerField(verbose_name=u"Номер упражнения в тесте", default=0)

    def __str__(self):
        return self.text + ', ' + self.test.apparatus.name + ' - ' + str(self.test.pk)

    def get_spent_timestamp(self):
        print(str(self.time_spent))
        return get_seconds_from_string(str(self.time_spent))

    class Meta:
        verbose_name = u'упражнение'
        verbose_name_plural = u'упражнения'



    















class NameForm(forms.Form):
    your_name = forms.CharField(label='Кол-во вариантов', max_length=100, required=True)
    fieldn = forms.CharField(label='Кол-во заданий в варианте', max_length=100, required=True)
class AnotherForm(forms.Form):
    field = forms.CharField(label='Ответ', max_length=100, required=False)
    # ModelMultipleChoiceField(**kwargs)

class SavedPrimer(models.Model):
    user = models.CharField(max_length=200)
    idNumber = models.CharField(max_length=200)
    value = models.CharField(max_length=200)


class ExcersiseTemplate(models.Model):
    text = models.TextField(max_length=1000)
    name = models.CharField(max_length=200)
    correctAnswer = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    grade = models.IntegerField()
    subject = models.CharField(max_length=200, default="Null")

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

# def makePdf(request, text):
#     # Create the HttpResponse object with the appropriate PDF headers.
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
#
#     # Create the PDF object, using the response object as its "file."
#     p = canvas.Canvas(response, pagesize=letter)
#     width, height = letter
#
#     pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))
#     p.setFont('FreeSans', 12)
#     # Draw things on the PDF. Here's where the PDF generation happens.
#     # See the ReportLab documentation for the full list of functionality.
#     for i in range(0,len(text)):
#         p.drawString(0, 600-100*i, str(text[i]))
#
#     # Close the PDF object cleanly, and we're done.
#     p.showPage()
#     p.save()
#     print ('вывел пдф')
#     return response


def makeNicePdf(request, text):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="exercise.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = SimpleDocTemplate(response,pagesize = A4,title='Тест документа',author='CAV Inc')
    width, height = letter

    pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))

    p.build(text)




    print ('вывел пдф')
    return response