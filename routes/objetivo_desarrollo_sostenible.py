from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.api_service import ApiService

ods_bp = Blueprint('ods', __name__)
api = ApiService()

# READ
@ods_bp.route('/ods')
def listar_ods():
    datos = api.listar("objetivo_desarrollo_sostenible")
    return render_template("pages/objetivo_desarrollo_sostenible/lista.html", datos=datos)

# CREAR
@ods_bp.route('/ods/crear', methods=['GET', 'POST'])
def crear_ods():
    if request.method == 'POST':
        datos_nuevos = {
            "nombre": request.form.get("nombre"),
            "categoria": request.form.get("categoria")
        }
        
        exito, mensaje = api.crear("objetivo_desarrollo_sostenible", datos_nuevos)
        
        if exito:
            flash(mensaje, "success")
            return redirect(url_for('ods.listar_ods'))
        else:
            flash(mensaje, "danger")
            
    return render_template("pages/objetivo_desarrollo_sostenible/crear.html")
