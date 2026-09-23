from django.db import models
from django.conf import settings
from appointments.models import Appointment

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.user.username}: {self.title}"

class AppointmentReminder(models.Model):
    REMINDER_TYPES = (
        ('confirmation', 'Booking Confirmation'),
        ('24_hours', '24 Hours Before'),
        ('2_hours', '2 Hours Before'),
        ('rescheduling', 'Rescheduling'),
        ('cancellation', 'Cancellation'),
    )
    
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='reminders')
    reminder_type = models.CharField(max_length=20, choices=REMINDER_TYPES)
    scheduled_for = models.DateTimeField()
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['scheduled_for']
        # Prevent duplicate reminder types per appointment
        unique_together = ('appointment', 'reminder_type')

    def __str__(self):
        return f"{self.get_reminder_type_display()} for {self.appointment}"
