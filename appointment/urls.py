from django.urls import path
from . import views



urlpatterns = [
    # path('register/', views.register, name='register'),
    path('register_appointment/', views.appointment, name='appointment'),
    path('register/', views.register, name='register'),
    path('', views.homepage, name='homepage'),
    path('login/', views.login_request, name='login'),
    path('login_home/', views.login_home, name='login_home'),
   
    path('logout/', views.logout_request, name='logout'),
    
    path('password_reset/', views.password_reset_request,name="password_reset")






]