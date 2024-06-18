from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import FilterForm
from django.http import HttpResponse
from .forms import PublishForm, AficheForm, RegisterForm
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
    filter_form = FilterForm(request.POST)
    if len(posters) > 8:
        posters = posters[:8]
    else:
        posters = posters
    return render(request, "index.html", {'filter_form': filter_form,'afiches': posters})


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
        afiche_form = AficheForm()
        publish_form = PublishForm()
        return render(request, "publicar.html", {"afiche_form": afiche_form, "publish_form": publish_form})
    
    elif request.method == "POST":
        afiche_form = AficheForm(request.POST, request.FILES)
        publish_form = PublishForm(request.POST)
        
        if afiche_form.is_valid() and publish_form.is_valid():
            course = publish_form.cleaned_data['courses']
            price = publish_form.cleaned_data['price']
            modality = publish_form.cleaned_data['modality']
            phone = publish_form.cleaned_data['phone']
            disponibility = publish_form.cleaned_data['disponibility']
            time_init = publish_form.cleaned_data['time_init']
            time_end = publish_form.cleaned_data['time_end']

            if not Tutor.objects.filter(usuario=request.user).exists():
                tutor = Tutor(
                    telefono=phone,
                    precio=price, 
                    modalidad_preferida=modality, 
                    usuario=request.user
                )
                tutor.save()
                horario = Horario(dia_semana=disponibility, hora_inicio=time_init, hora_fin=time_end)
                horario.save()
                tutor.horario.add(horario)
            else:
                tutor = Tutor.objects.get(usuario=request.user)
                
            subject = Materia.objects.get(nombre=course)
            dictates = Dicta(tutor=tutor, materia=subject)    
            dictates.save()
            afiche = afiche_form.save()
            publishes = Publica(dicta=dictates, afiche=afiche)
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
        register_form = RegisterForm()
        return render(request, "register.html", {"register_form": register_form})
    elif request.method == "POST":
        register_form = RegisterForm(request.POST)
        
        if register_form.is_valid():
            name = register_form.cleaned_data['name']
            username = register_form.cleaned_data['username']
            email = register_form.cleaned_data['email']
            user = Usuario(
                name = name,
                username = username,
                email = email,
            )
            password = register_form.cleaned_data['password']
            password_confirm = register_form.cleaned_data['password_confirm']
            if password != password_confirm:
                return HttpResponse("Las contraseñas no coinciden")
            user.set_password(password)
            user.save()
            student = Estudiante(usuario=user, tutorias_cursadas="[]", cursos_de_interes="[]")
            student.save()
            return redirect("login")
