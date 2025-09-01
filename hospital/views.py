# Admin Doctor Management CRUD
from django.shortcuts import get_object_or_404

def doctor_management(request):
	doctors = Doctor.objects.all()
	return render(request, 'admin/doctor_management.html', {'doctors': doctors})

def add_doctor(request):
	if request.method == 'POST':
		name = request.POST.get('name')
		email = request.POST.get('email')
		password = request.POST.get('password')
		specialization = request.POST.get('specialization', '')
		contact = request.POST.get('contact', '')
		department = request.POST.get('department')
		Doctor.objects.create(
			name=name,
			email=email,
			password=password,
			specialization=specialization,
			contact=contact,
			department=department
		)
		return redirect('/admin/doctor-management/')
	return render(request, 'admin/add_doctor.html')

def edit_doctor(request, doctor_id):
	doctor = get_object_or_404(Doctor, id=doctor_id)
	if request.method == 'POST':
		doctor.name = request.POST.get('name')
		doctor.email = request.POST.get('email')
		doctor.specialization = request.POST.get('specialization', '')
		doctor.contact = request.POST.get('contact', '')
		doctor.save()
		return redirect('/admin/doctor-management/')
	return redirect('/admin/doctor-management/')

def delete_doctor(request, doctor_id):
	doctor = get_object_or_404(Doctor, id=doctor_id)
	doctor.delete()
	next_url = request.META.get('HTTP_REFERER')
	if next_url:
		return redirect(next_url)
	return redirect('/admin/doctor-management/')

# Admin User Management CRUD

def patient_management(request):
	patients = Patient.objects.all()
	return render(request, 'admin/patient_management.html', {'patients': patients})


# def add_patient(request):
# 	if request.method == 'POST':
# 		pname = request.POST.get('pname')
# 		password = request.POST.get('password')
# 		email = request.POST.get('email')
# 		dob = request.POST.get('dob')
# 		gender = request.POST.get('gender')
# 		contact = request.POST.get('contact')
# 		address = request.POST.get('address')
# 		insurance_info = request.POST.get('insurance_info')
# 		Patient.objects.create(
# 			pname=pname,
# 			password=password,
# 			email=email,
# 			dob=dob or None,
# 			gender=gender or None,
# 			contact=contact,
# 			address=address,
# 			insurance_info=insurance_info
# 		)
# 		return redirect('/admin/patient-management/')
# 	return render(request, 'admin/add_patient.html')


def edit_patient(request, patient_id):
	patient = get_object_or_404(Patient, id=patient_id)
	if request.method == 'POST':
		patient.pname = request.POST.get('pname')
		patient.email = request.POST.get('email')
		patient.dob = request.POST.get('dob') or None
		patient.gender = request.POST.get('gender') or None
		patient.contact = request.POST.get('contact')
		patient.address = request.POST.get('address')
		patient.insurance_info = request.POST.get('insurance_info')
		patient.save()
		return redirect('/admin/patient-management/')
	# No GET form page, just redirect
	return redirect('/admin/patient-management/')


def delete_patient(request, patient_id):
	patient = get_object_or_404(Patient, id=patient_id)
	patient.delete()
	# Try to redirect to the referring page, fallback to patient management
	next_url = request.META.get('HTTP_REFERER')
	if next_url:
		return redirect(next_url)
	return redirect('/admin/patient-management/')
# Landing page view
def landing_page(request):
	return render(request, 'landing.html')

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *

# Authentication
def login_view(request):
	context = {
		'roles': ['patient', 'doctor', 'admin']
	}
	if request.method == 'POST':
		username = request.POST.get('username', '').strip()
		password = request.POST.get('password', '').strip()
		role = request.POST.get('role', '').strip()

		if not username or not password or not role:
			messages.error(request, 'All fields are required.')
			return render(request, 'login.html', context)

		# Explicitly fetch from the correct table for each role
		if role == 'doctor':
			# hospital_doctor table
			user = Doctor.objects.filter(name__iexact=username, password=password).first()
			if user:
				request.session['doctor_name'] = user.name
				return redirect('/doctor/dashboard/')
			else:
				messages.error(request, 'Invalid doctor credentials.')
		elif role == 'admin':
			# hospital_user table (role must be admin)
			user = User.objects.filter(username__iexact=username, password=password, role__iexact='admin').first()
			if user:
				return redirect('/admin/dashboard/')
			else:
				messages.error(request, 'Invalid admin credentials.')
		elif role == 'patient':
			# hospital_patient table
			user = Patient.objects.filter(pname__iexact=username, password=password).first()
			if user:
				request.session['patient_name'] = user.pname
				return redirect('/patient/dashboard/')
			else:
				messages.error(request, 'Invalid patient credentials.')
		else:
			messages.error(request, 'Invalid role selected.')

		return render(request, 'login.html', context)

	return render(request, 'login.html', context)

