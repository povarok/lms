from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'polls'

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('temp_make/', views.temp_make, name='temp_make'),
    path('practice/', views.practice, name='practice'),


    # ex: /polls/primer
    url(r'^primer$', views.exercise_view, name='primer'),
    path('api_get_exercise_from_test/', views.get_exercise_from_test, name='get_exercise_from_test'),
    path('api_check_answer/', views.check_answer, name='check_answer'),
    path('api_get_history/', views.get_history, name='get_history'),
    #path('api_get_test/')
    url(r'^temp_save$', views.temp_save, name='temp_save'),


]
