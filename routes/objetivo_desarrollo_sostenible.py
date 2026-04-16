from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.api_service import ApiService

ods_bp = Blueprint('ods', __name__)
api = ApiService()

# READ
@ods_bp.route('/ods')
def listar_ods():
    datos = api.listar("objetivo_desarrollo_sostenible")
    return render_template("pages/objetivo_desarrollo_sostenible/lista.html", datos=datos)