def register_view(request):
	context = {
		'genders': ['male', 'female', 'other']
	}
	if request.method == 'POST':
		username = request.POST.get('name')
		password = request.POST.get('password')
		email = request.POST.get('email')
		role = request.POST.get('role')
		doctor_id = request.POST.get('doctor_id')
		admin_id = request.POST.get('admin_id')
		# For demo, do not set dob or gender, leave them null
		if role == 'doctor':
			if Doctor.objects.filter(name=username).exists():
				messages.error(request, 'Doctor already exists.')
				return render(request, 'register.html', context)
			doc = Doctor.objects.create(
				name=username,
				password=password,
				email=email,
				specialization='',
				contact='',
				department=None
			)
			request.session['doctor_name'] = doc.name
			return redirect('/doctor/dashboard/')
		elif role == 'admin':
			if User.objects.filter(username=username, role='admin').exists():
				messages.error(request, 'Admin already exists.')
				return render(request, 'register.html', context)
			User.objects.create(
				username=username,
				password=password,
				role='admin',
				status='Active',
			)
			return redirect('/admin/dashboard/')
		else:  # patient
			if Patient.objects.filter(pname=username).exists():
				messages.error(request, 'Patient already exists.')
				return render(request, 'register.html', context)
			pat = Patient.objects.create(
				pname=username,
				password=password,
				email=email,
				contact='',
				address='',
				insurance_info='',
			)
			request.session['patient_name'] = pat.pname
			return redirect('/patient/dashboard/')
	return render(request, 'register.html', context)

def forgot_password_view(request):
	return render(request, 'forgot_password.html')

# Patient Module
def patient_dashboard(request):
	from datetime import date
	from .models import Appointment, Patient, MedicalHistory
	quick_links = [
		{'name': 'Book Appointment', 'url': '/patient/appointment-booking/'},
		{'name': 'Appointment History', 'url': '/patient/appointment-history/'},
		{'name': 'Medical History', 'url': '/patient/medical-history/'},
		{'name': 'Billing & Payment', 'url': '/patient/billing-payment/'},
		{'name': 'Health Education', 'url': '/patient/health-education/'},
	]
	# Determine current patient from session (fallback to first patient if absent)
	patient_name = request.session.get('patient_name')
	patient = None
	if patient_name:
		try:
			patient = Patient.objects.get(pname=patient_name)
		except Patient.DoesNotExist:
			patient = None
	if patient is None:
		patient = Patient.objects.first()

	if patient:
		upcoming = Appointment.objects.filter(patient=patient, date__gte=date.today()).order_by('date', 'time')[:3]
		recent_history = MedicalHistory.objects.filter(patient=patient).order_by('-id')[:3]
	else:
		upcoming = []
		recent_history = []

	return render(request, 'patient/dashboard.html', {
		'quick_links': quick_links,
	'upcoming': upcoming,
	'recent_history': recent_history,
	})

def appointment_booking(request):
	from .models import Appointment, Doctor, Patient
	# Fetch doctors for dropdown
	doctors = Doctor.objects.all()
	if request.method == 'POST':
		doctor_name = request.POST.get('doctor')
		date = request.POST.get('date')
		time = request.POST.get('time')
		# Try to get patient from session, else use first patient in DB
		patient_name = request.session.get('patient_name')
		try:
			doctor = Doctor.objects.get(name=doctor_name)
		except Doctor.DoesNotExist:
			doctor = None
		patient = None
		if patient_name:
			try:
				patient = Patient.objects.get(pname=patient_name)
			except Patient.DoesNotExist:
				patient = None
		if not patient:
			patient = Patient.objects.first()
		if doctor and patient:
			Appointment.objects.create(
				patient=patient,
				doctor=doctor,
				date=date,
				time=time,
				status='Upcoming'
			)
			# Redirect to patient dashboard after successful booking
			return redirect('/patient/dashboard/')
		else:
			message = 'Invalid doctor or patient.'
			return render(request, 'patient/appointment_booking.html', {'doctors': doctors, 'message': message})
	return render(request, 'patient/appointment_booking.html', {'doctors': doctors})

