from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from appointments.models import Appointment
from datetime import datetime


def _get_profile_photo(user):
    """Return the profile photo URL or None for any user type."""
    try:
        if user.is_patient:
            photo = user.patient_profile.profile_photo
            return photo.url if photo else None
        elif user.is_doctor:
            photo = user.doctor_profile.profile_photo
            return photo.url if photo else None
    except Exception:
        pass
    return None


@login_required
def patient_dashboard(request):
    if not request.user.is_patient:
        return redirect('home')

    patient = request.user.patient_profile
    now = datetime.now()

    upcoming_appointments = Appointment.objects.filter(
        patient=patient,
        status__in=['Pending', 'Confirmed', 'Rescheduled'],
        appointment_date__gte=now.date()
    ).exclude(
        appointment_date=now.date(), end_time__lte=now.time()
    ).order_by('appointment_date', 'start_time')

    past_appointments = (
        Appointment.objects.filter(patient=patient, status__in=['Completed', 'Cancelled']) |
        Appointment.objects.filter(patient=patient, appointment_date__lt=now.date()).exclude(status='Cancelled') |
        Appointment.objects.filter(patient=patient, appointment_date=now.date(), end_time__lte=now.time()).exclude(status='Cancelled')
    )

    next_appointment = upcoming_appointments.first()
    upcoming_count = upcoming_appointments.count()

    context = {
        'upcoming_count': upcoming_count,
        'next_appointment': next_appointment,
        'upcoming_appointments': upcoming_appointments[1:] if next_appointment else upcoming_appointments,
        'past_appointments': past_appointments.order_by('-appointment_date', '-start_time')[:10],
        'user_profile_photo': _get_profile_photo(request.user),
    }
    return render(request, 'patients/dashboard.html', context)


@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user.patient_profile)
    if request.method == 'POST':
        appointment.status = 'Cancelled'
        appointment.save()
        messages.success(request, 'Appointment successfully cancelled.')
        return redirect('patient_dashboard')
    return render(request, 'patients/cancel_appointment.html', {
        'appointment': appointment,
        'user_profile_photo': _get_profile_photo(request.user),
    })


@login_required
def patient_profile(request):
    if not request.user.is_patient:
        return redirect('home')
    patient = request.user.patient_profile

    if request.method == 'POST':
        # Update user fields
        request.user.first_name = request.POST.get('first_name', '').strip()
        request.user.last_name  = request.POST.get('last_name', '').strip()
        request.user.save()

        # Update patient fields
        patient.phone_number = request.POST.get('phone_number', '').strip()
        patient.date_of_birth = request.POST.get('date_of_birth') or None
        patient.gender = request.POST.get('gender', '')
        patient.address = request.POST.get('address', '').strip()
        if 'profile_photo' in request.FILES:
            patient.profile_photo = request.FILES['profile_photo']
        patient.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('patient_profile')

    return render(request, 'patients/profile.html', {
        'patient': patient,
        'user_profile_photo': _get_profile_photo(request.user),
    })


@login_required
def patient_appointments(request):
    if not request.user.is_patient:
        return redirect('home')
    
    appointments = Appointment.objects.filter(patient__user=request.user).order_by('-appointment_date', '-start_time')
    
    return render(request, 'patients/appointments.html', {
        'appointments': appointments,
        'user_profile_photo': _get_profile_photo(request.user),
    })
