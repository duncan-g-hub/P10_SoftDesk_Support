from rest_framework import serializers
from datetime import date

from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    birth_date = serializers.DateField(format='%d/%m/%Y', input_formats=['%d/%m/%Y'])
    password = serializers.CharField(write_only=True)
    created_time = serializers.DateTimeField(format='%d/%m/%Y %H:%M', read_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'birth_date', 'can_be_contacted', 'can_data_be_shared', 'created_time')

    def validate(self, data):
        # birth_date obligatoire
        if not self.partial and not data.get('birth_date'):
            raise serializers.ValidationError({"birth_date": "Ce champ est obligatoire."})

        if not self.control_age(data.get('birth_date')):
            raise serializers.ValidationError(
                {"birth_date": "Vous devez avoir au moins 15 ans pour vous inscrire."})
        return data


    def control_age(self, birth_date):
        # gestion age minimum
        if birth_date:
            date_now = date.today()
            age = date_now.year - birth_date.year - (
                    (date_now.month, date_now.day) < (birth_date.month, birth_date.day))
            if age < 15:
                return False
        return True

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


class PublicUserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('id', 'username',)
            read_only_fields = ('id', 'username',)
