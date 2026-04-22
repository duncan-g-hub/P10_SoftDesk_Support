from django.db import models
import uuid
from accounts.models import User


class Project(models.Model):
    """Modèle représentant un projet.

    Attributes:
        name (CharField): Nom du projet, limité à 100 caractères.
        description (TextField): Description détaillée du projet.
        type (CharField): Type de projet parmi : back-end, front-end, iOS, Android.
        created_time (DateTimeField): Horodatage de création, défini automatiquement.
        author (ForeignKey): Utilisateur auteur du projet.
            La suppression de l'auteur entraîne la suppression du projet.
    """

    name = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=9, choices=[
        ("back-end", "back-end"),
        ("front-end", "front-end"),
        ("iOS", "iOS"),
        ("Android", "Android")
    ])
    created_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')


class Contributor(models.Model):
    """Modèle représentant la relation entre un utilisateur et un projet.

    Un contributeur est un utilisateur ayant accès à un projet donné.
    Unique_together empêche qu'un même utilisateur soit ajouté
    plusieurs fois comme contributeur sur le même projet.

    Attributes:
        created_time (DateTimeField): Horodatage d'ajout du contributeur, défini automatiquement.
        user (ForeignKey): Utilisateur contributeur. Sa suppression entraîne la suppression de la relation.
        project (ForeignKey): Projet auquel l'utilisateur contribue. Sa suppression
            entraîne la suppression de la relation.

    Meta:
        unique_together: Garantit qu'un utilisateur ne peut être contributeur qu'une seule fois par projet.
    """

    created_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contributions')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='contributors')

    class Meta:
        unique_together = ('user', 'project')

    def __str__(self):
        """Retourne une représentation lisible du contributeur.

        Returns:
            str: Le nom d'utilisateur suivi du nom du projet entre parenthèses.
        """

        return f"{self.user.username} ({self.project.name})"


class Issue(models.Model):
    """Modèle représentant un problème (issue) rattaché à un projet.

    Attributes:
        name (CharField): Nom de l'issue, limité à 100 caractères.
        description (TextField): Description détaillée de l'issue.
        priority (CharField): Niveau de priorité parmi : LOW, MEDIUM, HIGH.
        tag (CharField): Catégorie de l'issue parmi : BUG, FEATURE, TASK.
        status (CharField): État d'avancement parmi : To Do, In Progress, Finished. Vaut "To Do" par défaut.
        created_time (DateTimeField): Horodatage de création, défini automatiquement.
        project (ForeignKey): Projet auquel l'issue est rattachée. Sa suppression entraîne la suppression de l'issue.
        assigned_to (ForeignKey): Contributeur assigné à l'issue. Peut être nul.
            Si le contributeur est supprimé, le champ est mis à NULL.
        author (ForeignKey): Utilisateur auteur de l'issue. Sa suppression entraîne la suppression de l'issue.
    """

    name = models.CharField(max_length=100)
    description = models.TextField()
    priority = models.CharField(max_length=6, choices=[
        ("LOW", "LOW"),
        ("MEDIUM", "MEDIUM"),
        ("HIGH", "HIGH")
    ])
    tag = models.CharField(max_length=7, choices=[
        ("BUG", "BUG"),
        ("FEATURE", "FEATURE"),
        ("TASK", "TASK")
    ])
    status = models.CharField(max_length=11, choices=[
        ("To Do", "To Do"),
        ("In Progress", "In Progress"),
        ("Finished", "Finished")
    ], default="To Do")
    created_time = models.DateTimeField(auto_now_add=True)

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='issues')
    assigned_to = models.ForeignKey(Contributor, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='assigned_issues')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_issues')


class Comment(models.Model):
    """Modèle représentant un commentaire rattaché à une issue.

    Attributes:
        description (TextField): Contenu textuel du commentaire.
        uuid (UUIDField): Identifiant universel unique, généré automatiquement et non modifiable.
        created_time (DateTimeField): Horodatage de création, défini automatiquement.
        issue (ForeignKey): Issue à laquelle le commentaire est rattaché.
            Sa suppression entraîne la suppression du commentaire.
        author (ForeignKey): Utilisateur auteur du commentaire. Sa suppression
            entraîne la suppression du commentaire.
    """

    description = models.TextField()
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_time = models.DateTimeField(auto_now_add=True)

    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_comments')
