import json

from reportlab.lib.utils import prev_this_next
from appointment.models import Appointment, Doctor, Profile
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import  AppointmentForm, NewUserForm, UserUpdateForm, ProfileUpdateForm, UserUpdateForm

from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages




# Create your views here.


import requests
def covid(request):
    data= True
    result=None
    countries=None
    while(data):
        try:
            result= requests.get('http://api.covid19api.com/summary') 
            #print(result.json()['Global'])
            #print(type(result))
            covid_data=result.json()['Global'] 
            json=result.json()  
            countries=json['Countries']
            print(countries)
            data=False
        except:
            data=True
        data_of_nepal={}

        for c in countries:
            if c['Country']=="Nepal":
                #print(c['TotalRecovered'])
                data_of_nepal={
                    'TotalRecovered':c['TotalRecovered'],
                    'NewConfirmed':c['NewConfirmed'],
                    'TotalConfirmed':c[ 'TotalConfirmed'],
                    'NewDeaths':c['NewDeaths'],
                    'TotalDeaths':c['TotalDeaths'],
                    'NewRecovered':c['NewRecovered']

                }
                break
        #print(type(data_of_nepal))
        #print(data_of_nepal)
        print(data_of_nepal['NewConfirmed'])
    return render(request,"covid.html", {'global':covid_data,
                                         'countries':countries, 
                                         'data_of_nepal':data_of_nepal  })



from django.http import FileResponse
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

def appointment_pdf(request):
    #create bytestream buffer
    buf=BytesIO()
    #create a canvas
    c= canvas.Canvas(buf, pagesize=letter, bottomup=0)
    #create text obj
    textob= c.beginText()
    textob.setTextOrigin(inch,inch)
    textob.setFont("Helvetica",14)
    #add some lines of text
    #lines=[
    #    'this is line 1',
    #    'this is line 2'
    #]
    lines=[]
    appoint=Doctor.objects.all()
    print(appoint)
    for appoints in appoint:
        lines.append(appoints.name)
        lines.append(appoints.department)
        lines.append(appoints.address)
        lines.append("________________________")

        #lines.append(appoints.user)
        #lines.append(appoints.date)
        #lines.append(appoints.patient_name)
        #lines.append(appoints.doctor)
        #lines.append(appoints.time)
        #lines.append(appoints.payment_method)
    for line in lines:
        textob.textLine(line)
    #finish up
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    #return something
    return FileResponse(buf,as_attachment=True,filename='appointment.pdf')
    


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
    if request.method=='POST':
        
        form=AppointmentForm(request.POST)
        if form.is_valid():
            print('we are valid')
            appointment=form.save(commit=False)
            appointment.user=request.user
            appointment.save()
            
   
    appointmentform=AppointmentForm()
    return render(request,'appointment.html', {'form':appointmentform})

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

def dashboard(request):
    appoint=Appointment.objects.all()
    current_user=request.user
    doctor=Doctor.objects.all()


    context={
        'appointment':appoint,
        'current_user':current_user,
        'doctor':doctor,

<<<<<<< HEAD
    }
    return render(request,'dashboard.html',context=context)
=======
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
            payment_method= appointment.payment_method
            id = appointment.id
            print(id)
            print(type(payment_method) )
            return render(request, 'esewa.html',{'id':id})
    else:
        if id==0:
            form = AppointmentForm()
            return render(request, 'appointment.html', {'form':form})
        else:
            obj=Appointment.objects.get(pk=id)
            form=AppointmentForm(instance=obj)
            return render(request,'appointment.html', {'form':form})

import requests as req
def EsewaVerifyView(request):
    if request.method =="GET" :
        amt = request.GET.get("amt")
        refId = request.GET.get("refId")
        oid= request.GET.get("pid")
        print(amt,refId,oid)
        url = "https://uat.esewa.com.np/epay/transrec"
        d = {
            'amt': amt,
            'scd': 'epay_payment',
            'rid': refId,
            'pid': oid,
        }
        return redirect('homepage')



'''
class EsewaVerifyView(View):
    def get(self, request, *args, **kwargs):
        import xml.etree.ElementTree as ET
        oid = request.GET.get("oid")
        amt = request.GET.get("amt")
        refId = request.GET.get("refId")

        url = "https://uat.esewa.com.np/epay/transrec"
        d = {
            'amt': amt,
            'scd': 'epay_payment',
            'rid': refId,
            'pid': oid,
        }
        resp = requests.post(url, d)
        root = ET.fromstring(resp.content)
        status = root[0].text.strip()

        order_id = oid.split("_")[1]
        order_obj = Order.objects.get(id=order_id)
        if status == "Success":
            order_obj.payment_completed = True
            order_obj.save()
            return redirect("/")
        else:

            return redirect("/esewa-request/?o_id="+order_id)
'''


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

<<<<<<< HEAD
    obj=Appointment.objects.filter(user=request.user)
=======
    obj=Appointment.objects.filter(user=request.user)  ## this line will solve your appointment problem in profile
>>>>>>> 1a14cea93dc8df39a6fb25a106bb70fe31b07578
    
    context = {
            'u_form':u_form,
            'p_form':p_form,
            'appointment':obj
        
        }
    return render(request,'profile.html', context)

    
<<<<<<< HEAD

from django.http import HttpResponse
from .resources import DoctorResource
def export(request):
    doctor_resource = DoctorResource()
    dataset = doctor_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="doctor.xls"'
    return response


from tablib import Dataset

def simple_upload(request):
    if request.method == 'POST':
        doctor_resource = DoctorResource()
        dataset = Dataset()
        new_doctors = request.FILES['myfile']

        imported_data = dataset.load(new_doctors.read())
        result = doctor_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            doctor_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'import.html')




########    ###these are for chat system############################
def index(request):
    return render(request,'index.html')

def logins(request):
    return render(request,'logins.html')
    

def signup(request):
    return render(request,'signup.html')

def chat(request):
    return render(request,'chat.html')
=======
>>>>>>> f89d409b3d2a4ac6e66b245991fb6c412ab8b9dd
>>>>>>> 1a14cea93dc8df39a6fb25a106bb70fe31b07578
