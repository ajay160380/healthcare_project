from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('patients/', include('patients.urls', namespace='patients')),
    path('doctors/', include('doctors.urls', namespace='doctors')),
    path('appointments/', include('appointments.urls', namespace='appointments')),
    path('pharmacy/', include('pharmacy.urls', namespace='pharmacy')),
    # Redirect old/incorrect login URLs to the correct login page
    path('dashboard/login', RedirectView.as_view(url='/accounts/login/', permanent=True)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)