from rest_framework import serializers

from projects.models import Project, Contributor, Issue, Comment
from accounts.models import User



class UserSerializer(serializers.ModelSerializer):
    # serializer qui permet de gerer l'affichage d'un user
    class Meta:
        model = User
        fields = ('id', 'username')






class ContributorSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format='%d/%m/%Y %H:%M', read_only=True)
    user_detail = UserSerializer(source='user', read_only=True) # lecture : affiche id + username
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True) # écriture : attend un id

    class Meta:
        model = Contributor
        fields = ('id', 'user', 'user_detail', 'created_time')
        read_only_fields = ('created_time', 'user_detail')




class IssueListSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format='%d/%m/%Y %H:%M', read_only=True)

    class Meta:
        model = Issue
        fields = ('id', 'name', 'priority', 'tag', 'status', 'created_time')



class IssueDetailSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format='%d/%m/%Y %H:%M', read_only=True)
    author = UserSerializer(read_only=True)
    assigned_to_contributor = ContributorSerializer(source='assigned_to', read_only=True) # lecture : affiche id + username
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=Contributor.objects.all(), write_only=True) # écriture : attend un id

    def get_fields(self):
        # permet de filtrer le champs assigned_to pour ne retourner que les contributeurs du projet
        fields = super().get_fields()
        view = self.context.get('view')
        if view:
            project_pk = view.kwargs.get('project_pk')
            if project_pk:
                fields['assigned_to'].queryset = Contributor.objects.filter(project_id=project_pk)
        return fields

    class Meta:
        model = Issue
        fields = ('id', 'name', 'description', 'priority', 'tag', 'status', 'created_time', 'author', 'assigned_to', 'assigned_to_contributor')






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
        fields = ('id', 'name', 'description', 'type', 'created_time', 'author',  'contributors', 'issues')
        read_only_fields = ('author', 'created_time', 'contributors', 'issues')



