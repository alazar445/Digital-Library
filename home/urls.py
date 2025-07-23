from django.urls import path
from .views import home, register, login_view

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
] 