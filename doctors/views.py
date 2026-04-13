from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Doctor, Specialization
from .forms import DoctorForm, SpecializationForm

# --- Doctor Views ---

@login_required
def doctor_list(request):
    query = request.GET.get('q', '')
    # select_related use karne se database hits kam ho jayenge (Foreign Key optimization)
    doctors = Doctor.objects.select_related('specialization').filter(is_active=True)
    
    if query:
        doctors = doctors.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(specialization__name__icontains=query) |
            Q(phone__icontains=query)
        )
    
    context = {'doctors': doctors, 'query': query}
    return render(request, 'doctors/doctor_list.html', context)

@login_required
def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    # Recent 10 appointments fetch ho rahi hain
    appointments = doctor.appointments.order_by('-appointment_date')[:10]
    return render(request, 'doctors/doctor_detail.html', {'doctor': doctor, 'appointments': appointments})

@login_required
def doctor_create(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            doctor = form.save()
            messages.success(request, f'{doctor.get_full_name()} successfully add ho gaye hain!')
            return redirect('doctor_detail', pk=doctor.pk)
    else:
        form = DoctorForm()
    
    return render(request, 'doctors/doctor_form.html', {'form': form, 'title': 'Add New Doctor'})

@login_required
def doctor_update(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doctor details update kar di gayi hain.')
            return redirect('doctor_detail', pk=doctor.pk)
    else:
        form = DoctorForm(instance=doctor)
    
    return render(request, 'doctors/doctor_form.html', {
        'form': form, 
        'title': 'Update Doctor',
        'doctor': doctor
    })

@login_required
def doctor_delete(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        name = doctor.get_full_name()
        # Hard delete ke bajaye soft delete (is_active=False) best practice hai
        doctor.is_active = False
        doctor.save()
        messages.success(request, f'{name} ko deactivate kar diya gaya hai.')
        return redirect('doctor_list')
    return render(request, 'doctors/doctor_confirm_delete.html', {'doctor': doctor})

# --- Specialization Views ---

@login_required
def specialization_list(request):
    specializations = Specialization.objects.all()
    return render(request, 'doctors/specialization_list.html', {'specializations': specializations})

@login_required
def specialization_create(request):
    if request.method == 'POST':
        form = SpecializationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Nayi Specialization add ho gayi!')
            return redirect('specialization_list')
    else:
        form = SpecializationForm()
    return render(request, 'doctors/specialization_form.html', {'form': form})