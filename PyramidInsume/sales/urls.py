from django.urls import path
from .views import DashboardView, registrar_venta

urlpatterns = [
    path('', DashboardView.as_view(), name='sales_dashboard'),
    path('vender/', registrar_venta, name='registrar_venta'),
]
