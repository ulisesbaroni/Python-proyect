from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Perfil


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class EditarUsuarioForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=False, label='Nombre')
    last_name = forms.CharField(max_length=100, required=False, label='Apellido')
    email = forms.EmailField(required=False, label='Email')
    experiencia = forms.CharField(max_length=100, required=False, label='Experiencia')
    avatar = forms.ImageField(required=False, label='Avatar')