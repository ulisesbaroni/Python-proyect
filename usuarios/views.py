from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
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


@login_required(login_url='/login/')
def cambiar_password_view(request):
    if request.method == 'POST':
        actual = request.POST.get('password_actual')
        nueva = request.POST.get('password_nueva')
        confirmar = request.POST.get('password_confirmar')

        if not request.user.check_password(actual):
            return render(request, 'usuarios/cambiar_password.html', {'error': 'La contraseña actual es incorrecta.'})

        if nueva != confirmar:
            return render(request, 'usuarios/cambiar_password.html', {'error': 'Las contraseñas nuevas no coinciden.'})

        if len(nueva) < 8:
            return render(request, 'usuarios/cambiar_password.html', {'error': 'La nueva contraseña debe tener al menos 8 caracteres.'})

        request.user.set_password(nueva)
        request.user.save()
        update_session_auth_hash(request, request.user)

        from django.contrib import messages
        messages.success(request, '¡Contraseña cambiada correctamente!')
        return redirect('home')

    return render(request, 'usuarios/cambiar_password.html')


def logout_view(request):
    logout(request)
    return redirect('home')