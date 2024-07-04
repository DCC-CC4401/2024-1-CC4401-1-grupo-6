from django.urls import path
from baseapp import views
from django.conf.urls.static import static
from django.conf import settings
from .forms import NewPasswordForm

from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.index, name="index"),
    path('search_courses/', views.search_courses, name='search_courses'),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("publicar/", views.publish, name="publicar"),
    path("register/", views.register, name="register"),
    path("afiche/<int:posterID>/", views.mostrar_afiche, name="mostrarAfiche"),
    
    # Restablecer Contraseña
    # Usa las páginas nativas de Django con sus funcionalidades y luego renderiza el diseño 
    # de la página en template_name
    path('restablecer_contraseña/', auth_views.PasswordResetView.as_view(
        template_name='restablecer_contraseña.html'),
        name='password_reset'),
    path('restablecer_contraseña_correo/', auth_views.PasswordResetDoneView.as_view(
        template_name='restablecer_contraseña_listo.html'), 
        name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(
        template_name='restablecer_nueva_contraseña.html',
        form_class=NewPasswordForm), 
        name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='restablecer_contraseña_completo.html'), 
        name='password_reset_complete'),
    
    # Definimos la ruta específica antes de la ruta general
    path("profile/edit/", views.profile_edit, name="profile_edit"),
    path("profile/<str:tutorUsername>/", views.profile_view, name="profile"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
