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