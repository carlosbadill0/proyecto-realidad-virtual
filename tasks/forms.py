from django import forms
from .models import Usuario, Practicante, DisenarEvaluacion,Evaluacion, Expositores
from django.contrib.auth.models import User, Group

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    group = forms.ModelChoiceField(queryset=Group.objects.all())
    class Meta:
        model = User
        fields = ['username', 'password', 'group']

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre_usuario', 'apellidoP_usuario', 'apellidoM_usuario', 'email_usuario', 'password_usuario', 'id_rol']


class PracticanteForm(forms.ModelForm):
    class Meta:
        model = Practicante
        fields = ['nombre_usuario', 'apellidoP_usuario', 'apellidoM_usuario', 'fecha_ingreso']

class EvaluacionForm(forms.ModelForm):
    class Meta:
        model = Evaluacion
        fields = ['nombre', 'descripcion', 'fecha']

class ExpositorForm(forms.ModelForm):
    class Meta:
        model = Expositores
        fields = [
            'nombre', 'fecha_ingreso', 'fecha_nacimiento', 'edad', 
            'genero', 'semestre_academico', 'carrera', 'observacion_inicial'
        ]

class ExpositorEditForm(forms.ModelForm):
    class Meta:
        model = Expositores
        fields = [
            'nombre', 'fecha_ingreso', 'fecha_nacimiento', 'edad', 
            'genero', 'semestre_academico', 'carrera', 'observacion_inicial', 
            'observacion_final'
        ]