from django.urls import path

from . import views

app_name = "control"

urlpatterns = [
    path('control/', views.control_page, name='control_page'),
]
