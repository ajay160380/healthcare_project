from django.urls import path
from . import views
urlpatterns = [
path('', views.home, name='home'),
path('register/', views.register, name='register'),
path('accounts/login/', views.login_view, name='login'),
path('accounts/logout/', views.logout_view, name='logout'),
path('dashboard/', views.dashboard, name='dashboard'),
path('profile/', views.profile, name='profile'),
path('ai-assistant/', views.ai_assistant, name='ai_assistant'),
path('hospitals/', views.hospital_locations, name='hospital_locations'),
]