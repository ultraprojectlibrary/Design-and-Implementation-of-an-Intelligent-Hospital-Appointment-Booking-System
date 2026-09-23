from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import ModernPatientRegistrationForm, EmailAuthForm


def register_patient(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = ModernPatientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to Regal, {user.first_name}! 🎉')
            return redirect('patient_dashboard')
    else:
        form = ModernPatientRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = EmailAuthForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            if user.is_doctor:
                return redirect('doctor_dashboard')
            elif user.is_patient:
                return redirect('patient_dashboard')
            else:
                return redirect('/admin/')
    else:
        form = EmailAuthForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')
