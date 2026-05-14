from django import forms
from .models import Place, VisitIdea


class PlaceForm(forms.Form):
    nombre = forms.CharField(max_length=200, label='Nombre del lugar')
    ubicacion = forms.CharField(max_length=100, required=False, label='Ubicación')
    km = forms.CharField(max_length=100, required=False, label='Km')
    descripcion = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        label='Descripción'
    )
    imagen = forms.ImageField(required=False, label='Imagen')
    fecha_visita = forms.DateField(
        required=False,
        label='Fecha de visita',
        widget=forms.DateInput(attrs={'type': 'date'})
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

    lugar = forms.ModelChoiceField(queryset=Place.objects.all(), label='Lugar')
    estado = forms.ChoiceField(choices=ESTADO_CHOICES, label='Estado')
    prioridad = forms.ChoiceField(choices=PRIORIDAD_CHOICES, label='Prioridad')
    notas = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        required=False,
        label='Notas'
    )

    def clean(self):
        cleaned_data = super().clean()
        estado = cleaned_data.get('estado')
        notas = cleaned_data.get('notas')
        if estado == 'planificado' and not notas:
            raise forms.ValidationError('Para pasar a "Planificado" es necesario agregar notas.')
        return cleaned_data
    