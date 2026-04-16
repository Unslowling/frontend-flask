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

# CREAR
@aplicacion_bp.route('/area_aplicacion/crear', methods=['GET', 'POST'])
def crear_aplicacion():
    if request.method == 'POST':
        datos_nuevos = {
            "nombre": request.form.get("nombre")
        }
        
        exito, mensaje = api.crear("area_aplicacion", datos_nuevos)
        
        if exito:
            flash(mensaje, "success")
            return redirect(url_for('aplicacion.listar_aplicaciones'))
        else:
            flash(mensaje, "danger")
            
    return render_template("pages/area_aplicacion/crear.html")

# EDITAR
@aplicacion_bp.route('/area_aplicacion/editar/<int:id>', methods=['GET', 'POST'])
def editar_aplicacion(id):
    if request.method == 'POST':
        datos_actualizados = {
            "nombre": request.form.get("nombre")
        }
        
        exito, mensaje = api.actualizar("area_aplicacion", "id", id, datos_actualizados)
        
        if exito:
            flash("Área de aplicación actualizada exitosamente.", "success")
            return redirect(url_for('aplicacion.listar_aplicaciones'))
        else:
            flash(f"Error al actualizar: {mensaje}", "danger")
            
    todas_aplicaciones = api.listar("area_aplicacion")
    aplicacion_actual = next((item for item in todas_aplicaciones if str(item.get('id')) == str(id)), None)
    
    if not aplicacion_actual:
        flash("El área de aplicación solicitada no existe.", "danger")
        return redirect(url_for('aplicacion.listar_aplicaciones'))
        
    return render_template("pages/area_aplicacion/editar.html", area_aplicacion=aplicacion_actual)
