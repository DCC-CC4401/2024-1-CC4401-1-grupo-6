from django.db import models
from django.contrib.auth.models import AbstractUser
import json


# ------------- ENTIDADES -------------
class Usuario(AbstractUser):
    pass


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
    def set_tutorias_cursadas(self, values):
        self.tutorias_cursadas = json.dumps(values)

    def set_cursos_de_interes(self, values):
        self.cursos_de_interes = json.dumps(values)

    def get_tutorias_cursadas(self):
        return json.loads(self.tutorias_cursadas) if self.tutorias_cursadas else []

    def get_cursos_de_interes(self):
        return json.loads(self.cursos_de_interes) if self.cursos_de_interes else []


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


modalidad_choices = [("rem", "remota"), ("pres", "presencial")]


class Tutor(models.Model):

    telefono = models.IntegerField(editable=True)
    precio = models.IntegerField(editable=True)
    modalidad_preferida = models.CharField(choices=modalidad_choices, editable=True, max_length=200)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)

    # ----- SINGLE VERSION -----
    # Que estas sean de tipo Charfield es opcional, ya que podrían ser una lista
    # horario = models.CharField(max_length=100)

    # ----- MULTIPLE VERSION -----
    horario = models.ManyToManyField(Horario)


class Materia(models.Model):
    codigo_curso = models.CharField(primary_key=True, max_length=200)
    nombre = models.CharField(max_length=200)


class Afiche(models.Model):
    url = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=200)


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


class Dicta(models.Model):
    # Quienes relaciona
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)


class Publica(models.Model):
    # Quienes relaciona
    dicta = models.ForeignKey(Dicta, on_delete=models.CASCADE)
    afiche = models.ForeignKey(Afiche, on_delete=models.CASCADE)

    fecha = models.DateTimeField()
