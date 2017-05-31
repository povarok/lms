from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
# Опять же, спасибо django за готовую форму аутентификации.
from django.contrib.auth.forms import AuthenticationForm

# Функция для установки сессионного ключа.
# По нему django будет определять, выполнил ли вход пользователь.
from django.contrib.auth import login, logout

from django.views.generic.base import View
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render, get_object_or_404
from polls.models import ExcersiseTemplate, Replacers, NameForm, templates, AnotherForm, ChoiseForm, Primer, TemplateForm

#from django.core.mail import send_mail





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
    #id = getId()
    # В случае успеха перенаправим на главную.
    success_url = "/home/" # + user.id <------ где его взять?
    #TODO как сделать корректный редирект на страницу вида /home/user.id ? ? ?

    def form_valid(self, form):
        # Получаем объект пользователя на основе введённых в форму данных.
        self.user = form.get_user()

        # id = self.user.id
        # return (id)

        # Выполняем аутентификацию пользователя.
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)

# def getId(request):
#     id = request.user.id
#     return (id)



def home(request, user_id):
    if request.user.id != int(user_id):
        #raise HTTP404
        raise Http404("Вы заходите не на свою страницу пользователя / не авторизованы")
    teacher_check = request.user.groups.filter(name='Учитель').exists()
    print (teacher_check)

    # userGroup = request.user.groups.all()
    # print (userGroup)
    # print (request.user.groups.all()[0])

    #ExcersiseTemplate.objects.create(text = 'test',name = 'test',correctAnswer = 'test',type = 'test',grade = 1,subject = 'test')



    numberOfTemplatesUser = 0
    stroka = []
    check = ''
    # /РЕШЕНО/ как в этой функции сгенерировать html код, использовав объекты из Replacers.objects.all() вместо city1,city2 etc. ??
    #template_name = "mysite/dom.html"
    success_url = "/login"
    # раскомментируй строку снизу, чтобы отображать шаблон по фильтру
    # template = ExcersiseTemplate.objects.filter(name="Повар").order_by('?').first()

    # def templates():
    #     template = ExcersiseTemplate.objects.order_by('?').first()
    #     subs = template.get_subs()
    #     answer = template.get_answer ()
    #     # print ('как выглядят ответы',answer)
    #     # print (subs)
    #     # print (subs[0][0])
    # #i=0
    # #replacer = [0]*4
    #     temp_text=template.text
    #     temp_answer = template.correctAnswer
    #     for name, number in subs:
    #         replacer = Replacers.objects.filter(type=name).order_by("?").first().value
    #         temp_text = temp_text.replace("{{"+name+number+"}}", replacer)
    #         # print (temp_text)
    #         # print(name,  number, replacer)
    #         for nameAns, numberAns in answer:
    #             if name == nameAns and number == numberAns:
    #                 temp_answer = temp_answer.replace ("{{"+nameAns+numberAns+"}}", replacer)
    #
    # #temp_answer = eval(temp_answer)
    #     temp_answer = float("{0:.2f}".format(eval(temp_answer)))
    #
    #     temp_name = template.name
    #     return temp_text, temp_answer, temp_name

    x = templates(check)
    #print ('ВЫВОД TEMPLATES',x)
    #print ('ВЫВОД TEMPLATES',x[0])


    if request.method == 'POST':
        numberOfTemplates = NameForm(request.POST)

        if numberOfTemplates.is_valid():
            numberOfTemplatesUser = numberOfTemplates.cleaned_data['your_name']
            stroka = []
            for i in range(int(numberOfTemplatesUser)):
                y = templates()
                stroka.append('Название задачи:\n' + str(y[2])+'\n \n' + 'Задача:\n' + str(y[0])+'\n \n' + 'Ответ:\n'+str(y[1])+'\n')
                print (stroka)

                #print ('пишу  ',i)



    else:
        numberOfTemplates = NameForm()






    # if request.method == 'POST':
    #     form = forms(request.POST)
    #     if form.is_valid():
    #
    #         request.user.email = form
    # userMail = request.user.email


        #replacer[i]= Replacers.objects.filter(type=name).order_by("?").first().value
        #i+=1
    
    
    

    return render(request, 'mysite/dom.html',{'teacher_check' : teacher_check ,'groups': request.user.groups.all(),
             'number' : numberOfTemplates, 'numberUser' : numberOfTemplatesUser, 'stroka' : stroka})


def temp_save(request):
    if request.user.groups.filter(name='Учитель').exists():
        if request.method == 'POST':
            form = TemplateForm(request.POST)
            if form.is_valid():
                form.save()
        else:
            form = TemplateForm()

        return render(request, 'mysite/temp_save.html',{'templateForm' : form})
    else:
        raise Http404("Вы не учитель")


def temp_make(request):
    numberOfTemplatesUser = 0
    numberOfTasks = 0
    stroka = []
    check = ''
    test = ExcersiseTemplate.objects.all()
    print (numberOfTasks)
    form3 = ChoiseForm(request.POST)

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
            stroka = []
            for i in range(int(numberOfTemplatesUser)):
                stroka.append('Вариант '+str(i+1))
                for k in range (int(numberOfTasks)):
                    y = templates(check)
                    stroka.append('Задача номер '+str(k+1)+'\nНазвание задачи:\n' + str(y[2])+'\n \n' + 'Задача:\n' + str(y[0])+'\n \n' + 'Ответ:\n'+str(y[1])+'\n')
                    # print (stroka)


    else:
        numberOfTemplates = NameForm()
        form2 = AnotherForm(request.POST)
        numberOfTemplatesUser = 0
        numberOfTasks = 0


    return render(request, 'mysite/temp_make.html',{
     'number' : numberOfTemplates, 'numberUser' : numberOfTemplatesUser, 'stroka' : stroka,  'check': check, 'test' : test, 'form3': form3})






class LogoutView(View):
    def get(self, request):
        # Выполняем выход для пользователя, запросившего данное представление.
        logout(request)

        # После чего, перенаправляем пользователя на главную страницу.
        return HttpResponseRedirect("/home")

def home1 (request):
    id = request.user.id
    idHome = "/home/" + str(request.user.id)
    if id == None:
        idHome = '/login/'
    return HttpResponseRedirect(idHome)

def lms (request):
    return render(request, 'mysite/lms.html')

# def mail(request):
#     send_mail('Subject here', 'Here is the message.', 'vasily.komarov1997@gmail.com',
#     ['ivan44050@gmail.com'], fail_silently=False)
