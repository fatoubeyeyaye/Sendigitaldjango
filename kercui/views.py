from django.shortcuts import render, redirect
from django.contrib import messages
from .form import InscriptionForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required as connexion_required
from .form import ProfessionnelSanteForm
from django.contrib.auth import authenticate, login as Connexion
from django.contrib.auth.models import User
from .form import ProfessionnelSanteForm
from django.contrib.auth import login as auth_login
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from django.http import JsonResponse
from kercui.models import ProfessionnelSante
from kercui.form import RendezVousForm
from django.contrib.auth.decorators import login_required
from django.db import connection
from .models import RendezVous
from django.shortcuts import get_object_or_404






def home(request):
    return render(request, 'kercui/home.html')

def Inscription(request):
    if request.method == "POST":
        form = InscriptionForm(request.POST)
        if form.is_valid(): 
            user = form.save(commit=False)
            
            user.email = request.POST.get('username') 
            user.save()

           
            Connexion(request, user)
            return redirect('home')
    else:
        form = InscriptionForm()
    return render(request, 'kercui/Authentification/Inscription.html', {'form': form})

@connexion_required
def patient_dashboard(request):
    context = {
        'user': request.user,
        'prenom': request.user.first_name,
        'nom': request.user.last_name,
    }
    return render(request, 'kercui/patient.html', context)

@connexion_required
def video_consultation(request):
    context = {
        'room_name': f"consultation_{request.user.id}",
        'patient_name': f"{request.user.first_name} {request.user.last_name}"
    }
    return render(request, 'kercui/video_consultation.html', context)

def Login_prof_view(request):
    return render(request, 'kercui/Authentification/Connexion.html')  

def form_prof(request):
    return render(request, 'kercui/form_prof.html') 

