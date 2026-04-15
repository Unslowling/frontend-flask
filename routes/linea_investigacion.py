from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.api_service import ApiService

linea_bp = Blueprint('linea', __name__)
api = ApiService()


@linea_bp.route('/linea_investigacion')
def listar_lineas():
    datos = api.listar("linea_investigacion")
    return render_template("pages/linea_investigacion/lista.html", datos=datos)

@linea_bp.route('/linea_investigacion/crear', methods=['GET', 'POST'])
def crear_linea():
    if request.method == 'POST':
        # Capturamos los datos enviados desde el formulario HTML
        datos_nuevos = {
            "nombre": request.form.get("nombre"),
            "descripcion": request.form.get("descripcion")
        }
        
        # Llamamos al método crear del ApiService
        exito, mensaje = api.crear("linea_investigacion", datos_nuevos)
        
        if exito:
            flash(mensaje, "success")
            return redirect(url_for('linea.listar_lineas'))
        else:
            flash(mensaje, "danger")
            
    # Si es una petición GET, simplemente renderizamos el formulario en blanco
    return render_template("pages/linea_investigacion/crear.html")

@linea_bp.route('/linea_investigacion/editar/<int:id>', methods=['GET', 'POST'])
def editar_linea(id):
    if request.method == 'POST':
        # Capturamos los datos enviados desde el HTML
        datos_actualizados = {
            "nombre": request.form.get("nombre"),
            "descripcion": request.form.get("descripcion")
        }
        
        # Llamamos al método actualizar del ApiService. 
        # Cuidado con el nombre de la clave primaria, asumimos que es "id"
        exito, mensaje = api.actualizar("linea_investigacion", "id", id, datos_actualizados)
        
        if exito:
            flash("Línea de investigación actualizada exitosamente.", "success")
            return redirect(url_for('linea.listar_lineas'))
        else:
            flash(f"Error al actualizar: {mensaje}", "danger")
            
    # Lógica GET para mostrar los datos actuales de la línea a editar
    # Buscamos en el listar puesto que api no tiene un obtener_por_id genérico.
    todas_lineas = api.listar("linea_investigacion")
    linea_actual = next((item for item in todas_lineas if str(item.get('id')) == str(id)), None)
    
    if not linea_actual:
        flash("La línea de investigación solicitada no existe.", "danger")
        return redirect(url_for('linea.listar_lineas'))
        
    return render_template("pages/linea_investigacion/editar.html", linea=linea_actual)

@linea_bp.route('/linea_investigacion/eliminar/<int:id>', methods=['POST'])
def eliminar_linea(id):
    # Llamamos al método eliminar del ApiService
    exito, mensaje = api.eliminar("linea_investigacion", "id", id)
    
    if exito:
        flash("Línea de investigación eliminada exitosamente.", "success")
    else:
        flash(f"Error al eliminar: {mensaje}", "danger")
        
    return redirect(url_for('linea.listar_lineas'))