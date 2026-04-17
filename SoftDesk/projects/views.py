from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from projects.models import Project, Contributor, Issue, Comment
from projects.serializers import (ProjectListSerializer, ProjectDetailSerializer,
                                  ContributorSerializer,
                                  IssueListSerializer, IssueDetailSerializer,
                                  CommentSerializer)


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectListSerializer
    serializer_detail_class = ProjectDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.all()

    def get_serializer_class(self):
        # on utilise le serializer de detail si on veut modifier ou ajouter un projet
        if self.action in ['retrieve', 'create', 'update', 'partial_update']:
            return self.serializer_detail_class
        return super().get_serializer_class()

    def perform_create(self, serializer):
        project = serializer.save(author=self.request.user)
        Contributor.objects.create(user=self.request.user, project=project)


class ContributorViewSet(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Contributor.objects.filter(project_id=self.kwargs['project_pk'])

    def perform_create(self, serializer):
        project = Project.objects.get(pk=self.kwargs['project_pk'])
        serializer.save(project=project)

    # project_pk est extrait par drf-nested-routers et placé dans self.kwargs
    # self.kwargs = {
    #     'project_pk': '1',  # extrait par drf-nested-routers
    #     'pk': '3'           # extrait par DRF (id du contributeur)
    # }
    # C'est le même principe que self.request qui donne accès à la requête,
    # ou self.action qui donne l'action en cours (list, retrieve, etc.)


class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueListSerializer
    serializer_detail_class = IssueDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Issue.objects.filter(project_id=self.kwargs['project_pk'])

    def get_serializer_class(self):
        if self.action in ['retrieve', 'create', 'update', 'partial_update']:
            return self.serializer_detail_class
        return super().get_serializer_class()

    def perform_create(self, serializer):
        project = Project.objects.get(pk=self.kwargs['project_pk'])
        serializer.save(author=self.request.user, project=project)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(issue_id=self.kwargs['issue_pk'])

    def perform_create(self, serializer):
        issue = Issue.objects.get(pk=self.kwargs['issue_pk'])
        serializer.save(author=self.request.user, issue=issue)
