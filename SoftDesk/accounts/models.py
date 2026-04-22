from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Modèle utilisateur personnalisé qui hérite d'AbstractUser.

    Ajoute des champs supplémentaires pour la date de naissance,
    les préférences de contact et de partage de données.

    Attributes:
        birth_date (DateField): Date de naissance de l'utilisateur.
        can_be_contacted (BooleanField): Indique si l'utilisateur accepte d'être contacté.
        can_data_be_shared (BooleanField): Indique si l'utilisateur autorise le partage de ses données.
        created_time (DateTimeField): Horodatage de création du compte, défini automatiquement.
    """

    birth_date = models.DateField(verbose_name='Date de naissance', null=True, blank=True)
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
