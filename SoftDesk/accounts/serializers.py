from rest_framework import serializers
from datetime import date

from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer complet pour le modèle User.

    Gère la création, la mise à jour et la validation des utilisateurs,
    notamment le hachage du mot de passe et le contrôle de l'âge minimum.

    Attributes:
        birth_date (DateField): Date de naissance au format JJ/MM/AAAA.
        password (CharField): Mot de passe en écriture seule.
        created_time (DateTimeField): Date de création en lecture seule au format JJ/MM/AAAA HH:MM.
    """

    birth_date = serializers.DateField(format='%d/%m/%Y', input_formats=['%d/%m/%Y'])
    password = serializers.CharField(write_only=True)
    created_time = serializers.DateTimeField(format='%d/%m/%Y %H:%M', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'birth_date', 'can_be_contacted', 'can_data_be_shared', 'created_time')

    def validate(self, data):
        """Valide les données de l'utilisateur.

        Vérifie que la date de naissance est fournie lors d'une création, et que l'utilisateur a au moins 15 ans.

        Args:
            data (dict): Dictionnaire des données désérialisées à valider.

        Returns:
            dict: Les données validées si toutes les conditions sont remplies.

        Raises:
            serializers.ValidationError: Si la date de naissance est absente, ou si l'utilisateur a moins de 15 ans.
        """
        if not self.partial and not data.get('birth_date'):
            raise serializers.ValidationError({"birth_date": "Ce champ est obligatoire."})

        if not self.control_age(data.get('birth_date')):
            raise serializers.ValidationError(
                {"birth_date": "Vous devez avoir au moins 15 ans pour vous inscrire."})
        return data

    def control_age(self, birth_date):
        """Vérifie que l'utilisateur a au moins 15 ans.

        Args:
            birth_date (datetime.date | None): La date de naissance à contrôler.

        Returns:
            bool: True si l'utilisateur a 15 ans ou plus, ou si aucune date
                n'est fournie. False si l'utilisateur a moins de 15 ans.
        """
        if birth_date:
            date_now = date.today()
            age = date_now.year - birth_date.year - (
                    (date_now.month, date_now.day) < (birth_date.month, birth_date.day))
            if age < 15:
                return False
        return True

    def create(self, validated_data):
        """Crée un nouvel utilisateur avec un mot de passe haché.

        Args:
            validated_data (dict): Données issues de la validation du serializer.

        Returns:
            User: L'instance utilisateur créée.
        """
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        """Met à jour un utilisateur existant.

        Si un mot de passe est fourni, il est haché avant d'être enregistré.
        Les autres champs sont mis à jour via ModelSerializer.update().

        Args:
            instance (User): L'instance utilisateur à mettre à jour.
            validated_data (dict): Données validées issues de la désérialisation.

        Returns:
            User: L'instance utilisateur mise à jour.
        """
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)


class PublicUserSerializer(serializers.ModelSerializer):
    """Serializer public pour le modèle User.

    Expose uniquement les informations non sensibles d'un utilisateur,
    destiné aux listes et aux vues accessibles à tous les utilisateurs authentifiés.
    """

    class Meta:
        model = User
        fields = ('id', 'username',)
        read_only_fields = ('id', 'username',)
