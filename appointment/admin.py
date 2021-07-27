from django.contrib import admin
from .models import Appointment, Doctor,Profile
# Register your models here.
admin.site.register(Appointment)
admin.site.register(Profile)




from import_export.admin import ImportExportModelAdmin

@admin.register(Doctor)
class DoctorAdmin(ImportExportModelAdmin):

    pass