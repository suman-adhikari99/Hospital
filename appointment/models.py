

from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    patient_name = models.CharField(max_length=120)
    doctor= models.ForeignKey(Doctor,on_delete=models.CASCADE)
    time = models.TimeField()
    def __str__(self):
        return '{} ({})'.format(self.user,self.doctor)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')

    def __str__(self) :
        return f'{self.user.username}Profile'







