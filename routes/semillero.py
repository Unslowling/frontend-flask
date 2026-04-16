from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.api_service import ApiService

bp = Blueprint('semillero', __name__)
api = ApiService()

@bp.route('/semillero')
def listar_semillero():
    datos = api.listar("semillero")
    return render_template("pages/semillero/lista.html", datos=datos)

@bp.route('/semillero/crear', methods=['GET', 'POST'])
def crear_semillero():
    if request.method == 'POST':
        datos_nuevos = {
            "nombre": request.form.get("nombre"),
            "fecha_fundacion": request.form.get("fecha_fundacion"),
            "grupo_investigacion": int(request.form.get("grupo_investigacion")) if request.form.get("grupo_investigacion") else None
        }
        
        exito, mensaje = api.crear("semillero", datos_nuevos)
        
        if exito:
            flash("Semillero creado exitosamente.", "success")
            return redirect(url_for('semillero.listar_semillero'))
        else:
            flash(f"Error al crear: {mensaje}", "danger")
            
    grupos = api.listar("grupo_investigacion")
    return render_template("pages/semillero/crear.html", grupos=grupos)

@bp.route('/semillero/editar/<int:id>', methods=['GET', 'POST'])
def editar_semillero(id):
    if request.method == 'POST':
        datos_actualizados = {
            "nombre": request.form.get("nombre"),
            "fecha_fundacion": request.form.get("fecha_fundacion"),
            "grupo_investigacion": int(request.form.get("grupo_investigacion")) if request.form.get("grupo_investigacion") else None
        }
        
        exito, mensaje = api.actualizar("semillero", "id", id, datos_actualizados)
        
        if exito:
            flash("Semillero actualizado exitosamente.", "success")
            return redirect(url_for('semillero.listar_semillero'))
        else:
            flash(f"Error al actualizar: {mensaje}", "danger")
            
    # Traer todos los semilleros para encontrar el actual
    todos = api.listar("semillero")
    semillero_actual = next((item for item in todos if str(item.get('id')) == str(id)), None)
    
    if not semillero_actual:
        flash("El Semillero solicitado no existe.", "danger")
        return redirect(url_for('semillero.listar_semillero'))
        
    grupos = api.listar("grupo_investigacion")
    
    # Manejar formato de fecha de C# (e.g., "2024-05-16T00:00:00") para el input type="date"
    fecha = semillero_actual.get('fecha_fundacion', '')
    if fecha and 'T' in  fecha:
        semillero_actual['fecha_fundacion'] = fecha.split('T')[0]
        
    return render_template("pages/semillero/editar.html", semillero=semillero_actual, grupos=grupos)

@bp.route('/semillero/eliminar/<int:id>', methods=['POST'])
def eliminar_semillero(id):
    exito, mensaje = api.eliminar("semillero", "id", id)
    
    if exito:
        flash("Semillero eliminado exitosamente.", "success")
    else:
        flash(f"Error al eliminar: {mensaje}", "danger")
        
    return redirect(url_for('semillero.listar_semillero'))
