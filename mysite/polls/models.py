# !/usr/bin/python
# -*- coding: utf-8 -*-

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4, letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


from reportlab.platypus import Paragraph,SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
import reportlab.rl_config
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont



from django.db import models
from django.utils.encoding import python_2_unicode_compatible
import datetime
from django.utils import timezone
from django import forms
import re
from django.forms import ModelForm
from django.http import HttpResponseRedirect, Http404, HttpResponse
from reportlab.pdfgen import canvas





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
    your_name = forms.CharField(label='Кол-во вариантов', max_length=100, required=True)
    fieldn = forms.CharField(label='Кол-во заданий в варианте', max_length=100, required=True)
class AnotherForm(forms.Form):
    field = forms.CharField(label='Ответ',max_length=100, required=False)
    # ModelMultipleChoiceField(**kwargs)

class SavedPrimer(models.Model):
    user = models.CharField(max_length=200)
    idNumber = models.CharField(max_length=200)
    value = models.CharField(max_length=200)




class ExcersiseTemplate(models.Model):
    text = models.TextField ( max_length=1000)
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