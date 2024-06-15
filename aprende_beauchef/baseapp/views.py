from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .models import Usuario, Tutor, Estudiante, Afiche, Horario, Dicta, Publica, Materia
from django.contrib.auth import logout
import os


def index(request):
    """
    Renderiza la página principal de la aplicación
    Usa el método render que construye la plantilla index
    Como requiere información de la base de datos, accede para extraer afiches y mostrarlos

    parámetro request Información relacionada a la solicitud que se realiza
    """
    posters = Afiche.objects.all().order_by('-id')
    if len(posters) > 8:
        posters = posters[:8]
    else:
        posters = posters
    return render(request, "index.html", {'afiches': posters})

def login_view(request):
    """
    Dependiendo el método, renderiza la página de acceso a la aplicación o permite el acceso.
    Si la solicitud es un GET, construye la plantilla login. Si es un POST, revisa que la
    información entregada corresponda a un usuario registrado en la página. Si es así,
    permite ingresar en la sesión y redireacciona a la página principal. Sino muestra un error. 

    parámetro request Información relacionada a la solicitud que se realiza, puede ser un GET o un POST
    """
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
            return HttpResponse("Usuario o contraseña incorrectos")

def logout_user(request):
    """
    Cierra la sesión de un usuario autentificado en la aplicación
    Usa el método logout para limpiar la información relacionada a la sesión del usuario. 
    No retorna. Luego se redirecciona a la página principal con el método redirect.

    parámetro request Información relacionada a la solicitud que se realiza
    """
    logout(request)
    return redirect("index")

def publish(request):
    """
    Si el metodo de la request es de tipo GET, renderiza la página relacionada a la publicación de afiches
    Usa el método render que construye la plantilla publicar

    Si el metodo de la request es de tipo POST, recibe la información enviada por el formulario de publicación y 
    la procesa para ser guardada en la base de datos.
    Si el usuario ingreso mal algun campo se retorna un HttpResponse con un mensaje de error, de caso contrario redireccionamos a la página principal.
    """
    if request.method == "GET":
        courses = Materia.objects.all()
        return render(request, "publicar.html", {"courses": courses})
    else:
        my_poster = request.FILES.get("my_poster")
        name = request.POST.get("name")
        description = request.POST.get("description")
        course = request.POST.get("courses")
        price = request.POST.get("price")
        modality = request.POST.get("modality")
        phone = request.POST.get("phone")
        modality = request.POST.get("modality")
        phone = request.POST.get("phone")
        disponibility = request.POST.get("disponibility")
        time_init = request.POST.get("time-init")
        time_end = request.POST.get("time-end")


        if name is not None:
            poster = Afiche(url = my_poster, descripcion = description, nombre = name)
            poster.save()

            if not Tutor.objects.filter(usuario=request.user).exists():
                tutor = Tutor(
                    telefono = phone,
                    precio = price, 
                    modalidad_preferida = modality, 
                    usuario = request.user
                    )
                tutor.save()
                print("acabo de guardar el tutor")
                horario = Horario(dia_semana = disponibility, hora_inicio = time_init, hora_fin = time_end)
                horario.save()
                tutor = Tutor.objects.get(usuario=request.user)
                tutor.horario.add(horario)

                subject = Materia.objects.get(codigo_curso=course)
                dictates = Dicta(tutor = tutor, materia = subject)    
                dictates.save()
                publishes = Publica(dicta = dictates, afiche = poster)
                publishes.save()
            else:
                tutor = Tutor.objects.get(usuario=request.user)
                subject = Materia.objects.get(codigo_curso=course)
                dictates = Dicta(tutor = tutor, materia = subject)    
                dictates.save()
                publishes = Publica(dicta = dictates, afiche = poster)
                publishes.save()

            return redirect('index')
        else:
            return HttpResponse("Error al publicar el afiche")



def register(request):
    """
    Dependiendo del método, renderiza la página de registro o ingresa la información 
    de un usuario nuevo a la base de datos.
    Si la solicitud es un GET, construye la plantilla register. Si es un POST, recibe
    la información enviada por el formulario de registro y crea un nuevo usuario y, en su defecto,
    un estudiante. Luego redirecciona a la página login para que el usuario pueda ingresar.

    parámetro request Información relacionada a la solicitud que se realiza, puede ser un GET o un POST

    """
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

def profile_view(request):
    """
    
    """
    user=request.user
    try:
        tutor = Tutor.objects.get(usuario=user)
        # Obtener todas las publicaciones de afiches de este tutor
        publicaciones = Publica.objects.filter(dicta__tutor=tutor).select_related('afiche')
        afiches = [publicacion.afiche for publicacion in publicaciones]
    except Tutor.DoesNotExist:
        tutor = None
        afiches = None
    return render(request, "profile.html", {'user': user, 'afiches': afiches})

def profile_edit(request):
    """
    
    """
    user=request.user
    if request.method == "GET":
        return render(request, "profile_config.html", {'user': user})
    elif request.method == "POST":
        data = request.POST
        user.name = data.get("name")
        user.email = data.get("email")
        user.save()
        return redirect(request, "profile.html", {'user': user})