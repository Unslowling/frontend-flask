"""
app.py - Punto de entrada de la aplicacion Flask.

Crea la aplicacion, registra los Blueprints (uno por tabla)
e inicia el servidor de desarrollo en el puerto 5100.
"""

# Flask: clase principal del framework web para crear la aplicacion
from flask import Flask, request, session, redirect, url_for, flash

# SECRET_KEY: clave secreta definida en config.py, necesaria para mensajes flash
from config import SECRET_KEY


# ══════════════════════════════════════════════
# CREAR LA APLICACION FLASK
# ══════════════════════════════════════════════

# Flask(__name__) crea la instancia de la aplicacion.
# __name__ le indica a Flask en que modulo esta corriendo (necesario para encontrar templates y static).
app = Flask(__name__)

# La clave secreta es necesaria para los mensajes flash (alertas).
# Flask la usa internamente para firmar las cookies de sesion.
app.secret_key = SECRET_KEY


# ══════════════════════════════════════════════
# REGISTRAR BLUEPRINTS
# Cada Blueprint agrupa las rutas de una tabla.
# Es el equivalente a tener una pagina separada por tabla.
# ══════════════════════════════════════════════

# Importar el Blueprint de cada modulo de rutas.
# 'bp' es la variable que cada archivo exporta con su Blueprint.
# Se renombra con 'as' para evitar conflictos de nombres entre modulos.
from routes.home import bp as home_bp          # Blueprint de la pagina de inicio
from routes.autenticacion import bp as autenticacion_bp  # Blueprint de autenticación y login

# Importaciones para tus nuevas tablas
from routes.linea_investigacion import linea_bp
from routes.objetivo_desarrollo_sostenible import ods_bp
from routes.area_aplicacion import aplicacion_bp
from routes.semillero import bp as semillero_bp
from routes.area_conocimiento import area_bp
from routes.ac_linea import bp as ac_linea_bp
from routes.aa_linea import bp as aa_linea_bp
from routes.ods_linea import bp as ods_linea_bp
from routes.participa_semillero import participa_semillero_bp
from routes.grupo_linea import grupo_linea_bp
from routes.grupo_investigacion import grupo_investigacion_bp
from routes.participa_grupo import participa_grupo_bp


# Registros de Blueprints base
app.register_blueprint(home_bp)      # Registra GET /
app.register_blueprint(autenticacion_bp) # Registra /login y /logout

# Registros de tus tablas
app.register_blueprint(linea_bp)
app.register_blueprint(ods_bp)
app.register_blueprint(aplicacion_bp)
app.register_blueprint(grupo_investigacion_bp)
app.register_blueprint(semillero_bp)
app.register_blueprint(area_bp)
app.register_blueprint(ac_linea_bp)
app.register_blueprint(aa_linea_bp)
app.register_blueprint(ods_linea_bp)
app.register_blueprint(participa_semillero_bp)
app.register_blueprint(grupo_linea_bp)
app.register_blueprint(participa_grupo_bp)


# ══════════════════════════════════════════════
# SEGURIDAD GLOBAL DE SESIONES
# ══════════════════════════════════════════════
@app.before_request
def proteger_rutas():
    """
    Middleware que verifica si el usuario tiene token JWT.
    Si no lo tiene, redirige a login.
    Las rutas publicas (login, static) no requieren autenticacion.
    """
    # Rutas que NO requieren autenticacion
    rutas_publicas = ['autenticacion.login', 'static']
    
    # request.endpoint es algo como: 'autenticacion.login' o 'home.index'
    if request.endpoint in rutas_publicas:
        return None
    
    # Si el endpoint es None (ruta no encontrada), dejar pasar
    if request.endpoint is None:
        return None
    
    # Verificar si el usuario tiene sesion con token JWT
    if 'api_token' not in session:
        flash('Debes iniciar sesion para acceder.', 'warning')
        return redirect(url_for('autenticacion.login'))
    
    return None


# ══════════════════════════════════════════════
# INICIAR EL SERVIDOR
# ══════════════════════════════════════════════

# __name__ == '__main__' se cumple solo cuando ejecutamos "python app.py" directamente.
# No se ejecuta si otro archivo importa este modulo.
if __name__ == '__main__':
    # app.run() inicia el servidor de desarrollo de Flask.
    # debug=True: recarga automaticamente al guardar cambios y muestra errores detallados.
    # port=5100: puerto del frontend, diferente al de la API (5034) para evitar conflicto.
    app.run(debug=True, port=5100)
