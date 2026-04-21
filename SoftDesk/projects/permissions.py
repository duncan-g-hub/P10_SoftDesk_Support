from rest_framework.permissions import BasePermission

from projects.models import Project, Contributor


class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Lecture toujours autorisée
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        # Écriture uniquement pour l'auteur, on controle l'auteur de l'objet
        return obj.author == request.user


class IsProjectAuthor(BasePermission):
    def has_permission(self, request, view):
        # Lecture toujours autorisée
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        # Écriture uniquement pour l'auteur du projet, on controle l'auteur du projet
        project_pk = view.kwargs.get('project_pk')
        return Project.objects.filter(pk=project_pk, author=request.user).exists()


class IsProjectContributor(BasePermission):
    def has_permission(self, request, view):
        # Lecture toujours autorisée
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        # Écriture uniquement pour les contributeurs du projet
        project_pk = view.kwargs.get('project_pk')
        return Contributor.objects.filter(project_id=project_pk, user=request.user).exists()
