from django import forms
from .models import Medicine, MedicineCategory, Dispensing, StockMovement

# Model ki jagah ModelForm use karein
class MedicineCategoryForm(forms.ModelForm):
    class Meta:
        model = MedicineCategory
        fields = ['name', 'description']

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = '__all__'
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }

class DispensingForm(forms.ModelForm):
    class Meta:
        model = Dispensing
        fields = ['medicine', 'patient_name', 'quantity', 'dispensed_by', 'prescription_ref', 'notes']

class StockMovementForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ['movement_type', 'quantity', 'reason', 'performed_by']