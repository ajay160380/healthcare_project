from django.urls import path
from . import views

app_name = 'doctors'

urlpatterns = [
    # Doctor routes
    path('', views.doctor_list, name='doctor_list'),
    path('create/', views.doctor_create, name='doctor_create'),
    path('<int:pk>/update/', views.doctor_update, name='doctor_update'),
    path('<int:pk>/delete/', views.doctor_delete, name='doctor_delete'),
    path('<int:pk>/', views.doctor_detail, name='doctor_detail'),

    # Specialization routes
    path('specializations/', views.specialization_list, name='specialization_list'),
    path('specializations/create/', views.specialization_create, name='specialization_create'),
]