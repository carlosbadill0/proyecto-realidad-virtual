from django import forms
from .models import Usuario, Practicante

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre_usuario', 'apellidoP_usuario', 'apellidoM_usuario', 'email_usuario', 'password_usuario', 'id_rol']


class PracticanteForm(forms.ModelForm):
    class Meta:
        model = Practicante
        fields = ['nombre_usuario', 'apellidoP_usuario', 'apellidoM_usuario', 'fecha_ingreso']
