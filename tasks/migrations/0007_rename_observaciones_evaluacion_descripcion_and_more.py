# Generated by Django 5.0.6 on 2024-07-31 03:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_disenarevaluacion_evaluacion_casos_estres'),
    ]

    operations = [
        migrations.RenameField(
            model_name='evaluacion',
            old_name='observaciones',
            new_name='descripcion',
        ),
        migrations.RenameField(
            model_name='evaluacion',
            old_name='fecha_evaluacion',
            new_name='fecha',
        ),
        migrations.RenameField(
            model_name='evaluacion',
            old_name='nombre_evaluador',
            new_name='nombre',
        ),
        migrations.RemoveField(
            model_name='evaluacion',
            name='casos_estres',
        ),
        migrations.RemoveField(
            model_name='evaluacion',
            name='tiempo_exposicion',
        ),
    ]
