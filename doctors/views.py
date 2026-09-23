from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from appointments.models import Appointment
from .models import DoctorAvailability
from datetime import datetime
from departments.models import Department


def _get_profile_photo(user):
    try:
        if user.is_doctor:
            photo = user.doctor_profile.profile_photo
            return photo.url if photo else None
        elif user.is_patient:
            photo = user.patient_profile.profile_photo
            return photo.url if photo else None
    except Exception:
        pass
    return None


@login_required
def doctor_dashboard(request):
    if not request.user.is_doctor:
        return redirect('home')

    doctor = request.user.doctor_profile
    now = datetime.now()

    todays_appointments = Appointment.objects.filter(
        doctor=doctor,
        appointment_date=now.date(),
        end_time__gt=now.time(),
        status__in=['Pending', 'Confirmed', 'Rescheduled']
    ).order_by('start_time')

    upcoming_appointments = Appointment.objects.filter(
        doctor=doctor,
        appointment_date__gt=now.date(),
        status__in=['Pending', 'Confirmed', 'Rescheduled']
    ).order_by('appointment_date', 'start_time')
    
    next_appointment = todays_appointments.filter(start_time__gte=now.time()).first()
    if not next_appointment:
        next_appointment = upcoming_appointments.first()

    context = {
        'todays_count': todays_appointments.count(),
        'pending_count': Appointment.objects.filter(doctor=doctor, status='Pending').count(),
        'upcoming_count': upcoming_appointments.count(),
        'todays_appointments': todays_appointments[:5],
        'upcoming_appointments': upcoming_appointments[:5],
        'next_appointment': next_appointment,
        'todays_count': todays_appointments.count(),
        'upcoming_count': upcoming_appointments.count(),
        'pending_count': Appointment.objects.filter(doctor=doctor, status='Pending').count(),
        'user_profile_photo': _get_profile_photo(request.user),
    }
    return render(request, 'doctors/dashboard.html', context)


@login_required
def update_appointment_status(request, appointment_id):
    if not request.user.is_doctor:
        return redirect('home')

    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=request.user.doctor_profile)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Appointment.STATUS_CHOICES):
            appointment.status = new_status
            appointment.save()
            messages.success(request, f'Appointment status updated to {new_status}.')
        else:
            messages.error(request, 'Invalid status.')
    return redirect('doctor_dashboard')


@login_required
def doctor_profile_view(request):
    if not request.user.is_doctor:
        return redirect('home')
    doctor = request.user.doctor_profile

    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', '').strip()
        request.user.last_name  = request.POST.get('last_name', '').strip()
        request.user.save()

        doctor.specialization = request.POST.get('specialization', '').strip()
        doctor.biography       = request.POST.get('biography', '').strip()
        doctor.years_of_experience = int(request.POST.get('years_of_experience', 0) or 0)
        doctor.consultation_fee    = request.POST.get('consultation_fee', 0) or 0
        if 'profile_photo' in request.FILES:
            doctor.profile_photo = request.FILES['profile_photo']
        doctor.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('doctor_profile_view')

    details = [
        ('Department',        doctor.department.name if doctor.department else '—'),
        ('Specialization',    doctor.specialization or '—'),
        ('Experience',        f"{doctor.years_of_experience} years"),
        ('Consultation Fee',  f"₦{doctor.consultation_fee}"),
        ('Session Duration',  f"{doctor.consultation_duration} minutes"),
        ('Email',             request.user.email),
    ]

    return render(request, 'doctors/profile.html', {
        'doctor': doctor,
        'details': details,
        'departments': Department.objects.filter(is_active=True),
        'user_profile_photo': _get_profile_photo(request.user),
    })


@login_required
def doctor_appointments(request):
    if not request.user.is_doctor:
        return redirect('home')
    
    appointments = Appointment.objects.filter(doctor__user=request.user).order_by('-appointment_date', '-start_time')
    
    return render(request, 'doctors/appointments.html', {
        'appointments': appointments,
        'user_profile_photo': _get_profile_photo(request.user),
    })


@login_required
def doctor_availability(request):
    if not request.user.is_doctor:
        return redirect('home')
    
    doctor = request.user.doctor_profile
    if request.method == 'POST':
        if 'delete' in request.POST:
            avail_id = request.POST.get('delete')
            DoctorAvailability.objects.filter(id=avail_id, doctor=doctor).delete()
            messages.success(request, 'Availability deleted.')
        else:
            date_str = request.POST.get('date')
            start = request.POST.get('start_time')
            end = request.POST.get('end_time')
            try:
                avail_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                DoctorAvailability.objects.create(doctor=doctor, date=avail_date, start_time=start, end_time=end)
                messages.success(request, 'Availability added successfully.')
            except Exception as e:
                messages.error(request, 'Error adding availability or duplicate date.')
        return redirect('doctor_availability')
        
    availabilities = doctor.availabilities.all()
    
    return render(request, 'doctors/availability.html', {
        'availabilities': availabilities,
        'user_profile_photo': _get_profile_photo(request.user),
    })
