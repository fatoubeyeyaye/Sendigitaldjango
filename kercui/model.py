from django.db import models
from django.contrib.auth.models import User

# class Patient(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     telephone = models.CharField(max_length=15)
#     date_naissance = models.DateField()
#     adresse = models.TextField()
    
#     def __str__(self):
#         return f"Patient: {self.user.username}"