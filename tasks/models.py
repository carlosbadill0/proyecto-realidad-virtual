from django.db import models # type: ignore
from django.contrib.auth.models import User # type: ignore
from django.contrib.auth.models import Group, Permission # type: ignore
from django.db.models.signals import post_migrate # type: ignore
from django.dispatch import receiver # type: ignore
from django import forms # type: ignore
from django.core.exceptions import ValidationError # type: ignore

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
 
class Scenario(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    function_name = models.CharField(max_length=100)
    tag_name = models.CharField(max_length=50)
    duration = models.IntegerField()

    def __str__(self):
        return f"{self.function_name} ({self.tag_name}) - {self.duration} mins"       
    
class CasoDeEstres(models.Model):
    expositor = models.ForeignKey(Expositores, on_delete=models.CASCADE, default=1, related_name='casos_de_estres')
    simulation_id = models.CharField(max_length=50)
    date = models.DateField()
    duration = models.DurationField()
    scene = models.CharField(max_length=100)
    description = models.TextField()
    scenarios = models.ManyToManyField(Scenario)

    def __str__(self):
        return f"{self.simulation_id}: {self.scene} - {self.duration}"     
 
    

class Evaluacion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha = models.DateField()
    casos_de_estres = models.ManyToManyField(CasoDeEstres, related_name='evaluaciones')

    def clean(self):
        # Validar que la evaluación tenga al menos 4 y como máximo 8 casos de estrés
        if not (4 <= self.casos_de_estres.count() <= 8):
            raise ValidationError('Una evaluación debe tener entre 4 y 8 casos de estrés.')

        # Validar que la duración total de la evaluación no exceda 2 minutos
        total_duration = sum(caso.duration.total_seconds() for caso in self.casos_de_estres.all()) / 60  # convertimos a minutos
        if total_duration > 2:
            raise ValidationError('La duración total de los casos de estrés no puede exceder los 2 minutos.')

    def __str__(self):
        return f'Evaluación por {self.nombre} el {self.fecha}'
    
    
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






class ECGData(models.Model):
    expositor = models.ForeignKey(Expositores, on_delete=models.CASCADE, default=1, related_name='ecg_data')
    timestamp = models.DateTimeField(auto_now_add=True)
    value = models.FloatField()

    def __str__(self):
        return f"{self.timestamp}: {self.value}"

