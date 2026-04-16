from flask import Blueprint, render_template, request, redirect, url_for
from services.api_service import ApiService

grupo_investigacion_bp = Blueprint(
    'grupo_investigacion',
    __name__,
    url_prefix='/grupo_investigacion'
)

api = ApiService()
API_URL = "grupo_investigacion"


@grupo_investigacion_bp.route("/")
def index():

    registros = api.listar(API_URL)
    universidades = api.listar("universidad")

    return render_template(
        "pages/grupo_investigacion/grupo_investigacion.html",
        registros=registros,
        universidades=universidades
    )

# @grupo_investigacion_bp.route("/crear", methods=["POST"])
# def crear():

#     data = {
#         "nombre": request.form["nombre"],
#         "url_gruplac": request.form["url_gruplac"],
#         "categoria": request.form["categoria"],
#         "convocatoria": request.form["convocatoria"],
#         "fecha_fundacion": request.form["fecha_fundacion"],
#         "universidad": request.form["universidad"],
#         "interno": request.form["interno"],
#         "ambito": request.form["ambito"]
#     }

#     api.crear(API_URL, data)

#     return redirect(url_for("grupo_investigacion.index"))
@grupo_investigacion_bp.route("/crear", methods=["POST"])
def crear():

    data = request.form.to_dict()

    print("DATA:", data)

    response = api.crear(API_URL, data)

    print("RESPONSE:", response)

    return redirect(url_for("grupo_investigacion.index"))


@grupo_investigacion_bp.route("/editar/<int:id>", methods=["POST"])
def editar(id):

    data = {
        "nombre": request.form["nombre"],
        "url_gruplac": request.form["url_gruplac"],
        "categoria": request.form["categoria"],
        "convocatoria": request.form["convocatoria"],
        "fecha_fundacion": request.form["fecha_fundacion"],
        "universidad": request.form["universidad"],
        "interno": request.form["interno"],
        "ambito": request.form["ambito"]
    }

    api.actualizar(
        API_URL,
        "id",
        id,
        data
    )

    return redirect(url_for("grupo_investigacion.index"))


@grupo_investigacion_bp.route("/eliminar/<int:id>")
def eliminar(id):

    api.eliminar(
        API_URL,
        "id",
        id
    )

    return redirect(url_for("grupo_investigacion.index"))
