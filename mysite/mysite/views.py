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


class RegisterFormView(FormView):
    form_class = UserCreationForm
    print (form_class)

    # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
    # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей.
    success_url = "/login/"

    # Шаблон, который будет использоваться при отображении представления.
    template_name = "mysite/register.html"

    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        form.save()

        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)


class LoginFormView(FormView):

    form_class = AuthenticationForm

    # Аналогично регистрации, только используем шаблон аутентификации.
    template_name = "mysite/login.html"
    # В случае успеха перенаправим на главную.
    success_url = "/" # + user.id <------ где его взять?
    #TODO как сделать корректный редирект на страницу вида /home/user.id ? ? ?

    def form_valid(self, form):
        # Получаем объект пользователя на основе введённых в форму данных.
        self.user = form.get_user()

        # id = self.user.id
        # return (id)

        # Выполняем аутентификацию пользователя.
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class LogoutView(View):
    def get(self, request):
        # Выполняем выход для пользователя, запросившего данное представление.
        logout(request)

        # После чего, перенаправляем пользователя на главную страницу.
        return HttpResponseRedirect("/home")


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
    return render(request, 'mysite/practice.html',{'teacher_check' : teacher_check, 'answerCheck' : answerCheck, 'temp_text' : x[0], 'form' : form, 'answer': x[1]})


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

