
from django.contrib import admin
from django.urls import path
from .views import (
    UserListView, 
    UserCreateView, 
    UserUpdateView, 
    UserDeleteView,
    toggle_user_active,
    CustomLoginView,
    logout_view,
)

urlpatterns = [
    path('', UserListView.as_view(), name='user_list'),
    path('new/', UserCreateView.as_view(), name='user_create'),
    path('<int:pk>/edit/', UserUpdateView.as_view(), name='user_update'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
    path('<int:pk>/toggle-active/', toggle_user_active, name='user_toggle_active'),
    #login
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
]