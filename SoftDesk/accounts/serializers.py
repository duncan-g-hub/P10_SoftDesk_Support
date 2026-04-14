from rest_framework.serializers import ModelSerializer

from accounts.models import User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'birth_date', 'can_be_contacted', 'can_data_be_shared')