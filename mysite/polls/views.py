from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from random import randint
from django.contrib.auth.decorators import login_required
#from polls.models import ExcersiseTemplate, Replacers, NameForm, templates, AnotherForm, ChoiseForm, Primer, TemplateForm, SavedPrimer,  makeNicePdf
from .models import Exercise, NameForm, TrainingTest, TrainingApparatus
from django.contrib.auth.models import User
from polls.models import ExcersiseTemplate, Replacers, NameForm, templates, AnotherForm, ChoiseForm, Exercise, TemplateForm, SavedPrimer,  makeNicePdf
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.views.generic.base import View
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
import datetime





@login_required
def index(request):
    # teacher_check = request.user.groups.filter(name='Учитель').exists()
    # context = {
    #     'teacher_check': teacher_check
    # }
    return render(request, 'mysite/lms.html')


@login_required
def home(request):
    teacher_check = request.user.groups.filter(name='Учитель').exists()
    numberOfTemplatesUser = 0
    stroka = []
    check = ''

    x = templates(check)
    if request.method == 'POST':
        numberOfTemplates = NameForm(request.POST)
        if numberOfTemplates.is_valid():
            numberOfTemplatesUser = numberOfTemplates.cleaned_data['your_name']
            stroka = []
            for i in range(int(numberOfTemplatesUser)):
                y = templates()
                stroka.append('Название задачи:\n' + str(y[2])+'\n \n' + 'Задача:\n' + str(y[0])+'\n \n' + 'Ответ:\n'+str(y[1])+'\n')
                print(stroka)
    else:
        numberOfTemplates = NameForm()

    context = {
        'teacher_check': teacher_check,
        'groups': request.user.groups.all(),
        'text': x[0],
        'answer': x[1],
        'name': x[2],
        'number': numberOfTemplates,
        'numberUser': numberOfTemplatesUser,
        'stroka': stroka
    }

    return render(request, 'mysite/home.html', context)


def exercise_view(request):
    return render(request, 'polls/primer.html')


def create_test(request):
    apparatus = TrainingApparatus.objects.last()
    user = User.objects.get(pk=request.user.id)
    test = TrainingTest(apparatus=apparatus, user=user, grade=0)
    test.save()
    unsolved_exercises = []
    for i in range(1, apparatus.exercises_amount+1):
        ch = (randint(2, 9))
        chh = (randint(11-ch, 9))
        znak = '+'
        result = ch+chh
        excess_value = result - 10
        exercise_index = i
        correct_answer = (str(ch-(ch-excess_value)) + '+' + str(ch-excess_value)).replace("'", '')
        unsolved_exercise = Exercise(test_id=test, type=apparatus.exercises_type, time_spent=None, correct_answer=correct_answer,
                                     given_answer='', answer_is_correct=False, text=str(ch) + str(znak) + str(chh),
                                     exercise_index=exercise_index)
        unsolved_exercise.save()
        unsolved_exercises.append(unsolved_exercise.pk)
    return JsonResponse({
        'status': 'ok'
    })


def get_exercise(request):
    apparatus = TrainingApparatus.objects.last()
    test = TrainingTest.objects.filter(user_id=request.user.id).last()
    exercise_index = test.solved_exercises + 1
    if exercise_index <= apparatus.exercises_amount:
        unsolved_exercise = Exercise.objects.filter(test_id=test, exercise_index=exercise_index)[0]
    else:
        return JsonResponse({
            "url": "/end_test/"
        })
    return JsonResponse({
        'text': unsolved_exercise.text,
        'pk': unsolved_exercise.pk,
        'test_id': unsolved_exercise.test_id.id,
        'exercise_index': unsolved_exercise.exercise_index
    })

def end_test(request):
    test = TrainingTest.objects.filter(user_id=request.user.id).last()
    time_spent = test.time_spent
    correct_answers = test.correct_answers
    exercises_amount = test.apparatus.exercises_amount
    correct_answers_percentage = correct_answers/exercises_amount*100
    if correct_answers_percentage >= test.apparatus.perfect:
        grade = 5
    elif correct_answers_percentage >= test.apparatus.good:
        grade = 4
    elif correct_answers_percentage >= test.apparatus.satisfactory:
        grade = 3
    else:
        grade = 2
    test.grade = grade
    test.save()
    context = {
        "time_spent": time_spent,
        "correct_answers": correct_answers,
        "correct_answers_percentage": str(correct_answers_percentage) + "%",
        "grade": grade,
    }
    return render(request, 'mysite/results.html', context)

