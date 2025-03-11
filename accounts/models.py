from django.db import models
from django.contrib.auth.models import AbstractUser 

# Create your models here.
class User(AbstractUser):
    '''"Generated Model"'''

    # Override the fields you want to make required
    email = models.EmailField(unique=True, blank=False, null=False)
    first_name = models.CharField(max_length=150, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=False, null=False)
    birthdate = models.DateField(blank=False, null=False)
    
    
    SEX_CHOICES = [
    ("male", 'Male'),
    ("female", 'Female'),
    ]
    
    sex = models.CharField( max_length=6, choices = SEX_CHOICES, default="male",)

    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


    def __str__(self):
        return self.username 