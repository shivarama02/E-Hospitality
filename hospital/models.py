
from django.db import models

# Patient Module
class Patient(models.Model):
	pname = models.CharField(max_length=100)
	dob = models.DateField(null=True, blank=True)
	gender = models.CharField(max_length=10, null=True, blank=True)
	contact = models.CharField(max_length=20)
	address = models.TextField()
	email = models.EmailField(unique=True)
	password = models.CharField(max_length=128)
	insurance_info = models.TextField(blank=True, null=True)

	def __str__(self):
		return self.pname

class Appointment(models.Model):
	patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
	doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE)
	date = models.DateField()
	time = models.TimeField()
	status = models.CharField(max_length=20)

	def __str__(self):
		return f"{self.patient.pname} - {self.date}"

class MedicalHistory(models.Model):
	patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
	diagnosis = models.CharField(max_length=255)
	treatment = models.TextField()
	allergies = models.TextField(blank=True, null=True)
	notes = models.TextField(blank=True, null=True)

	def __str__(self):
		return f"{self.patient.pname} - {self.diagnosis}"

class Billing(models.Model):
	patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
	invoice_number = models.CharField(max_length=50, unique=True)
	amount = models.DecimalField(max_digits=10, decimal_places=2)
	payment_status = models.CharField(max_length=20)
	payment_date = models.DateField(blank=True, null=True)

	def __str__(self):
		return self.invoice_number

class HealthResource(models.Model):
	title = models.CharField(max_length=255)
	description = models.TextField()
	file_url = models.URLField(blank=True, null=True)
	category = models.CharField(max_length=100)

	def __str__(self):
		return self.title

# Admin Module
class User(models.Model):
	ROLE_CHOICES = [
		('admin', 'Admin'),
		('doctor', 'Doctor'),
		('patient', 'Patient'),
	]
	username = models.CharField(max_length=100, unique=True)
	password = models.CharField(max_length=128)
	role = models.CharField(max_length=10, choices=ROLE_CHOICES)
	status = models.CharField(max_length=20)

	def __str__(self):
		return self.username

class Facility(models.Model):
	name = models.CharField(max_length=255)
	location = models.CharField(max_length=255)
	department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True)
	bed_count = models.IntegerField()

	def __str__(self):
		return self.name

class Department(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField()

	def __str__(self):
		return self.name

# appointment_overview is covered by Appointment model (admin can see all)

# Doctor Module
class Doctor(models.Model):
	name = models.CharField(max_length=100)
	specialization = models.CharField(max_length=100)
	contact = models.CharField(max_length=20)
	email = models.EmailField(unique=True)
	password = models.CharField(max_length=128)
	department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True)

	def __str__(self):
		return self.name

class Prescription(models.Model):
	patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
	doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE)
	medication_name = models.CharField(max_length=255)
	dosage = models.CharField(max_length=100)
	duration = models.CharField(max_length=100)
	notes = models.TextField(blank=True, null=True)

	def __str__(self):
		return f"{self.medication_name} for {self.patient.pname}"

class DrugInteraction(models.Model):
	drug1 = models.CharField(max_length=100)
	drug2 = models.CharField(max_length=100)
	interaction_details = models.TextField()

	def __str__(self):
		return f"{self.drug1} & {self.drug2}"

# Shared Table
class Notification(models.Model):
	user = models.ForeignKey('User', on_delete=models.CASCADE)
	message = models.TextField()
	type = models.CharField(max_length=50)
	status = models.CharField(max_length=20)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.user.username} - {self.type}"

# Create your models here.