# def get_exercise(request):
#     fortune_wheel = 1
#
#     if fortune_wheel == 1:
#         ch = (randint(2,9))
#         chh = (randint(11-ch,9))
#         znak = '+'
#         result = ch+chh
#         excess_value = result - 10
#         correct_answers = str(set([str(ch-excess_value) + '+' + str(ch-(ch-excess_value)),
#                                    str(ch-(ch-excess_value)) + '+' + str(ch-excess_value),
#                                    str(chh-excess_value) + '+' + str(chh-(chh-excess_value)),
#                                    str(chh-(chh-excess_value)) + '+' + str(chh-excess_value)])).replace('{','').replace("'",'').replace('}','')
#     if fortune_wheel == 2:
#         ch = (randint(1, 100))
#         chh = (randint(1, ch))
#         znak = '-'
#         result = ch-chh
#     if fortune_wheel == 3:
#         ch = (randint(1, 10))
#         chh = (randint(1, 10))
#         znak = '*'
#         result = ch*chh
#     if fortune_wheel == 4:
#         chh = (randint(1, 10))
#         ch = (randint(chh, 100))
#         result = round(ch/chh, 2)
#         znak = "/"
#     teacher_check = request.user.groups.filter(name='Учитель').exists()
#     unsolved_exercise = Exercise(test_id=request.user.id, time_spent=None, correct_answer=result,
#                                  given_answer='', answer_is_correct=False, text=str(ch) + str(znak) + str(chh), correct_answers=correct_answers)
#     unsolved_exercise.save()
#     return JsonResponse({
#         'text': unsolved_exercise.text,
#         'pk': unsolved_exercise.pk
#     })


def check_answer(request):
    req = json.loads(request.body)
    exercise = Exercise.objects.get(pk=req['pk'])
    exercise.given_answer = req['value']
    exercise.exercise_index = req['exercise_index']
    test = TrainingTest.objects.filter(user_id=request.user.id).last()
    test.solved_exercises += 1
    exercise.time_spent = datetime.datetime.fromtimestamp(req['time_spent'])
    if str(exercise.given_answer) != '' and exercise.given_answer == exercise.correct_answer:
        is_correct = True
        test.correct_answers += 1
    else:
        is_correct = False
    print(is_correct, str(exercise.given_answer), exercise.correct_answer)
    exercise.answer_is_correct = is_correct
    exercise.save()
    test.save()
    return JsonResponse({
        'is_correct': is_correct
    }, safe=False)


def get_history(request):
    req = json.loads(request.body)
    solved_exercises = Exercise.objects.filter(test_id=req['test_id'], time_spent__isnull=False)
    history = []
    for exercise in solved_exercises:
        solved_exercise = {
            'text': exercise.text,
            'pk': exercise.pk,
            'is_correct': exercise.answer_is_correct,
            'correct_answer': exercise.correct_answer,
            'given_answer': exercise.given_answer,
            'time_spent': exercise.time_spent
        }
        history.append(solved_exercise)
    return JsonResponse(
        history, safe=False
    )


@login_required
def practice(request):
    check = ''
    x = templates(check)
    idNumber = 3
    teacher_check = request.user.groups.filter(name='Учитель').exists()
    l = SavedPrimer(user = request.user.id, idNumber = idNumber, value = x[1] )

    if request.method == 'POST':
        form = AnotherForm(request.POST)


        if form.is_valid():
            form = form.cleaned_data['field']


           # summa = SavedPrimer.objects.last()

            if (str(SavedPrimer.objects.filter(user=request.user.id,idNumber=idNumber ).first().value) == str(form)):
                answerCheck = True
                print ('БД: ',SavedPrimer.objects.filter(user=request.user.id,idNumber=idNumber ).first().value,'введенное', form)
            else:
                answerCheck = False
                print ('БД: ',SavedPrimer.objects.filter(user=request.user.id,idNumber=idNumber ).first().value,'введенное', form)
    else:
        form = AnotherForm()
        answerCheck = 'Вы еще не ввели ответ'

    form = AnotherForm()
    SavedPrimer.objects.filter(user=request.user.id).all().delete()
    if request.user.id!=None:
        l.save()
    return render(request, 'mysite/practice.html',{'teacher_check' : teacher_check, 'answerCheck' : answerCheck, 'temp_text' : x[0],
                                                   'form' : form, 'answer': x[1]})


