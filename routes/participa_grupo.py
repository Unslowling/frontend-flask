# routes/participa_grupo.py
from flask import Blueprint, render_template, request, redirect, url_for
from services.api_service import ApiService

participa_grupo_bp = Blueprint(
    "participa_grupo",
    __name__,
    url_prefix="/participa_grupo"
)

api = ApiService()

API_URL = "participa_grupo"


@participa_grupo_bp.route("/")
def index():

    registros = api.listar(API_URL)

    return render_template(
    "pages/participa_grupo/participa_grupo.html",
    registros=registros
)


@participa_grupo_bp.route("/crear", methods=["POST"])
def crear():

    data = request.form.to_dict()

    api.crear(API_URL, data)

    return redirect(
        url_for("participa_grupo.index")
    )


@participa_grupo_bp.route("/editar/<int:docente_cedula>/<int:grupo_investigacion_id>", methods=["POST"])
def editar(docente_cedula, grupo_investigacion_id):

    data = request.form.to_dict()

    api.editar(
        API_URL,
        docente_cedula,
        data
    )

    return redirect(
        url_for("participa_grupo.index")
    )


@participa_grupo_bp.route("/eliminar/<int:docente_cedula>/<int:grupo_investigacion_id>")
def eliminar(docente_cedula, grupo_investigacion_id):

    api.eliminar(
        API_URL,
        docente_cedula
    )

    return redirect(
        url_for("participa_grupo.index")
    )