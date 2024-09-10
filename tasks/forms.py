from django import forms # type: ignore
from .models import Usuario, Practicante, DisenarEvaluacion,Evaluacion, Expositores, CasoDeEstres, Scenario
from django.contrib.auth.models import User, Group # type: ignore
from django.db import models # type: ignore

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    group = forms.ModelChoiceField(queryset=Group.objects.all())
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'group']

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
        fields = ['nombre', 'descripcion', 'fecha', 'casos_de_estres']

    def clean_casos_de_estres(self):
        casos_de_estres = self.cleaned_data['casos_de_estres']
        
        # Validar el número de casos de estrés
        if not (4 <= casos_de_estres.count() <= 8):
            raise forms.ValidationError('La evaluación debe tener entre 4 y 8 casos de estrés.')

        # Validar que la duración total de los casos de estrés no exceda 2 minutos
        total_duration = sum(caso.duration.total_seconds() for caso in casos_de_estres) / 60  # convertimos a minutos
        if total_duration > 2:
            raise forms.ValidationError('La duración total de los casos de estrés no puede exceder los 2 minutos.')
        
        return casos_de_estres

class ExpositorForm(forms.ModelForm):
    class Meta:
        model = Expositores
        fields = [
            'nombre', 'fecha_ingreso', 'fecha_nacimiento', 'edad', 
            'genero', 'semestre_academico', 'carrera', 'observacion_inicial', 'observacion_final'
        ]

class CasoDeEstresForm(forms.ModelForm):
    class Meta:
        model = CasoDeEstres
        fields = [
            'simulation_id', 'date', 'duration', 'scene', 'description', 'scenarios'
        ]

class ScenarioForm(forms.ModelForm):
    class Meta:
        model = Scenario
        fields = [
            'id', 'function_name', 'tag_name', 'duration'
        ]     
    