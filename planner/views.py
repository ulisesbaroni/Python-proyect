from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Place, VisitIdea
from .forms import PlaceForm, VisitIdeaForm


class HomeView(View):
    def get(self, request):
        total = VisitIdea.objects.filter(usuario=request.user).count() if request.user.is_authenticated else 0
        return render(request, 'planner/home.html', {'total': total})


class VisitIdeaListView(LoginRequiredMixin, View):
    login_url = '/admin/login/'

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
    login_url = '/admin/login/'

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
    login_url = '/admin/login/'

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
    login_url = '/admin/login/'

    def get(self, request, pk):
        idea = get_object_or_404(VisitIdea, pk=pk, usuario=request.user)
        return render(request, 'planner/visitidea_detail.html', {'idea': idea})
