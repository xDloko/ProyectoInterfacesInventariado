
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    #dashboard
    path('dashboard/', DashBoard.as_view(), name='admin_dashboard'),
    path('dashboard/list', UserListView.as_view(), name='user_list'),
    path('dashboard/new/', UserCreateView.as_view(), name='user_create'),
    path('dashboard/<int:pk>/edit/', UserUpdateView.as_view(), name='user_update'),
    path('dashboard/<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
    path('dashboard/<int:pk>/toggle-active/', toggle_user_active, name='user_toggle_active'),
    #login
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    #password reset
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/forbidenpassword/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/forbidenpassword/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/forbidenpassword/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/forbidenpassword/password_reset_complete.html'), name='password_reset_complete'),
    
]