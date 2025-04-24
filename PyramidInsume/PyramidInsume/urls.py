
from django.contrib import admin
from django.urls import path, include
from users.views import CustomLoginView

urlpatterns = [
    #Redirigir al login si estan en ''
    path('', CustomLoginView.as_view(), name='login'),
    #urls
    path('admin/', admin.site.urls),
    path('users/', include('users.url')),
    path('supplies/', include('supplies.url')),
    path('sales/', include('sales.urls')),
]

