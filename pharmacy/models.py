from django.db import models

class MedicineCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Medicine Categories"

class Medicine(models.Model):
    name = models.CharField(max_length=200)
    generic_name = models.CharField(max_length=200, blank=True)
    category = models.ForeignKey(MedicineCategory, on_delete=models.SET_NULL, null=True)
    manufacturer = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    dosage_form = models.CharField(max_length=100, blank=True, help_text="e.g. Tablet, Syrup, Injection")
    strength = models.CharField(max_length=100, blank=True, help_text="e.g. 500mg, 250mg/5ml")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock_quantity = models.IntegerField(default=0)
    reorder_level = models.IntegerField(default=10)
    expiry_date = models.DateField(null=True, blank=True)
    batch_number = models.CharField(max_length=50, blank=True)
    requires_prescription = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.strength})"

    @property
    def is_low_stock(self):
        return self.stock_quantity <= self.reorder_level

    @property
    def is_expired(self):
        if self.expiry_date:
            from datetime import date
            return self.expiry_date < date.today()
        return False

class Dispensing(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='dispensings')
    patient_name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    dispensed_by = models.CharField(max_length=100, blank=True)
    prescription_ref = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    dispensed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.medicine.name} to {self.patient_name} ({self.dispensed_at.date()})"

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
        # Reduce stock
        self.medicine.stock_quantity -= self.quantity
        self.medicine.save()

    class Meta:
        ordering = ['-dispensed_at']

class StockMovement(models.Model):
    MOVEMENT_TYPE = [
        ('in', 'Stock In'),
        ('out', 'Stock Out'),
        ('adjustment', 'Adjustment'),
        ('return', 'Return'),
    ]
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='stock_movements')
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPE)
    quantity = models.IntegerField()
    reason = models.CharField(max_length=200, blank=True)
    performed_by = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.medicine.name} - {self.movement_type} ({self.quantity})"

    class Meta:
        ordering = ['-created_at']