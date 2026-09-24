"""
==============================================================================
apps/datos/models.py - Modelo de Datos con Índices y Extracción Liviana (Tokens)
==============================================================================
Explicación para alumnos:
1. 'db_index=True' e 'indexes en Meta':
   En PostgreSQL y bases relacionales, los índices son estructuras tipo árbol B
   que aceleran drásticamente las consultas WHERE y ORDER BY (de O(N) a O(log N)).
2. Optimización de Tokens para IA (Claude / LLMs):
   Al consultar datos para enviárselos a un LLM en un flujo de Tool Calling,
   enviar registros enteros con descripciones largas consume miles de tokens innecesarios.
   El método 'obtener_catalogo_indice()' extrae ÚNICAMENTE los metadatos esenciales
   (id, titulo, categoria), reduciendo el consumo de tokens en hasta un 90%.
==============================================================================
"""

from django.db import models
from django.db.models import Q


class ItemManager(models.Manager):
    """
    Manager personalizado para operaciones de consulta y optimización de tokens.
    """

    def obtener_catalogo_indice(self):
        """
        Retorna una lista de diccionarios con metadatos ultralivianos (id, titulo, categoria)
        únicamente de los ítems disponibles.
        Ideal para la Fase 1 del Tool Calling de IA (selección económica de herramientas).
        """
        return list(self.filter(disponible=True).values('id', 'titulo', 'categoria'))

    def buscar_por_texto(self, query):
        """Búsqueda parametrizada que filtra por título o descripción ignorando mayúsculas."""
        if not query:
            return self.none()
        return self.filter(Q(titulo__icontains=query) | Q(descripcion__icontains=query))

    def filtrar_por_categoria(self, categoria):
        """Filtra registros por categoría específica de forma optimizada por índice."""
        return self.filter(categoria__iexact=categoria)


class Item(models.Model):
    """
    Modelo representativo de un Recurso / Ítem de catálogo con soporte para
    índices compuestos en PostgreSQL y consultas optimizadas para IA.
    """
    titulo = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name="Título del Ítem",
        help_text="Nombre descriptivo. Cuenta con índice en BD para búsquedas rápidas."
    )
    categoria = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name="Categoría",
        help_text="Clasificación temática (ej. Tecnología, Documentación, Tutoriales)."
    )
    descripcion = models.TextField(
        verbose_name="Descripción Completa",
        help_text="Detalle exhaustivo del contenido del ítem."
    )
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name="Precio / Costo",
        help_text="Valor numérico con dos decimales."
    )
    disponible = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name="¿Disponible?",
        help_text="Define si el ítem está visible para consultas y catálogo."
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación"
    )

    objects = ItemManager()

    class Meta:
        verbose_name = "Ítem / Recurso"
        verbose_name_plural = "Ítems / Recursos"
        ordering = ['-fecha_creacion']
        # Índices compuestos optimizados para PostgreSQL
        indexes = [
            models.Index(fields=['categoria', 'disponible'], name='idx_item_cat_disp'),
            models.Index(fields=['titulo'], name='idx_item_titulo'),
        ]

    def __str__(self):
        return f"{self.titulo} [{self.categoria}]"
