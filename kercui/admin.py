from django.contrib import admin
from .models import ProfessionnelSante
# from .models import ProfessionnelSante  # Assure-toi que c'est bien importé

# @admin.register(ProfessionnelSante)
# class ProfessionnelSanteAdmin(admin.ModelAdmin):
#     list_display = ('nom', 'prenom', 'profession', 'ville')
    # list_filter = ('profession')
    # search_fields = ('nom', 'prenom', 'numero_rpps', 'email')
    # ordering = ('nom', 'prenom')