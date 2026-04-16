from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.api_service import ApiService

bp = Blueprint('grupo_investigacion', __name__)
api = ApiService()

@bp.route('/grupo_investigacion')
def listar_grupos():
    datos = api.listar("grupo_investigacion")
    return render_template("pages/grupo_investigacion/lista.html", datos=datos)

@bp.route('/grupo_investigacion/crear', methods=['GET', 'POST'])
def crear_grupo():
    if request.method == 'POST':
        interno_val = request.form.get("interno")
        interno_bool = True if interno_val in ["on", "true", "1", "yes"] else False
        
        universidad_val = request.form.get("universidad")
        try:
            universidad_int = int(universidad_val) if universidad_val else None
        except ValueError:
            universidad_int = None
        
        datos_nuevos = {
            "nombre": request.form.get("nombre"),
            "url_gruplac": request.form.get("url_gruplac") or None,
            "categoria": request.form.get("categoria") or None,
            "convocatoria": request.form.get("convocatoria") or None,
            "fecha_fundacion": request.form.get("fecha_fundacion") or None,
            "universidad": universidad_int,
            "interno": interno_bool,
            "ambito": request.form.get("ambito") or None
        }
        
        exito, mensaje = api.crear("grupo_investigacion", datos_nuevos)
        
        if exito:
            flash("Grupo de investigación creado exitosamente.", "success")
            return redirect(url_for('grupo_investigacion.listar_grupos'))
        else:
            flash(f"Error al crear: {mensaje}", "danger")
            
    return render_template("pages/grupo_investigacion/crear.html")

@bp.route('/grupo_investigacion/editar/<int:id>', methods=['GET', 'POST'])
def editar_grupo(id):
    if request.method == 'POST':
        interno_val = request.form.get("interno")
        interno_bool = True if interno_val in ["on", "true", "1", "yes"] else False
        
        universidad_val = request.form.get("universidad")
        try:
            universidad_int = int(universidad_val) if universidad_val else None
        except ValueError:
            universidad_int = None
        
        datos_actualizados = {
            "nombre": request.form.get("nombre"),
            "url_gruplac": request.form.get("url_gruplac") or None,
            "categoria": request.form.get("categoria") or None,
            "convocatoria": request.form.get("convocatoria") or None,
            "fecha_fundacion": request.form.get("fecha_fundacion") or None,
            "universidad": universidad_int,
            "interno": interno_bool,
            "ambito": request.form.get("ambito") or None
        }
        
        exito, mensaje = api.actualizar("grupo_investigacion", "id", id, datos_actualizados)
        
        if exito:
            flash("Grupo de investigación actualizado exitosamente.", "success")
            return redirect(url_for('grupo_investigacion.listar_grupos'))
        else:
            flash(f"Error al actualizar: {mensaje}", "danger")
            
    todos = api.listar("grupo_investigacion")
    grupo_actual = next((item for item in todos if str(item.get('id')) == str(id)), None)
    
    if not grupo_actual:
        flash("El grupo de investigación solicitado no existe.", "danger")
        return redirect(url_for('grupo_investigacion.listar_grupos'))
    
    fecha = grupo_actual.get('fecha_fundacion', '')
    if fecha and 'T' in fecha:
        grupo_actual['fecha_fundacion'] = fecha.split('T')[0]
    
    return render_template("pages/grupo_investigacion/editar.html", grupo=grupo_actual)

@bp.route('/grupo_investigacion/eliminar/<int:id>', methods=['POST'])
def eliminar_grupo(id):
    exito, mensaje = api.eliminar("grupo_investigacion", "id", id)
    
    if exito:
        flash("Grupo de investigación eliminado exitosamente.", "success")
    else:
        flash(f"Error al eliminar: {mensaje}", "danger")
        
    return redirect(url_for('grupo_investigacion.listar_grupos'))