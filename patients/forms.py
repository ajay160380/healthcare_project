from django import forms
from .models import Patient, MedicalRecord, VitalRecord

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        exclude = ['user', 'created_at', 'updated_at']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'allergies': forms.Textarea(attrs={'rows': 2}),
            'chronic_conditions': forms.Textarea(attrs={'rows': 2}),
        }

class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        exclude = ['patient', 'created_at']
        widgets = {
            'record_date': forms.DateInput(attrs={'type': 'date'}),
            'diagnosis': forms.Textarea(attrs={'rows': 3}),
            'symptoms': forms.Textarea(attrs={'rows': 2}),
            'treatment': forms.Textarea(attrs={'rows': 3}),
            'prescription': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

class VitalRecordForm(forms.ModelForm):
    class Meta:
        model = VitalRecord
        exclude = ['patient', 'recorded_at']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2}),
        }