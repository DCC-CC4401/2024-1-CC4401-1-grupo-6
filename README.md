# 2024-1-CC4401-1-grupo-6

Crear ambiente virtual con:
```
python -m venv ing_software
```

Para activarlo se debe ir a la carpeta del ambiente virtual, Scripts y luego hacer ./activate

```
cd ing_software/Scripts
./activate
```

Luego, cuando alguien descargue el proyecto, y ya tenga ACTIVADO su ambiente virtual, en lugar de instalar Django u otras librerías a mano, debe hacer:

```
pip install -r requirements.txt
```