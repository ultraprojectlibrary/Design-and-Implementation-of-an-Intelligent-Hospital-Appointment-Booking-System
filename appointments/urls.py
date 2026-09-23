from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('book/', views.book_start, name='book_start'),
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctor/<int:doctor_id>/', views.doctor_profile, name='doctor_profile'),
    path('doctor/<int:doctor_id>/book/', views.book_slot, name='book_slot'),
    path('doctor/<int:doctor_id>/api/slots/', views.api_get_slots, name='api_get_slots'),
    path('confirmation/', TemplateView.as_view(template_name='appointments/booking_confirmation.html'), name='booking_confirmation'),
]
