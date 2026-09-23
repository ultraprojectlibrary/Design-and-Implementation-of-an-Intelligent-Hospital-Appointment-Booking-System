from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)

    def __str__(self):
        return self.username

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Automatically create a Doctor or Patient profile if the flag is checked"""
    if instance.is_patient:
        from patients.models import Patient
        Patient.objects.get_or_create(user=instance)
    if instance.is_doctor:
        from doctors.models import Doctor
        Doctor.objects.get_or_create(user=instance)
