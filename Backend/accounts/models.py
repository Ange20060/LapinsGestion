from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.

class User(AbstractUser):
  """
  Utilisateur de LapinGestion.

  Nous pourrons ajouter des information specifiques a l'application ultérieurement.
  """
  pin_hash = models.CharField(max_length=128, blank=True, null=True, help_text=_("Hash du code PIN de l'utilisateur."), default="")

  pin_failed_attempts = models.PositiveSmallIntegerField(default=0, help_text=_("Nombre de tentatives de code PIN échouées."))

  pin_locked_until = models.DateTimeField(blank=True, null=True, help_text=_("Date et heure jusqu'à laquelle le code PIN est verrouillé."))

  def set_pin(self, pin):
    """
    Définit le code PIN sécurisé de 6 chiffre """

    if not pin.isdigit() or len(pin) != 6:
      raise ValidationError(_("Le code PIN doit être un nombre à 6 chiffres."))
    self.pin_hash = make_password(pin)
    self.pin_failed_attempts = 0
    self.pin_locked_until = None

    def verify_pin(self, pin: str) -> bool:
        """
        Vérifie  le code PIN fourni sans jamais le stocker en clair.
        """
        if not self.pin_hash:
            return False  # Aucun code PIN défini
        if self.pin_locked_until and timezone.now() < self.pin_locked_until:
            return False  # Le code PIN est verrouillé
        return check_password(pin, self.pin_hash)
    def __str__(self):
        return self.username
  pass
