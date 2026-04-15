from flask import Blueprint, render_template
from services.api_service import ApiService

linea_bp = Blueprint('linea', __name__)
api = ApiService()


@linea_bp.route('/linea_investigacion')
def listar_lineas():
    datos = api.listar("linea_investigacion")
    return render_template("pages/linea_investigacion/lista.html", datos=datos)