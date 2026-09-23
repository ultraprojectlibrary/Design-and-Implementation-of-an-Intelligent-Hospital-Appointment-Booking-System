from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from patients.models import Patient
from doctors.models import Doctor, DoctorAvailability
from departments.models import Department
from appointments.models import Appointment
from datetime import datetime, date, time

User = get_user_model()

class AppointmentsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Create department
        self.dept = Department.objects.create(name='Cardiology', is_active=True)
        
        # Create doctor
        self.doc_user = User.objects.create_user(username='doctor1', password='password123', is_doctor=True)
        self.doctor = Doctor.objects.create(user=self.doc_user, department=self.dept, consultation_duration=30)
        
        # Add doctor availability
        self.avail_date = date.today()
        DoctorAvailability.objects.create(
            doctor=self.doctor,
            date=self.avail_date,
            start_time=time(9, 0),
            end_time=time(17, 0)
        )
        
        # Create patient
        self.pat_user = User.objects.create_user(username='patient1', password='password123', is_patient=True)
        self.patient = Patient.objects.create(user=self.pat_user)
        
    def test_book_appointment(self):
        # Login as patient
        self.client.login(username='patient1', password='password123')
        
        # Try booking
        book_url = reverse('book_slot', args=[self.doctor.id])
        response = self.client.post(book_url, {
            'date': self.avail_date.strftime('%Y-%m-%d'),
            'start_time': '09:00:00',
            'end_time': '09:30:00',
            'reason_for_visit': 'Heart checkup'
        })
        
        # Should redirect to confirmation or dashboard
        self.assertEqual(response.status_code, 302)
        
        # Check if appointment was created
        self.assertTrue(Appointment.objects.filter(doctor=self.doctor, patient=self.patient).exists())
        appt = Appointment.objects.get(doctor=self.doctor, patient=self.patient)
        self.assertEqual(appt.status, 'Pending')
        self.assertEqual(appt.reason_for_visit, 'Heart checkup')

    def test_double_booking_prevention(self):
        # Login as patient
        self.client.login(username='patient1', password='password123')
        
        # Create an existing appointment
        Appointment.objects.create(
            doctor=self.doctor,
            patient=self.patient,
            department=self.dept,
            appointment_date=self.avail_date,
            start_time=time(9, 0),
            end_time=time(9, 30),
            status='Confirmed'
        )
        
        # Try booking the exact same time slot
        book_url = reverse('book_slot', args=[self.doctor.id])
        response = self.client.post(book_url, {
            'date': self.avail_date.strftime('%Y-%m-%d'),
            'start_time': '09:00:00',
            'end_time': '09:30:00',
            'reason_for_visit': 'Another checkup'
        })
        
        # Should redirect back with error
        self.assertEqual(response.status_code, 302)
        
        # Check that only the FIRST appointment exists in that slot
        appts = Appointment.objects.filter(
            doctor=self.doctor,
            appointment_date=self.avail_date,
            start_time=time(9, 0)
        )
        self.assertEqual(appts.count(), 1)
        self.assertEqual(appts.first().reason_for_visit, '') # Initial didn't set reason via create

    def test_api_get_slots(self):
        # Check that the API returns the correct slots for the doctor
        api_url = reverse('api_get_slots', args=[self.doctor.id])
        response = self.client.get(api_url, {'date': self.avail_date.strftime('%Y-%m-%d')})
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('slots', data)
        self.assertTrue(len(data['slots']) > 0)
