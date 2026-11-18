from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
  """
  Utilisateur de LapinGestion.

  Nous pourrons ajouter des information specifiques a l'application ultérieurement.
  """
  pass
