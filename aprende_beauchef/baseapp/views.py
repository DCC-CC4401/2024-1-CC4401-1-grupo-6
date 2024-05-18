from django.shortcuts import render, redirect
from .models import Usuario, Tutor, Estudiante


# Create your views here.
def index(request):
    return render(request, "index.html")


def login(request):
    return render(request, "login.html")


def publicar(request):
    return render(request, "publicar.html")


def register(request):
    if request.method == "GET":
        return render(request, "register.html")
    if request.method == "POST":
        data = request.POST
        user = Usuario(
            username=data.get("nombre_de_usuario"),
            name=data.get("nombre"),
            password=data.get("contrasenha"),
            email=data.get("email"),
        )
        user.save()
        estudiante = Estudiante(usuario=user, tutorias_cursadas="[]", cursos_de_interes="[]")
        estudiante.save()
        return render(request, "test_items.html", {"data": data})
