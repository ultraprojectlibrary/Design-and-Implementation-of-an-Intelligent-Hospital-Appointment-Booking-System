from django.db import models
from django.conf import settings

class Patient(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patient_profile')
    phone_number = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], blank=True)
    address = models.TextField(blank=True)
    profile_photo = models.ImageField(upload_to='patient_photos/', null=True, blank=True)

    def __str__(self):
        return f"Patient: {self.user.get_full_name() or self.user.username}"
