from django.db import models
from django.conf import settings
from departments.models import Department

class Doctor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doctor_profile')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='doctors')
    specialization = models.CharField(max_length=200, blank=True)
    biography = models.TextField(blank=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    consultation_duration = models.PositiveIntegerField(default=30, help_text="Duration in minutes")
    profile_photo = models.ImageField(upload_to='doctor_photos/', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Dr. {self.user.get_full_name() or self.user.username} - {self.specialization or 'General'}"

class DoctorAvailability(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='availabilities')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ('doctor', 'date')
        ordering = ['date']

    def __str__(self):
        return f"{self.doctor} - {self.date.strftime('%Y-%m-%d')} ({self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')})"

class DoctorBreak(models.Model):
    availability = models.ForeignKey(DoctorAvailability, on_delete=models.CASCADE, related_name='breaks')
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"Break {self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"

