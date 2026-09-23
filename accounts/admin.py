from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_patient', 'is_doctor', 'is_staff')
    list_filter = ('is_patient', 'is_doctor', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Roles', {'fields': ('is_patient', 'is_doctor')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Roles', {'fields': ('is_patient', 'is_doctor')}),
    )
