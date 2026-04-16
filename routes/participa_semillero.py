from flask import Blueprint, render_template, request, redirect, url_for
from services.api_service import ApiService 

participa_semillero_bp = Blueprint(
    'participa_semillero',
    __name__,
    url_prefix='/participa_semillero'
)

# Creamos una instancia de la clase para usarla en todas las rutas
api = ApiService() 
API_URL = "participa_semillero"

# LISTAR
@participa_semillero_bp.route("/")
def index():
    # Usamos api.listar en lugar de get_data
    registros = api.listar(API_URL) 
    return render_template(
        "pages/participa_semillero/participa_semillero.html",
        registros=registros
    )

# CREAR
@participa_semillero_bp.route("/crear", methods=["POST"])
def crear():
    data = {
        "docente": request.form["docente"],
        "semillero": request.form["semillero"],
        "rol": request.form["rol"],
        "fecha_inicio": request.form["fecha_inicio"],
        "fecha_fin": request.form["fecha_fin"]
    }

    # Usamos api.crear en lugar de post_data
    api.crear(API_URL, data) 

    return redirect(url_for("participa_semillero.index"))

# EDITAR
@participa_semillero_bp.route("/editar/<int:docente>/<int:semillero>", methods=["POST"])
def editar(docente, semillero):
    data = {
        # No enviamos las llaves en el cuerpo si la API no lo requiere, 
        # pero mantenemos tu estructura:
        "rol": request.form["rol"],
        "fecha_inicio": request.form["fecha_inicio"],
        "fecha_fin": request.form["fecha_fin"]
    }

    api.actualizar(API_URL, "docente/semillero", f"{docente}/{semillero}", data) 

    return redirect(url_for("participa_semillero.index"))

# ELIMINAR
@participa_semillero_bp.route("/eliminar/<int:docente>/<int:semillero>")
def eliminar(docente, semillero):
    # Tu clase 'eliminar' pide: tabla, nombre_clave, valor_clave
    api.eliminar(API_URL, "docente/semillero", f"{docente}/{semillero}") 

    return redirect(url_for("participa_semillero.index"))