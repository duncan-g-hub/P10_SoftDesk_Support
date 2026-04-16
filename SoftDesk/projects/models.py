from django.db import models
import uuid
from accounts.models import User


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=9, choices=[
        ("back-end", "back-end"),
        ("front-end", "front-end"),
        ("iOS", "iOS"),
        ("Android", "Android")
    ])
    created_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')  # auteur du projet



class Contributor(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contributions')  # contributeur d'un projet
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='contributors')  # projet contribué

    class Meta:
        unique_together = ('user', 'project')  # un user ne peut pas être contributeur plusieurs fois du meme projet



class Issue(models.Model):
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
    assigned_to = models.ForeignKey(Contributor, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_issues')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_issues')


class Comment(models.Model):
    description = models.TextField()
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_time = models.DateTimeField(auto_now_add=True)

    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_comments')


