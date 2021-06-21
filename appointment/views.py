from appointment.models import Appointment, Doctor
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
        print('yes')
        date = request.POST['date']
        patient_name = request.POST['patient_name']
        doctor = request.POST['doctor']
        time = request.POST['time']
        user = request.user
        appointments=Appointment(user=user,date=date,patient_name=patient_name,doctor=doctor,time=time)
        appointments.save()
        print(user)
        return redirect('homepage')
    doctor=Doctor.objects.all()
    return render(request, 'appointment.html',{'doctor':doctor})



def register(request):
    if request.method=='POST':
        form=NewUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request, user,backend='django.contrib.auth.backends.ModelBackend')
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
            messages.error(request, 'Invalid form')
    
    form = AuthenticationForm()
    return render(request, 'login.html', {'login_form':form})

  

def login_home(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'successfully logged')
            return redirect('appointment')
        else:
            messages.error(request, 'Invalid username or password')
       
    
    form = AuthenticationForm()
    return render(request, 'home.html',{'form':form})



def logout_request(request):
    logout(request)
    return redirect('login')


from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


def password_reset_request(request):
    if request.method == 'POST':
        password_reset_from = PasswordResetForm(request.POST)
        if password_reset_from.is_valid():
            data= password_reset_from.cleaned_data['email']
            user= User.objects.get(email=data)
            print(user)
            if user:
                subject='password RESET Request'
                email_template_name ='password_reset_email.txt'
                c={
                    'email': user.email,
                    'domain': '127.0.0.1:8000',
                    'site': 'demo website',
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    'protocol': 'http',
                }
                email= render_to_string(email_template_name,c)
                send_mail(subject,email,'abc@gmail.com',[user.email], fail_silently=False)
                return redirect('/password_reset/done/')
            messages.error(request, 'An invalid email has been entered.')
    password_reset_from= PasswordResetForm()
    return render(request=request, template_name='password_reset.html',context={'password_reset_form':password_reset_from})



