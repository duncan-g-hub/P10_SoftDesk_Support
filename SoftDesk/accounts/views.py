from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from accounts.models import User
from accounts.serializers import UserSerializer



class UserViewSet(viewsets.ModelViewSet):
#     mixins.CreateModelMixin,
#     mixins.RetrieveModelMixin,
#     mixins.UpdateModelMixin,
#     mixins.DestroyModelMixin,
#     viewsets.GenericViewSet
# ): # correspond au ModelViewSet avec ListModelMixin en moins pour ne pas afficher la liste de tous les utilisateurs

    serializer_class = UserSerializer

    def get_queryset(self):
        # return User.objects.filter(id=self.request.user.id)
        return User.objects.all()

    # def get_permissions(self):
    #     if self.action == 'create':
    #         return [AllowAny()]
    #     return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save()