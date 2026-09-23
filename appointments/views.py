from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from datetime import datetime
from departments.models import Department
from doctors.models import Doctor
from .models import Appointment
from .utils import get_available_slots, get_intelligent_recommendation


def _get_profile_photo(user):
    try:
        if user.is_patient:
            p = user.patient_profile.profile_photo
            return p.url if p else None
        elif user.is_doctor:
            p = user.doctor_profile.profile_photo
            return p.url if p else None
    except Exception:
        pass
    return None


@login_required
def book_start(request):
    return redirect('doctor_list')


@login_required
def doctor_list(request):
    dept_id = request.GET.get('department')
    search  = request.GET.get('search', '')

    doctors = Doctor.objects.filter(is_active=True).select_related('user', 'department')
    if dept_id:
        doctors = doctors.filter(department_id=dept_id)
    if search:
        doctors = (
            doctors.filter(user__first_name__icontains=search) |
            doctors.filter(user__last_name__icontains=search)  |
            doctors.filter(specialization__icontains=search)
        )

    departments = Department.objects.filter(is_active=True)

    return render(request, 'appointments/doctor_list.html', {
        'doctors': doctors,
        'departments': departments,
        'selected_dept': int(dept_id) if dept_id and dept_id.isdigit() else None,
        'search': search,
        'user_profile_photo': _get_profile_photo(request.user),
    })


@login_required
def doctor_profile(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id, is_active=True)

    date_str = request.GET.get('date')
    selected_date = None
    slots = []
    recommendation = None

    if date_str:
        try:
            selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            if selected_date < datetime.now().date():
                messages.error(request, 'Cannot book appointments in the past.')
            else:
                slots = get_available_slots(doctor, selected_date)
                if not any(s['is_available'] for s in slots):
                    recommendation = get_intelligent_recommendation(doctor, selected_date)
        except ValueError:
            messages.error(request, 'Invalid date format.')

    availabilities = doctor.availabilities.filter(date__gte=datetime.now().date()).order_by('date')
    return render(request, 'appointments/doctor_profile.html', {
        'doctor': doctor,
        'selected_date': selected_date,
        'slots': slots,
        'recommendation': recommendation,
        'availabilities': availabilities,
        'user_profile_photo': _get_profile_photo(request.user),
    })


@login_required
def book_slot(request, doctor_id):
    if request.method != 'POST':
        return redirect('doctor_profile', doctor_id=doctor_id)

    doctor   = get_object_or_404(Doctor, id=doctor_id, is_active=True)
    date_str = request.POST.get('date')
    start_str = request.POST.get('start_time')
    end_str   = request.POST.get('end_time')
    reason    = request.POST.get('reason_for_visit', 'General consultation')

    try:
        appt_date  = datetime.strptime(date_str, '%Y-%m-%d').date()
        start_time = datetime.strptime(start_str, '%H:%M:%S').time()
        end_time   = datetime.strptime(end_str,   '%H:%M:%S').time()
    except (ValueError, TypeError):
        messages.error(request, 'Invalid appointment parameters.')
        return redirect('doctor_profile', doctor_id=doctor_id)

    try:
        with transaction.atomic():
            overlapping = Appointment.objects.select_for_update().filter(
                doctor=doctor,
                appointment_date=appt_date,
                status__in=['Pending', 'Confirmed'],
                start_time__lt=end_time,
                end_time__gt=start_time,
            ).exists()

            if overlapping:
                messages.error(request, 'This slot was just taken. Please select another time.')
                return redirect(f'/appointments/doctor/{doctor_id}/?date={date_str}')

            Appointment.objects.create(
                patient=request.user.patient_profile,
                doctor=doctor,
                department=doctor.department,
                appointment_date=appt_date,
                start_time=start_time,
                end_time=end_time,
                reason_for_visit=reason,
                status='Pending',
            )
            
            # Send Email Notifications
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

                print(f"Email sending failed: {e}")

            messages.success(request, 'Appointment booked successfully!')
            return redirect('booking_confirmation')

    except Exception:
        messages.error(request, 'An error occurred while booking. Please try again.')
        return redirect(f'/appointments/doctor/{doctor_id}/?date={date_str}')


@login_required
def booking_confirmation(request):
    return render(request, 'appointments/booking_confirmation.html', {
        'user_profile_photo': _get_profile_photo(request.user),
    })


from django.http import JsonResponse

def api_get_slots(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id, is_active=True)
    date_str = request.GET.get('date')
    if not date_str:
        return JsonResponse({'error': 'No date provided'}, status=400)
    
    try:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        if selected_date < datetime.now().date():
            return JsonResponse({'error': 'Cannot book appointments in the past.'}, status=400)
        
        slots = get_available_slots(doctor, selected_date)
        
        # Serialize times
        serialized_slots = []
        for slot in slots:
            serialized_slots.append({
                'start_time': slot['start'].strftime('%H:%M:%S'),
                'start_time_display': slot['start'].strftime('%I:%M %p'),
                'end_time': slot['end'].strftime('%H:%M:%S'),
                'end_time_display': slot['end'].strftime('%I:%M %p'),
                'is_available': slot['is_available']
            })
            
        rec = None
        if not any(s['is_available'] for s in serialized_slots):
            r = get_intelligent_recommendation(doctor, selected_date)
            if r:
                rec = {
                    'date': r['date'].strftime('%Y-%m-%d'),
                    'display': r['date'].strftime('%A, %b %d')
                }
                
        return JsonResponse({'slots': serialized_slots, 'recommendation': rec})
    except ValueError:
        return JsonResponse({'error': 'Invalid date format.'}, status=400)
