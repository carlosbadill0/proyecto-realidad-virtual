from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    dateCompleted = models.DateTimeField(null=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title + '- by ' + self.user.username
    

class FrecuenciaCardiaca(models.Model):
    frecuencia = models.FloatField()
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Frecuencia Cardíaca: {self.frecuencia} BPM'
    
class Evaluation(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Evaluacion(models.Model):
    tiempo_exposicion = models.CharField(max_length=20)
    fecha_evaluacion = models.DateField()
    nombre_evaluador = models.CharField(max_length=100)
    observaciones = models.TextField()

    def __str__(self):
        return f'Evaluación por {self.nombre_evaluador} el {self.fecha_evaluacion}'
    
# codigo lucho 
class Rol(models.Model):
    nombre_rol = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre_rol


class Usuario(models.Model):
    nombre_usuario = models.CharField(max_length=255)
    apellidoP_usuario = models.CharField(max_length=255)
    apellidoM_usuario = models.CharField(max_length=255)
    email_usuario = models.EmailField(max_length=255)
    password_usuario = models.CharField(max_length=255)
    id_rol = models.ForeignKey(Rol, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre_usuario} {self.apellidoP_usuario} {self.apellidoM_usuario}"

class Practicante(models.Model):
    nombre_usuario = models.CharField(max_length=255)
    apellidoP_usuario = models.CharField(max_length=255)
    apellidoM_usuario = models.CharField(max_length=255)
    fecha_ingreso = models.DateField()
    observacionInicial = models.CharField(max_length=255)
    observacionFinal = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.nombre_usuario} {self.apellidoP_usuario} {self.apellidoM_usuario} {self.fecha_ingreso} {self.observacionInicial} {self.observacionFinal}"
