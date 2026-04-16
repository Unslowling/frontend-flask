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

# EDITAR
@ods_bp.route('/ods/editar/<int:id>', methods=['GET', 'POST'])
def editar_ods(id):
    if request.method == 'POST':
        datos_actualizados = {
            "nombre": request.form.get("nombre"),
            "categoria": request.form.get("categoria")
        }
        
        exito, mensaje = api.actualizar("objetivo_desarrollo_sostenible", "id", id, datos_actualizados)
        
        if exito:
            flash("ODS actualizado exitosamente.", "success")
            return redirect(url_for('ods.listar_ods'))
        else:
            flash(f"Error al actualizar: {mensaje}", "danger")
            
    todos_ods = api.listar("objetivo_desarrollo_sostenible")
    ods_actual = next((item for item in todos_ods if str(item.get('id')) == str(id)), None)
    
    if not ods_actual:
        flash("El ODS solicitado no existe.", "danger")
        return redirect(url_for('ods.listar_ods'))
        
    return render_template("pages/objetivo_desarrollo_sostenible/editar.html", ods=ods_actual)

# ELIMINAR
@ods_bp.route('/ods/eliminar/<int:id>', methods=['POST'])
def eliminar_ods(id):
    exito, mensaje = api.eliminar("objetivo_desarrollo_sostenible", "id", id)
    
    if exito:
        flash("ODS eliminado exitosamente.", "success")
    else:
        flash(f"Error al eliminar: {mensaje}", "danger")
        
    return redirect(url_for('ods.listar_ods'))
