from django import forms
from .models import Appointment, Prescription, PrescriptionItem
from django.forms import inlineformset_factory


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        exclude = ['created_at', 'updated_at']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
            'appointment_time': forms.TimeInput(attrs={'type': 'time'}),
            'follow_up_date': forms.DateInput(attrs={'type': 'date'}),
            'reason': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        exclude = ['appointment', 'issued_date']
        widgets = {
            'valid_until': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


PrescriptionItemFormSet = inlineformset_factory(
    Prescription,
    PrescriptionItem,
    fields=['medicine_name', 'dosage', 'frequency', 'duration', 'instructions'],
    extra=3,
    can_delete=True,
)