import logging
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from appointments.models import Appointment
from notifications.models import AppointmentReminder

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Sends scheduled appointment reminders via email.'

    def handle(self, *args, **options):
        now = timezone.now()
        
        # 1. Ensure all upcoming appointments have reminder records generated
        upcoming_appointments = Appointment.objects.filter(
            status__in=['Pending', 'Confirmed', 'Rescheduled'],
            appointment_date__gte=now.date()
        )
        
        for appt in upcoming_appointments:
            appt_datetime = timezone.make_aware(
                timezone.datetime.combine(appt.appointment_date, appt.start_time)
            )
            
            # Generate 24 hour reminder
            reminder_24h_time = appt_datetime - timezone.timedelta(hours=24)
            if reminder_24h_time > now:
                AppointmentReminder.objects.get_or_create(
                    appointment=appt,
                    reminder_type='24_hours',
                    defaults={'scheduled_for': reminder_24h_time}
                )
                
            # Generate 2 hour reminder
            reminder_2h_time = appt_datetime - timezone.timedelta(hours=2)
            if reminder_2h_time > now:
                AppointmentReminder.objects.get_or_create(
                    appointment=appt,
                    reminder_type='2_hours',
                    defaults={'scheduled_for': reminder_2h_time}
                )

        # 2. Find pending reminders that are due
        due_reminders = AppointmentReminder.objects.filter(
            is_sent=False,
            scheduled_for__lte=now,
            appointment__status__in=['Pending', 'Confirmed', 'Rescheduled']
        )
        
        sent_count = 0
        for reminder in due_reminders:
            appt = reminder.appointment
            patient_email = appt.patient.user.email
            
            if not patient_email:
                continue
                
            # Prepare email content based on type
            if reminder.reminder_type == '24_hours':
                subject = f"Reminder: Your appointment with Dr. {appt.doctor.user.last_name} is tomorrow"
                body = f"Dear {appt.patient.user.first_name},\n\nThis is a friendly reminder that you have an appointment with Dr. {appt.doctor.user.last_name} tomorrow, {appt.appointment_date} at {appt.start_time.strftime('%I:%M %p')}.\n\nThank you for choosing SmartCare!"
            elif reminder.reminder_type == '2_hours':
                subject = f"Reminder: Your appointment with Dr. {appt.doctor.user.last_name} is in 2 hours"
                body = f"Dear {appt.patient.user.first_name},\n\nThis is a friendly reminder that you have an appointment with Dr. {appt.doctor.user.last_name} today at {appt.start_time.strftime('%I:%M %p')}.\n\nThank you for choosing SmartCare!"
            else:
                continue
                
            try:
                send_mail(
                    subject,
                    body,
                    settings.DEFAULT_FROM_EMAIL,
                    [patient_email],
                    fail_silently=False,
                )
                # Mark as sent (Idempotent)
                reminder.is_sent = True
                reminder.sent_at = now
                reminder.save()
                sent_count += 1
            except Exception as e:
                logger.error(f"Failed to send email to {patient_email}: {e}")

        self.stdout.write(self.style.SUCCESS(f'Successfully sent {sent_count} reminders.'))
