from django.contrib import admin
from .models import Patient, Appointment, MedicalHistory, Billing, HealthResource, User, Facility, Department, Doctor, Prescription, DrugInteraction, Notification

admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(MedicalHistory)
admin.site.register(Billing)
admin.site.register(HealthResource)
admin.site.register(User)
admin.site.register(Facility)
admin.site.register(Department)
admin.site.register(Doctor)
admin.site.register(Prescription)
admin.site.register(DrugInteraction)
admin.site.register(Notification)
