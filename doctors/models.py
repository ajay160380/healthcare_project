from django.db import models
from django.contrib.auth.models import User


class Specialization(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    specialization = models.ForeignKey(
        Specialization,
        on_delete=models.SET_NULL,
        null=True
    )

    qualification = models.CharField(max_length=200)
    experience_years = models.IntegerField(default=0)
    phone = models.CharField(max_length=15)
    email = models.EmailField()

    license_number = models.CharField(max_length=50, unique=True)
    consultation_fee = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0
    )

    available_days = models.CharField(
        max_length=100,
        blank=True,
        help_text="e.g. Mon,Tue,Wed"
    )
    available_time_start = models.TimeField(null=True, blank=True)
    available_time_end = models.TimeField(null=True, blank=True)

    bio = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name}"

    def get_full_name(self):
        return f"Dr. {self.first_name} {self.last_name}"