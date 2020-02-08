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
    path('api_create_test/', views.create_test, name='create_test'),
    path('api_get_exercise/', views.get_exercise, name='get_exercise'),
    path('api_check_answer/', views.check_answer, name='check_answer'),
    path('api_get_history/', views.get_history, name='get_history'),
    path('end_test/', views.end_test, name='end_test'),
    path('end_test/<int:test_id>', views.end_test_id, name='end_test_id'),
    url(r'^temp_save$', views.temp_save, name='temp_save'),


]
