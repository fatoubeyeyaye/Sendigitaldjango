from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from kercui.views import video_consultation

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('Connexion/', views.Connexion_view, name='Connexion'),
    path('Inscription/', views.Inscription, name='Inscription'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('video/', video_consultation, name='video_consultation'),
    path('Connexion/professional/', views.Login_prof_view, name='login_prof'),
    path('form_prof/', views.form_prof, name='form_prof'),
    path('patient/', views.patient_dashboard, name='patient'),
    path('medecin/', views.medecin_view, name='medecin'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('rdv/', views.creer_rendez_vous, name='rdv'),

    
     path('rdv/edit/<int:rdv_id>/', views.edit_rdv, name='edit_rdv'),
    path('rdv/cancel/<int:rdv_id>/', views.cancel_rdv, name='cancel_rdv'),
    path('rdv/confirm/<int:rdv_id>/', views.confirm_rdv, name='confirm_rdv'),
    path('rdv/reschedule/<int:rdv_id>/', views.reschedule_rdv, name='reschedule_rdv'),
    path('rdv/archive/<int:rdv_id>/', views.archive_rdv, name='archive_rdv'),
]