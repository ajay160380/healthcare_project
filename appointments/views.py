from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Appointment, Prescription, PrescriptionItem
from .forms import AppointmentForm, PrescriptionForm, PrescriptionItemFormSet
from patients.models import Patient
from doctors.models import Doctor

@login_required
def appointment_list(request):
    query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')
    appointments = Appointment.objects.select_related('patient', 'doctor').order_by('-appointment_date', '-appointment_time')
    
    if query:
        appointments = appointments.filter(
            Q(patient__first_name__icontains=query) |
            Q(patient__last_name__icontains=query) |
            Q(doctor__first_name__icontains=query) |
            Q(doctor__last_name__icontains=query)
        )
    if status_filter:
        appointments = appointments.filter(status=status_filter)
        
    return render(request, 'appointments/appointment_list.html', {
        'appointments': appointments,
        'query': query,
        'status_filter': status_filter,
        'status_choices': Appointment.STATUS_CHOICES,
    })

@login_required
def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    try:
        prescription = appointment.prescription
    except Prescription.DoesNotExist:
        prescription = None
    return render(request, 'appointments/appointment_detail.html', {
        'appointment': appointment, 
        'prescription': prescription
    })

@login_required
def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appt = form.save()
            messages.success(request, 'Appointment booked successfully!')
            return redirect('appointment_detail', pk=appt.pk)
    else:
        form = AppointmentForm()
        patient_id = request.GET.get('patient')
        doctor_id = request.GET.get('doctor')
        if patient_id:
            form.initial['patient'] = patient_id
        if doctor_id:
            form.initial['doctor'] = doctor_id
            
    return render(request, 'appointments/appointment_form.html', {
        'form': form, 
        'title': 'Book Appointment'
    })

@login_required
def appointment_update(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment updated successfully!')
            return redirect('appointment_detail', pk=appointment.pk)
    else:
        form = AppointmentForm(instance=appointment)
        
    return render(request, 'appointments/appointment_form.html', {
        'form': form, 
        'title': 'Update Appointment', 
        'appointment': appointment
    })

@login_required
def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, 'Appointment cancelled and deleted.')
        return redirect('appointment_list')
    return render(request, 'appointments/appointment_confirm_delete.html', {
        'appointment': appointment
    })

@login_required
def update_status(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Appointment.STATUS_CHOICES):
            appointment.status = new_status
            appointment.save()
            messages.success(request, f'Appointment status updated to {appointment.get_status_display()}.')
    return redirect('appointment_detail', pk=pk)

@login_required
def add_prescription(request, appointment_pk):
    appointment = get_object_or_404(Appointment, pk=appointment_pk)
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.appointment = appointment
            prescription.save()
            
            # Save prescription items
            medicines = request.POST.getlist('medicine_name')
            dosages = request.POST.getlist('dosage')
            frequencies = request.POST.getlist('frequency')
            durations = request.POST.getlist('duration')
            instructions_list = request.POST.getlist('instructions')
            
            for i in range(len(medicines)):
                if medicines[i]:
                    PrescriptionItem.objects.create(
                        prescription=prescription,
                        medicine_name=medicines[i],
                        dosage=dosages[i] if i < len(dosages) else '',
                        frequency=frequencies[i] if i < len(frequencies) else '',
                        duration=durations[i] if i < len(durations) else '',
                        instructions=instructions_list[i] if i < len(instructions_list) else '',
                    )
            messages.success(request, 'Prescription added successfully!')
            return redirect('appointment_detail', pk=appointment_pk)
    else:
        form = PrescriptionForm()
    return render(request, 'appointments/prescription_form.html', {
        'form': form, 
        'appointment': appointment
    })

@login_required
def today_appointments(request):
    from datetime import date
    today = date.today()
    appointments = Appointment.objects.filter(appointment_date=today).select_related('patient', 'doctor').order_by('appointment_time')
    return render(request, 'appointments/today_appointments.html', {
        'appointments': appointments, 
        'today': today
    })