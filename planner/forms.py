from django import forms
from .models import Place, VisitIdea


class PlaceForm(forms.Form):
    nombre = forms.CharField(
        max_length=200,
        label='Nombre del lugar',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Cascada del Río'})
    )
    ubicacion = forms.CharField(
        max_length=100,
        required=False,
        label='Ubicación',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Sierra de Córdoba'})
    )
    km = forms.CharField(
        max_length=100,
        required=False,
        label='Km desde casa',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 45'})
    )
    descripcion = forms.CharField(
        required=False,
        label='Descripción',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Contá algo sobre este lugar...'})
    )
    imagen = forms.ImageField(
        required=False,
        label='Imagen',
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    fecha_visita = forms.DateField(
        required=False,
        label='Fecha de visita',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )


class VisitIdeaForm(forms.Form):
    ESTADO_CHOICES = [
        ('idea', 'Idea'),
        ('investigando', 'Investigando'),
        ('planificado', 'Planificado'),
        ('listo', 'Listo'),
        ('descartado', 'Descartado'),
    ]

    PRIORIDAD_CHOICES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
    ]

    lugar = forms.ModelChoiceField(
        queryset=Place.objects.all(),
        label='Lugar',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    estado = forms.ChoiceField(
        choices=ESTADO_CHOICES,
        label='Estado',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    prioridad = forms.ChoiceField(
        choices=PRIORIDAD_CHOICES,
        label='Prioridad',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    notas = forms.CharField(
        required=False,
        label='Notas',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Anotá lo que necesitás recordar...'})
    )

    def clean(self):
        cleaned_data = super().clean()
        estado = cleaned_data.get('estado')
        notas = cleaned_data.get('notas')
        if estado == 'planificado' and not notas:
            raise forms.ValidationError('Para pasar a "Planificado" es necesario agregar notas.')
        return cleaned_data