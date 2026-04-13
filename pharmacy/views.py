from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum
from .models import Medicine, MedicineCategory, Dispensing, StockMovement
from .forms import MedicineForm, DispensingForm, StockMovementForm, MedicineCategoryForm

@login_required
def medicine_list(request):
    query = request.GET.get('q', '')
    low_stock = request.GET.get('low_stock', '')
    medicines = Medicine.objects.select_related('category').filter(is_active=True)
    
    if query:
        medicines = medicines.filter(
            Q(name__icontains=query) |
            Q(generic_name__icontains=query) |
            Q(category__name__icontains=query)
        )
    
    if low_stock:
        medicines = [m for m in medicines if m.is_low_stock]
        
    return render(request, 'pharmacy/medicine_list.html', {
        'medicines': medicines, 
        'query': query, 
        'low_stock': low_stock
    })

@login_required
def medicine_detail(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    dispensings = medicine.dispensings.all()[:10]
    stock_movements = medicine.stock_movements.all()[:10]
    return render(request, 'pharmacy/medicine_detail.html', {
        'medicine': medicine, 
        'dispensings': dispensings, 
        'stock_movements': stock_movements
    })

@login_required
def medicine_create(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            medicine = form.save()
            messages.success(request, f'{medicine.name} added to pharmacy!')
            return redirect('medicine_detail', pk=medicine.pk)
    else:
        form = MedicineForm()
    return render(request, 'pharmacy/medicine_form.html', {'form': form, 'title': 'Add Medicine'})

@login_required
def medicine_update(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    if request.method == 'POST':
        form = MedicineForm(request.POST, instance=medicine)
        if form.is_valid():
            form.save()
            messages.success(request, 'Medicine updated successfully!')
            return redirect('medicine_detail', pk=medicine.pk)
    else:
        form = MedicineForm(instance=medicine)
    return render(request, 'pharmacy/medicine_form.html', {
        'form': form, 
        'title': 'Update Medicine', 
        'medicine': medicine
    })

@login_required
def dispense_medicine(request):
    if request.method == 'POST':
        form = DispensingForm(request.POST)
        if form.is_valid():
            dispensing = form.save(commit=False)
            medicine = dispensing.medicine
            if dispensing.quantity > medicine.stock_quantity:
                messages.error(request, f'Insufficient stock. Available: {medicine.stock_quantity}')
            else:
                dispensing.unit_price = medicine.unit_price
                dispensing.save()
                messages.success(request, f'Medicine dispensed successfully! Total: ₹{dispensing.total_price}')
                return redirect('dispensing_list')
    else:
        form = DispensingForm()
    return render(request, 'pharmacy/dispense_form.html', {'form': form})

@login_required
def dispensing_list(request):
    dispensings = Dispensing.objects.select_related('medicine').order_by('-dispensed_at')
    return render(request, 'pharmacy/dispensing_list.html', {'dispensings': dispensings})

@login_required
def add_stock(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    if request.method == 'POST':
        form = StockMovementForm(request.POST)
        if form.is_valid():
            movement = form.save(commit=False)
            movement.medicine = medicine
            
            if movement.movement_type == 'in':
                medicine.stock_quantity += movement.quantity
            elif movement.movement_type == 'out':
                if movement.quantity > medicine.stock_quantity:
                    messages.error(request, 'Insufficient stock.')
                    return render(request, 'pharmacy/stock_form.html', {'form': form, 'medicine': medicine})
                medicine.stock_quantity -= movement.quantity
            elif movement.movement_type == 'adjustment':
                medicine.stock_quantity = movement.quantity
            
            medicine.save()
            movement.save()
            messages.success(request, 'Stock updated successfully!')
            return redirect('medicine_detail', pk=pk)
    else:
        form = StockMovementForm()
    return render(request, 'pharmacy/stock_form.html', {'form': form, 'medicine': medicine})

@login_required
def pharmacy_dashboard(request):
    total_medicines = Medicine.objects.filter(is_active=True).count()
    low_stock_medicines = [m for m in Medicine.objects.filter(is_active=True) if m.is_low_stock]
    expired_medicines = [m for m in Medicine.objects.filter(is_active=True) if m.is_expired]
    recent_dispensings = Dispensing.objects.select_related('medicine').order_by('-dispensed_at')[:10]
    
    total_dispensed_today = Dispensing.objects.filter(
        dispensed_at__date=__import__('datetime').date.today()
    ).aggregate(total=Sum('total_price'))['total'] or 0
    
    return render(request, 'pharmacy/pharmacy_dashboard.html', {
        'total_medicines': total_medicines,
        'low_stock_medicines': low_stock_medicines,
        'expired_medicines': expired_medicines,
        'recent_dispensings': recent_dispensings,
        'total_dispensed_today': total_dispensed_today,
    })

@login_required
def category_list(request):
    categories = MedicineCategory.objects.all()
    return render(request, 'pharmacy/category_list.html', {'categories': categories})

@login_required
def category_create(request):
    if request.method == 'POST':
        form = MedicineCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('category_list')
    else:
        form = MedicineCategoryForm()
    return render(request, 'pharmacy/category_form.html', {'form': form})