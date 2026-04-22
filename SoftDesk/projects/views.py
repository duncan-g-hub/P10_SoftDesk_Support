from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from projects.permissions import IsAuthorOrReadOnly, IsProjectAuthor, IsProjectContributor
from projects.models import Project, Contributor, Issue, Comment
from projects.serializers import (ProjectListSerializer, ProjectDetailSerializer,
                                  ContributorSerializer,
                                  IssueListSerializer, IssueDetailSerializer,
                                  CommentSerializer)


class ProjectViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des projets.

    Un utilisateur ne peut voir et interagir qu'avec les projets dont il est contributeur.
    À la création, l'auteur est automatiquement enregistré comme contributeur du projet.

    Attributes:
        serializer_class (ProjectListSerializer): Serializer utilisé pour la liste.
        serializer_detail_class (ProjectDetailSerializer): Serializer utilisé pour le détail.
        permission_classes (list): Authentification requise. L'accès est limité aux contributeurs du projet,
            seul l'auteur peut modifier ou supprimer.
    """

    serializer_class = ProjectListSerializer
    serializer_detail_class = ProjectDetailSerializer
    permission_classes = [IsAuthenticated, IsProjectContributor, IsAuthorOrReadOnly]

    def get_queryset(self):
        """Retourne les projets dont l'utilisateur authentifié est contributeur.

        Returns:
            QuerySet: Les projets liés à l'utilisateur via la relation Contributor.
        """
        return Project.objects.filter(contributors__user=self.request.user)

    def get_serializer_class(self):
        """Retourne la classe de serializer adaptée à l'action en cours.

        Utilise le serializer complet pour les actions de détail et d'écriture, et le serializer allégé pour la liste.

        Returns:
            serializer: La classe de serializer à utiliser pour l'action courante.
        """
        if self.action in ['retrieve', 'create', 'update', 'partial_update']:
            return self.serializer_detail_class
        return super().get_serializer_class()

    def perform_create(self, serializer):
        """Crée un projet et ajoute automatiquement son auteur comme contributeur.

        L'utilisateur authentifié est enregistré comme auteur du projet,
        puis une entrée Contributor est créée pour lui sur ce même projet.

        Args:
            serializer (ProjectDetailSerializer): Le serializer validé prêt à être sauvegardé.
        """
        project = serializer.save(author=self.request.user)
        Contributor.objects.create(user=self.request.user, project=project)


class ContributorViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des contributeurs d'un projet.

    Limité aux contributeurs du projet identifié par project_pk dans l'URL.
    Seul l'auteur du projet peut ajouter ou retirer des contributeurs.

    Attributes:
        serializer_class (ContributorSerializer): Serializer utilisé pour toutes les actions.
        permission_classes (list): Authentification requise. L'accès est limité
            aux contributeurs du projet, seul l'auteur peut modifier la liste.

    Note:
        project_pk est extrait automatiquement par drf-nested-routers et placé
        dans self.kwargs, au même titre que pk pour l'identifiant du contributeur.
    """

    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, IsProjectContributor, IsProjectAuthor]

    def get_queryset(self):
        """Retourne les contributeurs du projet courant.

        Returns:
            QuerySet: Les contributeurs filtrés par project_pk extrait de l'URL.
        """
        return Contributor.objects.filter(project_id=self.kwargs['project_pk'])

    def perform_create(self, serializer):
        """Crée un contributeur en l'associant au projet courant.

        Le projet est récupéré depuis project_pk dans l'URL et injecté automatiquement lors de la sauvegarde.

        Args:
            serializer (ContributorSerializer): Le serializer validé prêt à être sauvegardé.
        """
        project = Project.objects.get(pk=self.kwargs['project_pk'])
        serializer.save(project=project)


class IssueViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des issues d'un projet.

    Limité aux issues du projet identifié par project_pk dans l'URL.
    L'auteur est automatiquement injecté à la création. Seul l'auteur d'une issue peut la modifier ou la supprimer.

    Attributes:
        serializer_class (IssueListSerializer): Serializer utilisé pour la liste.
        serializer_detail_class (IssueDetailSerializer): Serializer utilisé pour le détail.
        permission_classes (list): Authentification requise. L'accès est limité
            aux contributeurs du projet, seul l'auteur peut modifier ou supprimer.
    """

    serializer_class = IssueListSerializer
    serializer_detail_class = IssueDetailSerializer
    permission_classes = [IsAuthenticated, IsProjectContributor, IsAuthorOrReadOnly]

    def get_queryset(self):
        """Retourne les issues du projet courant.

        Returns:
            QuerySet: Les issues filtrées par project_pk extrait de l'URL.
        """
        return Issue.objects.filter(project_id=self.kwargs['project_pk'])

    def get_serializer_class(self):
        """Retourne la classe de serializer adaptée à l'action en cours.

        Utilise le serializer complet pour les actions de détail et d'écriture, et le serializer allégé pour la liste.

        Returns:
            serializer: La classe de serializer à utiliser pour l'action courante.
        """
        if self.action in ['retrieve', 'create', 'update', 'partial_update']:
            return self.serializer_detail_class
        return super().get_serializer_class()

    def perform_create(self, serializer):
        """Crée une issue en l'associant au projet courant et à son auteur.

        Le projet est récupéré depuis project_pk dans l'URL.
        L'utilisateur authentifié est automatiquement enregistré comme auteur de l'issue.

        Args:
            serializer (IssueDetailSerializer): Le serializer validé prêt à être sauvegardé.
        """
        project = Project.objects.get(pk=self.kwargs['project_pk'])
        serializer.save(author=self.request.user, project=project)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des commentaires d'une issue.

    Limité aux commentaires de l'issue identifiée par issue_pk dans l'URL.
    L'auteur est automatiquement injecté à la création.
    Seul l'auteur d'un commentaire peut le modifier ou le supprimer.

    Attributes:
        serializer_class (CommentSerializer): Serializer utilisé pour toutes les actions.
        permission_classes (list): Authentification requise. L'accès est limité
            aux contributeurs du projet, seul l'auteur peut modifier ou supprimer.
    """

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsProjectContributor, IsAuthorOrReadOnly]

    def get_queryset(self):
        """Retourne les commentaires de l'issue courante.

        Returns:
            QuerySet: Les commentaires filtrés par issue_pk extrait de l'URL.
        """
        return Comment.objects.filter(issue_id=self.kwargs['issue_pk'])

    def perform_create(self, serializer):
        """Crée un commentaire en l'associant à l'issue courante et à son auteur.

        L'issue est récupérée depuis issue_pk dans l'URL.
        L'utilisateur authentifié est automatiquement enregistré comme auteur du commentaire.

        Args:
            serializer (CommentSerializer): Le serializer validé prêt à être sauvegardé.
        """
        issue = Issue.objects.get(pk=self.kwargs['issue_pk'])
        serializer.save(author=self.request.user, issue=issue)
