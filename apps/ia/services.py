"""
==============================================================================
apps/ia/services.py - Servicio de IA con Anthropic SDK y Tool Calling en 2 Fases
==============================================================================
Explicación Pedagógica Exhaustiva para Alumnos:

1. ¿QUÉ ES EL PATRÓN "TOOL CALLING" O "FUNCTION CALLING"?
   En lugar de pedirle al Modelo de Lenguaje (LLM como Claude) que adivine
   datos o invente respuestas (alucinaciones), le otorgamos un conjunto de
   herramientas ("Tools") que describen funciones de nuestro backend.
   El LLM analiza la pregunta del usuario y responde con un objeto estructurado
   indicando qué función ejecutar y con qué argumentos.

2. ¿POR QUÉ UN PATRÓN EN 2 FASES CON OPTIMIZACIÓN DE TOKENS?
   - PROBLEMA COMÚN (Enfoque ingenuo):
     Enviar TODA la base de datos o tablas enteras en el prompt inicial del sistema.
     Esto consume decenas de miles de tokens ($$$ de costo), supera límites de ventana
     y degrada la velocidad de respuesta.
   
   - SOLUCIÓN OPTIMIZADA (Arquitectura en 2 Fases):
     * FASE 1 (Resolución / Selección de Herramienta):
       Se envía ÚNICAMENTE la pregunta del usuario y el esquema JSON liviano
       de las herramientas disponibles (sin filas de datos).
       Claude decide qué herramienta llamar (ej: buscar_items_por_texto, query='django').
       Consumo de tokens: MÍNIMO (~100-200 tokens).

     * EJECUCIÓN LOCAL (Backend Python + PostgreSQL ORM):
       El servidor ejecuta la consulta SQL/ORM de forma local y eficiente usando
       índices de PostgreSQL (db_index, compound indexes). Solo se recuperan
       las filas estrictamente necesarias.

     * FASE 2 (Síntesis Contextualizada):
       Se envían a Claude únicamente los registros filtrados obtenidos en la consulta local.
       Claude redacta una respuesta en lenguaje natural precisa y libre de alucinaciones.
       Consumo de tokens: MUY BAJO (~300-500 tokens).

3. MANEJO RESILIENTE DE ERRORES:
   Las llamadas a APIs remotas pueden fallar por:
   - Falta de API Key configurada.
   - Errores de autenticación (clave inválida).
   - Cuotas de uso o Rate Limits excedidos.
   - Caídas de red o timeouts.
   El servicio captura todas estas excepciones de la librería `anthropic` y retorna
   diccionarios estructurados con mensajes didácticos sin romper la aplicación (sin 500).
==============================================================================
"""

import json
import logging
from typing import Dict, Any, Optional
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder

logger = logging.getLogger(__name__)

# Importación condicional segura del SDK de Anthropic
try:
    import anthropic
    from anthropic import (
        APIError,
        APIConnectionError,
        AuthenticationError,
        RateLimitError,
        BadRequestError
    )
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    anthropic = None
    APIError = Exception
    APIConnectionError = Exception
    AuthenticationError = Exception
    RateLimitError = Exception
    BadRequestError = Exception

# Importamos el modelo y servicio de datos
from apps.datos.services import CatalogoService
from apps.datos.models import Item


# ==============================================================================
# DEFINICIÓN DEL ESQUEMA LIVIANO DE HERRAMIENTAS (MINIMAL JSON SCHEMA)
# ==============================================================================
TOOLS_DEFINITIONS = [
    {
        "name": "buscar_items_por_texto",
        "description": "Busca registros en el catálogo por coincidencia de texto en título o descripción.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Término o palabra clave a buscar en el catálogo."
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "filtrar_items_por_categoria",
        "description": "Filtra registros del catálogo según su categoría temática.",
        "input_schema": {
            "type": "object",
            "properties": {
                "categoria": {
                    "type": "string",
                    "description": "Nombre de la categoría a filtrar (ej: tutoriales, desarrollo, postgresql, arquitectura)."
                }
            },
            "required": ["categoria"]
        }
    },
    {
        "name": "obtener_detalle_item",
        "description": "Recupera la ficha completa y detalles de un ítem a partir de su ID numérico.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "Identificador numérico ID del ítem en la base de datos."
                }
            },
            "required": ["id"]
        }
    },
    {
        "name": "listar_catalogo_resumen",
        "description": "Devuelve un índice ultraliviano con el resumen (ID, título, categoría) de los ítems disponibles.",
        "input_schema": {
            "type": "object",
            "properties": {}
        }
    }
]


