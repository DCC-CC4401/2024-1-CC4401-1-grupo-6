from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import FilterForm
from django.http import HttpResponse, JsonResponse, Http404
from .forms import PublishForm, AficheForm, RegisterForm, LoginForm, NewPasswordForm, EditProfileForm
from .models import Usuario, Tutor, Estudiante, Afiche, Horario, Dicta, Publica, Materia
from django.contrib.auth import logout
from django.core.mail import send_mail
import re 


def index(request):
    """
    Renderiza la página principal de la aplicación. Como requiere información de la base de datos, 
    accede para extraer afiches y mostrarlos

    Si el método es GET, obtiene y muestra los afiches más recientes, limitados a 8.
    Si el método es POST, aplica los filtros del formulario y muestra los afiches que cumplen con los criterios.

    Parameters:
    request (HttpRequest): Información relacionada a la solicitud que se realiza.

    Returns:
    HttpResponse: Página renderizada con afiches y formulario de filtro.
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
                publicaciones = publicaciones.filter(precio__lte=max_price).order_by('-id') #sino funciona apagar
            if min_price is not None:
                publicaciones = publicaciones.filter(precio__gte=min_price).order_by('-id') #sino funciona apagar
            if alldisponibility != 'ALL':
                publicaciones = publicaciones.filter(publica__dicta__tutor__horario__dia_semana=disponibility).order_by('-id')
            if modality != 'AMB':
                publicaciones = publicaciones.filter(publica__dicta__tutor__modalidad_preferida=modality).order_by('-id')

            afiches = [publicacion for publicacion in publicaciones]
            return render(request, "index.html", {'filter_form': filter_form,'afiches': afiches})
        else:
            return HttpResponse("Error al filtrar los afiches")
        

def search_courses(request):
    """
    Vista que transforma la búsqueda de cursos en tiempo real en una lista de sugerencias JSON.
    
    Parameters:
    request (HttpRequest): Información relacionada a la solicitud que se realiza.

    Returns:
    JsonResponse: Lista de cursos que coinciden con la búsqueda.
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

    Si el método es GET, muestra el formulario de inicio de sesión.
    Si el método es un POST, revisa que la información entregada corresponda a un usuario registrado en la página. Si es así,
    permite ingresar en la sesión y redireacciona a la página principal. Sino vuelve a redireccionar al login. 

    Parameters:
    request (HttpRequest): Información relacionada a la solicitud que se realiza, puede ser un GET o un POST.

    Returns:
    HttpResponse: Página de inicio de sesión o redirección a la página principal.
    """
    if request.method == "GET":
        login_form = LoginForm()
        return render(request, "login.html", {'login_form': login_form})
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")
            else:
                return redirect("login")


def logout_user(request):
    """
    Cierra la sesión del usuario autenticado y redirige a la página principal.
    """
    logout(request)
    return redirect("index")


def publish(request):
    """
    Maneja la publicación de nuevos afiches.
    
    Si el método es GET, muestra el formulario de publicación.
    Si el método es POST, procesa el formulario (Validandolo en FrontEnd y BackEnd) y guarda la nueva publicación en la base de datos.

    Parameters:
    request (HttpRequest): Información relacionada a la solicitud que se realiza, puede ser un GET o un POST.

    Returns:
    HttpResponse: Página de publicación o redirección a la página principal.
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
            modality = publish_form.cleaned_data['modality']
            phone = publish_form.cleaned_data['phone']
            disponibility = publish_form.cleaned_data['disponibility']
            time_init = publish_form.cleaned_data['time_init']
            time_end = publish_form.cleaned_data['time_end']

            if not Tutor.objects.filter(usuario=request.user).exists():
                tutor = Tutor(
                    telefono=phone,
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
    Renderiza la página de registro o maneja el proceso de registro de nuevos usuarios.
    
    Si el método es GET, muestra el formulario de registro.
    Si el método es POST, crea un nuevo usuario y estudiante en la base de datos.

    Parameters:
    request (HttpRequest): Información relacionada a la solicitud que se realiza, puede ser un GET o un POST.

    Returns:
    HttpResponse: Página de registro o redirección a la página de inicio de sesión.
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
    Renderiza la página de detalles de un afiche específico.
    
    Si el método es GET, muestra los detalles del afiche.
    Si el método es POST, envía un correo al tutor indicando el interés de un estudiante en la tutoría.

    Parameters:
    request (HttpRequest): Información relacionada a la solicitud que se realiza.
    posterID (int): ID del afiche a mostrar.

    Returns:
    HttpResponse: Página de detalles del afiche.
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

    disponibilidad = publicacion.dicta.tutor.horario.all()[0].dia_semana 
    if(disponibilidad == "LUN"):
        disponibilidad = "Lunes"
    if(disponibilidad == "MAR"):
        disponibilidad = "Martes"
    if(disponibilidad == "MIE"):
        disponibilidad = "Miércoles"
    if(disponibilidad == "JUE"):
        disponibilidad = "Jueves"
    if(disponibilidad == "VIE"):
        disponibilidad = "Viernes"
    if(disponibilidad == "SAB"):
        disponibilidad = "Sábado"
    if(disponibilidad == "DOM"):
        disponibilidad = "Domingo"
    
    disponibilidad = disponibilidad + " o a coordinar"
    data ={
        'titulo': afiche.nombre,
        'imagen': afiche.url.url,
        'descripcion': descripcion,
        'precio': afiche.precio,
        'tutor': publicacion.dicta.tutor.usuario.name,
        'tutorUsername': publicacion.dicta.tutor.usuario.username,
        'telefono': publicacion.dicta.tutor.telefono,
        'modalidad': modalidad,
        'disponibilidad': disponibilidad,
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
            f"Estimado/a {tutorName}, tiene un estudiante interesado en su tutoría: {afiche.nombre} de precio: {afiche.precio}.\nPor favor, contáctelo a la brevedad.\n    Nombre del estudiante: {studentName}\n    Email del estudiante: {studentEmail}",
            emailApp,  
            [emailTutor], 
            fail_silently=False,
        )
        return render(request, "mostrarAfiche.html", data)


def newPassword(request):
    """
    Maneja el proceso de restablecimiento de contraseña para el usuario autenticado.
    
    Si el método es GET, muestra el formulario de restablecimiento de contraseña.
    Si el método es POST, actualiza la contraseña del usuario en la base de datos si las contraseñas coinciden.

    Parameters:
    request (HttpRequest): Información relacionada a la solicitud que se realiza, puede ser un GET o un POST.

    Returns:
    HttpResponse: Página de restablecimiento de contraseña o redirección a la página de inicio de sesión.
    """
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


def profile_view(request, tutorUsername):
    """
    Renderiza la página de perfil de un tutor específico.
    
    Si el usuario autenticado no es el tutor especificado, busca el perfil del tutor.
    Si el tutor existe, obtiene y muestra los afiches publicados por el tutor.
    Si el tutor no existe, muestra un mensaje de error.

    Parameters:
    request (HttpRequest): Información relacionada a la solicitud que se realiza.
    tutorUsername (str): Nombre de usuario del tutor cuyo perfil se desea ver.

    Returns:
    HttpResponse: Página de perfil del tutor.
    """
    user=request.user
    if user.username != tutorUsername:
        try:
            user = Usuario.objects.get(username=tutorUsername)
        except Usuario.DoesNotExist:
            print("Usuario does not exist")  # Debug line
            return HttpResponse("Usuario no existe")

    try:
        tutor = Tutor.objects.get(usuario=user)
        # Obtener todas las publicaciones de afiches de este tutor
        publicaciones = Publica.objects.filter(dicta__tutor=tutor).select_related('afiche')
        afiches = [publicacion.afiche for publicacion in publicaciones]
    except Tutor.DoesNotExist:
        tutor = None
        afiches = None
    return render(request, "profile.html", {'user': user, 'afiches': afiches, 'requesting_user': request.user})


def profile_edit(request):
    """
    Maneja la edición del perfil del usuario autenticado.
    
    Si el método es GET, muestra el formulario de edición de perfil con los datos actuales del usuario.
    Si el método es POST, actualiza la información del perfil del usuario en la base de datos si el formulario es válido.

    Parameters:
    request (HttpRequest): Información relacionada a la solicitud que se realiza, puede ser un GET o un POST.

    Returns:
    HttpResponse: Página de perfil actualizada o redirección a la página de inicio de sesión si no está autenticado.
    """
    user=request.user
    if not user.is_authenticated:
        return redirect('login')  # Redirige a la página de inicio de sesión si no está autenticado

    if request.method == "GET":
        editProfile_form = EditProfileForm(initial={'name': user.name, 'username': user.username, 'email': user.email})
        return render(request, "profile_config.html", {"editProfile_form": editProfile_form})
    
    elif request.method == "POST":
        editProfile_form = EditProfileForm(request.POST)

        if editProfile_form.is_valid():
            name = editProfile_form.cleaned_data['name']
            username = editProfile_form.cleaned_data['username']
            email = editProfile_form.cleaned_data['email']
            user.name = name
            user.username = username
            user.email = email
            user.save()
            return render(request ,"profile.html", {'user': user})