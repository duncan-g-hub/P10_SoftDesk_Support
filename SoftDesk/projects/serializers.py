from rest_framework import serializers

from projects.models import Project, Contributor

from SoftDesk.accounts.serializers import UserSerializer


class ProjectListSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format='%d/%m/%Y %H:%M')

    class Meta:
        model = Project
        fields = ('id', 'name', 'type', 'created_time')
        read_only_fields = ('author', 'created_time')

class ProjectDetailSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format='%d/%m/%Y %H:%M')
    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'type', 'author', 'created_time')
        read_only_fields = ('author', 'created_time')



class ContributorListSerializer(serializers.ModelSerializer):
    pass

class ContributorDetailSerializer(serializers.ModelSerializer):
    pass
