import os
import django
import random
import shutil

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from doctors.models import Doctor
from departments.models import Department
from django.core.files import File

User = get_user_model()

# Departments
depts = [
    "Cardiology", "Neurology", "Pediatrics", "Orthopedics",
    "Dermatology", "Psychiatry", "General Surgery", "Ophthalmology",
    "Gynaecology", "Dentistry"
]

for d_name in depts:
    Department.objects.get_or_create(name=d_name, defaults={'description': f'{d_name} department'})

all_depts = list(Department.objects.all())

# Doctor data
doctors_data = [
    {"first": "Amina", "last": "Okonkwo", "spec": "Pediatrician", "exp": 8, "fee": 15000},
    {"first": "Chidi", "last": "Eze", "spec": "Cardiologist", "exp": 12, "fee": 25000},
    {"first": "Fatima", "last": "Bello", "spec": "Neurologist", "exp": 10, "fee": 20000},
    {"first": "Kwame", "last": "Mensah", "spec": "Orthopedic Surgeon", "exp": 15, "fee": 30000},
    {"first": "Nia", "last": "Adebayo", "spec": "Dermatologist", "exp": 5, "fee": 10000},
    {"first": "Olu", "last": "Ogunleye", "spec": "Psychiatrist", "exp": 7, "fee": 18000},
    {"first": "Zainab", "last": "Ibrahim", "spec": "General Surgeon", "exp": 14, "fee": 28000},
    {"first": "Tariq", "last": "Abubakar", "spec": "Ophthalmologist", "exp": 9, "fee": 16000},
    {"first": "Yaa", "last": "Osei", "spec": "Gynaecologist", "exp": 11, "fee": 22000},
    {"first": "Kofi", "last": "Boateng", "spec": "Dentist", "exp": 6, "fee": 12000},
]

# Generated images
img_paths = [
    r"C:\Users\jepht\.gemini\antigravity-ide\brain\3f2d71ac-8594-42e5-b19a-c1ccd471a1f8\doctor_1_1789973110880.jpg",
    r"C:\Users\jepht\.gemini\antigravity-ide\brain\3f2d71ac-8594-42e5-b19a-c1ccd471a1f8\doctor_2_1789973119061.jpg",
    r"C:\Users\jepht\.gemini\antigravity-ide\brain\3f2d71ac-8594-42e5-b19a-c1ccd471a1f8\doctor_3_1789973129433.jpg",
]

for idx, data in enumerate(doctors_data):
    username = f"{data['first'].lower()}.{data['last'].lower()}"
    email = f"{username}@smartcare.com"

    user, created = User.objects.get_or_create(username=username, defaults={
        'first_name': data['first'],
        'last_name': data['last'],
        'email': email,
        'is_doctor': True
    })

    if created:
        user.set_password('password123')
        user.save()

    dept = random.choice(all_depts)
    img_path = img_paths[idx % len(img_paths)]

    doctor, d_created = Doctor.objects.get_or_create(user=user, defaults={
        'department': dept,
        'specialization': data['spec'],
        'biography': f"Dr. {data['last']} is an experienced {data['spec']} dedicated to providing the best care.",
        'years_of_experience': data['exp'],
        'consultation_fee': data['fee']
    })

    if os.path.exists(img_path):
        with open(img_path, 'rb') as f:
            doctor.profile_photo.save(f"doc_{idx}.jpg", File(f), save=True)

print("10 doctors seeded successfully.")
