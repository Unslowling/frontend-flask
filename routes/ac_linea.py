from flask import Blueprint, render_template

from services.api_service import ApiService

bp = Blueprint('ac_linea', __name__)
api = ApiService()

@bp.route('/ac_linea')
def listar_ac_linea():
    # 🔹 PASO 1: Obtener la lista
    datos = api.listar("ac_linea")
    
    # 🔹 PASO 2: Ver datos en pantalla
    return render_template("pages/ac_linea/lista_ac_linea.html", datos=datos)
