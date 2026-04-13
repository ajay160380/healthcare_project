from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Patient, MedicalRecord, VitalRecord
from .forms import PatientForm, MedicalRecordForm, VitalRecordForm


@login_required
def patient_list(request):
    query = request.GET.get('q', '')
    patients = Patient.objects.all().order_by('-created_at')

    if query:
        patients = patients.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(phone__icontains=query) |
            Q(email__icontains=query)
        )

    return render(request, 'patients/patient_list.html', {
        'patients': patients,
        'query': query
    })


@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    medical_records = patient.medical_records.all()[:10]
    vitals = patient.vitals.all()[:5]

    return render(request, 'patients/patient_detail.html', {
        'patient': patient,
        'medical_records': medical_records,
        'vitals': vitals
    })


@login_required
def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save()
            messages.success(request, f'Patient {patient.get_full_name()} added successfully!')
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = PatientForm()

    return render(request, 'patients/patient_form.html', {
        'form': form,
        'title': 'Add New Patient'
    })


@login_required
def patient_update(request, pk):
    patient = get_object_or_404(Patient, pk=pk)

    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patient information updated successfully!')
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = PatientForm(instance=patient)

    return render(request, 'patients/patient_form.html', {
        'form': form,
        'title': 'Update Patient',
        'patient': patient
    })


@login_required
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)

    if request.method == 'POST':
        name = patient.get_full_name()
        patient.delete()
        messages.success(request, f'Patient {name} deleted successfully.')
        return redirect('patient_list')

    return render(request, 'patients/patient_confirm_delete.html', {
        'patient': patient
    })


@login_required
def add_medical_record(request, patient_pk):
    patient = get_object_or_404(Patient, pk=patient_pk)

    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.patient = patient
            record.save()
            messages.success(request, 'Medical record added successfully!')
            return redirect('patient_detail', pk=patient_pk)
    else:
        form = MedicalRecordForm()

    return render(request, 'patients/medical_record_form.html', {
        'form': form,
        'patient': patient
    })


@login_required
def add_vital_record(request, patient_pk):
    patient = get_object_or_404(Patient, pk=patient_pk)

    if request.method == 'POST':
        form = VitalRecordForm(request.POST)
        if form.is_valid():
            vital = form.save(commit=False)
            vital.patient = patient
            vital.save()
            messages.success(request, 'Vital signs recorded successfully!')
            return redirect('patient_detail', pk=patient_pk)
    else:
        form = VitalRecordForm()

    return render(request, 'patients/vital_record_form.html', {
        'form': form,
        'patient': patient
    })