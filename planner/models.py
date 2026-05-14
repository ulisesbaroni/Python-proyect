from django.db import models
from django.contrib.auth.models import User


class Place(models.Model):
    nombre = models.CharField(max_length=200)
    ubicacion = models.CharField(max_length=100, blank=True, null=True)
    km = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    imagen = models.ImageField(upload_to='lugares/', blank=True, null=True)
    fecha_visita = models.DateField(blank=True, null=True)

    def __str__(self):
        if self.ubicacion:
            return f'{self.nombre} - {self.ubicacion}'
        return self.nombre

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Lugar'
        verbose_name_plural = 'Lugares'


class VisitIdea(models.Model):
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

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    lugar = models.ForeignKey(Place, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='idea')
    prioridad = models.CharField(max_length=10, choices=PRIORIDAD_CHOICES, default='media')
    notas = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.lugar.nombre} ({self.get_estado_display()}) - {self.usuario.username}'

    class Meta:
        ordering = ['-fecha_actualizacion']
        verbose_name = 'Idea de visita'
        verbose_name_plural = 'Ideas de visita'