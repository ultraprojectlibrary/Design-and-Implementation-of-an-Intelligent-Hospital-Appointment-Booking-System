from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register_patient, name='register'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout'),
    
    # Password Reset
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset_form.html',
        email_template_name='emails/password_reset_email.html',
        html_email_template_name='emails/password_reset_email.html',
        subject_template_name='emails/password_reset_subject.txt',
        success_url='/accounts/password_reset/done/'
    ), name='password_reset'),
    
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ), name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html',
        success_url='/accounts/reset/done/'
    ), name='password_reset_confirm'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ), name='password_reset_complete'),
]
