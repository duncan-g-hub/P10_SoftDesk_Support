from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from accounts.models import User
from accounts.serializers import UserSerializer, PublicUserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des utilisateurs.

    Fournit les actions CRUD complètes sur le modèle User.
    Les actions de modification et de suppression sont restreintes à l'utilisateur lui-même.
    La création est ouverte à tous.

    Attributes:
        serializer_class (PublicUserSerializer): Serializer utilisé pour les listes.
        serializer_detail_class (UserSerializer): Serializer utilisé pour les vues de détail.
    """

    serializer_class = PublicUserSerializer
    serializer_detail_class = UserSerializer

    def get_queryset(self):
        """Retourne le queryset adapté à l'action en cours.

        Pour les actions de détail, modification et suppression, limite le queryset à l'utilisateur authentifié.
        Pour les autres actions, retourne l'ensemble des utilisateurs.

        Returns:
            QuerySet: Un queryset de User filtré selon l'action courante.
        """
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return User.objects.filter(id=self.request.user.id)
        return User.objects.all()

    def get_serializer_class(self):
        """Retourne la classe de serializer adaptée à l'action en cours.

        Utilise le serializer complet (UserSerializer) pour les actions de
        détail et de création, et le serializer public (PublicUserSerializer)
        pour les autres actions (liste).

        Returns:
            serializer: La classe de serializer à utiliser pour l'action courante.
        """
        if self.action in ['retrieve', 'create', 'update', 'partial_update']:
            return self.serializer_detail_class
        return self.serializer_class

    def get_permissions(self):
        """Retourne les permissions adaptées à l'action en cours.

        La création de compte est accessible sans authentification.
        Toutes les autres actions nécessitent d'être authentifié.

        Returns:
            list: Une liste d'instances de permissions à appliquer.
        """
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        """Exécute la création d'un utilisateur via le serializer.

        Args:
            serializer (UserSerializer): Le serializer validé prêt à être sauvegardé.
        """
        serializer.save()
