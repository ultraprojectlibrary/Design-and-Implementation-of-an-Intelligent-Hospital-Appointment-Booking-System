from django.core.management.base import BaseCommand
from accounts.models import User
from patients.models import Patient
from doctors.models import Doctor, DoctorAvailability
from departments.models import Department
from datetime import time

class Command(BaseCommand):
    help = 'Seeds the database with initial demo data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')
        
        # 1. Departments
        depts = ['Cardiology', 'Pediatrics', 'Dermatology', 'General Medicine', 'Orthopedics', 'Neurology']
        dept_objs = {}
        for name in depts:
            dept, created = Department.objects.get_or_create(name=name, defaults={'description': f'Expert {name} department.'})
            dept_objs[name] = dept
            
        # 2. Doctors
        doctors_data = [
            {'username': 'drsmith', 'first': 'John', 'last': 'Smith', 'dept': 'Cardiology', 'spec': 'Cardiologist', 'fee': 15000},
            {'username': 'drjones', 'first': 'Sarah', 'last': 'Jones', 'dept': 'Pediatrics', 'spec': 'Pediatrician', 'fee': 10000},
            {'username': 'drhouse', 'first': 'Gregory', 'last': 'House', 'dept': 'General Medicine', 'spec': 'Diagnostician', 'fee': 25000},
            {'username': 'drdavis', 'first': 'Emily', 'last': 'Davis', 'dept': 'Dermatology', 'spec': 'Dermatologist', 'fee': 12000},
            {'username': 'drwilson', 'first': 'James', 'last': 'Wilson', 'dept': 'Orthopedics', 'spec': 'Orthopedic Surgeon', 'fee': 20000},
        ]
        
        for data in doctors_data:
            user, created = User.objects.get_or_create(username=data['username'], defaults={
                'first_name': data['first'],
                'last_name': data['last'],
                'email': f"{data['username']}@smartcare.com",
                'is_doctor': True,
            })
            if created:
                user.set_password('password123')
                user.save()
                
            doc, created = Doctor.objects.get_or_create(user=user, defaults={
                'department': dept_objs[data['dept']],
                'specialization': data['spec'],
                'years_of_experience': 10,
                'consultation_fee': data['fee'],
                'consultation_duration': 30
            })
            
            # Create availability (Monday to Friday, 9 AM to 5 PM)
            if created:
                for day in range(5):
                    DoctorAvailability.objects.create(
                        doctor=doc,
                        day=day,
                        start_time=time(9, 0),
                        end_time=time(17, 0)
                    )
                    
        # 3. Patient
        patient_user, created = User.objects.get_or_create(username='patient1', defaults={
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'jane.doe@example.com',
            'is_patient': True,
        })
        if created:
            patient_user.set_password('password123')
            patient_user.save()
            Patient.objects.get_or_create(user=patient_user, phone_number='1234567890')
            
        self.stdout.write(self.style.SUCCESS('Successfully seeded database!'))
