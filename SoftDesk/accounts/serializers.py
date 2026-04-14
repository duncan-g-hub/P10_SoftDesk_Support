from rest_framework import serializers

from accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    birth_date = serializers.DateTimeField(format='%d/%m/%Y %H:%M')
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'birth_date', 'can_be_contacted', 'can_data_be_shared')

    def validate(self, data):
        # birth_date obligatoire
        if not data.get('birth_date'):
            raise serializers.ValidationError({"birth_date": "Ce champ est obligatoire."})
        return data