from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('STUDENT', 'Student'),
        ('TEACHER', 'Teacher'),
        ('ADMIN', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='STUDENT')
    department = models.CharField(max_length=100, blank=True)
    grade = models.CharField(max_length=50, blank=True) # e.g., "Year 3"

    def __str__(self):
        return f"{self.username} - {self.role}"