from flask import Blueprint, render_template, request, redirect, url_for, flash

from services.api_service import ApiService

bp = Blueprint('aa_linea', __name__)
api = ApiService()

@bp.route('/aa_linea')
def listar_aa_linea():
    # 🔹 PASO 1: Obtener la lista
    datos = api.listar("aa_linea")
    
    # 🔹 PASO 2: Ver datos en pantalla
    return render_template("pages/aa_linea/lista_aa_linea.html", datos=datos)

@bp.route('/aa_linea/crear', methods=['GET', 'POST'])
def crear_aa_linea():
    if request.method == 'POST':
        # Capturamos del formulario los IDs
        datos_nuevos = {
            "linea_investigacion": request.form.get("linea_investigacion"),
            "area_aplicacion": request.form.get("area_aplicacion")
        }
        
        exito, mensaje = api.crear("aa_linea", datos_nuevos)
        
        if exito:
            flash("Relación creada exitosamente.", "success")
            return redirect(url_for('aa_linea.listar_aa_linea'))
        else:
            flash(f"Error al crear: {mensaje}", "danger")
            
    # GET: Traer listas de las otras tablas para llenar los Selects
    lineas = api.listar("linea_investigacion")
    areas = api.listar("area_aplicacion")
    
    return render_template("pages/aa_linea/crear_aa_linea.html", lineas=lineas, areas=areas)

@bp.route('/aa_linea/eliminar/<int:id_linea>/<int:id_area>', methods=['POST'])
def eliminar_aa_linea(id_linea, id_area):
    import requests
    from config import API_BASE_URL
    
    # 🔹 DELETE "con consultas" (Opción 1: SQL parametrizado)
    try:
        url = f"{API_BASE_URL}/api/consultas/ejecutarconsultaparametrizada"
        
        # El endpoint /consultas/ejecutarconsultaparametrizada es muy estricto con el formato
        payload = {
            "consulta": "DELETE FROM aa_linea WHERE linea_investigacion = @lineaId AND area_aplicacion = @areaId",
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

    return redirect(url_for('aa_linea.listar_aa_linea'))
