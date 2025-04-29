from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('SuperAdmin', 'SuperAdmin'),
        ('Admin', 'Admin'),
        ('User', 'User'),
    ) 
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='User')
    phone = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(max_length=20, choices=GENDER, default='male')
    value = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.username} ({self.role})"
    
class Task(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('On Hold', 'On Hold'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    worked_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    completion_report = models.TextField(blank=True, null=True)
    priority = models.IntegerField(default=0)  # Optional: priority field

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['due_date']
