from django.contrib import admin
from .models import Doctor, DoctorAvailability, DoctorBreak

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'specialization', 'is_active')
    list_filter = ('department', 'is_active')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'specialization')

@admin.register(DoctorAvailability)
class DoctorAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'date', 'start_time', 'end_time')
    list_filter = ('date',)

@admin.register(DoctorBreak)
class DoctorBreakAdmin(admin.ModelAdmin):
    list_display = ('availability', 'start_time', 'end_time')
