from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
import random

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=20)
    date_naissance = models.DateField()
    adresse = models.TextField()

    def __str__(self):
        return self.user.username


class Inscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=20)
    date_naissance = models.DateField()
    adresse = models.TextField()
    date_inscription = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inscription de {self.user.username}"


class ProfessionnelSante(models.Model):
    CIVILITE_CHOICES = [
        ('M', 'M'),
        ('Mlle', 'Mlle'),
        ('Mme', 'Mme'),
    ]
    
    PROFESSION_CHOICES = [
        ('medecin', 'Médecin'),
        ('infirmier', 'Infirmier'),
        ('kinesitherapeute', 'Kinésithérapeute'),
        ('dentiste', 'Dentiste'),
        ('sage-femme', 'Sage-femme'),
    ]
    
    civilite = models.CharField(max_length=10, choices=CIVILITE_CHOICES)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128) 
    telephone = models.CharField(max_length=20)
    profession = models.CharField(max_length=100, choices=PROFESSION_CHOICES)
    adresse_cabinet = models.TextField()
    
    def __str__(self):
        return f"{self.civilite} {self.nom} {self.prenom}"
    
    class Meta:
        db_table = 'kercui_professionnelsante'


class RendezVous(models.Model):
    """
    Modèle représentant un rendez-vous médical.
    """
    STATUT_CHOICES = [
        ('CONFIRMÉ', 'Confirmé'),
        ('EN_ATTENTE', 'En attente'),
        ('ANNULÉ', 'Annulé'),
    ]
   
    TYPE_CHOICES = [
        ('Consultation vidéo', 'Consultation vidéo'),
        ('Suivi médical', 'Suivi médical'),
        ('Première consultation', 'Première consultation'),
        ('Consultation en cabinet', 'Consultation en cabinet'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rendez_vous_patient')
    date_heure = models.DateTimeField()
    type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='EN_ATTENTE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"RDV: {self.user.first_name} {self.user.last_name} - {self.date_heure.strftime('%d/%m/%Y %H:%M')}"
   
    class Meta:
        verbose_name = "Rendez-vous"
        verbose_name_plural = "Rendez-vous"
        ordering = ['date_heure']