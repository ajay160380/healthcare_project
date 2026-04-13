from django.urls import path
from . import views

urlpatterns = [
    # Patient routes
    path('', views.patient_list, name='patient_list'),
    path('create/', views.patient_create, name='patient_create'),
    path('<int:pk>/update/', views.patient_update, name='patient_update'),
    path('<int:pk>/delete/', views.patient_delete, name='patient_delete'),

    # Related records (must come before detail)
    path('<int:patient_pk>/medical-record/add/', views.add_medical_record, name='add_medical_record'),
    path('<int:patient_pk>/vitals/add/', views.add_vital_record, name='add_vital_record'),

    # Detail route (keep last to prevent greedy matching issues)
    path('<int:pk>/', views.patient_detail, name='patient_detail'),
]