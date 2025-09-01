from django.urls import path, include
from . import views

# REST API
from rest_framework.routers import DefaultRouter
from .api_views import (
    PatientViewSet, AppointmentViewSet, MedicalHistoryViewSet, BillingViewSet, HealthResourceViewSet,
    UserViewSet, FacilityViewSet, DepartmentViewSet, DoctorViewSet, PrescriptionViewSet, DrugInteractionViewSet, NotificationViewSet
)

router = DefaultRouter()
router.register(r'api/patients', PatientViewSet)
router.register(r'api/appointments', AppointmentViewSet)
router.register(r'api/medical-history', MedicalHistoryViewSet)
router.register(r'api/billing', BillingViewSet)
router.register(r'api/health-resources', HealthResourceViewSet)
router.register(r'api/users', UserViewSet)
router.register(r'api/facilities', FacilityViewSet)
router.register(r'api/departments', DepartmentViewSet)
router.register(r'api/doctors', DoctorViewSet)
router.register(r'api/prescriptions', PrescriptionViewSet)
router.register(r'api/drug-interactions', DrugInteractionViewSet)
router.register(r'api/notifications', NotificationViewSet)

urlpatterns = [
    path('', views.landing_page, name='landing'),
    # Authentication
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),

    # Patient Module
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('patient/appointment-booking/', views.appointment_booking, name='appointment_booking'),
    path('patient/appointment-history/', views.appointment_history, name='appointment_history'),
    path('patient/appointments/<int:appointment_id>/cancel/', views.cancel_appointment, name='cancel_appointment'),
    path('patient/appointments/<int:appointment_id>/reschedule/', views.reschedule_appointment, name='reschedule_appointment'),
    path('patient/medical-history/', views.medical_history, name='medical_history'),
    path('patient/billing-payment/', views.billing_payment, name='billing_payment'),
    path('patient/health-education/', views.health_education, name='health_education'),
        path('patient/profile/', views.patient_profile, name='patient_profile'),
        path('patient/profile-settings/', views.patient_profile_settings, name='patient_profile_settings'),

    # Admin Module
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/patient-management/', views.patient_management, name='patient_management'),
    # path('admin/add-patient/', views.add_patient, name='add_patient'),
    path('admin/edit-patient/<int:patient_id>/', views.edit_patient, name='edit_patient'),
    path('admin/delete-patient/<int:patient_id>/', views.delete_patient, name='delete_patient'),

    path('admin/doctor-management/', views.doctor_management, name='doctor_management'),
    path('admin/add-doctor/', views.add_doctor, name='add_doctor'),
    path('admin/edit-doctor/<int:doctor_id>/', views.edit_doctor, name='edit_doctor'),
    path('admin/delete-doctor/<int:doctor_id>/', views.delete_doctor, name='delete_doctor'),
    path('admin/facility-management/', views.facility_management, name='facility_management'),
    path('admin/appointment-management/', views.appointment_management, name='appointment_management'),

    # Doctor Module
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctor/patient-records/', views.patient_records, name='patient_records'),
    path('doctor/appointment-schedule/', views.appointment_schedule, name='appointment_schedule'),
    path('doctor/appointments/<int:appointment_id>/cancel/', views.doctor_cancel_appointment, name='doctor_cancel_appointment'),
    path('doctor/appointments/<int:appointment_id>/complete/', views.doctor_complete_appointment, name='doctor_complete_appointment'),
    path('doctor/appointments/<int:appointment_id>/reschedule/', views.doctor_reschedule_appointment, name='doctor_reschedule_appointment'),
    path('doctor/e-prescribing/', views.e_prescribing, name='e_prescribing'),
    path('doctor/update-medical-history/<int:patient_id>/', views.update_medical_history, name='update_medical_history'),
        path('doctor/profile/', views.doctor_profile, name='doctor_profile'),
        path('doctor/profile-settings/', views.doctor_profile_settings, name='doctor_profile_settings'),

    # Common
    path('notifications/', views.notifications_view, name='notifications'),
    path('logout-confirmation/', views.logout_confirmation, name='logout_confirmation'),
    path('logout/', views.logout_confirmation, name='logout'),
    path('', include(router.urls)),
]
