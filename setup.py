#!/usr/bin/env python3
"""
HealthCare Portal - Setup Script (Massive Data Version)
Run this to initialize the database with 500 realistic Lucknow doctors.
"""
import os
import sys
import django
from datetime import date, time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthcare_dashboard.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile
from doctors.models import Doctor, Specialization
from patients.models import Patient
from pharmacy.models import Medicine, MedicineCategory
from appointments.models import Appointment

print("🏥 Setting up HealthCare Portal with 500+ Lucknow Doctors...")

# 1. Create superuser
if not User.objects.filter(username='admin').exists():
    admin = User.objects.create_superuser('admin', 'admin@healthcare.com', 'admin123')
    UserProfile.objects.create(user=admin, role='admin')
    print("✅ Admin user created")

# 2. Create Specializations
specs = ['Cardiology', 'Neurology', 'Orthopedics', 'Pediatrics', 'Dermatology',
         'Gynecology', 'Ophthalmology', 'ENT', 'General Medicine', 'Psychiatry', 
         'Oncology', 'Urology', 'Gastroenterology', 'Pulmonology', 'Endocrinology', 'Nephrology']
for s in specs:
    Specialization.objects.get_or_create(name=s)
print("✅ Specializations created")

# 3. Dynamic Generator for 500 Realistic Lucknow Doctors
print("👨‍⚕️ Generating Massive Doctor Database...")

# Expanded name lists for more combinations (UP/North India focused)
first_names = [
    'Amit', 'Rajesh', 'Sanjay', 'Vikram', 'Anil', 'Pooja', 'Neha', 'Sunita', 'Meera', 'Kavita', 
    'Deepak', 'Tarun', 'Saurabh', 'Manoj', 'Arun', 'Vandana', 'Shikha', 'Aarti', 'Ritu', 'Swati',
    'Rahul', 'Gaurav', 'Abhishek', 'Prashant', 'Nitin', 'Manish', 'Ravi', 'Vivek', 'Sachin', 'Anurag',
    'Priyanka', 'Anjali', 'Komal', 'Rashmi', 'Jyoti', 'Divya', 'Shweta', 'Sneha', 'Pallavi', 'Garima'
]

last_names = [
    'Verma', 'Singh', 'Gupta', 'Mishra', 'Yadav', 'Patel', 'Dixit', 'Awasthi', 'Rastogi', 'Chauhan',
    'Sharma', 'Pandey', 'Tiwari', 'Shukla', 'Tripathi', 'Chaturvedi', 'Srivastava', 'Saxena', 'Khatri', 'Nigam',
    'Agarwal', 'Garg', 'Bansal', 'Jain', 'Goyal'
]

# Expanded Lucknow Areas
locations = [
    'Gomti Nagar', 'Aliganj', 'Hazratganj', 'Mahanagar', 'Jankipuram', 'Rajajipuram', 
    'Kapoorthala', 'Aashiana', 'Chowk', 'Aminabad', 'Thakurganj', 'Vikas Nagar', 
    'Khurram Nagar', 'Indira Nagar', 'Sushant Golf City', 'LDA Colony', 'Vibhuti Khand'
]

TARGET_DOCTORS = 500
lucknow_doctors_data = []
count = 0

# Generate unique combinations
for fn in first_names:
    for ln in last_names:
        if count >= TARGET_DOCTORS:
            break
            
        spec = specs[count % len(specs)]
        loc = locations[count % len(locations)]
        
        # Assign logic-based qualifications
        if spec in ['Cardiology', 'Neurology', 'Oncology', 'Gastroenterology', 'Nephrology']:
            qual = 'MBBS, DM'
        elif spec in ['Orthopedics', 'Gynecology', 'ENT', 'Urology']:
            qual = 'MBBS, MS'
        else:
            qual = 'MBBS, MD'
            
        exp = 5 + (count % 30) # Experience between 5 to 34 years
        fee = 500 + ((count * 50) % 1500) # Fees variation between 500 to 2000
        if fee < 500: fee = 500
        
        lucknow_doctors_data.append((fn, ln, spec, loc, qual, exp, fee))
        count += 1
    if count >= TARGET_DOCTORS:
        break

doc_count = 0
for i, (fn, ln, spec_name, loc, qual, exp, fee) in enumerate(lucknow_doctors_data, start=1):
    spec_obj = Specialization.objects.get(name=spec_name)
    
    # Generate unique dummy contact info
    phone = f"91{8000000000 + i}" 
    email = f"dr.{fn.lower()}.{ln.lower()}{i}@lko-health.in"
    license_num = f"UPMC/LKO/20{exp:02d}/{i:05d}"
    
    Doctor.objects.get_or_create(
        license_number=license_num,
        defaults=dict(
            first_name=fn, last_name=ln, specialization=spec_obj, 
            qualification=qual, experience_years=exp, 
            phone=phone, email=email, consultation_fee=fee,
            available_days='Mon,Tue,Wed,Thu,Fri,Sat',
            available_time_start=time(10, 0), 
            available_time_end=time(17, 0)
        )
    )
    doc_count += 1
    
    # Just to show progress in terminal since 500 might take a few seconds
    if doc_count % 100 == 0:
        print(f"⏳ Created {doc_count} doctors...")

print(f"✅ Successfully created {doc_count} Doctors for Lucknow region!")

# 4. Create Patients (UP/Lucknow context)
patients_data = [
    ('Rahul', 'Gupta', date(1985, 3, 15), 'M', 'B+', '9812345671', 'rahul@example.com', 'A-101, Gomti Nagar, Lucknow'),
    ('Meera', 'Singh', date(1992, 7, 22), 'F', 'O+', '9812345672', 'meera@example.com', 'B-202, Indira Nagar, Lucknow'),
]
for fn, ln, dob, gender, bg, ph, em, addr in patients_data:
    Patient.objects.get_or_create(
        phone=ph,
        defaults=dict(first_name=fn, last_name=ln, date_of_birth=dob, gender=gender,
                      blood_group=bg, email=em, address=addr)
    )
print("✅ Sample patients created")

# 5. Create Appointments
if Doctor.objects.exists() and Patient.objects.exists():
    doc = Doctor.objects.first()
    pat = Patient.objects.first()
    Appointment.objects.get_or_create(
        patient=pat, doctor=doc, appointment_date=date.today(),
        defaults=dict(appointment_time=time(11,0), appointment_type='consultation',
                      status='scheduled', reason='Viral Fever Symptoms')
    )
    print("✅ Sample appointment created")

print("\n🎉 Setup complete! Massive Database Ready.")