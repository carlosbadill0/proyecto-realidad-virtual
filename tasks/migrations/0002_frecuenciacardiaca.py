# Generated by Django 5.0.6 on 2024-07-03 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FrecuenciaCardiaca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frecuencia', models.FloatField()),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
