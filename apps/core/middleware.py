"""
==============================================================================
apps/core/middleware.py - Middlewares Didácticos del Sistema
==============================================================================
Explicación para alumnos:
¿Qué es CORS (Cross-Origin Resource Sharing)?
Por defecto, los navegadores web aplican una política de seguridad llamada
'Same-Origin Policy' (Política del Mismo Origen). Esta política impide que un sitio web
(por ejemplo, la plataforma Scrum Master en https://scrum.misitiowebpersonal.com.ar)
haga peticiones AJAX/fetch hacia tu servidor local (http://127.0.0.1:8000), a menos que
tu servidor Django declare explícitamente que lo autoriza mediante cabeceras HTTP.

Este Middleware:
1. Intercepta toda petición HTTP entrante.
2. Si es una petición preflight 'OPTIONS' del navegador, responde inmediatamente HTTP 200 con los permisos.
3. Agrega a todas las respuestas salientes las cabeceras:
   - 'Access-Control-Allow-Origin'
   - 'Access-Control-Allow-Methods'
   - 'Access-Control-Allow-Headers'
==============================================================================
"""

from django.http import HttpResponse


class DidacticCorsMiddleware:
    """
    Middleware didáctico para habilitar CORS (Cross-Origin Resource Sharing)
    permitiendo la verificación en vivo desde navegadores y la plataforma Scrum Master AI.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Manejo de peticiones preflight (OPTIONS)
        # El navegador envía un OPTIONS previo para verificar si el servidor acepta el método y los headers.
        if request.method == 'OPTIONS':
            response = HttpResponse()
        else:
            response = self.get_response(request)

        # 2. Inyección de cabeceras CORS
        # Permitimos el origen de la plataforma Scrum Master AI o peticiones locales
        origin = request.headers.get('Origin', '*')
        response['Access-Control-Allow-Origin'] = origin
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With, X-CSRFToken'
        response['Access-Control-Allow-Credentials'] = 'true'

        return response
