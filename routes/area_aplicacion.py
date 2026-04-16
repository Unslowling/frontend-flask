from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.api_service import ApiService

aplicacion_bp = Blueprint('aplicacion', __name__)
api = ApiService()

# LECTURA (READ)
@aplicacion_bp.route('/area_aplicacion')
def listar_aplicaciones():
    # Consulta a la API para traer todos los registros
    datos = api.listar("area_aplicacion")
    return render_template("pages/area_aplicacion/lista.html", datos=datos)
