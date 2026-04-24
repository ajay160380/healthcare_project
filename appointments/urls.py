from django.urls import path
from . import views

app_name = 'appointments'

# Spelling check karein: urlpatterns (all lowercase)
urlpatterns = [
    path('', views.appointment_list, name='appointment_list'),
    path('today/', views.today_appointments, name='today_appointments'),
    path('<int:pk>/', views.appointment_detail, name='appointment_detail'),
    path('create/', views.appointment_create, name='appointment_create'),
    path('<int:pk>/update/', views.appointment_update, name='appointment_update'),
    path('<int:pk>/delete/', views.appointment_delete, name='appointment_delete'),
    path('<int:pk>/status/', views.update_status, name='update_status'),
    path('<int:appointment_pk>/prescription/', views.add_prescription, name='add_prescription'),
]