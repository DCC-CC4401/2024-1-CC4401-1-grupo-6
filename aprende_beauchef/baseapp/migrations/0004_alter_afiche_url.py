# Generated by Django 5.0.4 on 2024-05-21 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseapp', '0003_afiche_nombre_alter_publica_fecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='afiche',
            name='url',
            field=models.FileField(upload_to='uploads/'),
        ),
    ]
