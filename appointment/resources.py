from import_export import resources
from .models import Doctor

class DoctorResource(resources.ModelResource):
    class Meta:
        model = Doctor

#https://simpleisbetterthancomplex.com/packages/2016/08/11/django-import-export.html