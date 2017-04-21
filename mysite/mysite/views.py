from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
# Опять же, спасибо django за готовую форму аутентификации.
from django.contrib.auth.forms import AuthenticationForm

# Функция для установки сессионного ключа.
# По нему django будет определять, выполнил ли вход пользователь.
from django.contrib.auth import login, logout

from django.views.generic.base import View
from django.http import HttpResponseRedirect
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

    # В случае успеха перенаправим на главную.
    success_url = "/home"

    def form_valid(self, form):
        # Получаем объект пользователя на основе введённых в форму данных.
        self.user = form.get_user()

        # Выполняем аутентификацию пользователя.
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)

def home(request):
    # как в этой функции сгенерировать html код, использовав объекты из Replacers.objects.all() вместо city1,city2 etc. ??
    #template_name = "mysite/dom.html"
    success_url = "/login"
    template=ExcersiseTemplate.objects.all()
    replaser = Replacers.objects.all()


    return render(request, 'mysite/dom.html',{
            'text': template[0].text})

class LogoutView(View):
    def get(self, request):
        # Выполняем выход для пользователя, запросившего данное представление.
        logout(request)

        # После чего, перенаправляем пользователя на главную страницу.
        return HttpResponseRedirect("/home")

#def user (request, user_id):
