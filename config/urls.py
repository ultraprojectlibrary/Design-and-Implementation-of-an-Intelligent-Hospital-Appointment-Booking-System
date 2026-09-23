from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

# Admin Site Customization
admin.site.site_header = "SmartCare Admin"
admin.site.site_title = "SmartCare Admin Portal"
admin.site.index_title = "Welcome to SmartCare Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('appointments/', include('appointments.urls')),
    path('patient/', include('patients.urls')),
    path('doctor/', include('doctors.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
]

# Serve uploaded media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
