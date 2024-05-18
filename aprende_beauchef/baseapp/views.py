from django.shortcuts import render, redirect   
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from .models import Usuario, Tutor, Estudiante
from django.contrib.auth import logout
from django.http import HttpResponseRedirect

# Create your views here.
def index(request):
    return render(request, "index.html")


def login_view(request):
    if request.method == "GET":
        return render(request, "login.html")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print("User:", user)  # Debe mostrar el objeto usuario si la autenticación es exitosa, None de lo contrario
        if user is not None:
            login(request, user)
            return redirect('index')  # Asegúrate de que 'index' sea una URL válida en tu archivo urls.py
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})

def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")

def publicar(request):
    return render(request, "publicar.html")

def register(request):
    if request.method == "GET":
        return render(request, "register.html")
    elif request.method == "POST":
        data = request.POST
        user = Usuario(
            username=data.get("nombre_de_usuario"),
            name=data.get("nombre"),
            email=data.get("email"),
        )
        user.set_password(data.get("contrasenha"))  # Esto hashea la contraseña correctamente
        user.save()
        estudiante = Estudiante(usuario=user, tutorias_cursadas="[]", cursos_de_interes="[]")
        estudiante.save()
        return render(request, "test_items.html", {"data": data})
