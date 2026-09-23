from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from patients.models import Patient

User = get_user_model()

class AccountsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login_view')
        
    def test_patient_registration(self):
        response = self.client.post(self.register_url, {
            'full_name': 'Test Patient',
            'email': 'test@patient.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        })
        
        # Should redirect to dashboard on success
        self.assertEqual(response.status_code, 302)
        
        # Verify user and patient profile were created
        self.assertTrue(User.objects.filter(email='test@patient.com').exists())
        user = User.objects.get(email='test@patient.com')
        self.assertTrue(user.is_patient)
        self.assertTrue(Patient.objects.filter(user=user).exists())
        
    def test_user_login(self):
        # Create user
        user = User.objects.create_user(username='loginuser', email='login@test.com', password='testpassword123', is_patient=True)
        Patient.objects.create(user=user)
        
        response = self.client.post(self.login_url, {
            'email': 'login@test.com',
            'password': 'testpassword123'
        })
        
        # Should redirect to dashboard on successful login
        self.assertEqual(response.status_code, 302)
        self.assertTrue('_auth_user_id' in self.client.session)
        
    def test_invalid_login(self):
        response = self.client.post(self.login_url, {
            'email': 'wrong@test.com',
            'password': 'wrongpassword'
        })
        
        # Should stay on the login page and show error (status 200)
        self.assertEqual(response.status_code, 200)
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_password_reset_page_loads(self):
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Forgot Password?')
