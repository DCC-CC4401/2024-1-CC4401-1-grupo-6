from django.urls import path
from baseapp import views

urlpatterns =  [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    ]