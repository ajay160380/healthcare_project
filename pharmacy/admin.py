from django.contrib import admin
from .models import Medicine, MedicineCategory, Dispensing, StockMovement
admin.site.register(Medicine)
admin.site.register(MedicineCategory)
admin.site.register(Dispensing)
admin.site.register(StockMovement)