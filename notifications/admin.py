from django.contrib import admin
from .models import Notification, AppointmentReminder

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__username', 'title')

@admin.register(AppointmentReminder)
class AppointmentReminderAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'reminder_type', 'scheduled_for', 'is_sent', 'sent_at')
    list_filter = ('reminder_type', 'is_sent', 'scheduled_for')
    search_fields = ('appointment__patient__user__username',)