@login_required
def temp_save(request):
    teacher_check = request.user.groups.filter(name='Учитель').exists()
    if request.user.groups.filter(name='Учитель').exists():
        if request.method == 'POST':
            form = TemplateForm(request.POST)
            if form.is_valid():
                form.save()
        else:
            form = TemplateForm()

        return render(request, 'mysite/temp_save.html',{'templateForm' : form, 'teacher_check' : teacher_check})
    else:
        raise Http404("Вы не учитель")


@login_required
def temp_make(request):
    numberOfTemplatesUser = 0
    numberOfTasks = 0
    stroka = []
    check = ''
    test = ExcersiseTemplate.objects.all()
    print (numberOfTasks)
    form3 = ChoiseForm(request.POST)
    teacher_check = request.user.groups.filter(name='Учитель').exists()
    if request.method == 'POST':
        numberOfTemplates = NameForm(request.POST)
        #print (numberOfTemplates)
        # form2 = AnotherForm(request.POST)
        #form2 = NameForm(request.POST)
        #print ('form2',form2)
        form3 = ChoiseForm(request.POST)
        # if form2.is_valid():
        #     numberOfTasks = form2.cleaned_data['fieldn']
        #     print (numberOfTasks)
        if form3.is_valid():
            # print ('check1',check)
            check = form3.cleaned_data['field']
            if check == None:
                check = ''
            # print ('check2',check)

        if numberOfTemplates.is_valid():
            numberOfTemplatesUser = numberOfTemplates.cleaned_data['your_name']
            numberOfTasks = numberOfTemplates.cleaned_data['fieldn']
            # print ('sd', numberOfTemplatesUser)
            if numberOfTemplatesUser == None:
                numberOfTemplatesUser = 0
            PDFstroka = []
            stroka = []
            styles = getSampleStyleSheet()
            print (styles)
            pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))
            for i in range(int(numberOfTemplatesUser)):
                stroka.append('Вариант '+str(i+1))
                PDFstroka.append(Paragraph('<font name="FreeSans">Вариант '+str(i+1)+'</font>',styles["title"]))

                for k in range (int(numberOfTasks)):
                    y = templates(check)

                    PDFstroka.append(Paragraph('<font name="FreeSans">Задача номер '+str(k+1)+'</font>',styles["Normal"] ))
                    PDFstroka.append(Paragraph('<font name="FreeSans"> </font>',styles["Normal"] ))

                    PDFstroka.append(Paragraph('<font name="FreeSans">Название задачи:</font>',styles["Normal"]))
                    PDFstroka.append(Paragraph('<font name="FreeSans">'+str(y[2])+ '</font>',styles["Normal"]))
                    PDFstroka.append(Paragraph('<font name="FreeSans"> </font>',styles["Normal"] ))

                    PDFstroka.append(Paragraph('<font name="FreeSans">Задача:</font>',styles["Normal"]))
                    PDFstroka.append(Paragraph('<font name="FreeSans">'+str(y[0])+'</font>',styles["Normal"]))
                    PDFstroka.append(Paragraph('<font name="FreeSans"> </font>',styles["Normal"] ))

                    PDFstroka.append(Paragraph('<font name="FreeSans">Ответ:</font>',styles["Normal"]))
                    PDFstroka.append(Paragraph('<font name="FreeSans">'+str(y[1])+'</font>',styles["Normal"]))
                    PDFstroka.append(Paragraph('<font name="FreeSans"> </font>',styles["Normal"] ))

                    PDFstroka.append(Paragraph('<font name="FreeSans">_________________________________________________________________</font>',styles["Normal"] ))
                    PDFstroka.append(Paragraph('<font name="FreeSans"> </font>',styles["Normal"] ))


                    stroka.append('Задача номер '+str(k+1)+'\nНазвание задачи:\n' + str(y[2])+'\n \n' + 'Задача:\n' + str(y[0])+'\n \n' + 'Ответ:\n'+str(y[1])+'\n')
                    # print (stroka)
            return makeNicePdf(request,PDFstroka)


    else:
        numberOfTemplates = NameForm()
        form2 = AnotherForm(request.POST)
        numberOfTemplatesUser = 0
        numberOfTasks = 0


    return render(request, 'mysite/temp_make.html',{'teacher_check':teacher_check,
     'number' : numberOfTemplates, 'numberUser' : numberOfTemplatesUser, 'stroka' : stroka,  'check': check, 'test' : test, 'form3': form3})


@login_required
def home1(request):
    id = request.user.id
    idHome = "/home/" + str(request.user.id)
    if id == None:
        idHome = '/login/'
    return HttpResponseRedirect(idHome)




    
    

