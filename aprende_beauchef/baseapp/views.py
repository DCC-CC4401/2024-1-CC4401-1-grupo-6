from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import FilterForm
from django.http import HttpResponse
from .forms import PublishForm, AficheForm, RegisterForm, LoginForm, NewPasswordForm
from .models import Usuario, Tutor, Estudiante, Afiche, Horario, Dicta, Publica, Materia
from django.contrib.auth import logout
from django.http import JsonResponse
from django.core.mail import send_mail
import re 


def index(request):
    """
    Renderiza la página principal de la aplicación
    Usa el método render que construye la plantilla index
    Como requiere información de la base de datos, accede para extraer afiches y mostrarlos

    parámetro request Información relacionada a la solicitud que se realiza
    """
    if request.method == "GET":
        posters = Afiche.objects.all().order_by('-id')
        filter_form = FilterForm(request.POST)
        if len(posters) > 8:
            posters = posters[:8]
        else:
            posters = posters
        return render(request, "index.html", {'filter_form': filter_form,'afiches': posters})
        
    elif request.method == "POST":
        filter_form = FilterForm(request.POST)
        if filter_form.is_valid():
            # Al menos para los precios es necesario tener valor por default, por eso el if else
            search = filter_form.cleaned_data['search']
            max_price = filter_form.cleaned_data['max_price']
            min_price = filter_form.cleaned_data['min_price'] 
            modality = filter_form.cleaned_data['modality']
            disponibility = filter_form.cleaned_data['disponibility']
            alldisponibility = filter_form.cleaned_data.get('disponibility')

            if max_price is None or max_price == '':
                max_price = 999999999
            if min_price is None or min_price == '':
                min_price = 0

            # Obtener todas las publicaciones de afiches
            publicaciones = Afiche.objects.all().order_by('-id')

            # Aplicar los filtros opcionales
            if search:
                publicaciones = publicaciones.filter(publica__dicta__materia__nombre__icontains=search).order_by('-id')
            if max_price is not None:
                publicaciones = publicaciones.filter(publica__dicta__tutor__precio__lte=max_price).order_by('-id')
            if min_price is not None:
                publicaciones = publicaciones.filter(publica__dicta__tutor__precio__gte=min_price).order_by('-id')
            if alldisponibility != 'ALL':
                publicaciones = publicaciones.filter(publica__dicta__tutor__horario__dia_semana=disponibility).order_by('-id')
            
            #La idea es que sigan filtrando de esta forma, es decir, reasignando publicaciones
            #con los filtros para modalidad.

            afiches = [publicacion for publicacion in publicaciones]
            return render(request, "index.html", {'filter_form': filter_form,'afiches': afiches})
        else:
            return HttpResponse("Error al filtrar los afiches")
        

def search_courses(request):
    """
    Vista que transforma la búsqueda de cursos en tiempo real en una lista de sugerencias JSON
    """
    codigo_curso = re.compile(r'^[A-Z]{2}\d{0,4}$')
    query = request.GET.get('search', '')
    if codigo_curso.match(query):
        courses = Materia.objects.filter(codigo_curso__icontains=query).order_by('nombre')
    else:
        courses = Materia.objects.filter(nombre__icontains=query).order_by('nombre')
    results = []
    for course in courses:
        results.append({
            'codigo_curso': course.codigo_curso,
            'nombre': course.nombre
        })
    return JsonResponse(results, safe=False)


def login_view(request):
    """
    Dependiendo el método, renderiza la página de acceso a la aplicación o permite el acceso.
    Si la solicitud es un GET, construye la plantilla login. Si es un POST, revisa que la
    información entregada corresponda a un usuario registrado en la página. Si es así,
    permite ingresar en la sesión y redireacciona a la página principal. Sino muestra un error. 

    parámetro request Información relacionada a la solicitud que se realiza, puede ser un GET o un POST
    """
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {'form': form})
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
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


def mostrar_afiche(request, posterID):
    """
    Renderiza la página de un afiche más detallado
    Si la solicitud es un GET, construye la plantilla mostrarAfiche.
    Usa el método render que construye la plantilla mostrarAfciche
    Como requiere información de la base de datos, accede para extraer afiches y mostrarlos

    parámetro request Información relacionada a la solicitud que se realiza
    """
    afiche = Afiche.objects.filter(id=posterID).first()
    publicacion = Publica.objects.filter(afiche=afiche).first()

    if(afiche.descripcion == ''):
        descripcion = afiche.nombre
    else:
        descripcion = afiche.descripcion

    if(publicacion.dicta.tutor.modalidad_preferida == 'rem'):
        modalidad = 'Remota'
    elif(publicacion.dicta.tutor.modalidad_preferida == 'pres'):
        modalidad = 'Presencial'
    else:
        modalidad = 'Remota o Presencial'

    #disponibilidad no lo pudo obtener
        
    data ={
        'titulo': afiche.nombre,
        'imagen': afiche.url.url,
        'descripcion': descripcion,
        'tutor': publicacion.dicta.tutor.usuario.name,
        'telefono': publicacion.dicta.tutor.telefono,
        'precio': publicacion.dicta.tutor.precio,
        'modalidad': modalidad,
        'disponibilidad': 'A coordinar',
    }

    if request.method == "GET":
        return render(request, "mostrarAfiche.html", data)
    elif request.method == "POST":
        
        student = request.user
        studentName = student.name
        studentEmail = student.email
        
        tutorName = publicacion.dicta.tutor.usuario.name
        emailTutor = publicacion.dicta.tutor.usuario.email
        emailApp = 'aprendebeauchef@gmail.com'

        send_mail(
            afiche.nombre,
            f"Estimado/a {tutorName}, tiene un estudiante interesado en su tutoría: {afiche.nombre} de precio: {publicacion.dicta.tutor.precio}.\nPor favor, contáctelo a la brevedad.\n    Nombre del estudiante: {studentName}\n    Email del estudiante: {studentEmail}",
            studentEmail,  #acá va el email de la app
            [emailApp], #acá iría el email del tutor, pero como no existe para efectos de demo se prueba con otro correo
            fail_silently=False,
        )
        return render(request, "mostrarAfiche.html", data)

def newPassword(request):
    user=request.user
    if request.method == "GET":
        newPassword_form = NewPasswordForm()
        return render(request, "restablecer_nueva_contraseña.html", {"newPassword_form": newPassword_form})
    elif request.method == "POST":
        newPassword_form = NewPasswordForm(request.POST)
        
        if newPassword_form.is_valid():
            password = newPassword_form.cleaned_data['new_password1']
            password_confirm = newPassword_form.cleaned_data['new_password2']
            if password != password_confirm:
                return HttpResponse("Las contraseñas no coinciden")
            user.set_password(password)
            user.save()
            return redirect("login")

"""
def reset_password(request):

    Renderiza la página de restablecimiento de contraseña.
    Usa el método render que construye la plantilla restablecer_contraseña

    parámetro request Información relacionada a la solicitud que se realiza
    
    recovery_password_form = LoginRecoveryPassword()
    return render(request, "restablecer_contraseña.html", {'form': recovery_password_form})

def new_password(request):
    
    Renderiza la página de nueva contraseña.
    Usa el método render que construye la plantilla nueva_contraseña

    parámetro request Información relacionada a la solicitud que se realiza
    
    new_password_form = LoginNewPassword()
    return render(request, "nueva_contraseña.html", {'form': new_password_form})
"""

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