from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from random import randint
from django.contrib.auth.decorators import login_required
#from polls.models import ExcersiseTemplate, Replacers, NameForm, templates, AnotherForm, ChoiseForm, Primer, TemplateForm, SavedPrimer,  makeNicePdf
from .models import Question, Choice, Exercise, NameForm

from polls.models import ExcersiseTemplate, Replacers, NameForm, templates, AnotherForm, ChoiseForm, Exercise, TemplateForm, SavedPrimer,  makeNicePdf
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.views.generic.base import View
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


@login_required
def index(request):
    teacher_check = request.user.groups.filter(name='Учитель').exists()
    context = {
        'teacher_check': teacher_check
    }
    return render(request, 'mysite/lms.html', context)


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


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def exercise_view(request):
    fortune_wheel = (randint(1,4))

    if fortune_wheel == 1:
        ch = (randint(1,100))
        chh = (randint(1,100))
        znak = '+'
        result = ch+chh
    if fortune_wheel == 2:
        ch = (randint(1, 100))
        chh = (randint(1, ch))
        znak = '-'
        result = ch-chh
    if fortune_wheel == 3:
        ch = (randint(1, 10))
        chh = (randint(1, 10))
        znak = '*'
        result = ch*chh
    if fortune_wheel == 4:
        chh = (randint(1, 10))
        ch = (randint(chh, 100))
        result = round(ch/chh, 2)
        znak = "/"
    teacher_check = request.user.groups.filter(name='Учитель').exists()
    summmm = 0
    check = ''
    answer_check = 'Вы еще не ввели ответ'
    try:
        if request.method == 'POST':
            print(request)
            form = AnotherForm(request.POST)
            if form.is_valid():
                cleaned_result = form.cleaned_data['field']
                # print(cleaned_result, "cleanedresult")
                # print (p,'не из бд',p.summ)
                # print ('из БД',summa.summ)
                # print("summa.summ, ", summa.summ, ', ', type(summa.summ))
                # print("cleaned_result, ",cleaned_result,', ', type(cleaned_result))
                if float(result) == float(cleaned_result):
                    answer_check = True
                else:
                    answer_check = False
                solved_exercise = Exercise(user_id=request.user.id, time_spent=None, correct_answer=result,
                                           given_answer=cleaned_result, answer_is_correct=answer_check, text=str(ch)+str(znak)+str(chh))
                solved_exercise.save()
    except ValueError:
        answer_check = False
        print("valueerror")
        pass

    else:
        form = AnotherForm()

     #   answerCheck = 'Вы еще не ввели ответ'
    # Primer.objects.all().delete()
    # p.save()
    return render(request, 'polls/primer.html', {'teacher_check' : teacher_check,
            'sl': ch, 'sll': chh,'znak' : znak,'form' : form, 'number' : summmm,
            'answer_check' : answer_check,  'check' : check, 'fortune_wheel': fortune_wheel, "result" : result})


def get_exercise(request):
    return JsonResponse({
        'text': '2+2',
        'pk': 1
    })


def check_answer(request):
    print(request.user.pk)
    req = json.loads(request.body)
    print(req)
    return JsonResponse({
        'is_correct': True
    })


def get_history(request):
    print(request.user.pk)
    return JsonResponse(
        [
            {
                'text': '2+2',
                'pk': 1,
                'is_correct': True
            }
        ]
    )


@login_required
def practice(request):
    check = ''
    x = templates(check)
    print (x[1])
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




    
    