def appointment_history(request):
	from .models import Appointment, Doctor, Patient
	# For demo, get patient from session or use a placeholder
	patient_name = request.session.get('patient_name', 'Demo Patient')
	try:
		patient = Patient.objects.get(pname=patient_name)
		appointments = Appointment.objects.filter(patient=patient).order_by('-date', '-time')
	except Patient.DoesNotExist:
		appointments = []
	return render(request, 'patient/appointment_history.html', {'appointments': appointments})

from django.views.decorators.http import require_http_methods

@require_http_methods(["POST"])
def cancel_appointment(request, appointment_id):
	from .models import Appointment, Patient
	# Ensure the appointment belongs to the current session patient
	patient_name = request.session.get('patient_name')
	try:
		patient = Patient.objects.get(pname=patient_name)
	except Patient.DoesNotExist:
		return redirect('appointment_history')
	appt = get_object_or_404(Appointment, id=appointment_id, patient=patient)
	# Set status with by who information
	appt.status = 'Cancelled (by patient)'
	appt.save()
	# Redirect back to where the action came from if provided
	next_url = request.POST.get('next') or request.META.get('HTTP_REFERER')
	if next_url:
		return redirect(next_url)
	return redirect('appointment_history')

def reschedule_appointment(request, appointment_id):
	from .models import Appointment, Patient
	patient_name = request.session.get('patient_name')
	try:
		patient = Patient.objects.get(pname=patient_name)
	except Patient.DoesNotExist:
		return redirect('appointment_history')
	appt = get_object_or_404(Appointment, id=appointment_id, patient=patient)
	if request.method == 'POST':
		# Update date/time and reset status to Pending
		new_date = request.POST.get('date')
		new_time = request.POST.get('time')
		if new_date:
			appt.date = new_date
		if new_time:
			appt.time = new_time
		# Normalize status after reschedule
		appt.status = 'Pending'
		appt.save()
	# Always redirect to appointment history after reschedule
	return redirect('appointment_history')
	# GET: show a simple form
	return render(request, 'patient/reschedule_appointment.html', {'appointment': appt})

def medical_history(request):
	from .models import MedicalHistory, Patient
	# For demo, get patient from session or use a placeholder
	patient_name = request.session.get('patient_name', 'Demo Patient')
	try:
		patient = Patient.objects.get(pname=patient_name)
		history = MedicalHistory.objects.filter(patient=patient)
	except Patient.DoesNotExist:
		history = []
	return render(request, 'patient/medical_history.html', {'history': history})

def billing_payment(request):
	bills = [
		{'invoice': 'INV-001', 'amount': 100.00, 'status': 'Unpaid', 'payment_date': '-', 'pay_url': '#'},
	]
	return render(request, 'patient/billing_payment.html', {'bills': bills})

def health_education(request):
	resources = [
		{'type': 'Article', 'title': 'Healthy Eating', 'url': '#'},
		{'type': 'Video', 'title': 'Exercise Tips', 'url': '#'},
	]
	return render(request, 'patient/health_education.html', {'resources': resources})

# Admin Module
def admin_dashboard(request):
	links = [
		{'name': 'User Management', 'url': '/admin/user-management/'},
		{'name': 'Facility Management', 'url': '/admin/facility-management/'},
		{'name': 'Appointment Management', 'url': '/admin/appointment-management/'},
	]
	return render(request, 'admin/dashboard.html', {'links': links})

def user_management(request):
	users = [
		{'username': 'admin1', 'role': 'Admin', 'status': 'Active'},
	]
	return render(request, 'admin/user_management.html', {'users': users})

