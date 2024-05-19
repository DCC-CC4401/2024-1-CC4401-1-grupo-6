from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Usuario, Tutor, Estudiante
from django.contrib.auth import logout


"""
Renderiza la página principal de la aplicación
Usa el método render que construye la plantilla index
Como requiere información de la base de datos, accede para extraer afiches y mostrarlos

parámetro request Información relacionada a la solicitud que se realiza
"""
def index(request):
    return render(request, "index.html")

"""
Dependiendo el método, renderiza la página de acceso a la aplicación o permite el acceso.
Si la solicitud es un GET, construye la plantilla login. Si es un POST, revisa que la
información entregada corresponda a un usuario registrado en la página. Si es así,
permite ingresar en la sesión y redireacciona a la página principal. Sino muestra un error. 

parámetro request Información relacionada a la solicitud que se realiza, puede ser un GET o un POST
"""
def login_view(request):
    if request.method == "GET":
        return render(request, "login.html")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(
                request, "login.html", {"error": "Invalid username or password"}
            )

"""
Cierra la sesión de un usuario autentificado en la aplicación
Usa el método logout para limpiar la información relacionada a la sesión del usuario. 
No retorna. Luego se redirecciona a la página principal con el método redirect.

parámetro request Información relacionada a la solicitud que se realiza
"""
def logout_user(request):
    logout(request)
    return redirect("index")

"""
Renderiza la página relacionada a la publicación de afiches
Usa el método render que construye la plantilla publicar

parámetro request Información relacionada a la solicitud que se realiza
"""
def publish(request):
    return render(request, "publicar.html")

"""
Dependiendo del método, renderiza la página de registro o ingresa la información 
de un usuario nuevo a la base de datos.
Si la solicitud es un GET, construye la plantilla register. Si es un POST, recibe
la información enviada por el formulario de registro y crea un nuevo usuario y, en su defecto,
un estudiante. Luego redirecciona a la página login para que el usuario pueda ingresar.

parámetro request Información relacionada a la solicitud que se realiza, puede ser un GET o un POST

"""
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
