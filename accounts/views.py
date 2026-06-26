from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from django.http import JsonResponse
import requests
import json
from .forms import UserRegistrationForm, UserProfileForm
from .models import UserProfile
from patients.models import Patient
from doctors.models import Doctor
from appointments.models import Appointment
from pharmacy.models import Medicine



def home(request):
    return render(request, 'base/home.html')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to HealthCare Portal.')
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


@login_required
def dashboard(request):
    context = {
        'total_patients': Patient.objects.count(),
        'total_doctors': Doctor.objects.count(),
        'total_appointments': Appointment.objects.count(),
        'total_medicines': Medicine.objects.count(),
        'recent_appointments': Appointment.objects.order_by('-created_at')[:5],
        'recent_patients': Patient.objects.order_by('-created_at')[:5],
    }
    return render(request, 'base/dashboard.html', context)


@login_required
def profile(request):
    try:
        user_profile = request.user.profile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'accounts/profile.html', {
        'form': form,
        'user_profile': user_profile
    })


@login_required
def ai_assistant(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Check for clear action
            if data.get('action') == 'clear':
                request.session['ai_chat_history'] = []
                request.session.modified = True
                return JsonResponse({'status': 'cleared'})
                
            user_message = data.get('message', '')
            if not user_message:
                return JsonResponse({'error': 'Message cannot be empty.'}, status=400)
            
            api_key = getattr(settings, 'GROQ_API_KEY', '')
            if not api_key:
                return JsonResponse({'error': 'AI Health Assistant is not configured. Please add the GROQ_API_KEY in Django settings.'}, status=500)
                
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            
            system_prompt = (
                "You are a highly helpful, empathetic, and knowledgeable AI Health Assistant in the HealthCare Portal.\n"
                "You can help patients understand symptoms, answer general medical queries, explain clinical terms, and offer healthy lifestyle tips.\n"
                "Always provide structured, clear explanations using markdown formatting (bullet points, bold text).\n"
                "CRITICAL: Always include a standard, brief disclaimer reminding the user that you are an AI assistant and they should consult a professional healthcare provider for diagnostic assessments or emergencies."
            )
            
            # Retrieve history from session
            history = request.session.get('ai_chat_history', [])
            
            # Limit history to prevent payload bloating (last 10 messages)
            if len(history) > 10:
                history = history[-10:]
                
            messages_payload = [{'role': 'system', 'content': system_prompt}]
            for msg in history:
                messages_payload.append({'role': msg['role'], 'content': msg['content']})
                
            # Append new user message
            messages_payload.append({'role': 'user', 'content': user_message})
            
            payload = {
                'model': 'llama-3.1-8b-instant',
                'messages': messages_payload,
                'temperature': 0.7,
                'max_tokens': 1024
            }
            
            response = requests.post(
                'https://api.groq.com/openai/v1/chat/completions',
                headers=headers,
                json=payload,
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                reply = result['choices'][0]['message']['content']
                
                # Append user message and AI response to history
                history.append({'role': 'user', 'content': user_message})
                history.append({'role': 'assistant', 'content': reply})
                request.session['ai_chat_history'] = history
                request.session.modified = True
                
                return JsonResponse({'reply': reply})
            else:
                error_data = response.json()
                error_msg = error_data.get('error', {}).get('message', 'Failed to communicate with Groq.')
                return JsonResponse({'error': f"Groq API Error: {error_msg}"}, status=response.status_code)
                
        except Exception as e:
            return JsonResponse({'error': f"Internal Server Error: {str(e)}"}, status=500)
            
    # GET request
    chat_history = request.session.get('ai_chat_history', [])
    return render(request, 'base/ai_assistant.html', {'chat_history': chat_history})


@login_required
def hospital_locations(request):
    hospitals = [
        {
            'id': 1,
            'name': "King George's Medical University (KGMU)",
            'address': "Chowk, Shah Mina Road, Lucknow, UP 226003",
            'lat': 26.8672,
            'lng': 80.9168,
            'specialty': "Level 1 Trauma Center, Multi-specialty & General Clinical Care",
            'phone': "0522-2257540",
            'distance': "4.2 km"
        },
        {
            'id': 2,
            'name': "Sanjay Gandhi Post Graduate Institute of Medical Sciences (SGPGIMS)",
            'address': "Raebareli Road, Subhash Chandra Bose Nagar, Lucknow, UP 226014",
            'lat': 26.7634,
            'lng': 80.9388,
            'specialty': "Super-specialty (Cardiology, Endocrinology, Gastroenterology, Nephrology)",
            'phone': "0522-2668700",
            'distance': "11.8 km"
        },
        {
            'id': 3,
            'name': "Dr. Ram Manohar Lohia Institute of Medical Sciences (RMLIMS)",
            'address': "Vibhuti Khand, Gomti Nagar, Lucknow, UP 226010",
            'lat': 26.8624,
            'lng': 81.0029,
            'specialty': "Oncology, Neurology, Cardiology & Emergency Trauma Care",
            'phone': "0522-6692000",
            'distance': "6.1 km"
        },
        {
            'id': 4,
            'name': "Medanta Hospital Lucknow",
            'address': "Sector A, Pocket 1, Amar Shaheed Path, Golf City, Lucknow, UP 226030",
            'lat': 26.7972,
            'lng': 80.9995,
            'specialty': "Premium Multi-specialty & Emergency Cardiac/Stroke Care",
            'phone': "0522-4505050",
            'distance': "8.5 km"
        },
        {
            'id': 5,
            'name': "Sahara Hospital",
            'address': "Viraj Khand, Gomti Nagar, Lucknow, UP 226010",
            'lat': 26.8483,
            'lng': 81.0125,
            'specialty': "Multi-specialty, ICU & Critical Care",
            'phone': "0522-6780001",
            'distance': "7.3 km"
        },
        {
            'id': 6,
            'name': "Apollo Medics Super Speciality Hospital",
            'address': "Kanpur - Lucknow Road, LDA Colony, Lucknow, UP 226012",
            'lat': 26.7901,
            'lng': 80.8931,
            'specialty': "Advanced Cardiology, Trauma, ICU & Multi-specialty Care",
            'phone': "0522-6788888",
            'distance': "9.8 km"
        },
        {
            'id': 7,
            'name': "Command Hospital Central Command (Military Hospital)",
            'address': "Cantonment Road, Lucknow, UP 226002",
            'lat': 26.8225,
            'lng': 80.9634,
            'specialty': "Defense Medical Services, General Surgery & Intensive Care Unit",
            'phone': "0522-2296180",
            'distance': "3.5 km"
        },
        {
            'id': 8,
            'name': "Tender Palm Super Speciality Hospital",
            'address': "Sector 7, Gomti Nagar Extension, Lucknow, UP 226010",
            'lat': 26.8234,
            'lng': 81.0189,
            'specialty': "Cardiac Sciences, Neurosciences & Critical Care Units",
            'phone': "0522-3500111",
            'distance': "7.8 km"
        },
        {
            'id': 9,
            'name': "Dr. Shyama Prasad Mukherjee (Civil) Hospital",
            'address': "Park Road, Hazratganj, Lucknow, UP 226001",
            'lat': 26.8432,
            'lng': 80.9498,
            'specialty': "Government General Hospital, 24x7 Emergency, Surgery & Orthopedics",
            'phone': "0522-2239006",
            'distance': "1.2 km"
        },
        {
            'id': 10,
            'name': "Balrampur Hospital",
            'address': "Kaiserbagh, Lucknow, UP 226001",
            'lat': 26.8525,
            'lng': 80.9272,
            'specialty': "Famous Public Hospital, Diagnostic Labs, General Medicine & OPD",
            'phone': "0522-2622222",
            'distance': "2.1 km"
        },
        {
            'id': 11,
            'name': "Era's Lucknow Medical College and Hospital",
            'address': "Sarfarazganj, Hardoi Road, Lucknow, UP 226003",
            'lat': 26.8795,
            'lng': 80.8712,
            'specialty': "Medical Research, Trauma Center, Pediatrics & Maternity Care",
            'phone': "0522-2408123",
            'distance': "8.2 km"
        },
        {
            'id': 12,
            'name': "Charak Hospital & Research Centre",
            'address': "Dubagga, Hardoi Road, Lucknow, UP 226003",
            'lat': 26.8654,
            'lng': 80.8524,
            'specialty': "Multi-specialty Surgery, Gynecology, Neonatal ICU & General Wards",
            'phone': "0522-4244444",
            'distance': "10.1 km"
        },
        {
            'id': 13,
            'name': "Mayo Hospital",
            'address': "Vikas Khand, Gomti Nagar, Lucknow, UP 226010",
            'lat': 26.8519,
            'lng': 80.9992,
            'specialty': "ICU, Nephrology Dialysis Center, Orthopedics & Dialysis Unit",
            'phone': "0522-2303030",
            'distance': "6.0 km"
        },
        {
            'id': 14,
            'name': "Avadh Hospital and Heart Centre",
            'address': "Singar Nagar, Alambagh, Lucknow, UP 226005",
            'lat': 26.8094,
            'lng': 80.8988,
            'specialty': "Cardiology Diagnostics, Pacemaker Implantation & General Medicine",
            'phone': "0522-2453835",
            'distance': "6.8 km"
        }
    ]
    return render(request, 'base/hospital_locations.html', {'hospitals': hospitals})