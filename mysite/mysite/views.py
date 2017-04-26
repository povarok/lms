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
from polls.models import ExcersiseTemplate, Replacers




class RegisterFormView(FormView):
    form_class = UserCreationForm

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
        raise Http404("Вы заходите не на ту страницу пользователя")

    
    # /РЕШЕНО/ как в этой функции сгенерировать html код, использовав объекты из Replacers.objects.all() вместо city1,city2 etc. ??
    #template_name = "mysite/dom.html"
    success_url = "/login"
    # раскомментируй строку снизу, чтобы отображать шаблон по фильтру
    # template = ExcersiseTemplate.objects.filter(name="Повар").order_by('?').first()
    template = ExcersiseTemplate.objects.order_by('?').first()
    subs = template.get_subs()
    answer = template.get_answer ()
    print ('как выглядят ответы',answer)
    print (subs)
    print (subs[0][0])
    #i=0
    #replacer = [0]*4
    temp_text=template.text
    temp_answer = template.correctAnswer
    for name, number in subs:
        replacer = Replacers.objects.filter(type=name).order_by("?").first().value
        temp_text = temp_text.replace("{{"+name+number+"}}", replacer)
        print (temp_text)
        print(name,  number, replacer)
        for nameAns, numberAns in answer:
            if name == nameAns and number == numberAns:
                temp_answer = temp_answer.replace ("{{"+nameAns+numberAns+"}}", replacer)

    #temp_answer = eval(temp_answer)
    temp_answer = float("{0:.2f}".format(eval(temp_answer)))
    temp_name = template.name


        #replacer[i]= Replacers.objects.filter(type=name).order_by("?").first().value
        #i+=1
    
    
    
     
    return render(request, 'mysite/dom.html',{
            'text': temp_text,'answer' : temp_answer, 'name' : temp_name})

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
