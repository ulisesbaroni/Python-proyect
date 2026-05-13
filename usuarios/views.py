from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.models import User
from .forms import RegistroForm, EditarUsuarioForm
from .models import Perfil


class RegistroView(View):
    def get(self, request):
        form = RegistroForm()
        return render(request, 'usuarios/registro.html', {'form': form})

    def post(self, request):
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            Perfil.objects.create(usuario=user)
            login(request, user)
            return redirect('home')
        return render(request, 'usuarios/registro.html', {'form': form})


class LoginView(View):
    def get(self, request):
        return render(request, 'usuarios/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        return render(request, 'usuarios/login.html', {'error': 'Usuario o contraseña incorrectos'})


# uso decorador acá en vez de mixin, para mostrar las dos formas
@login_required(login_url='/login/')
def perfil_view(request):
    perfil, _ = Perfil.objects.get_or_create(usuario=request.user)
    return render(request, 'usuarios/perfil.html', {'perfil': perfil})


@login_required(login_url='/login/')
def editar_perfil_view(request):
    perfil, _ = Perfil.objects.get_or_create(usuario=request.user)

    if request.method == 'POST':
        form = EditarUsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()

            perfil.experiencia = form.cleaned_data['experiencia']
            if form.cleaned_data.get('avatar'):
                perfil.avatar = form.cleaned_data['avatar']
            perfil.save()
            return redirect('perfil')
    else:
        form = EditarUsuarioForm(initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'experiencia': perfil.experiencia,
        })

    return render(request, 'usuarios/editar_perfil.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')