class ClaudeService:
    """
    Servicio de integración con la API de Anthropic Claude implementando
    el patrón de Tool Calling en 2 Fases con optimización estricta de tokens.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-3-5-haiku-20241022"
    ):
        """
        Inicializa el cliente de Anthropic con la API key provista o desde settings.
        """
        if api_key is not None:
            self.api_key = api_key
        else:
            self.api_key = getattr(settings, 'ANTHROPIC_API_KEY', '')

        self.model = model
        self.client = None

        if ANTHROPIC_AVAILABLE and self.api_key:
            try:
                self.client = anthropic.Anthropic(api_key=self.api_key)
            except Exception as e:
                logger.error(f"Error al inicializar Anthropic client: {e}")
                self.client = None

    @classmethod
    def get_tools_schema(cls) -> list:
        """
        Retorna la lista de definiciones livianas de herramientas (JSON Schema).
        No contiene filas de la base de datos, optimizando el costo en tokens.
        """
        return TOOLS_DEFINITIONS

    def ejecutar_herramienta_local(self, tool_name: str, tool_args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ejecuta la herramienta seleccionada en el backend local usando el ORM de Django.
        Garantiza que la búsqueda sea rápida gracias a los índices en PostgreSQL.
        """
        try:
            if tool_name == "buscar_items_por_texto":
                query = tool_args.get("query", "")
                qs = CatalogoService.buscar_items(query=query)
                datos = list(qs.values('id', 'titulo', 'categoria', 'descripcion', 'precio', 'disponible'))
                return {"tool": tool_name, "parametros": tool_args, "resultados": datos, "total": len(datos)}

            elif tool_name == "filtrar_items_por_categoria":
                categoria = tool_args.get("categoria", "")
                qs = CatalogoService.buscar_items(categoria=categoria)
                datos = list(qs.values('id', 'titulo', 'categoria', 'descripcion', 'precio', 'disponible'))
                return {"tool": tool_name, "parametros": tool_args, "resultados": datos, "total": len(datos)}

            elif tool_name == "obtener_detalle_item":
                item_id = tool_args.get("id")
                item = Item.objects.filter(id=item_id).first()
                if item:
                    detalle = {
                        "id": item.id,
                        "titulo": item.titulo,
                        "categoria": item.categoria,
                        "descripcion": item.descripcion,
                        "precio": float(item.precio),
                        "disponible": item.disponible,
                        "fecha_creacion": item.fecha_creacion.isoformat() if item.fecha_creacion else None
                    }
                    return {"tool": tool_name, "parametros": tool_args, "resultados": [detalle], "total": 1}
                else:
                    return {"tool": tool_name, "parametros": tool_args, "resultados": [], "total": 0, "mensaje": f"No se encontró ítem con ID {item_id}."}

            elif tool_name == "listar_catalogo_resumen":
                catalogo = CatalogoService.obtener_indice_liviano()
                return {"tool": tool_name, "parametros": tool_args, "resultados": catalogo, "total": len(catalogo)}

            else:
                return {"tool": tool_name, "parametros": tool_args, "error": f"Herramienta desconocida: {tool_name}", "resultados": []}

        except Exception as e:
            logger.error(f"Error al ejecutar herramienta local '{tool_name}': {e}", exc_info=True)
            return {"tool": tool_name, "parametros": tool_args, "error": str(e), "resultados": []}

    def procesar_consulta(self, user_prompt: str) -> Dict[str, Any]:
        """
        Ejecuta el flujo completo de consulta en 2 Fases:
        - FASE 1: Envía pregunta + esquemas mínimos a Claude para resolver el Tool a usar.
        - EJECUCIÓN LOCAL: Ejecuta la consulta ORM local contra la base de datos.
        - FASE 2: Envía a Claude los datos locales recuperados para redactar la síntesis final.
        """
        # Validación 1: Verificar SDK disponible
        if not ANTHROPIC_AVAILABLE:
            return {
                "status": "error",
                "error_type": "DependencyError",
                "message": "La librería 'anthropic' no está instalada en el entorno Python."
            }

        # Validación 2: Verificar API Key configurada
        if not self.api_key:
            return {
                "status": "error",
                "error_type": "MissingApiKey",
                "message": "No se ha configurado la variable de entorno ANTHROPIC_API_KEY. Configúrala en tu archivo .env o en settings.py."
            }

        # Validación 3: Cliente inicializado
        if not self.client:
            return {
                "status": "error",
                "error_type": "ClientInitError",
                "message": "No se pudo inicializar el cliente de Anthropic. Verifica tu API Key."
            }

        system_prompt = (
            "Eres un asistente didáctico inteligente integrado en una aplicación web Django con PostgreSQL. "
            "Tu objetivo es responder las consultas del usuario consultando el catálogo de la base de datos "
            "a través de las herramientas proporcionadas. Usa siempre la herramienta más precisa y optimizada."
        )

        try:
            # ------------------------------------------------------------------
            # FASE 1: RESOLUCIÓN Y SELECCIÓN DE TOOL (TOKEN-OPTIMIZED)
            # ------------------------------------------------------------------
            mensajes = [{"role": "user", "content": user_prompt}]
            
            respuesta_fase1 = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=system_prompt,
                tools=self.get_tools_schema(),
                messages=mensajes
            )

            # Analizar el resultado de la Fase 1
            tool_call_block = None
            for block in respuesta_fase1.content:
                if block.type == "tool_use":
                    tool_call_block = block
                    break

            # Si el modelo respondió directamente sin invocar herramientas
            if not tool_call_block:
                texto_directo = "".join([b.text for b in respuesta_fase1.content if hasattr(b, 'text')])
                return {
                    "status": "success",
                    "tipo_respuesta": "directa",
                    "fase_1": {
                        "tool_invocado": None,
                        "parametros": {},
                        "tokens_fase_1": {
                            "input_tokens": getattr(respuesta_fase1.usage, 'input_tokens', 0),
                            "output_tokens": getattr(respuesta_fase1.usage, 'output_tokens', 0)
                        }
                    },
                    "fase_2": {
                        "registros_encontrados": 0,
                        "datos_locales": [],
                        "respuesta_final": texto_directo,
                        "tokens_fase_2": {"input_tokens": 0, "output_tokens": 0}
                    },
                    "total_tokens": getattr(respuesta_fase1.usage, 'input_tokens', 0) + getattr(respuesta_fase1.usage, 'output_tokens', 0)
                }

            tool_name = tool_call_block.name
            tool_args = tool_call_block.input
            tool_id = tool_call_block.id

            # ------------------------------------------------------------------
            # EJECUCIÓN LOCAL: CONSULTA CONTRA LA BASE DE DATOS LOCAL
            # ------------------------------------------------------------------
            resultado_db = self.ejecutar_herramienta_local(tool_name, tool_args)
            datos_locales = resultado_db.get("resultados", [])

            # ------------------------------------------------------------------
            # FASE 2: SÍNTESIS CONTEXTUALIZADA CON DATOS LOCALES
            # ------------------------------------------------------------------
            mensajes.append({"role": "assistant", "content": respuesta_fase1.content})
            mensajes.append({
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_id,
                        "content": json.dumps(resultado_db, cls=DjangoJSONEncoder, ensure_ascii=False)
                    }
                ]
            })

            respuesta_fase2 = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=system_prompt,
                messages=mensajes
            )

            texto_final = "".join([b.text for b in respuesta_fase2.content if hasattr(b, 'text')])

            # Métricas de consumo de tokens para mostrar visualmente el ahorro
            t1_in = getattr(respuesta_fase1.usage, 'input_tokens', 0)
            t1_out = getattr(respuesta_fase1.usage, 'output_tokens', 0)
            t2_in = getattr(respuesta_fase2.usage, 'input_tokens', 0)
            t2_out = getattr(respuesta_fase2.usage, 'output_tokens', 0)

            return {
                "status": "success",
                "tipo_respuesta": "tool_calling",
                "fase_1": {
                    "tool_invocado": tool_name,
                    "parametros": tool_args,
                    "tokens_fase_1": {"input_tokens": t1_in, "output_tokens": t1_out}
                },
                "fase_2": {
                    "registros_encontrados": len(datos_locales) if isinstance(datos_locales, list) else 1,
                    "datos_locales": datos_locales,
                    "respuesta_final": texto_final,
                    "tokens_fase_2": {"input_tokens": t2_in, "output_tokens": t2_out}
                },
                "total_tokens": t1_in + t1_out + t2_in + t2_out
            }

        except AuthenticationError as e:
            logger.error(f"Error de autenticación en Anthropic API: {e}")
            return {
                "status": "error",
                "error_type": "AuthenticationError",
                "message": "Clave de API de Anthropic inválida o no autorizada. Revisa ANTHROPIC_API_KEY en tu .env."
            }
        except RateLimitError as e:
            logger.error(f"Límite de tasa / cuota excedida en Anthropic API: {e}")
            return {
                "status": "error",
                "error_type": "RateLimitError",
                "message": "Se ha excedido el límite de peticiones o la cuota de la API de Anthropic. Intenta nuevamente en unos momentos."
            }
        except APIConnectionError as e:
            logger.error(f"Error de conexión con Anthropic API: {e}")
            return {
                "status": "error",
                "error_type": "ConnectionError",
                "message": "No se pudo establecer conexión con los servidores de Anthropic. Verifica tu conexión a internet."
            }
        except BadRequestError as e:
            logger.error(f"Petición inválida a Anthropic API: {e}")
            return {
                "status": "error",
                "error_type": "BadRequestError",
                "message": f"Petición rechazada por Anthropic: {str(e)}"
            }
        except APIError as e:
            logger.error(f"Error general de Anthropic API: {e}")
            return {
                "status": "error",
                "error_type": "APIError",
                "message": f"Ocurrió un error en el servicio de IA: {str(e)}"
            }
        except Exception as e:
            logger.error(f"Error no controlado en ClaudeService: {e}", exc_info=True)
            return {
                "status": "error",
                "error_type": "UnexpectedError",
                "message": f"Ocurrió un error inesperado al procesar la consulta: {str(e)}"
            }
