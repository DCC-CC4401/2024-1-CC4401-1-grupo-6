from django.urls import path
from baseapp import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("publicar/", views.publish, name="publicar"),
    path("register/", views.register, name="register"),
    path("restablecer_contraseña/", views.reset_password, name="restablecer_contraseña"),
    path("nueva_contraseña/", views.new_password, name="nueva_contraseña"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
