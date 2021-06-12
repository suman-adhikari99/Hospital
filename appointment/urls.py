from django.urls import path
from . import views

urlpatterns = [
    # path('register/', views.register, name='register'),
    path('register_appointment/', views.appointment, name='appointment'),
    path('register/', views.register, name='register'),
    path('homepage/', views.homepage, name='homepage'),
    path('login/', views.login_request, name='login'),
   
    path('logout/', views.logout_request, name='logout'),




]