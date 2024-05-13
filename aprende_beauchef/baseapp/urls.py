from django.urls import path
from baseapp import views

urlpatterns =  [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
<<<<<<< HEAD
    path("publicar/", views.publicar, name="publicar"),
=======
    path("register/", views.register, name="register"),
>>>>>>> 31c44294a46444807fd89463589d4931cf1aa2d9
    ]