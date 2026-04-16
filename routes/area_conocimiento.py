from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.api_service import ApiService

area_bp = Blueprint('area', __name__)
api = ApiService()

# LISTAR
@area_bp.route('/area_conocimiento')
def listar_areas():
    datos = api.listar("area_conocimiento")
    return render_template("pages/area_conocimiento/lista.html", datos=datos)

# CREAR
@area_bp.route('/area_conocimiento/crear', methods=['GET', 'POST'])
def crear_area():
    if request.method == 'POST':
        datos_nuevos = {
            "gran_area": request.form.get("gran_area"),
            "area": request.form.get("area"),
            "disciplina": request.form.get("disciplina")
        }
        
        exito, mensaje = api.crear("area_conocimiento", datos_nuevos)
        
        if exito:
            flash(mensaje, "success")
            return redirect(url_for('area.listar_areas'))
        else:
            flash(mensaje, "danger")
            
    return render_template("pages/area_conocimiento/crear.html")

# EDITAR
@area_bp.route('/area_conocimiento/editar/<int:id>', methods=['GET', 'POST'])
def editar_area(id):
    if request.method == 'POST':
        datos_actualizados = {
            "gran_area": request.form.get("gran_area"),
            "area": request.form.get("area"),
            "disciplina": request.form.get("disciplina")
        }
        
        exito, mensaje = api.actualizar("area_conocimiento", "id", id, datos_actualizados)
        
        if exito:
            flash("Área de conocimiento actualizada exitosamente.", "success")
            return redirect(url_for('area.listar_areas'))
        else:
            flash(f"Error al actualizar: {mensaje}", "danger")
            
    todas_areas = api.listar("area_conocimiento")
    area_actual = next((item for item in todas_areas if str(item.get('id')) == str(id)), None)
    
    if not area_actual:
        flash("El área de conocimiento solicitada no existe.", "danger")
        return redirect(url_for('area.listar_areas'))
        
    return render_template("pages/area_conocimiento/editar.html", area=area_actual)

# ELIMINAR
@area_bp.route('/area_conocimiento/eliminar/<int:id>', methods=['POST'])
def eliminar_area(id):
    # Utilizamos el nombre de clave primara "id" que vimos en la API
    exito, mensaje = api.eliminar("area_conocimiento", "id", id)
    
    if exito:
        flash("Área de conocimiento eliminada exitosamente.", "success")
    else:
        flash(f"Error al eliminar: {mensaje}", "danger")
        
    return redirect(url_for('area.listar_areas'))
