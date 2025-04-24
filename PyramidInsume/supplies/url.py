
from django.contrib import admin
from django.urls import path
from .views import SuppliesListView, SuppliesCreateView, SuppliesUpdateView, SuppliesDeleteView

urlpatterns = [
    path('list', SuppliesListView.as_view(), name='supplies_list'),
    path('new/', SuppliesCreateView.as_view(), name='insumo_create'),
    path('<int:pk>/edit/', SuppliesUpdateView.as_view(), name='insumo_update'),
    path('<int:pk>/delete/', SuppliesDeleteView.as_view(), name='insumo_delete'),
    
]
