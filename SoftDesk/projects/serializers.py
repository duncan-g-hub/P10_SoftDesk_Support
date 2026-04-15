from rest_framework import serializers

from projects.models import Project, Contributor
from accounts.models import User



class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class ProjectListSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format='%d/%m/%Y %H:%M', read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'name', 'type', 'created_time')


class ProjectDetailSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format='%d/%m/%Y %H:%M', read_only=True)
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'type', 'author', 'created_time')
        read_only_fields = ('author', 'created_time')



class ContributorListSerializer(serializers.ModelSerializer):
    pass

class ContributorDetailSerializer(serializers.ModelSerializer):
    pass
