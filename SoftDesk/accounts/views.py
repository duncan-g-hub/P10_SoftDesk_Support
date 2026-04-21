from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from accounts.models import User
from accounts.serializers import UserSerializer, PublicUserSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = PublicUserSerializer
    serializer_detail_class = UserSerializer

    def get_queryset(self):
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return User.objects.filter(id=self.request.user.id)
        return User.objects.all()

    def get_serializer_class(self):
        if self.action in ['retrieve', 'create', 'update', 'partial_update']:
            return self.serializer_detail_class
        return self.serializer_class

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save()
