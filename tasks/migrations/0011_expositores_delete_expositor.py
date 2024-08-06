# Generated by Django 5.0.6 on 2024-08-06 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0010_expositor_carrera_expositor_edad_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expositores',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('fecha_ingreso', models.DateField()),
                ('fecha_nacimiento', models.DateField()),
                ('edad', models.IntegerField()),
                ('genero', models.CharField(max_length=10)),
                ('semestre_academico', models.IntegerField()),
                ('carrera', models.CharField(max_length=100)),
                ('observacion_inicial', models.TextField()),
                ('observacion_final', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Expositor',
        ),
    ]
