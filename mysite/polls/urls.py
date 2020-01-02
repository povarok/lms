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

    # ex: /polls/5/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # ex: /polls/5/results/
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    # ex: /polls/5/vote/
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),

    # ex: /polls/primer
    url(r'^primer$', views.primer, name='primer'),

    url(r'^temp_save$', views.temp_save, name='temp_save'),


]
