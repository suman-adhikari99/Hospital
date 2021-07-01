from appointment.models import Appointment, Doctor, Profile
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import  AppointmentForm, NewUserForm, UserUpdateForm, ProfileUpdateForm, UserUpdateForm

from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages




# Create your views here.



#def appointment(request):
#    if request.method=='POST':
#        
#        form=AppointmentForm(request.POST)
#        if form.is_valid():
#            print('we are valid')
#            appointment=form.save(commit=False)
#            appointment.user=request.user
#            appointment.save()
#            
#    else:
#        form=AppointmentForm()
#    return render(request,'appointment.html',{'form':form})

'''
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

'''

def register(request):
    if request.method=='POST':
        form=NewUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request, user,backend='django.contrib.auth.backends.ModelBackend')
            return redirect('profile')
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
                return redirect('profile')
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
            return redirect('profile')
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



def updateAppointment(request,id=0):
    if request.method == "POST":
        if id==0:
            form = AppointmentForm(request.POST)
        else:
            obj=Appointment.objects.get(pk=id)
            form=AppointmentForm(request.POST,instance=obj)

        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.save()    
            return redirect('homepage')
            
    else:
        if id==0:
            form = AppointmentForm()
            return render(request, 'appointment.html', {'form':form})
        else:
            obj=Appointment.objects.get(pk=id)
            form=AppointmentForm(instance=obj)
            return render(request,'appointment.html', {'form':form})


def delAppointment(request,id=id):
    obj=Appointment.objects.get(pk=id)
    obj.delete()
    return redirect(profile)




def profile(request):
    if request.method=='POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            print('we reach to valid form ')
            uform = u_form.save(commit=False)
            pform = p_form.save(commit=False)
            uform.save()
            pform.save()
            messages.success(request, f'your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    obj=Appointment.objects.filter(user=request.user)  ## this line will solve your appointment problem in profile
    
    context = {
            'u_form':u_form,
            'p_form':p_form,
            'appointment':obj
        
        }
    return render(request,'profile.html', context)

    