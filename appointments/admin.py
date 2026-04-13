from django.contrib import admin
from .models import Appointment, Prescription, PrescriptionItem
admin.site.register(Appointment)
admin.site.register(Prescription)
admin.site.register(PrescriptionItem)