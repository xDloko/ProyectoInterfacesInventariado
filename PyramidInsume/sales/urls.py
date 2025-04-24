from django.urls import path
from .views import SalesList, VentaCreateView, VentaUpdateView, VentaDeleteView

urlpatterns = [
    path('list', SalesList.as_view(), name='sales_list'),
    path('vender/', VentaCreateView.as_view(), name='venta_create'),
    path('<int:pk>/edit/', VentaUpdateView.as_view(), name='venta_update'),
    path('<int:pk>/delete/', VentaDeleteView.as_view(), name='venta_delete'),
    
]
