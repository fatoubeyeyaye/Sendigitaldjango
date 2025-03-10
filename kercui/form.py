# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import Patient, Inscription as InscriptionModel, ProfessionnelSante
from django.apps import apps
from .models import RendezVous



class PatientInscriptionForm(UserCreationForm):
    email = forms.EmailField(required=True)
    telephone = forms.CharField(max_length=20)
    date_naissance = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    adresse = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'telephone', 'date_naissance', 'adresse')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
       
        if commit:
            user.save()
            Patient.objects.create(
                user=user,
                telephone=self.cleaned_data['telephone'],
                date_naissance=self.cleaned_data['date_naissance'],
                adresse=self.cleaned_data['adresse']
            )
        return user

class InscriptionForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    telephone = forms.CharField(max_length=11, required=True)
    adresse = forms.CharField(max_length=233, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'telephone', 'adresse')

class ConnexionForm(forms.Form):
    username = forms.CharField(label='Nom d utilisateur')
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)


class ProfessionnelSanteForm(forms.ModelForm):
    CIVILITE_CHOICES = [
        ('M', 'M'),
        ('Mlle', 'Mlle'),
        ('Mme', 'Mme'),
    ]
    
    civilite = forms.ChoiceField(choices=CIVILITE_CHOICES)
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    adresse_cabinet = forms.CharField(widget=forms.Textarea(attrs={
    'placeholder': 'Adresse du cabinet',
    'rows': '1', 
    'style': 'height: 38px; resize: vertical;' 
}))
    
    class Meta:
        model = ProfessionnelSante
        fields = ['civilite', 'nom', 'prenom', 'email', 'telephone', 
                  'profession', 'adresse_cabinet']
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Les mots de passe ne correspondent pas.")
        
        return cleaned_data

class RendezVousForm(forms.ModelForm):
    STATUT_CHOICES = [
        ('CONFIRMÉ', 'Confirmé'),
    ('EN_ATTENTE', 'En attente'),
    ('ANNULÉ', 'Annulé'),
    ]
    
    patient = forms.ModelChoiceField(
        queryset=User.objects.all(),
        empty_label="Sélectionnez un patient",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    statut = forms.ChoiceField(
        choices=STATUT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = RendezVous
        fields = ['patient', 'date_heure', 'type', 'statut']
        widgets = {
            'date_heure': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'},
                format='%Y-%m-%dT%H:%M'
            ),
            'type': forms.Select(
                choices=[
                    ('Consultation vidéo', 'Consultation vidéo'),
                    ('Suivi médical', 'Suivi médical'),
                    ('Première consultation', 'Première consultation')
                ],
                attrs={'class': 'form-control'}
            )
        }
        labels = {
            'date_heure': 'Date et heure',
            'type': 'Type de consultation'
        }