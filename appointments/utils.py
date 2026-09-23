from datetime import datetime, date, time, timedelta
from .models import Appointment
from doctors.models import DoctorAvailability, DoctorBreak

def generate_time_slots(start_time, end_time, duration_minutes):
    """Generates a list of time slots given start/end time and duration."""
    slots = []
    current_time = datetime.combine(date.today(), start_time)
    end_datetime = datetime.combine(date.today(), end_time)
    
    while current_time + timedelta(minutes=duration_minutes) <= end_datetime:
        slot_end = current_time + timedelta(minutes=duration_minutes)
        slots.append({
            'start': current_time.time(),
            'end': slot_end.time()
        })
        current_time = slot_end
        
    return slots

def is_slot_overlapping(slot_start, slot_end, check_start, check_end):
    """Checks if a time slot overlaps with another period."""
    return (slot_start < check_end) and (slot_end > check_start)

def get_available_slots(doctor, appointment_date):
    """
    Returns a list of available time slots for a doctor on a specific date.
    Returns: [{'start': time, 'end': time, 'is_available': bool, 'reason': str}]
    """
    # 1. Get day of week (Monday=0, Sunday=6) - Not needed anymore but we check the specific date
    
    # 2. Check doctor's availability for this date
    try:
        availability = DoctorAvailability.objects.get(doctor=doctor, date=appointment_date)
    except DoctorAvailability.DoesNotExist:
        return [] # Doctor is not available on this date
        
    # 3. Generate all possible slots based on availability and consultation_duration
    all_slots = generate_time_slots(
        availability.start_time, 
        availability.end_time, 
        doctor.consultation_duration
    )
    
    # 4. Get breaks for this availability
    breaks = availability.breaks.all()
    
    # 5. Get existing active appointments for this doctor on this date
    existing_appointments = Appointment.objects.filter(
        doctor=doctor,
        appointment_date=appointment_date
    ).exclude(status__in=['Cancelled', 'Rescheduled'])
    
    # 6. Check availability for each slot
    available_slots = []
    
    now = datetime.now()
    is_today = (appointment_date == now.date())
    
    for slot in all_slots:
        slot_data = {
            'start': slot['start'],
            'end': slot['end'],
            'is_available': True,
            'reason': ''
        }
        
        # Don't show past slots if it's today
        if is_today and slot['start'] <= now.time():
            slot_data['is_available'] = False
            slot_data['reason'] = 'Time has passed'
            available_slots.append(slot_data)
            continue
            
        # Check breaks
        for b in breaks:
            if is_slot_overlapping(slot['start'], slot['end'], b.start_time, b.end_time):
                slot_data['is_available'] = False
                slot_data['reason'] = 'Doctor is on break'
                break
                
        if not slot_data['is_available']:
            available_slots.append(slot_data)
            continue
            
        # Check existing appointments
        for appt in existing_appointments:
            if is_slot_overlapping(slot['start'], slot['end'], appt.start_time, appt.end_time):
                slot_data['is_available'] = False
                slot_data['reason'] = 'Booked'
                break
                
        available_slots.append(slot_data)
        
    return available_slots

def get_intelligent_recommendation(doctor, preferred_date, preferred_period=None):
    """
    Finds the earliest/best available slot.
    preferred_period: 'morning' (before 12:00) or 'afternoon' (after 12:00)
    """
    # Check up to 14 days ahead
    for i in range(14):
        check_date = preferred_date + timedelta(days=i)
        slots = get_available_slots(doctor, check_date)
        
        available = [s for s in slots if s['is_available']]
        if not available:
            continue
            
        if preferred_period == 'morning':
            period_slots = [s for s in available if s['start'].hour < 12]
            if period_slots:
                return {'date': check_date, 'slot': period_slots[0]}
        elif preferred_period == 'afternoon':
            period_slots = [s for s in available if s['start'].hour >= 12]
            if period_slots:
                return {'date': check_date, 'slot': period_slots[0]}
                
        # If no preferred period match, just return the first available
        return {'date': check_date, 'slot': available[0]}
        
    return None
