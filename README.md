# Project Aprende Beauchef / 2024-1-CC4401-1-grupo-6

Cada año en el foro de la facultad y las redes sociales, cientos de jóvenes buscan un/a tutor/a para reforzar sus estudios, sin embargo, las ofertas de servicios que se publican se pierden en la inmensidad de mensajes en las plataformas ocasionando a los estudiantes la dificultad en encontrar tutores y a los tutores, estudiantes. 

Como solución a este problema, se propone la creación de una aplicación donde tanto estudiantes como tutores puedan satisfacer sus necesidades las cuales se reflejan en las siguiente historias de usuario:

"Como estudiante quiero ver las ofertas de clases particulares para reforzar mis estudios"
"Como tutor quiero ofrecer mis servicios para ayudar a los estudiantes y ganar dinero"
"Como estudiante quiero comparar tutores para encontrar el que más me conviene"
"Como tutor quiero informar mis horarios para dar a conocer mi disponibilidad"

En este Sprint 1, solo se abordarán las primeras dos.

## Data models

Se usó el siguiente modelo Entidad-Relación para la base de datos y su modelado:

![Modelo Entidad-Relacion](/readme_assets/modeloEntidadRelacion.png  "Modelo Entidad Relacion")

## Run the page

Crear ambiente virtual con:
```
python -m venv ing_software
```

Para activarlo se debe ejecutar el siguiente comando:

```
./ing_software/Scripts/activate
```

Luego, al clonar el repositorio, teniendo **ACTIVADO** el ambiente virtual, para facilitar la compatibilidad de librerias, ejecutar el siguiente comando:

```
pip install -r requirements.txt
```

Finalmente para ejecutar el proyecto, estando dentro de la carpeta del proyecto "aprende_beauchef":
```
python manage.py runserver 
```

**Observación:** Puede ocurrir que al ejecutar el comando anterior no se hayan aplicado las migraciones necesarias (configuración de la base de datos) no permitiendo ejecutar run, en ese caso se deben ingresar por consola los siguientes comandos:

```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Visualize the database 
Creación de superusuario en entornos locales: Cada miembro del equipo deberá crear su propio superusuario localmente después de configurar su entorno de desarrollo. Con las migraciones actualizadas, esto se hace fácilmente con el comando: 

```
python manage.py createsuperuser
```

Usando su admin panel se puede visualizar la base de datos y los datos que allí se almacenan.

## Tests 
Para correr los tests de models que ya se encuentran creados en la carpeta tests, se usa el siguiente comando:
```
python manage.py test baseapp.tests.test_models
```

## Aclaraciones
La rama que contiene el Sprint 1 está en develop, la rama main tendrá el proyeto final luego tener terminado tanto el Sprint 1 como el 2. Después de la revisión de este Sprint, se borrarán la mayoría de las ramas pues ya habrán cumplido con su función y así el repositorio estará más ordenado.
Con respecto a los commits, al inicio no se contaba con un formato determinado y eran genéricos, después el equipo aprendió a realizar descripciones más específicas y decidió la siguiente convención utilizando las palabras claves aprendidas en el Auxiliar 0:

PALABRACLAVE: descripcion en ingles en presente
