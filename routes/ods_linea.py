from flask import Blueprint, render_template, request, redirect, url_for, flash
import requests
from config import API_BASE_URL
from services.api_service import ApiService

bp = Blueprint('ods_linea', __name__)
api = ApiService()

@bp.route('/ods_linea')
def listar_ods_linea():
    datos = api.listar("ods_linea")
    return render_template("pages/ods_linea/lista_ods_linea.html", datos=datos)

@bp.route('/ods_linea/crear', methods=['GET', 'POST'])
def crear_ods_linea():
    if request.method == 'POST':
        datos_nuevos = {
            "linea_investigacion": request.form.get("linea_investigacion"),
            "ods": request.form.get("ods")
        }
        
        exito, mensaje = api.crear("ods_linea", datos_nuevos)
        
        if exito:
            flash("Relación creada exitosamente.", "success")
            return redirect(url_for('ods_linea.listar_ods_linea'))
        else:
            flash(f"Error al crear: {mensaje}", "danger")
            
    lineas = api.listar("linea_investigacion")
    ods_list = api.listar("objetivo_desarrollo_sostenible")
    
    return render_template("pages/ods_linea/crear_ods_linea.html", lineas=lineas, ods_list=ods_list)

@bp.route('/ods_linea/eliminar/<int:id_linea>/<int:id_ods>', methods=['POST'])
def eliminar_ods_linea(id_linea, id_ods):
    try:
        url = f"{API_BASE_URL}/api/consultas/ejecutarconsultaparametrizada"
        
        payload = {
            "consulta": "DELETE FROM ods_linea WHERE linea_investigacion = @lineaId AND ods = @odsId",
            "parametros": {
                "lineaId": id_linea,
                "odsId": id_ods
            }
        }
        
        resp = requests.post(url, json=payload, headers=api._get_headers())
        
        if resp.ok or (resp.status_code == 404 and "no devolvió resultados" in resp.text):
            flash("Relación eliminada exitosamente.", "success")
        else:
            flash(f"Error al eliminar en la BD. Backend dijo: {resp.text}", "danger")
            
    except Exception as e:
        flash(f"Error interno al eliminar: {str(e)}", "danger")

    return redirect(url_for('ods_linea.listar_ods_linea'))
