import base64
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

# Create your models here.
class User(AbstractUser):
    USER_ROLES = [
        ('user', 'USER'),
        ('student', 'STUDENT'),
        ('admin', 'ADMIN'),
        ('chair', 'CHAIR'),
        ('dean', 'DEAN'),
        ('hoq', 'HOQ'),
        ('hoc', 'HOC'),
    ]

    USER_STATUS_CHOICES = [
    ('active', 'Active'),
    ('inactive', 'Inactive'),
    ('suspended', 'Suspended'),
    ]

    must_change_password = models.BooleanField(default=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=USER_ROLES, default='student')
    created_by = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='created_users',
        editable=False,
    )
    user_status = models.CharField(
        max_length=20,
        choices=USER_STATUS_CHOICES,
        default='active'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   
    
    department = models.ForeignKey(
        'Department', 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='users',
    )

    
    def __str__(self):
        return self.username

    # --------- Instance method here ---------
    def deactivate(self):
        self.user_status = 'inactive'
        self.save()


class Role(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name
