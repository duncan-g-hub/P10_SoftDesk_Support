from rest_framework import serializers

from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    birth_date = serializers.DateField(format='%d/%m/%Y')
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'birth_date', 'can_be_contacted', 'can_data_be_shared')

    def validate(self, data):
        # birth_date obligatoire
        if not data.get('birth_date'):
            raise serializers.ValidationError({"birth_date": "Ce champ est obligatoire."})
        return data

    def create(self, validated_data):
        # créer l'utilisateur en hachant le mdp
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        # si le password est modifié, on le hache
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        # mise à jour des autres champs
        return super().update(instance, validated_data)