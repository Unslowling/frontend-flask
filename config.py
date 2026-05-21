"""
config.py - Configuracion centralizada de la aplicacion Flask.

Contiene las constantes que se usan en toda la aplicacion:
la URL de la API y la clave secreta para sesiones/flash.
"""

# ──────────────────────────────────────────────
# URL base de la API REST que consume este frontend.
# La API generica en C# corre en el puerto 7231 (HTTPS).
# Se usa en ApiService para construir las URLs de cada peticion HTTP.
# Ejemplo: f"{API_BASE_URL}/api/producto" genera "https://localhost:7231/api/producto"
# ──────────────────────────────────────────────
API_BASE_URL = "https://localhost:7231"

# ──────────────────────────────────────────────
# Configuración de verificación SSL para el cliente HTTP (requests).
# En entornos de desarrollo con certificados auto-firmados (como el de ASP.NET Core),
# se establece en False para evitar errores de conexión SSL.
# ──────────────────────────────────────────────
VERIFY_SSL = False

# Deshabilitar advertencias de urllib3 sobre peticiones HTTPS inseguras/no verificadas
if not VERIFY_SSL:
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ──────────────────────────────────────────────
# Clave secreta para el manejo de sesiones y mensajes flash.
# Flask la necesita para firmar las cookies de sesion de forma segura.
# Sin esta clave, flash() lanza un error porque no puede guardar mensajes en la sesion.
# En produccion deberia ser un valor aleatorio largo guardado en variable de entorno.
# ──────────────────────────────────────────────
SECRET_KEY = "clave-secreta-flask-frontend-2024"

