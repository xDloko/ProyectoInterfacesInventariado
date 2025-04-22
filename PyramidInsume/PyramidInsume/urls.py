
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.url')),
    path('supplies/', include('supplies.url')),
    path('sales/', include('sales.urls')),
]