def facility_management(request):
	facilities = [
		{'name': 'General Ward', 'location': 'Main Building', 'department': 'General Medicine', 'bed_count': 50},
	]
	return render(request, 'admin/facility_management.html', {'facilities': facilities})

def appointment_management(request):
	from .models import Appointment
	appointments = Appointment.objects.all().order_by('-date', '-time')
	return render(request, 'admin/appointment_management.html', {'appointments': appointments})

# Doctor Module
def doctor_dashboard(request):
	from datetime import date
	from .models import Appointment, Doctor
	links = [
		{'name': 'Patient Records', 'url': '/doctor/patient-records/'},
		{'name': 'Appointment Schedule', 'url': '/doctor/appointment-schedule/'},
		{'name': 'E-Prescribing', 'url': '/doctor/e-prescribing/'},
	]
	# Determine current doctor from session, fallback to first doctor
	doctor_name = request.session.get('doctor_name')
	doctor = None
	if doctor_name:
		try:
			doctor = Doctor.objects.get(name=doctor_name)
		except Doctor.DoesNotExist:
			doctor = None
	if doctor is None:
		doctor = Doctor.objects.first()

	if doctor:
		schedule_today = Appointment.objects.filter(doctor=doctor, date=date.today()).select_related('patient').order_by('time')
		today_count = schedule_today.count()
		next_appt = schedule_today.first()
		department_name = doctor.department.name if doctor.department else ''
	else:
		schedule_today = []
		today_count = 0
		next_appt = None
		department_name = ''

	return render(request, 'doctor/dashboard.html', {
		'links': links,
		'schedule_today': schedule_today,
		'today_count': today_count,
		'next_appt': next_appt,
		'department_name': department_name,
	})

def patient_records(request):
	from .models import Patient
	query = request.GET.get('q', '')
	if query:
		patients = Patient.objects.filter(pname__icontains=query)
	else:
		patients = Patient.objects.all()
	return render(request, 'doctor/patient_records.html', {'patients': patients, 'query': query})

def update_medical_history(request, patient_id):
	from .models import Patient, MedicalHistory
	patient = get_object_or_404(Patient, id=patient_id)
	if request.method == 'POST':
		diagnosis = request.POST.get('diagnosis')
		treatment = request.POST.get('treatment')
		allergies = request.POST.get('allergies')
		notes = request.POST.get('notes')
		MedicalHistory.objects.create(
			patient=patient,
			diagnosis=diagnosis,
			treatment=treatment,
			allergies=allergies,
			notes=notes
		)
		return redirect('/doctor/patient-records/')
	return render(request, 'doctor/update_medical_history.html', {'patient': patient})

def appointment_schedule(request):
	from .models import Appointment, Doctor
	# For demo, get doctor from session or use a placeholder
	doctor_name = request.session.get('doctor_name')
	doctor = None
	if doctor_name:
		try:
			doctor = Doctor.objects.get(name=doctor_name)
		except Doctor.DoesNotExist:
			doctor = None
	if doctor is None:
		doctor = Doctor.objects.first()
	if doctor:
		schedule = Appointment.objects.filter(doctor=doctor).order_by('-date', '-time')
	else:
		schedule = []
	return render(request, 'doctor/appointment_schedule.html', {'schedule': schedule})

def e_prescribing(request):
	patients = [
		{'id': 1, 'name': 'Jane Doe'},
	]
	return render(request, 'doctor/e_prescribing.html', {'patients': patients})

# Doctor actions on appointments
from django.views.decorators.http import require_POST

@require_POST
def doctor_cancel_appointment(request, appointment_id):
	from .models import Appointment, Doctor
	doctor_name = request.session.get('doctor_name')
	doctor = None
	if doctor_name:
		try:
			doctor = Doctor.objects.get(name=doctor_name)
		except Doctor.DoesNotExist:
			doctor = None
	if doctor is None:
		return redirect('appointment_schedule')
	appt = get_object_or_404(Appointment, id=appointment_id, doctor=doctor)
	appt.status = 'Cancelled (by doctor)'
	appt.save()
	next_url = request.POST.get('next') or request.META.get('HTTP_REFERER')
	return redirect(next_url or 'appointment_schedule')

