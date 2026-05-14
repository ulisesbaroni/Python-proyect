from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Perfil


class RegistroForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'tu@email.com'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nombre de usuario'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Contraseña'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Repetí la contraseña'})


class EditarUsuarioForm(forms.Form):
    first_name = forms.CharField(
        max_length=100,
        required=False,
        label='Nombre',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre'})
    )
    last_name = forms.CharField(
        max_length=100,
        required=False,
        label='Apellido',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu apellido'})
    )
    email = forms.EmailField(
        required=False,
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'tu@email.com'})
    )
    experiencia = forms.CharField(
        max_length=100,
        required=False,
        label='Experiencia',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Viajero frecuente'})
    )
    avatar = forms.ImageField(
        required=False,
        label='Avatar',
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )