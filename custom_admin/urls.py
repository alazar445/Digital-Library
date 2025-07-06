from django.urls import path
from . import views

urlpatterns = [
    path('admin_login/', views.custom_admin_login, name='admin_login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('logout/', views.custom_logout, name='logout'),


]

