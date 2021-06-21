

from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# Create your models here.
class Appointment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    patient_name = models.CharField(max_length=120)
    doctor= models.CharField(max_length=120)
    time = models.TimeField()
    def __str__(self):
        return '{} ({})'.format(self.user,self.doctor)

class Doctor(models.Model):
    name =models.CharField(max_length=120)
    address=models.CharField(max_length=33)
    departments = [('Cardiology', 'Cardiology'), ('Dermatology','Dermatology'), ('Immunology','Immunology'), ('Anesthesiology','Anesthesiology'), ('Emergency', 'Emergency')]
    department=models.CharField(max_length=23,choices=departments, default='cardiologist')
    status=models.BooleanField(default=False)
    def __str__(self):
        return '{} ({})'.format(self.name,self.department)










