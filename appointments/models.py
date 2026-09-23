from django.db import models
from patients.models import Patient
from doctors.models import Doctor
from departments.models import Department

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
        ('Rescheduled', 'Rescheduled'),
    )

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='appointments')
    
    appointment_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    reason_for_visit = models.TextField(blank=True)
    
    reminder_1_sent = models.BooleanField(default=False)
    reminder_2_sent = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-appointment_date', '-start_time']
        # Note: We don't rely solely on unique_together for double-booking 
        # prevention because of cancelled/rescheduled appointments, but we 
        # will handle that logic in the view/forms layer.

    def __str__(self):
        return f"{self.patient} with {self.doctor} on {self.appointment_date} at {self.start_time.strftime('%H:%M')}"
