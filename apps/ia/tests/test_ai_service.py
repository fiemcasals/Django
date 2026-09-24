"""
==============================================================================
apps/ia/tests/test_ai_service.py - Suite de Tests Unitarios para ClaudeService
==============================================================================
Explicación para alumnos:
En aplicaciones que interactúan con APIs externas de Inteligencia Artificial
(como Anthropic Claude), NO debemos hacer peticiones HTTP reales durante las
pruebas automatizadas por tres motivos clave:
1. Consumo de dinero/cuota innecesario en cada ejecución de 'python manage.py test'.
2. Dependencia de conexión a internet o de la disponibilidad de la API externa.
3. Falta de predictibilidad (los LLM pueden variar sutilmente su salida).

Por ello, usamos 'unittest.mock' (@patch, MagicMock) para simular las respuestas
de Anthropic y verificar fielmente que la lógica de las 2 Fases y el manejo de
errores funcionen a la perfección.
==============================================================================
"""

from unittest.mock import patch, MagicMock
from django.test import TestCase
from apps.datos.models import Item
from apps.ia.services import ClaudeService, TOOLS_DEFINITIONS


class ClaudeServiceTestCase(TestCase):
    """
    Suite de pruebas para validar el servicio de IA ClaudeService:
    1. Esquema mínimo de herramientas (ahorro de tokens).
    2. Fase 1: Selección de Tool y ejecución local con ORM.
    3. Fase 2: Síntesis completa en dos pasos.
    4. Manejo resiliente de errores de API y claves faltantes.
    """

    def setUp(self):
        """Crea registros de prueba en la base de datos para la ejecución local."""
        self.item1 = Item.objects.create(
            titulo="Introducción a Django",
            categoria="tutorial",
            descripcion="Aprende la arquitectura MVT y el flujo HTTP en Django.",
            precio=0.00,
            disponible=True
        )
        self.item2 = Item.objects.create(
            titulo="Indexación en PostgreSQL",
            categoria="avanzado",
            descripcion="Optimización de consultas con índices compuestos B-Tree.",
            precio=25.50,
            disponible=True
        )

    def test_herramientas_schema_minimo(self):
        """
        1. Valida que el esquema de herramientas sea liviano y cumpla con el estándar
        JSON Schema requerido por Anthropic para no transferir filas innecesarias.
        """
        schemas = ClaudeService.get_tools_schema()
        self.assertIsInstance(schemas, list)
        self.assertGreaterEqual(len(schemas), 4)

        nombres_herramientas = [t["name"] for t in schemas]
        self.assertIn("buscar_items_por_texto", nombres_herramientas)
        self.assertIn("filtrar_items_por_categoria", nombres_herramientas)
        self.assertIn("obtener_detalle_item", nombres_herramientas)
        self.assertIn("listar_catalogo_resumen", nombres_herramientas)

        # Verificamos que contengan 'input_schema'
        for t in schemas:
            self.assertIn("input_schema", t)
            self.assertEqual(t["input_schema"]["type"], "object")

    def test_fase_1_seleccion_de_herramienta_y_ejecucion_local(self):
        """
        2. Valida la ejecución local de las herramientas seleccionadas en Fase 1,
        asegurando que interactúen con el ORM y devuelvan los datos filtrados.
        """
        service = ClaudeService(api_key="test-dummy-key")

        # Test de búsqueda por texto
        res_busqueda = service.ejecutar_herramienta_local("buscar_items_por_texto", {"query": "PostgreSQL"})
        self.assertEqual(res_busqueda["tool"], "buscar_items_por_texto")
        self.assertEqual(res_busqueda["total"], 1)
        self.assertEqual(res_busqueda["resultados"][0]["id"], self.item2.id)

        # Test de filtrado por categoría
        res_cat = service.ejecutar_herramienta_local("filtrar_items_por_categoria", {"categoria": "tutorial"})
        self.assertEqual(res_cat["total"], 1)
        self.assertEqual(res_cat["resultados"][0]["id"], self.item1.id)

        # Test de detalle puntual
        res_det = service.ejecutar_herramienta_local("obtener_detalle_item", {"id": self.item1.id})
        self.assertEqual(res_det["total"], 1)
        self.assertEqual(res_det["resultados"][0]["titulo"], "Introducción a Django")

    @patch("apps.ia.services.anthropic.Anthropic")
    def test_fase_2_sintesis_completa_con_datos_locales(self, mock_anthropic_class):
        """
        3. Valida el ciclo completo en 2 Fases simulando las dos respuestas de Claude:
        - Turno 1: Devuelve 'tool_use' para 'buscar_items_por_texto'.
        - Turno 2: Devuelve la respuesta final sintetizada con los datos locales.
        """
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        # Mock de Fase 1 (Bloque de tool_use)
        mock_block_tool = MagicMock()
        mock_block_tool.type = "tool_use"
        mock_block_tool.id = "toolu_01ABC123"
        mock_block_tool.name = "buscar_items_por_texto"
        mock_block_tool.input = {"query": "Django"}

        mock_resp_fase1 = MagicMock()
        mock_resp_fase1.content = [mock_block_tool]
        mock_resp_fase1.usage.input_tokens = 150
        mock_resp_fase1.usage.output_tokens = 40

        # Mock de Fase 2 (Texto final sintetizado)
        mock_block_text = MagicMock()
        mock_block_text.type = "text"
        mock_block_text.text = "Encontré 1 recurso sobre Django: 'Introducción a Django' (categoría: tutorial)."

        mock_resp_fase2 = MagicMock()
        mock_resp_fase2.content = [mock_block_text]
        mock_resp_fase2.usage.input_tokens = 280
        mock_resp_fase2.usage.output_tokens = 60

        # El cliente responde primero con Fase 1, luego con Fase 2
        mock_client.messages.create.side_effect = [mock_resp_fase1, mock_resp_fase2]

        service = ClaudeService(api_key="sk-ant-test-dummy-key-12345")
        resultado = service.procesar_consulta("¿Tienen algún tutorial introductorio sobre Django?")

        # Verificaciones del flujo completo
        self.assertEqual(resultado["status"], "success")
        self.assertEqual(resultado["tipo_respuesta"], "tool_calling")
        self.assertEqual(resultado["fase_1"]["tool_invocado"], "buscar_items_por_texto")
        self.assertEqual(resultado["fase_1"]["parametros"], {"query": "Django"})
        self.assertEqual(resultado["fase_2"]["registros_encontrados"], 1)
        self.assertIn("Introducción a Django", resultado["fase_2"]["respuesta_final"])
        self.assertEqual(resultado["total_tokens"], 150 + 40 + 280 + 60)
        self.assertEqual(mock_client.messages.create.call_count, 2)

    @patch("apps.ia.services.anthropic.Anthropic")
    def test_manejo_resiliente_de_errores(self, mock_anthropic_class):
        """
        4. Valida que ante errores de conexión, cuota excedida o clave faltante,
        el servicio responda limpiamente con diccionarios de error sin lanzar HTTP 500.
        """
        # Caso A: Falta de API Key
        service_sin_key = ClaudeService(api_key="")
        res_sin_key = service_sin_key.procesar_consulta("Hola")
        self.assertEqual(res_sin_key["status"], "error")
        self.assertEqual(res_sin_key["error_type"], "MissingApiKey")

        # Caso B: Error de Autenticación simulado
        import anthropic
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client
        mock_client.messages.create.side_effect = anthropic.AuthenticationError(
            message="Invalid API Key",
            response=MagicMock(status_code=401),
            body={"error": {"type": "authentication_error"}}
        )

        service_con_error = ClaudeService(api_key="sk-ant-clave-invalida")
        res_auth_error = service_con_error.procesar_consulta("Buscar Django")
        self.assertEqual(res_auth_error["status"], "error")
        self.assertEqual(res_auth_error["error_type"], "AuthenticationError")
        self.assertIn("inválida", res_auth_error["message"])
