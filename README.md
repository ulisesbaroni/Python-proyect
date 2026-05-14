# 🗺️ Viajero

Aplicación web desarrollada con Django para gestionar destinos que querés visitar. Podés guardar lugares, organizarlos por estado (Idea → Investigando → Planificado → Listo) y administrar tu perfil de usuario.

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone <url-del-repo>
cd viajero
```

### 2. Crear y activar el entorno virtual

```bash
python -m venv .venv

# Windows
source .venv/Scripts/activate

# Linux/Mac
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Aplicar migraciones

```bash
python manage.py migrate
```

### 5. Crear superusuario (opcional, para acceder al admin)

```bash
python manage.py createsuperuser
```

### 6. Ejecutar el servidor

```bash
python manage.py runserver
```

Accedé a [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## Funcionalidades

- Registro, login y logout de usuarios
- Perfil de usuario con avatar, nombre, apellido, email y experiencia
- Edición de perfil y cambio de contraseña
- Gestión de lugares (CRUD completo): nombre, ubicación, km, descripción, imagen y fecha de visita
- Gestión de ideas de visita con estados y prioridades
- Buscador y filtros en el listado de lugares e ideas
- Agrupamiento de ideas por estado

---

## Estructura del proyecto

viajero/
├── home/                   # App de vistas generales
│   ├── urls.py
│   └── views.py
├── planner/                # App principal con lugares e ideas
│   ├── migrations/
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── usuarios/               # App de autenticación y perfiles
│   ├── migrations/
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── templates/
│   ├── base.html
│   ├── home/
│   ├── planner/
│   └── usuarios/
├── viajero/                # Configuración del proyecto
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── .gitignore
├── manage.py
├── README.md
└── requirements.txt

---

## Tecnologías

- Python 3.14
- Django 6.0
- Bootstrap 5.3
- SQLite