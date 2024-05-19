from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Usuario, Tutor, Estudiante
from django.contrib.auth import logout


# Create your views here.
def index(request):
    return render(request, "index.html")


def login_view(request):
    if request.method == "GET":
        return render(request, "login.html")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        print("User: ", user)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(
                request, "login.html", {"error": "Invalid username or password"}
            )


def logout_user(request):
    logout(request)
    return redirect("index")


def publish(request):
    return render(request, "publicar.html")


def register(request):
    if request.method == "GET":
        return render(request, "register.html")
    elif request.method == "POST":
        data = request.POST
        user = Usuario(
            username = data.get("username"),
            name = data.get("name"),
            email = data.get("email"),
        )
        user.set_password(data.get("password"))
        user.save()
        student = Estudiante(usuario=user, tutorias_cursadas="[]", cursos_de_interes="[]")
        student.save()
        return redirect("login")
