from django.db import models
from django.contrib.auth.models import AbstractUser
import json


# ------------- ENTIDADES -------------
"""
Una clase que representa un usuario
Extiende del usuario nativo de Django.
parametro Abstractuser El usuario nativo de Django
Campo: name de tipo TextField
VersionInicial 1.0.0
VersionActual 1.0.0
"""
class Usuario(AbstractUser):
    name = models.TextField(blank=True, null=True)

"""
Una clase que representa un estudiante
El estudiante guarda sus cursos cursados y de interes
Campo: tutorias_cursadas de tipo TextField
Campo: cursos_de_interes de tipo TextField
Campo: usuario de tipo OneToOneField
VersionInicial 1.0.0
VersionActual 1.0.0
"""
class Estudiante(models.Model):
    tutorias_cursadas = models.TextField(blank=True, null=True)
    cursos_de_interes = models.TextField(blank=True, null=True)
    # Si se borra la instancia de Usuario id=1 (y este era un estudiante) este es borrado también de la database
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)

    # ----- SINGLE VERSION -----
    # Que estas sean de tipo Charfield es opcional, ya que podrían ser una lista
    # tutorias_cursadas = models.CharField(max_length=100)
    # cursos_de_interes = models.CharField(max_length=100)

    # ----- MULTIPLE VERSION -----
    """
    Actualiza tutorias cursadas (que hace)
    se serializa la lista (values) a un objeto de tipo json y la guardamos en tutorias_cursadas
    parametro self -> hace referencia al conenido del objeto asociado
    sin necesidad de hacer una referencia explícita del objeto
    parametro values -> una lista de las tutorias cursadas
    """
    def set_tutorias_cursadas(self, values):
        self.tutorias_cursadas = json.dumps(values)
    
    """
    Actualiza cursos de interes
    se serializa la lista (values) a un objeto de tipo json y la guardamos en cursos_de_interes
    parametro self -> referencia al contenido del objeto asociado
    parametro values -> una lista de las tutorias cursadas
    """
    def set_cursos_de_interes(self, values):
        self.cursos_de_interes = json.dumps(values)
    
    """
    Retorna las tutorias cursadas del estudiante
    se cargan las tutorias cursadas en un archivo tipo json y las de vuelve,
    en caso de no haber cursado cursos devuelve una lista vacia
    parametro self -> referencia al contenido del objeto asociado
    """
    def get_tutorias_cursadas(self):
        return json.loads(self.tutorias_cursadas) if self.tutorias_cursadas else []

    """
    Retorna los cursos de interes del estudiante
    se cargan los cursos de interes en un archivo tipo json y las de vuelve,
    en caso de no haber cursado cursos devuelve una lista vacia
    parametro self -> referencia al contenido del objeto asociado
    """
    def get_cursos_de_interes(self):
        return json.loads(self.cursos_de_interes) if self.cursos_de_interes else []

"""
Una clase que representa un Horario
El Horario contiene los dias de las semanas
Campo: DIA_SEMANA_CHOICES de tipo Choices
Campo: dia_semana de tipo CharField
Campo: hora_inicio de tipo TimeField
Campo: hora_fin de tipo TimeField
VersionInicial 1.0.0
VersionActual 1.0.0
"""
class Horario(models.Model):
    DIA_SEMANA_CHOICES = [
        ("LUN", "Lunes"),
        ("MAR", "Martes"),
        ("MIE", "Miércoles"),
        ("JUE", "Jueves"),
        ("VIE", "Viernes"),
        ("SAB", "Sábado"),
        ("DOM", "Domingo"),
    ]

    dia_semana = models.CharField(max_length=3, choices=DIA_SEMANA_CHOICES)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

# tipos de modalidad (se puede elegir remota o presencial)
modalidad_choices = [("rem", "remota"), ("pres", "presencial")]

"""
Una clase que representa un Tutor
El tutor guarda su telefono, precio, modalidad preferida y horario
Campo: telefono de tipo IntegerField
Campo: precio de tipo IntegerField
Campo: modalidad_preferida de tipo CharField
Campo: horario de tipo ManyToManyField
VersionInicial 1.0.0
VersionActual 1.0.0
"""
class Tutor(models.Model):

    telefono = models.IntegerField(editable=True)
    precio = models.IntegerField(editable=True)
    modalidad_preferida = models.CharField(
        choices=modalidad_choices, editable=True, max_length=200
    )
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)

    # ----- SINGLE VERSION -----
    # Que estas sean de tipo Charfield es opcional, ya que podrían ser una lista
    # horario = models.CharField(max_length=100)

    # ----- MULTIPLE VERSION -----
    horario = models.ManyToManyField(Horario)

"""
Una clase que representa una Materia
La materia guarda su codigo de curso y su nombre
Campo: codigo_curso de tipo CharField
Campo: nombre de tipo CharField
VersionInicial 1.0.0
VersionActual 1.0.0
"""
class Materia(models.Model):
    codigo_curso = models.CharField(primary_key=True, max_length=200)
    nombre = models.CharField(max_length=200)

"""
Una clase que representa un Afiche
El Afiche guarda su url y descripcion
Campo: url de tipo CharField
Campo: desacripcion de tipo CharField
VersionInicial 1.0.0
VersionActual 1.0.0
"""
class Afiche(models.Model):
    url = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=200)
    #Pendiente
    nombre = models.CharField(max_length=200)

"""
Una clase que representa una tutoria
La tutoria guarda el estudiante, el tutor, la fecha, el curso, la duracion, la modalildad y la sala
Campo: estudiante de tipo ForeignKey
Campo: tutor de tipo ForeignKey
Campo: fecha de tipo DateTimeField
Campo: curso de tipo ForeignKey
Campo: duracion de tipo IntegerField
Campo: modalildad de tipo CharField
Campo: sala de tipo CharField
VersionInicial 1.0.0
VersionActual 1.0.0
"""
# ------------- RELACIONES -------------
class Tutoria(models.Model):
    # Quienes relaciona
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)

    fecha = models.DateTimeField()
    curso = models.ForeignKey(Materia, on_delete=models.CASCADE)
    duracion = models.IntegerField(default=0, help_text="ingrese minutos")
    modalidad = models.CharField(choices=modalidad_choices, max_length=200)
    sala = models.CharField(max_length=200)

"""
Una clase que representa quien Dicta una mateira
se guarda el tutor y la materia
Campo: tutor de tipo ForeignKey
Campo: materia de tipo ForeignKey
VersionInicial 1.0.0
VersionActual 1.0.0
"""
class Dicta(models.Model):
    # Quienes relaciona
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)

"""
Una clase que representa una publicación
se guarda la persona que dicata el afiche y la fecha
Campo: dicta de tipo ForeignKey
Campo: afiche de tipo ForeignKey
Campo: fecha de tipo DateTimeField
VersionInicial 1.0.0
VersionActual 1.0.0
"""
class Publica(models.Model):
    # Quienes relaciona
    dicta = models.ForeignKey(Dicta, on_delete=models.CASCADE)
    afiche = models.ForeignKey(Afiche, on_delete=models.CASCADE)

    fecha = models.DateTimeField(auto_now_add=True)
