from django.test import TestCase
from baseapp.models import Usuario, Estudiante


class EstudianteTestCase(TestCase):
    def setUp(self):
        usuario = Usuario.objects.create_user(username="testuser", password="12345")
        Estudiante.objects.create(
            usuario=usuario, tutorias_cursadas="[]", cursos_de_interes="[]"
        )

    def test_estudiante_creation(self):
        usuario = Usuario.objects.get(username="testuser")
        estudiante = Estudiante.objects.get(usuario=usuario)
        self.assertEqual(estudiante.usuario.username, "testuser")
