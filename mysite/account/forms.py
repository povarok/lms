from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Account

class RegistrationForm(UserCreationForm):
    # first_name = forms.CharField(label=u'Имя', max_length=100)
    # last_name = forms.CharField(label=u'Фамилия', max_length=100)
    # # middle_name = forms.CharField(label=u'Отчество', max_length=100)
    # email = forms.EmailField(label=u"Эл. почта", max_length=100)

    class Meta:
        model = Account
        fields = ['username', 'email',
                  'first_name', 'last_name', 'middle_name',
                  'phone_number', "school", 'city',
                  'password1', 'password2']