@require_POST
def doctor_complete_appointment(request, appointment_id):
	from .models import Appointment, Doctor
	doctor_name = request.session.get('doctor_name')
	doctor = None
	if doctor_name:
		try:
			doctor = Doctor.objects.get(name=doctor_name)
		except Doctor.DoesNotExist:
			doctor = None
	if doctor is None:
		return redirect('appointment_schedule')
	appt = get_object_or_404(Appointment, id=appointment_id, doctor=doctor)
	appt.status = 'Completed'
	appt.save()
	next_url = request.POST.get('next') or request.META.get('HTTP_REFERER')
	return redirect(next_url or 'appointment_schedule')

def doctor_reschedule_appointment(request, appointment_id):
	from .models import Appointment, Doctor
	doctor_name = request.session.get('doctor_name')
	doctor = None
	if doctor_name:
		try:
			doctor = Doctor.objects.get(name=doctor_name)
		except Doctor.DoesNotExist:
			doctor = None
	if doctor is None:
		return redirect('appointment_schedule')
	appt = get_object_or_404(Appointment, id=appointment_id, doctor=doctor)
	if request.method == 'POST':
		new_date = request.POST.get('date')
		new_time = request.POST.get('time')
		if new_date:
			appt.date = new_date
		if new_time:
			appt.time = new_time
		appt.status = 'Pending'
		appt.save()
		return redirect('appointment_schedule')
	return render(request, 'doctor/reschedule_appointment.html', {'appointment': appt})

# Common
def notifications_view(request):
	notifications = [
		{'message': 'Appointment confirmed', 'status': 'unread'},
		{'message': 'Payment received', 'status': 'unread'},
	]
	return render(request, 'notifications.html', {'notifications': notifications})



# Doctor profile view
def doctor_profile(request):
	# For demo, get doctor from session or use a placeholder
	doctor_name = request.session.get('doctor_name', 'Dr. John Doe')
	from .models import Doctor
	try:
		doctor = Doctor.objects.get(name=doctor_name)
	except Doctor.DoesNotExist:
		doctor = None
	return render(request, 'doctor/profile.html', {'doctor': doctor})

# Doctor profile settings view
def doctor_profile_settings(request):
	doctor_name = request.session.get('doctor_name', 'Dr. John Doe')
	from .models import Doctor
	try:
		doctor = Doctor.objects.get(name=doctor_name)
	except Doctor.DoesNotExist:
		doctor = None
	if request.method == 'POST' and doctor:
		doctor.name = request.POST.get('name')
		doctor.email = request.POST.get('email')
		doctor.specialization = request.POST.get('specialization')
		doctor.contact = request.POST.get('contact')
		# Profile picture upload logic can be added here
		doctor.save()
		return redirect('/doctor/profile/')
	return render(request, 'doctor/profile_settings.html', {'doctor': doctor})

# Patient profile view
def patient_profile(request):
	patient_name = request.session.get('patient_name', 'Demo Patient')
	from .models import Patient
	try:
		patient = Patient.objects.get(pname=patient_name)
	except Patient.DoesNotExist:
		patient = None
	return render(request, 'patient/profile.html', {'patient': patient})

# Patient profile settings view
def patient_profile_settings(request):
	patient_name = request.session.get('patient_name', 'Demo Patient')
	from .models import Patient
	try:
		patient = Patient.objects.get(pname=patient_name)
	except Patient.DoesNotExist:
		patient = None
	if request.method == 'POST' and patient:
		patient.pname = request.POST.get('name')
		patient.email = request.POST.get('email')
		patient.dob = request.POST.get('dob') or None
		patient.gender = request.POST.get('gender') or None
		patient.contact = request.POST.get('contact')
		patient.address = request.POST.get('address')
		patient.insurance_info = request.POST.get('insurance_info')
		# Profile picture upload logic can be added here
		patient.save()
		return redirect('/patient/profile/')
	return render(request, 'patient/profile_settings.html', {'patient': patient})
from django.shortcuts import redirect

def logout_confirmation(request):
	if request.method == "POST":
		logout(request)  # logs the user out
		request.session.flush()
		return redirect('landing')  # send to landing page
	return render(request, 'logout_confirmation.html')
