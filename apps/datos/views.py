"""
==============================================================================
apps/datos/views.py - Vistas CRUD para el Catálogo de Ítems
==============================================================================
Explicación para alumnos:
En Django, las Class-Based Views (CBV) simplifican enormemente las operaciones CRUD
(Create, Read, Update, Delete) siguiendo el principio DRY (Don't Repeat Yourself):
- 'ListView': Consulta y lista objetos con soporte para paginación y búsqueda.
- 'DetailView': Muestra un único registro según su Primary Key (pk).
- 'CreateView' / 'UpdateView': Manejan formularios automáticamente.
- 'DeleteView': Muestra pantalla de confirmación y elimina el registro.
- 'LoginRequiredMixin': Protege las vistas para requerir inicio de sesión previo.
==============================================================================
"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .forms import ItemForm
from .models import Item


class ItemListView(ListView):
    """Lista todos los ítems con buscador por texto y filtro por categoría."""
    model = Item
    template_name = 'datos/lista.html'
    context_object_name = 'items'
    paginate_by = 10

    def get_queryset(self):
        queryset = Item.objects.all()
        q = self.request.GET.get('q', '').strip()
        categoria = self.request.GET.get('categoria', '').strip()

        if q:
            queryset = queryset.buscar_por_texto(q)
        if categoria:
            queryset = queryset.filtrar_por_categoria(categoria)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['categoria_filtro'] = self.request.GET.get('categoria', '')
        context['categorias_disponibles'] = Item.objects.values_list('categoria', flat=True).distinct()
        return context


class ItemDetailView(DetailView):
    """Muestra la vista en detalle de un ítem."""
    model = Item
    template_name = 'datos/detalle.html'
    context_object_name = 'item'


class ItemCreateView(LoginRequiredMixin, CreateView):
    """Crea un nuevo ítem en el catálogo (Requiere autenticación)."""
    model = Item
    form_class = ItemForm
    template_name = 'datos/form.html'
    success_url = reverse_lazy('datos:lista')

    def form_valid(self, form):
        messages.success(self.request, f"Ítem '{form.instance.titulo}' creado exitosamente.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accion'] = 'Crear Nuevo Ítem'
        return context


class ItemUpdateView(LoginRequiredMixin, UpdateView):
    """Edita un ítem existente (Requiere autenticación)."""
    model = Item
    form_class = ItemForm
    template_name = 'datos/form.html'
    success_url = reverse_lazy('datos:lista')

    def form_valid(self, form):
        messages.success(self.request, f"Ítem '{form.instance.titulo}' actualizado correctamente.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accion'] = 'Editar Ítem'
        return context


class ItemDeleteView(LoginRequiredMixin, DeleteView):
    """Elimina un ítem con confirmación previa (Requiere autenticación)."""
    model = Item
    template_name = 'datos/confirmar_eliminar.html'
    context_object_name = 'item'
    success_url = reverse_lazy('datos:lista')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.warning(self.request, f"El ítem '{obj.titulo}' ha sido eliminado.")
        return super().delete(request, *args, **kwargs)
