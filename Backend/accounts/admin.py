from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
  fieldsets = UserAdmin.fieldsets + (
    (
      'Sécurité LapinGestion',  # Titre du fieldset
      {
        'fields': ('pin_hash', 'pin_failed_attempts', 'pin_locked_until'),
      }
    ),
  )
readonly_fields = ('pin_hash', 'pin_failed_attempts', 'pin_locked_until')  # Rendre ces champs en lecture seule dans l'admin
