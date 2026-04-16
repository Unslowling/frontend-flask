from flask import Blueprint, render_template, request, redirect, url_for
from services.api_service import ApiService

grupo_linea_bp = Blueprint(
    'grupo_linea',
    __name__,
    url_prefix='/grupo_linea'
)

api = ApiService()
API_URL = "grupo_linea"


@grupo_linea_bp.route("/")
def index():

    registros = api.listar(API_URL)
    grupos = api.listar("grupo_investigacion")
    lineas = api.listar("linea_investigacion")

    return render_template(
        "pages/grupo_linea/grupo_linea.html",
        registros=registros,
        grupos=grupos,
        lineas=lineas
    )


@grupo_linea_bp.route("/crear", methods=["POST"])
def crear():

    data = {
        "grupo": request.form["grupo"],
        "linea": request.form["linea"]
    }

    api.crear(API_URL, data)

    return redirect(url_for("grupo_linea.index"))


@grupo_linea_bp.route("/editar/<int:grupo>/<int:linea>", methods=["POST"])
def editar(grupo, linea):

    data = {
        "grupo": request.form["grupo"],
        "linea": request.form["linea"]
    }

    api.actualizar(
        API_URL,
        "grupo/linea",
        f"{grupo}/{linea}",
        data
    )

    return redirect(url_for("grupo_linea.index"))


@grupo_linea_bp.route("/eliminar/<int:grupo>/<int:linea>")
def eliminar(grupo, linea):

    api.eliminar(
        API_URL,
        "grupo/linea",
        f"{grupo}/{linea}"
    )

    return redirect(url_for("grupo_linea.index"))