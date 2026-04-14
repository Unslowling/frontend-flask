# FrontFlask - Frontend Flask para ApiGenericaCsharp

Frontend web construidocon Flask que consume la API REST genérica ApiGenericaCsharp.

## Estructura del Proyecto

```
📁 FrontFlask/
├── app.py                 # Punto de entrada. Crea la app Flask y registra los Blueprints
├── config.py             # Configuración centralizada (URL de la API, SECRET_KEY)
├── requirements.txt     # Dependencias Python
├── routes/             # Blueprints (controladores)
│   ├── __init__.py
│   ├── autenticacion.py # Login/Logout
│   ├── home.py         # Página de inicio
│   └── plantilla_ejemplo.py  # Ejemplo para crear nuevas rutas
├── services/           # Lógica de negocio
│   ├── __init__.py
│   └── api_service.py  # Cliente HTTP genérico para la API
├── templates/           # Plantillas HTML (Jinja2)
│   ├── pages/         # Páginas dinámicas
│   ├── layout/       # Plantillas base
│   └── components/  # Componentes reutilizables
└── static/            # Archivos estáticos
    └── css/
        └── app.css
```

## Arquitectura

### Flujo de Comunicación

```
┌─────────────┐    HTTP     ┌─────────────┐    HTTP     ┌──────────────┐
│  Navegador │ ◄───────► │   Flask    │ ◄───────► │  ApiGenerica │
│  (Puerto  │           │ (Puerto   │           │   C#        │
│   5100)   │           │  5100)    │           │ (Puerto    │
│           │           │           │           │  5034)     │
└─────────────┘           └─────────────┘           └──────────────┘
```

### Capas

1. **Routes (routes/)** - Blueprints de Flask
   - Definen las rutas URL y manejan las peticiones HTTP
   - Usan Jinja2 para renderizar templates HTML

2. **Services (services/)** - Lógica de negocio
   - `ApiService`: Cliente HTTP que consume la API REST
   - Métodos: listar, crear, actualizar, eliminar

3. **Templates (templates/)** - Vistas
   - Jinja2 templates con herencia de plantillas
   - Pages: páginas completas
   - Layout: plantillas base
   - Components: fragmentos reutilizables

## Cómo Funciona

### 1. Inicio de la Aplicación

```python
# app.py
app = Flask(__name__)
app.register_blueprint(home_bp)
app.register_blueprint(autenticacion_bp)
app.run(port=5100)
```

### 2. Protección de Rutas

```python
@app.before_request
def proteger_rutas():
    if 'api_token' not in session:
        return redirect(url_for('autenticacion.login'))
```

Toda ruta que no sea `/login` o estática requiere un token JWT en sesión.

### 3. Consumo de la API

```python
# En cualquier route
api = ApiService()
datos = api.listar('empresa')           # GET /api/empresa
exito, msg = api.crear('producto', {...})  # POST /api/producto
exito, msg = api.actualizar('producto', 'codigo', 'PR001', {...})  # PUT
exito, msg = api.eliminar('producto', 'codigo', 'PR001')  # DELETE
```

### 4. Autenticación

```python
# POST /login -> autenticacion.py
respuesta = requests.post(f"{API_BASE_URL}/api/autenticacion/login", json={...})
token = respuesta.json().get("token")
session['api_token'] = token
```

## Endpoints del Frontend

| Ruta | Blueprint | Descripción |
|------|----------|------------|
| `/` | home | Página de inicio |
| `/login` | autenticacion | Formulario de login |
| `/logout` | autenticacion | Cerrar sesión |

## Agregar una Nueva Tabla

1. **Crear el Blueprint:**

```python
# routes/nueva_tabla.py
from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from services.api_service import ApiService

bp = Blueprint('nueva_tabla', __name__)

@bp.route('/nueva_tabla')
def listar():
    api = ApiService()
    registros = api.listar('nueva_tabla')
    return render_template('pages/nueva_tabla.html', registros=registros)

@bp.route('/nueva_tabla/crear', methods=['POST'])
def crear():
    api = ApiService()
    datos = request.form.to_dict()
    exito, msg = api.crear('nueva_tabla', datos)
    flash(msg, 'success' if exito else 'danger')
    return redirect(url_for('nueva_tabla.listar'))
```

2. **Registrar en app.py:**

```python
from routes.nueva_tabla import bp as nueva_tabla_bp
app.register_blueprint(nueva_tabla_bp)
```

3. **Crear la plantilla:**

```html
<!-- templates/pages/nueva_tabla.html -->
{% extends "layout/base.html" %}

{% block content %}
<h1>Nueva Tabla</h1>
<table>
  {% for registro in registros %}
  <tr>
    <td>{{ registro.campo1 }}</td>
    <td>{{ registro.campo2 }}</td>
  </tr>
  {% endfor %}
</table>
{% endblock %}
```

## Configuración

### Puertos

- **Frontend Flask:** Puerto 5100
- **API C#:** Puerto 5034 (configurable en `config.py`)

### Variables de Entorno (production)

```bash
export API_BASE_URL="http://tu-servidor:5034"
export SECRET_KEY="clave-secreta-muy-larga"
```

## Instalación y Ejecución

```bash
# 1. Crear entorno virtual
python -m venv venv

# 2. Activar
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar
python app.py
```

Acceder a: `http://localhost:5100`

## Dependencias

- **Flask** - Framework web
- **requests** - Cliente HTTP

Ver `requirements.txt` para versiones completas.