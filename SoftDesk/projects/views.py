from rest_framework import viewsets

from projects.models import Project, Contributor
from projects.serializers import (ProjectListSerializer, ProjectDetailSerializer,
                                  ContributorSerializer)


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectListSerializer
    serializer_detail_class = ProjectDetailSerializer

    def get_queryset(self):
        return Project.objects.all()

    def get_serializer_class(self):
        # on utilise le serilizer de detail si on veut modifier ou ajouter un projet
        if self.action in ['retrieve', 'create', 'update', 'partial_update']:
            return self.serializer_detail_class
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, contributor=self.request.user)



class ContributorViewSet(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer

    def get_queryset(self):
        return Contributor.objects.filter(project_id=self.kwargs['project_pk'])

    def perform_create(self, serializer):
        project = Project.objects.get(pk=self.kwargs['project_pk'])
        serializer.save(project=project)
