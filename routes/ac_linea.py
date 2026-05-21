from flask import Blueprint, render_template, request, redirect, url_for, flash

from services.api_service import ApiService

bp = Blueprint('ac_linea', __name__)
api = ApiService()

@bp.route('/ac_linea')
def listar_ac_linea():
    # 🔹 PASO 1: Obtener la lista
    datos = api.listar("ac_linea")
    
    # 🔹 PASO 2: Ver datos en pantalla
    return render_template("pages/ac_linea/lista_ac_linea.html", datos=datos)

@bp.route('/ac_linea/crear', methods=['GET', 'POST'])
def crear_ac_linea():
    if request.method == 'POST':
        # Capturamos del formulario los IDs
        datos_nuevos = {
            "linea_investigacion": request.form.get("linea_investigacion"),
            "area_conocimiento": request.form.get("area_conocimiento")
        }
        
        exito, mensaje = api.crear("ac_linea", datos_nuevos)
        
        if exito:
            flash("Relación creada exitosamente.", "success")
            return redirect(url_for('ac_linea.listar_ac_linea'))
        else:
            flash(f"Error al crear: {mensaje}", "danger")
            
    # GET: Traer listas de las otras tablas para llenar los Selects
    lineas = api.listar("linea_investigacion")
    areas = api.listar("area_conocimiento")
    
    return render_template("pages/ac_linea/crear_ac_linea.html", lineas=lineas, areas=areas)

@bp.route('/ac_linea/eliminar/<int:id_linea>/<int:id_area>', methods=['POST'])
def eliminar_ac_linea(id_linea, id_area):
    import requests
    from config import API_BASE_URL
    
    # 🔹 DELETE "con consultas" (Opción 1: SQL parametrizado)
    try:
        url = f"{API_BASE_URL}/api/consultas/ejecutarconsultaparametrizada"
        
        # El endpoint /consultas/ejecutarconsultaparametrizada es muy estricto con el formato
        payload = {
            "consulta": "DELETE FROM ac_linea WHERE linea_investigacion = @lineaId AND area_conocimiento = @areaId",
            "parametros": {
                "lineaId": id_linea,
                "areaId": id_area
            }
        }
        
        # Se envía por POST con el body JSON
        resp = requests.post(url, json=payload, headers=api._get_headers(), verify=api.verify)
        
        # El endpoint de consultas devuelve 404 "no devolvió resultados" cuando el DELETE se ejecuta exitosamente (porque no retorna filas)
        if resp.ok or (resp.status_code == 404 and "no devolvió resultados" in resp.text):
            flash("Relación eliminada exitosamente.", "success")
        else:
            flash(f"Error al eliminar en la BD. Backend dijo: {resp.text}", "danger")
            print("STATUS DE ERROR:", resp.status_code)
            print("RESPUESTA COMPLETA:", resp.text)
            
    except Exception as e:
        flash(f"Error interno al eliminar: {str(e)}", "danger")

    return redirect(url_for('ac_linea.listar_ac_linea'))
