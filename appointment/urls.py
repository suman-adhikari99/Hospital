from collections import namedtuple
from django.urls import path
from . import views



urlpatterns = [
    # path('register/', views.register, name='register'),
    path('appoint_pdf/',views.appointment_pdf),
    path('covid/',views.covid),
    path('register_appointment/', views.updateAppointment, name='appointment'),
    path("esewa-verify/", views.EsewaVerifyView, name="esewaverify"),
    path('register/', views.register, name='register'),
    path('', views.homepage, name='homepage'),
    path('login/', views.login_request, name='login'),
    path('login_home/', views.login_home, name='login_home'),
   
    path('logout/', views.logout_request, name='logout'),
    
    path('password_reset/', views.password_reset_request,name="password_reset"),
    path('update/<int:id>/', views.updateAppointment,name='updateAppointment'),
    
    path('delete/<int:id>/', views.delAppointment, name='delAppointment'),
    path('profile/', views.profile, name='profile'),
    path('profile/', views.profile, name='profile'),







]