def Inscription_healthcare(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        form = ProfessionnelSanteForm(data)
        if form.is_valid():
            professionnel = form.save()
            return JsonResponse({'message': 'Inscription réussie'})
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

def Connexion_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')
       
        if user_type == 'patient':
            user = authenticate(request, username=email, password=password)
           
            if user is not None:
                auth_login(request, user)
                return redirect('patient')
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect")
       
        elif user_type == 'medecin':
            try:
                from django.contrib.auth.hashers import check_password
                
                professionnel = ProfessionnelSante.objects.get(email=email)
                if check_password(password, professionnel.password):
                    try:
                        user = User.objects.get(username=email)
                        auth_login(request, user)
                    except User.DoesNotExist:
                        request.session['professionnel_id'] = professionnel.id
                        request.session['is_authenticated'] = True
                        
                    return redirect('medecin')
                else:
                    messages.error(request, "Mot de passe incorrect")
            except ProfessionnelSante.DoesNotExist:
                messages.error(request, "Ce compte professionnel de santé n'existe pas")
   
    return render(request, 'kercui/Authentification/Connexion.html')
    
def patient_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('Connexion')
    return render(request, 'kercui/patient.html')

def password_reset(request):
    pass   

def inscription_professionnel(request):
    if request.method == 'POST':
        form = ProfessionnelSanteForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['email'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['prenom'],
                last_name=form.cleaned_data['nom']
            )
            professionnel = form.save(commit=False)
            professionnel.user = user
            professionnel.save()
            
            messages.success(request, "Votre compte a été créé avec succès. Vous pouvez maintenant vous connecter.")
            return redirect('Connexion')
    else:
        form = ProfessionnelSanteForm()
    
    return render(request, 'kercui/inscription_professionnel.html', {'form': form})

def form_prof(request):
    if request.method == 'POST':
        form = ProfessionnelSanteForm(request.POST)
        if form.is_valid():
            professional = form.save(commit=False)
            professional.password = make_password(form.cleaned_data['password'])
            professional.save()
            
            messages.success(request, "Votre compte professionnel a été créé avec succès!")
            return redirect('Connexion')
    else:
        form = ProfessionnelSanteForm()
    
    return render(request, 'kercui/form_prof.html', {'form': form}) 

def medecin_view(request):
    if not request.user.is_authenticated and not request.session.get('is_authenticated'):
        return redirect('connexion') 
    rendezvous = RendezVous.objects.all()
    context = {
        'debug_data': rendezvous,
        'model_fields': [field.name for field in RendezVous._meta.get_fields()],
        'rendezvous_list': rendezvous
    }
    return render(request, 'kercui/medecin.html', context)  

def mes_rendez_vous(request):
    rendez_vous = RendezVous.objects.filter(patient=request.user).order_by('date_heure')
    return render(request, 'mes_rendez_vous.html', {'rendez_vous': rendez_vous})

@login_required
def creer_rendez_vous(request):
    users = User.objects.all()
    print("Users with emails:", [(user.id, user.email) for user in users])
    
    if request.method == 'POST':
        form = RendezVousForm(request.POST)
        if form.is_valid():
            rendez_vous = form.save(commit=False)
            rendez_vous.user = request.user
            
            patient_id = request.POST.get('patient')
            print(f"Patient ID from form: {patient_id}")
            
            if patient_id:
                try:
                    selected_patient = User.objects.get(id=patient_id)
                    print(f"Found patient: {selected_patient.email}")
                    rendez_vous.patient = selected_patient
                except User.DoesNotExist:
                    print(f"No user found with ID: {patient_id}")
            
            rendez_vous.save()
            return redirect('medecin')
    else:
        form = RendezVousForm()
    
    return render(request, 'kercui/rdv.html', {
        'form': form,
        'users': users,
        'STATUT_CHOICES': RendezVousForm.STATUT_CHOICES,
    })
def annuler_rendez_vous(request, rdv_id):
    rendez_vous = get_object_or_404(RendezVous, id=rdv_id, patient=request.user)
    
    if rendez_vous.statut == 'annule':
        messages.error(request, 'Ce rendez-vous a déjà été annulé.')
    else:
        rendez_vous.statut = 'annule'
        rendez_vous.save()
        messages.success(request, 'Votre rendez-vous a été annulé avec succès.')
    
    return redirect('mes_rendez_vous')     


@login_required
def liste_rendezvous(request):
    """Vue pour afficher les rendez-vous directement depuis la table"""
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM kercui_rendezvous")
        columns = [col[0] for col in cursor.description]
        rendezvous_raw = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    user_ids = [rdv['user_id'] for rdv in rendezvous_raw if rdv['user_id']]
    
    from django.contrib.auth import get_user_model
    User = get_user_model()
    users = {user.id: user for user in User.objects.filter(id__in=user_ids)}
    
    for rdv in rendezvous_raw:
        user_id = rdv.get('user_id')
        if user_id and user_id in users:
            user = users[user_id]
            rdv['patient_name'] = f"{user.first_name} {user.last_name}" if user.first_name else f"Utilisateur {user.id}"
        else:
            rdv['patient_name'] = "Non assigné"
    
    context = {
        'rendezvous': rendezvous_raw,
        'total_count': len(rendezvous_raw),
        'patients': User.objects.all(),
        'debug_data': rendezvous_raw 
    }
    return render(request, 'kercui/medecin.html', context)

@login_required
def edit_rdv(request, rdv_id):
    """Vue pour modifier un rendez-vous existant"""
    rdv = get_object_or_404(RendezVous, id=rdv_id)
    
    if request.user.is_staff or (rdv.user and rdv.user == request.user):
        if request.method == 'POST':
            form = RendezVousForm(request.POST, instance=rdv)
            if form.is_valid():
                form.save()
                messages.success(request, "Le rendez-vous a été modifié avec succès!")
                return redirect('rdv') 
        else:
            form = RendezVousForm(instance=rdv)
        from django.contrib.auth import get_user_model
        User = get_user_model()
        users = User.objects.all()
        
        return render(request, 'kercui/modifier_rendezvous.html', {
            'form': form,
            'rdv': rdv,
            'users': users
        })
    else:
        messages.error(request, "Vous n'avez pas l'autorisation de modifier ce rendez-vous.")
        return redirect('rdv') 

@login_required
def cancel_rdv(request, rdv_id):
    """Vue pour annuler un rendez-vous"""
    rdv = get_object_or_404(RendezVous, id=rdv_id, user=request.user)
    
    if request.method == 'POST':
        rdv.statut = 'Annulé'  
        rdv.save()
        messages.success(request, "Le rendez-vous a été annulé avec succès!")
        return redirect('medecin')
    else:
        return render(request, 'kercui/confirmer_annulation.html', {
            'rdv': rdv
        })


@login_required
def reschedule_rdv(request, rdv_id):
    """Vue pour reprogrammer un rendez-vous annulé"""
    try:
        professionnel = ProfessionnelSante.objects.get(user=request.user)
        rdv = get_object_or_404(RendezVous, id=rdv_id, professionnel=professionnel)
        
        if request.method == 'POST':
            form = RendezVousForm(request.POST, instance=rdv)
            if form.is_valid():
                rdv = form.save(commit=False)
                rdv.statut = 'CONFIRMÉ'  
                rdv.save()
                messages.success(request, "Le rendez-vous a été reprogrammé avec succès!")
                return redirect('rdv')
        else:
            form = RendezVousForm(instance=rdv)
        
        return render(request, 'kercui/reprogrammer_rendezvous.html', {
            'form': form,
            'rdv': rdv,
            'professionnel': professionnel
        })
    except ProfessionnelSante.DoesNotExist:
        messages.error(request, "Vous n'avez pas l'autorisation d'accéder à cette page.")
        return redirect('medecin')

def video_consultation(request, id):
    from .models import VideoConsultation
    consultation = get_object_or_404(VideoConsultation, id=id)
    return render(request, 'kercui/video_consultation.html', {"rdv_id": rdv_id})