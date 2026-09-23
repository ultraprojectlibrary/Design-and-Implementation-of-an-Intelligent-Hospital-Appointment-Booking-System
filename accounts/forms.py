import re
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from .models import User
from patients.models import Patient


class ModernPatientRegistrationForm(forms.Form):
    """
    Frictionless registration: only asks for Full Name, Email, Password.
    Auto-generates a unique username behind the scenes.
    """
    full_name = forms.CharField(
        max_length=60,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Amara Johnson', 'autocomplete': 'name'}),
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'you@example.com', 'autocomplete': 'email'}),
    )
    password1 = forms.CharField(
        label='Password',
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'At least 8 characters', 'autocomplete': 'new-password'}),
    )
    password2 = forms.CharField(
        label='Confirm Password',
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Repeat password', 'autocomplete': 'new-password'}),
    )

    def clean_email(self):
        email = self.cleaned_data['email'].lower().strip()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    def clean_password1(self):
        password = self.cleaned_data.get('password1', '')
        if len(password) < 8:
            raise forms.ValidationError('Password must be at least 8 characters.')
        return password

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            self.add_error('password2', 'Passwords do not match.')
        return cleaned

    def _generate_username(self, email, full_name):
        """Generate a unique username from email prefix or sanitised name."""
        base = email.split('@')[0]
        base = re.sub(r'[^a-zA-Z0-9_]', '', base)[:20] or 'user'
        username = base
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f'{base}{counter}'
            counter += 1
        return username

    def save(self):
        full_name = self.cleaned_data['full_name'].strip()
        email = self.cleaned_data['email']
        password = self.cleaned_data['password1']

        # Split full name
        parts = full_name.split(' ', 1)
        first_name = parts[0]
        last_name = parts[1] if len(parts) > 1 else ''

        username = self._generate_username(email, full_name)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_patient=True,
        )
        return user


class EmailAuthForm(forms.Form):
    """Login using Email address instead of username."""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'you@example.com', 'autocomplete': 'email'}),
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Your password', 'autocomplete': 'current-password'}),
    )

    def clean(self):
        cleaned = super().clean()
        email = cleaned.get('email', '').lower().strip()
        password = cleaned.get('password', '')

        if email and password:
            try:
                user_obj = User.objects.get(email=email)
                user = authenticate(username=user_obj.username, password=password)
                if user is None:
                    raise forms.ValidationError('Invalid email or password. Please try again.')
                cleaned['user'] = user
            except User.DoesNotExist:
                raise forms.ValidationError('No account found with that email address.')
        return cleaned

    def get_user(self):
        return self.cleaned_data.get('user')


# Keep legacy form name as alias for any code still referencing it
PatientRegistrationForm = ModernPatientRegistrationForm
