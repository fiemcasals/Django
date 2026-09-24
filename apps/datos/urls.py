"""
==============================================================================
apps/datos/urls.py - Enrutador del Catálogo CRUD de Ítems
==============================================================================
"""

from django.urls import path
from . import views

app_name = 'datos'

urlpatterns = [
    path('', views.ItemListView.as_view(), name='lista'),
    path('<int:pk>/', views.ItemDetailView.as_view(), name='detalle'),
    path('crear/', views.ItemCreateView.as_view(), name='crear'),
    path('<int:pk>/editar/', views.ItemUpdateView.as_view(), name='editar'),
    path('<int:pk>/eliminar/', views.ItemDeleteView.as_view(), name='eliminar'),
]
