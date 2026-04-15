from django.db import models

from accounts.models import User


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=3, choices=[
        ("BCK", "back-end"),
        ("FRT", "front-end"),
        ("IOS", "iOS"),
        ("ADR", "Android")
    ])
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects') # auteur du projet
    created_time = models.DateTimeField(auto_now_add=True)



class Contributor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contributions') # contributeur d'un projet
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='contributors') # projet contribué
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'project')  # un user ne peut pas être contributeur plusieurs fois du meme projet