from appointment.models import Appointment
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import  AppointmentForm, NewUserForm

from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages




# Create your views here.

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html" 

def appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            return redirect('appointment')
        
    else:
        form = AppointmentForm()
    return render(request, 'appointment.html', {'form': form})



def register(request):
    if request.method=='POST':
        form=NewUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request, user)
        return redirect('homepage')
    else:
        form= NewUserForm()
    return render(request,'register.html', {'form':form})


def homepage(request):
    return render(request, 'home.html')

    

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('appointment')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password')
    
    form = AuthenticationForm()
    return render(request, 'login.html', {'login_form':form})

  
    

def logout_request(request):
    logout(request)
    return redirect('login')