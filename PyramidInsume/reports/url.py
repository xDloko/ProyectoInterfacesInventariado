
from django.contrib import admin
from django.urls import path
from .views import ReportesView


urlpatterns = [
    path('reportes/', ReportesView.as_view(), name='reports'),
    
]


