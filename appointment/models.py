

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


# Create your models here.



class Doctor(models.Model):
    name =models.CharField(max_length=120)
    address=models.CharField(max_length=33)
    departments = [('Cardiology', 'Cardiology'), ('Dermatology','Dermatology'), ('Immunology','Immunology'), ('Anesthesiology','Anesthesiology'), ('Emergency', 'Emergency')]
    department=models.CharField(max_length=23,choices=departments, default='cardiologist')
    status=models.BooleanField(default=False)
    def __str__(self):
        return '{} ({})'.format(self.name,self.department)


class Appointment(models.Model):
    METHOD = (
    ("Cash On Delivery", "Cash On Delivery"),
    ("Khalti", "Khalti"),
    ("Esewa", "Esewa"),)


    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    patient_name = models.CharField(max_length=120)
    doctor= models.ForeignKey(Doctor,on_delete=models.CASCADE)
    time = models.TimeField()
    payment_method = models.CharField( max_length=20, choices=METHOD, default="Cash On Delivery")
    payment_completed = models.BooleanField(
        default=False, null=True, blank=True)

    def __str__(self):
        return '{} ({})'.format(self.user,self.doctor)




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')


    def __str__(self) :
        return f'{self.user.username}Profile'







