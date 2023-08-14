from django.contrib.auth.models import User
from django.db import models


class UserRole(models.Model):
    ROLE_CHOICES = [
        ('superadmin', 'Super Admin'),
        ('admin', 'Admin'),
        ('user', 'User'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class Vehicle(models.Model):
    VEHICLE_TYPES = [
        ('Two', 'Two Wheeler'),
        ('Three', 'Three Wheeler'),
        ('Four', 'Four Wheeler'),
    ]

    vehicle_number = models.CharField(max_length=20, unique=True)
    vehicle_type = models.CharField(max_length=10, choices=VEHICLE_TYPES)
    vehicle_model = models.CharField(max_length=50)
    vehicle_description = models.TextField()

    def __str__(self):
        return self.vehicle_number
