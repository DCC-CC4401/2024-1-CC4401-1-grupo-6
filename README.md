# 2024-1-CC4401-1-grupo-6

## Project Aprende Beauchef

Usamos el siguiente modelo Entidad-Relación para la base de datos y su modelado:

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

Luego, cuando alguien descargue el proyecto, y ya tenga ACTIVADO su ambiente virtual, en lugar de instalar Django u otras librerías a mano, debe hacer:

```
pip install -r requirements.txt
```

## Testing the app and visualize the database 
Creación de superusuario en entornos locales: Cada miembro del equipo deberá crear su propio superusuario localmente después de configurar su entorno de desarrollo. Esto se hace fácilmente con el comando: 

```
python manage.py createsuperuser.
```

Usando su admin panel se puede visualizar la base de datos y los datos que allí almacenamos.


Para correr los tests de models que ya se encuentran creados en la carpeta tests, se usa el siguiente comando:
```
python manage.py test baseapp.tests.test_models
```