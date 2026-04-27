# 🗺️ Viajero

Tercera Pre-Entrega Python

App para gestionar destinos que querés visitar. Podés guardar lugares, organizarlos por estado (Idea → Investigando → Planificado → Listo) y filtrarlos por nombre, estado o país.

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

### 5. Crear superusuario

```bash
python manage.py createsuperuser
```

### 6. Ejecutar el servidor

```bash
python manage.py runserver
```

Accedé a [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## Uso

1. Iniciá sesión con el superusuario creado
2. Desde el panel de administración (`/admin/`) podés crear lugares (`Place`)
3. Desde la app podés crear ideas de visita, editarlas y filtrarlas por estado o país

---

## Estructura del proyecto

```
viajero/
├── planner/              # App principal
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── templates/
│   └── planner/
│       ├── base.html
│       ├── home.html
│       ├── visitidea_list.html
│       ├── visitidea_form.html
│       └── visitidea_detail.html
├── viajero/              # Configuración del proyecto
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── .gitignore
├── manage.py
├── README.md
└── requirements.txt
```

---

## Modelos

- **Place**: representa un lugar geográfico (nombre, ubicación, km, descripción)
- **VisitIdea**: representa la idea de visitar un lugar, asociada a un usuario, con estado, prioridad y notas
