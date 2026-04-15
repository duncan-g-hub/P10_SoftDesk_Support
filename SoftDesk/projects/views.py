from rest_framework import viewsets

from projects.models import Project, Contributor
from projects.serializers import (ProjectListSerializer, ProjectDetailSerializer,
                                  ContributorListSerializer, ContributorDetailSerializer)



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
        serializer.save(author=self.request.user)





class ContributorViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectListSerializer
    serializer_detail_class = ProjectDetailSerializer