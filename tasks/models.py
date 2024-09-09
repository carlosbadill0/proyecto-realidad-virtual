from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def create_user_roles(sender, **kwargs):
    admin_group, created = Group.objects.get_or_create(name='Administrador')
    evaluator_group, created = Group.objects.get_or_create(name='Evaluador')

    # Asigna permisos al grupo administrador
    admin_permissions = Permission.objects.all()
    admin_group.permissions.set(admin_permissions)

    # Asigna permisos específicos al grupo evaluador
    evaluator_permissions = [
        'add_evaluacion',
        'change_evaluacion',
        'view_evaluacion',
        # Añade otros permisos necesarios
    ]
    evaluator_group.permissions.set(Permission.objects.filter(codename__in=evaluator_permissions))
# Create your models here.

CASOS_ESTRES_CHOICES = [
        ('caso1', 'Caso 1'),
        ('caso2', 'Caso 2'),
    ]

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
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha = models.DateField()

    def __str__(self):
        return f'Evaluación por {self.nombre_evaluador} el {self.fecha_evaluacion}'
    
    
class DisenarEvaluacion(models.Model):
    nombre_evaluacion = models.CharField(max_length=100)
    casos_estres = models.CharField(max_length=50, choices=CASOS_ESTRES_CHOICES)    
    
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


class Expositores(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_ingreso = models.DateField()  
    fecha_nacimiento = models.DateField()  
    edad = models.IntegerField()
    genero = models.CharField(max_length=10)
    semestre_academico = models.IntegerField()  
    carrera = models.CharField(max_length=100)
    observacion_inicial = models.TextField()
    observacion_final = models.TextField(default= 'sin información')


    def __str__(self):
        return f"{self.nombre}" 
    
class ECGData(models.Model):
    expositor = models.ForeignKey(Expositores, on_delete=models.CASCADE, default=1, related_name='ecg_data')
    timestamp = models.DateTimeField(auto_now_add=True)
    value = models.FloatField()

    def __str__(self):
        return f"{self.timestamp}: {self.value}"