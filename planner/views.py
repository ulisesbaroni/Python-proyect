from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Place, VisitIdea
from .forms import PlaceForm, VisitIdeaForm


class HomeView(View):
    def get(self, request):
        return render(request, 'home/index.html')


# -- Place views --

class PlaceListView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        busqueda = request.GET.get('busqueda', '')
        places = Place.objects.filter(nombre__icontains=busqueda) if busqueda else Place.objects.all()
        return render(request, 'planner/place_list.html', {'places': places, 'busqueda': busqueda})


class PlaceCreateView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        form = PlaceForm()
        return render(request, 'planner/place_form.html', {'form': form, 'accion': 'Crear'})

    def post(self, request):
        form = PlaceForm(request.POST, request.FILES)
        if form.is_valid():
            Place.objects.create(
                nombre=form.cleaned_data['nombre'],
                ubicacion=form.cleaned_data['ubicacion'],
                km=form.cleaned_data['km'],
                descripcion=form.cleaned_data['descripcion'],
                imagen=form.cleaned_data.get('imagen'),
                fecha_visita=form.cleaned_data.get('fecha_visita'),
            )
            return redirect('place_list')
        return render(request, 'planner/place_form.html', {'form': form, 'accion': 'Crear'})


class PlaceEditView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, pk):
        place = get_object_or_404(Place, pk=pk)
        form = PlaceForm(initial={
            'nombre': place.nombre,
            'ubicacion': place.ubicacion,
            'km': place.km,
            'descripcion': place.descripcion,
            'fecha_visita': place.fecha_visita,
        })
        return render(request, 'planner/place_form.html', {'form': form, 'accion': 'Editar'})

    def post(self, request, pk):
        place = get_object_or_404(Place, pk=pk)
        form = PlaceForm(request.POST, request.FILES)
        if form.is_valid():
            place.nombre = form.cleaned_data['nombre']
            place.ubicacion = form.cleaned_data['ubicacion']
            place.km = form.cleaned_data['km']
            place.descripcion = form.cleaned_data['descripcion']
            place.fecha_visita = form.cleaned_data.get('fecha_visita')
            if form.cleaned_data.get('imagen'):
                place.imagen = form.cleaned_data['imagen']
            place.save()
            return redirect('place_list')
        return render(request, 'planner/place_form.html', {'form': form, 'accion': 'Editar'})


class PlaceDetailView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, pk):
        place = get_object_or_404(Place, pk=pk)
        return render(request, 'planner/place_detail.html', {'place': place})


class PlaceDeleteView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, pk):
        place = get_object_or_404(Place, pk=pk)
        return render(request, 'planner/place_confirm_delete.html', {'place': place})

    def post(self, request, pk):
        place = get_object_or_404(Place, pk=pk)
        place.delete()
        return redirect('place_list')


# -- VisitIdea views --

class VisitIdeaListView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        ideas = VisitIdea.objects.filter(usuario=request.user)

        busqueda = request.GET.get('busqueda', '')
        estado = request.GET.get('estado', '')
        km = request.GET.get('km', '')

        if busqueda:
            ideas = ideas.filter(lugar__nombre__icontains=busqueda)
        if estado:
            ideas = ideas.filter(estado=estado)
        if km:
            ideas = ideas.filter(lugar__km__icontains=km)

        estados = VisitIdea.ESTADO_CHOICES
        kms = Place.objects.values_list('km', flat=True).distinct().exclude(km__isnull=True).exclude(km='')

        ideas_por_estado = {}
        for codigo, nombre in VisitIdea.ESTADO_CHOICES:
            ideas_por_estado[nombre] = ideas.filter(estado=codigo)

        return render(request, 'planner/visitidea_list.html', {
            'ideas': ideas,
            'ideas_por_estado': ideas_por_estado,
            'estados': estados,
            'kms': kms,
            'busqueda': busqueda,
            'estado_activo': estado,
            'km_activo': km,
        })


class VisitIdeaCreateView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        form = VisitIdeaForm()
        return render(request, 'planner/visitidea_form.html', {'form': form, 'accion': 'Crear'})

    def post(self, request):
        form = VisitIdeaForm(request.POST)
        if form.is_valid():
            VisitIdea.objects.create(
                usuario=request.user,
                lugar=form.cleaned_data['lugar'],
                estado=form.cleaned_data['estado'],
                prioridad=form.cleaned_data['prioridad'],
                notas=form.cleaned_data['notas'],
            )
            return redirect('visitidea_list')
        return render(request, 'planner/visitidea_form.html', {'form': form, 'accion': 'Crear'})


class VisitIdeaEditView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, pk):
        idea = get_object_or_404(VisitIdea, pk=pk, usuario=request.user)
        form = VisitIdeaForm(initial={
            'lugar': idea.lugar,
            'estado': idea.estado,
            'prioridad': idea.prioridad,
            'notas': idea.notas,
        })
        return render(request, 'planner/visitidea_form.html', {'form': form, 'accion': 'Editar', 'idea': idea})

    def post(self, request, pk):
        idea = get_object_or_404(VisitIdea, pk=pk, usuario=request.user)
        form = VisitIdeaForm(request.POST)
        if form.is_valid():
            idea.lugar = form.cleaned_data['lugar']
            idea.estado = form.cleaned_data['estado']
            idea.prioridad = form.cleaned_data['prioridad']
            idea.notas = form.cleaned_data['notas']
            idea.save()
            return redirect('visitidea_list')
        return render(request, 'planner/visitidea_form.html', {'form': form, 'accion': 'Editar', 'idea': idea})


class VisitIdeaDetailView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, pk):
        idea = get_object_or_404(VisitIdea, pk=pk, usuario=request.user)
        return render(request, 'planner/visitidea_detail.html', {'idea': idea})
    