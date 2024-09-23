from xml.dom import ValidationErr
from django import forms # type: ignore
from .models import Usuario, Practicante, DisenarEvaluacion,Evaluacion,EvaluacionRealizada ,Expositores, CasoDeEstres, Scenario
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
        fields = ['nombre', 'descripcion', 'fecha', 'scenarios']
        widgets = {
            'scenarios': forms.CheckboxSelectMultiple,
        }

    def clean_scenarios(self):
        scenarios = self.cleaned_data.get('scenarios')
        # if not (4 <= len(scenarios) <= 8):
        #     raise ValidationErr('Debe seleccionar entre 4 y 8 escenarios.')

        # total_duration = sum(scenario.duration.total_seconds() for scenario in scenarios)
        # if total_duration > 120:
        #     raise ValidationErr('La duración total de los escenarios no debe exceder los 2 minutos.')

        return scenarios

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

<<<<<<< HEAD
class UserForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True, label="Rol")

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'group']
=======
class EvaluacionRealizadaForm(forms.ModelForm):
    class Meta:
        model = EvaluacionRealizada
        fields = [
            'expositor',
            'nombre_evaluador',
            'fecha_evaluacion',
            'observacion_inicial',
            'observacion_final',
            'tiempo_exposicion',
            'video_evaluacion',
            'evaluacion_aplicada'
        ]        
    
>>>>>>> 9d075d6f26881bf912b021697bbe6063b94c1531
