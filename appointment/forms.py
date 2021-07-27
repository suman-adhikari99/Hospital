from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import fields

from .models import Appointment,Doctor, Profile

# Create your forms here.

# Create Appointment form here
class AppointmentForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    patient_name = forms.CharField(max_length=120)
    # doctor = forms.CharField(max_length=120)
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type':'time'}))
    class Meta:
        model = Appointment
        fields = ('user','date','patient_name','doctor','time','payment_method')

class NewUserForm(UserCreationForm):
    email= forms.EmailField()
     
    class Meta:
        model=User 
        fields=("username", 'email', 'password1','password2')

    def save(self,commit=True):
        user = super(NewUserForm,self).save(commit=False)
        user.email=self.cleaned_data['email']
        if commit:
            user.save()
        return user
    

    def __str__(self):
        return 

    def __unicode__(self):
        return 

'''
  


<<<<<<< HEAD
=======
class UserUpdateForm(forms.ModelForm):
    email= forms.EmailField()
    class Meta:
        model = User
        fields=['username','email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['image']



<<<<<<< HEAD
=======

>>>>>>> f89d409b3d2a4ac6e66b245991fb6c412ab8b9dd
'''
>>>>>>> 1a14cea93dc8df39a6fb25a106bb70fe31b07578
