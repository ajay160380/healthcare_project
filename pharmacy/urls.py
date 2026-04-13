from django.urls import path
from . import views


urlpatterns = [
    path('', views.pharmacy_dashboard, name='pharmacy_dashboard'),

    path('medicines/', views.medicine_list, name='medicine_list'),
    path('medicines/create/', views.medicine_create, name='medicine_create'),
    path('medicines/<int:pk>/', views.medicine_detail, name='medicine_detail'),
    path('medicines/<int:pk>/update/', views.medicine_update, name='medicine_update'),
    path('medicines/<int:pk>/stock/', views.add_stock, name='add_stock'),

    path('dispense/', views.dispense_medicine, name='dispense_medicine'),
    path('dispensings/', views.dispensing_list, name='dispensing_list'),

    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
]