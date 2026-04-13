#!/usr/bin/env python3
"""
HealthCare Portal - Setup Script
Run this after installing requirements to initialize the database with sample data.
Usage: python setup.py
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthcare_dashboard.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile
from doctors.models import Doctor, Specialization
from patients.models import Patient
from pharmacy.models import Medicine, MedicineCategory
from appointments.models import Appointment
from datetime import date, time

print("🏥 Setting up HealthCare Portal...")

# Create superuser
if not User.objects.filter(username='admin').exists():
    admin = User.objects.create_superuser('admin', 'admin@healthcare.com', 'admin123')
    UserProfile.objects.create(user=admin, role='admin')
    print("✅ Admin user created: username=admin, password=admin123")

# Create Specializations
specs = ['Cardiology', 'Neurology', 'Orthopedics', 'Pediatrics', 'Dermatology',
         'Gynecology', 'Ophthalmology', 'ENT', 'General Medicine', 'Psychiatry']
for s in specs:
    Specialization.objects.get_or_create(name=s, defaults={'description': f'{s} specialist'})
print("✅ Specializations created")

# Create Doctors
docs_data = [
    ('Rajesh', 'Kumar', 'Cardiology', 'MBBS, MD (Cardiology)', 12, '9876543210', 'dr.rajesh@hc.com', 'DL001', 800),
    ('Priya', 'Sharma', 'Neurology', 'MBBS, DM (Neurology)', 8, '9876543211', 'dr.priya@hc.com', 'DL002', 700),
    ('Amit', 'Verma', 'Orthopedics', 'MBBS, MS (Ortho)', 15, '9876543212', 'dr.amit@hc.com', 'DL003', 600),
    ('Sunita', 'Patel', 'Pediatrics', 'MBBS, MD (Pediatrics)', 10, '9876543213', 'dr.sunita@hc.com', 'DL004', 500),
    ('Vikram', 'Singh', 'General Medicine', 'MBBS, MD', 6, '9876543214', 'dr.vikram@hc.com', 'DL005', 400),
]
for fn, ln, spec, qual, exp, ph, em, lic, fee in docs_data:
    s = Specialization.objects.get(name=spec)
    Doctor.objects.get_or_create(
        license_number=lic,
        defaults=dict(first_name=fn, last_name=ln, specialization=s, qualification=qual,
                      experience_years=exp, phone=ph, email=em, consultation_fee=fee,
                      available_days='Mon,Tue,Wed,Thu,Fri',
                      available_time_start=time(9,0), available_time_end=time(17,0))
    )
print("✅ Sample doctors created")

# Create Patients
patients_data = [
    ('Rahul', 'Gupta', date(1985, 3, 15), 'M', 'B+', '9812345671', 'rahul@example.com', 'A-101, Lucknow'),
    ('Meera', 'Singh', date(1992, 7, 22), 'F', 'O+', '9812345672', 'meera@example.com', 'B-202, Lucknow'),
    ('Suresh', 'Yadav', date(1970, 11, 5), 'M', 'A+', '9812345673', 'suresh@example.com', 'C-303, Lucknow'),
    ('Anita', 'Mishra', date(2000, 1, 30), 'F', 'AB-', '9812345674', 'anita@example.com', 'D-404, Kanpur'),
    ('Deepak', 'Tiwari', date(1965, 9, 18), 'M', 'O-', '9812345675', 'deepak@example.com', 'E-505, Varanasi'),
]
for fn, ln, dob, gender, bg, ph, em, addr in patients_data:
    Patient.objects.get_or_create(
        phone=ph,
        defaults=dict(first_name=fn, last_name=ln, date_of_birth=dob, gender=gender,
                      blood_group=bg, email=em, address=addr)
    )
print("✅ Sample patients created")

# Create Medicine Categories
cats = ['Antibiotics', 'Analgesics', 'Antihypertensives', 'Antidiabetics',
        'Vitamins & Supplements', 'Antihistamines', 'Antacids', 'Cardiovascular']
for c in cats:
    MedicineCategory.objects.get_or_create(name=c)
print("✅ Medicine categories created")

# Create Medicines
meds_data = [
    ('Paracetamol', 'Acetaminophen', 'Analgesics', 'Tablet', '500mg', 2.5, 500, 50),
    ('Amoxicillin', 'Amoxicillin', 'Antibiotics', 'Capsule', '250mg', 8.0, 300, 30),
    ('Amlodipine', 'Amlodipine Besylate', 'Antihypertensives', 'Tablet', '5mg', 5.0, 400, 40),
    ('Metformin', 'Metformin HCl', 'Antidiabetics', 'Tablet', '500mg', 3.5, 600, 60),
    ('Cetirizine', 'Cetirizine HCl', 'Antihistamines', 'Tablet', '10mg', 4.0, 250, 25),
    ('Pantoprazole', 'Pantoprazole', 'Antacids', 'Tablet', '40mg', 6.5, 350, 35),
    ('Atorvastatin', 'Atorvastatin Calcium', 'Cardiovascular', 'Tablet', '10mg', 12.0, 200, 20),
    ('Vitamin C', 'Ascorbic Acid', 'Vitamins & Supplements', 'Tablet', '500mg', 1.5, 1000, 100),
]
for name, generic, cat_name, form, strength, price, stock, reorder in meds_data:
    cat = MedicineCategory.objects.get(name=cat_name)
    Medicine.objects.get_or_create(
        name=name,
        defaults=dict(generic_name=generic, category=cat, dosage_form=form,
                      strength=strength, unit_price=price, stock_quantity=stock,
                      reorder_level=reorder, expiry_date=date(2026, 12, 31))
    )
print("✅ Sample medicines created")

# Create Appointments
if Doctor.objects.exists() and Patient.objects.exists():
    doc = Doctor.objects.first()
    pat = Patient.objects.first()
    Appointment.objects.get_or_create(
        patient=pat, doctor=doc, appointment_date=date.today(),
        defaults=dict(appointment_time=time(10,0), appointment_type='consultation',
                      status='scheduled', reason='Routine checkup')
    )
    print("✅ Sample appointment created")

print("\n🎉 Setup complete!")
print("=" * 50)
print("Admin Panel:  http://127.0.0.1:8000/admin/")
print("Login:        http://127.0.0.1:8000/accounts/login/")
print("Username:     admin")
print("Password:     admin123")
print("=" * 50)
print("\nRun the server with: python manage.py runserver")