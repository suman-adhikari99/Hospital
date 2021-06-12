from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import fields

from .models import Appointment

# Create your forms here.

# Create Appointment form here
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'

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



