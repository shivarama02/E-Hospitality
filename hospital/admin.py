from django.contrib import admin
from .models import Patient, Appointment, MedicalHistory, Billing, HealthResource, User, Facility, Department, Doctor, Prescription, PrescriptionItem, DrugInteraction, Notification


class PrescriptionItemInline(admin.TabularInline):
	model = PrescriptionItem
	extra = 0


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
	list_display = ('id', 'patient', 'doctor', 'visit_datetime', 'amount', 'created_at')
	list_filter = ('doctor', 'patient')
	search_fields = ('patient__pname', 'doctor__name')
	inlines = [PrescriptionItemInline]

admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(MedicalHistory)
admin.site.register(Billing)
admin.site.register(HealthResource)
admin.site.register(User)
admin.site.register(Facility)
admin.site.register(Department)
admin.site.register(Doctor)
admin.site.register(DrugInteraction)
admin.site.register(Notification)
