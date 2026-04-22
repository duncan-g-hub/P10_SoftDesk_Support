from rest_framework.permissions import BasePermission

from projects.models import Project, Contributor


class IsAuthorOrReadOnly(BasePermission):
    """Permission accordant l'écriture uniquement à l'auteur de l'objet.

    Les requêtes en lecture seule (GET, HEAD, OPTIONS) sont toujours autorisées.
    Les requêtes d'écriture (POST, PUT, PATCH, DELETE) sont réservées à
    l'utilisateur authentifié qui est l'auteur de l'objet ciblé.
    """

    def has_object_permission(self, request, view, obj):
        """Vérifie si l'utilisateur est autorisé à agir sur l'objet.

        Args:
            request (Request): La requête HTTP entrante.
            view (View): La vue traitant la requête.
            obj (Model): L'instance du modèle sur laquelle la permission est vérifiée.

        Returns:
            bool: True si la méthode est en lecture seule ou si l'utilisateur est l'auteur de l'objet. False sinon.
        """
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return obj.author == request.user


class IsProjectAuthor(BasePermission):
    """Permission accordant l'écriture uniquement à l'auteur du projet parent.

    Utilisée sur les ressources imbriquées (ex: contributeurs) pour restreindre
    les modifications au seul auteur du projet, identifié via project_pk dans l'URL.
    Les requêtes en lecture seule sont toujours autorisées.
    """

    def has_permission(self, request, view):
        """Vérifie si l'utilisateur est l'auteur du projet courant.

        Args:
            request (Request): La requête HTTP entrante.
            view (View): La vue traitant la requête, dont les kwargs contiennent project_pk.

        Returns:
            bool: True si la méthode est en lecture seule ou si l'utilisateur
                est l'auteur du projet identifié par project_pk. False sinon.
        """
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        project_pk = view.kwargs.get('project_pk')
        return Project.objects.filter(pk=project_pk, author=request.user).exists()


class IsProjectContributor(BasePermission):
    """Permission limitant l'accès aux contributeurs du projet courant.

    Sur les routes sans project_pk (liste et création de projets), l'accès est toujours accordé.
    Sur les routes imbriquées sous un projet, seuls les contributeurs de ce projet peuvent accéder à la ressource.
    """

    def has_permission(self, request, view):
        """Vérifie si l'utilisateur est contributeur du projet courant.

        Si aucun project_pk n'est présent dans l'URL,
        la permission est accordée sans vérification (cas des routes /projects/).
        Dans le cas contraire, l'utilisateur doit être contributeur du projet identifié par project_pk.

        Args:
            request (Request): La requête HTTP entrante.
            view (View): La vue traitant la requête, dont les kwargs peuvent contenir project_pk.

        Returns:
            bool: True si aucun project_pk n'est présent dans l'URL, ou si l'utilisateur est contributeur du projet.
                False sinon.
        """
        project_pk = view.kwargs.get('project_pk')
        if not project_pk:
            return True
        return Contributor.objects.filter(project_id=project_pk, user=request.user).exists()
