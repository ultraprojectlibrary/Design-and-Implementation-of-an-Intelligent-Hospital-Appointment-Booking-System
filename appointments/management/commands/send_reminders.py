from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from appointments.models import Appointment
from datetime import timedelta
from datetime import datetime

class Command(BaseCommand):
    help = 'Send appointment reminders (run via cron every hour or minute)'

    def handle(self, *args, **options):
        now = timezone.now()
        
        # 1. Day before reminder (approx 24h before -> changed to 1 Hour before based on user req)
        # 1 Hour before
        one_hour_from_now_time = (now + timedelta(hours=1)).time()
        hour_before_appts = Appointment.objects.filter(
            status='Confirmed',
            appointment_date=now.date(),
            start_time__hour=one_hour_from_now_time.hour,
            reminder_1_sent=False
        )
        for appt in hour_before_appts:
            self.send_reminder_email(appt, '1 Hour')
            appt.reminder_1_sent = True
            appt.save(update_fields=['reminder_1_sent'])

        # 2. Time of session reminder (0 hours / exactly time reached)
        current_time = now.time()
        exact_time_appts = Appointment.objects.filter(
            status='Confirmed',
            appointment_date=now.date(),
            start_time__hour=current_time.hour,
            start_time__minute=current_time.minute,
            reminder_2_sent=False
        )
        for appt in exact_time_appts:
            self.send_reminder_email(appt, 'Starting Now')
            appt.reminder_2_sent = True
            appt.save(update_fields=['reminder_2_sent'])

        self.stdout.write(self.style.SUCCESS('Successfully processed reminders.'))

    def send_reminder_email(self, appt, timeframe):
        from_email = settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@smartcare.com'
        context = {
            'patient': appt.patient,
            'doctor': appt.doctor,
            'appt_date': appt.appointment_date,
            'start_time': appt.start_time,
        }
        
        if timeframe == 'Starting Now':
            title = 'Your Appointment is Starting Now'
            msg_body_pat = f'Your appointment with Dr. {appt.doctor.user.last_name} is starting right now.'
            msg_body_doc = f'Your appointment with {appt.patient.user.first_name} is starting right now.'
        else:
            title = f'Reminder: Appointment in {timeframe}'
            msg_body_pat = f'This is a reminder that your appointment with Dr. {appt.doctor.user.last_name} is in {timeframe}.'
            msg_body_doc = f'This is a reminder that your appointment with {appt.patient.user.first_name} is in {timeframe}.'

        # To Patient
        context['is_doctor'] = False
        context['title'] = title
        context['message_body'] = msg_body_pat
        try:
            html_content = render_to_string('emails/reminder.html', context)
            msg = EmailMultiAlternatives(title, msg_body_pat, from_email, [appt.patient.user.email])
            msg.attach_alternative(html_content, "text/html")
            msg.send(fail_silently=True)
        except Exception:
            pass

        # To Doctor
        context['is_doctor'] = True
        context['title'] = title
        context['message_body'] = msg_body_doc
        try:
            html_content_doc = render_to_string('emails/reminder.html', context)
            msg_doc = EmailMultiAlternatives(title, msg_body_doc, from_email, [appt.doctor.user.email])
            msg_doc.attach_alternative(html_content_doc, "text/html")
            msg_doc.send(fail_silently=True)
        except Exception:
            pass
