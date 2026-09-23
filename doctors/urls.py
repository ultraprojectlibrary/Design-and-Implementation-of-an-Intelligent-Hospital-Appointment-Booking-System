from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('profile/', views.doctor_profile_view, name='doctor_profile_view'),
    path('appointments/', views.doctor_appointments, name='doctor_appointments'),
    path('availability/', views.doctor_availability, name='doctor_availability'),
    path('appointment/<int:appointment_id>/status/', views.update_appointment_status, name='update_appointment_status'),
]
