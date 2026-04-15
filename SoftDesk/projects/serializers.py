from rest_framework import serializers

from projects.models import Project, Contributor
from accounts.models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class ProjectNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name')


class ContributorSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format='%d/%m/%Y %H:%M', read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Contributor
        fields = ('id', 'user', 'created_time')
        read_only_fields = ('created_time', 'user')



class ProjectListSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format='%d/%m/%Y %H:%M', read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'name', 'type', 'created_time')


class ProjectDetailSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format='%d/%m/%Y %H:%M', read_only=True)
    author = UserSerializer(read_only=True)
    contributors = ContributorSerializer(many=True, read_only=True)
    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'type', 'author', 'created_time', 'contributors')
        read_only_fields = ('author', 'created_time', 'contributors')






