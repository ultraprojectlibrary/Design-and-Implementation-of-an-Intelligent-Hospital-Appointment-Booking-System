import re
filepath = r'c:\Users\jepht\Music\rojex_projects\hospital_booking\appointments\views.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

if 'from django.template.loader import render_to_string' not in content:
    content = content.replace('from django.core.mail import send_mail', 'from django.core.mail import send_mail, EmailMultiAlternatives\nfrom django.template.loader import render_to_string')

pattern = re.compile(r'            # Send Email Notifications\s*try:\s*# Patient Email\s*send_mail\(.*?\)\s*# Doctor Email\s*send_mail\(.*?\)\s*except Exception.*?:', re.DOTALL)

replacement = '''            # Send Email Notifications
            try:
                from_email = settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@smartcare.com'
                context = {
                    'patient': request.user.patient_profile,
                    'doctor': doctor,
                    'appt_date': appt_date,
                    'start_time': start_time,
                    'site_url': request.build_absolute_uri('/')
                }
                
                # Patient Email
                context['is_doctor'] = False
                html_content = render_to_string('emails/booking_confirmation.html', context)
                msg = EmailMultiAlternatives('Appointment Booking Confirmation', 'Your appointment is confirmed.', from_email, [request.user.email])
                msg.attach_alternative(html_content, "text/html")
                msg.send(fail_silently=True)
                
                # Doctor Email
                context['is_doctor'] = True
                html_content_doc = render_to_string('emails/booking_confirmation.html', context)
                msg_doc = EmailMultiAlternatives('New Appointment Booking', 'You have a new appointment.', from_email, [doctor.user.email])
                msg_doc.attach_alternative(html_content_doc, "text/html")
                msg_doc.send(fail_silently=True)
            except Exception as e:
'''

new_content = re.sub(pattern, replacement, content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_content)
print('Updated views.py emails')
