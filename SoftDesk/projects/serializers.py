from rest_framework import serializers

from projects.models import Project, Contributor, Issue, Comment
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer pour l'affichage public d'un utilisateur.

    Expose uniquement l'identifiant et le nom d'utilisateur.
    Utilisé en lecture seule comme champ imbriqué dans d'autres serializers.
    """

    class Meta:
        model = User
        fields = ('id', 'username')


class ContributorSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Contributor.

    Gère deux représentations du champ user selon le sens de la requête :
    en lecture, un objet imbriqué avec id et username ; en écriture, un simple id.

    Attributes:
        created_time (DateTimeField): Date d'ajout du contributeur au format JJ/MM/AAAA HH:MM, en lecture seule.
        user_detail (UserSerializer): Représentation imbriquée de l'utilisateur, en lecture seule.
        user (PrimaryKeyRelatedField): Identifiant de l'utilisateur attendu en écriture.
    """

    created_time = serializers.DateTimeField(format='%d/%m/%Y %H:%M', read_only=True)
    user_detail = UserSerializer(source='user', read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)

    class Meta:
        model = Contributor
        fields = ('id', 'user', 'user_detail', 'created_time')
        read_only_fields = ('created_time', 'user_detail')


class CommentSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Comment.

    L'auteur est automatiquement injecté par la vue. L'UUID est généré automatiquement et non modifiable.

    Attributes:
        created_time (DateTimeField): Date de création au format JJ/MM/AAAA HH:MM, en lecture seule.
        author (UserSerializer): Représentation imbriquée de l'auteur, en lecture seule.
    """

    created_time = serializers.DateTimeField(format='%d/%m/%Y %H:%M', read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'uuid', 'description', 'created_time', 'author')
        read_only_fields = ('created_time', 'author', 'uuid')


class IssueListSerializer(serializers.ModelSerializer):
    """Serializer allégé pour l'affichage d'une issue en liste.

    Expose uniquement les champs utiles à une vue d'ensemble, sans les détails comme la description,
    l'auteur ou les commentaires.

    Attributes:
        created_time (DateTimeField): Date de création au format JJ/MM/AAAA HH:MM, en lecture seule.
    """

    created_time = serializers.DateTimeField(format='%d/%m/%Y %H:%M', read_only=True)

    class Meta:
        model = Issue
        fields = ('id', 'name', 'priority', 'tag', 'status', 'created_time')


class IssueDetailSerializer(serializers.ModelSerializer):
    """Serializer complet pour l'affichage et la modification d'une issue.

    Gère deux représentations du champ assigned_to selon le sens de la requête :
    en lecture, un objet contributeur imbriqué ; en écriture, un simple id.
    Le queryset de assigned_to est filtré dynamiquement pour ne proposer que les contributeurs du projet courant.

    Attributes:
        created_time (DateTimeField): Date de création au format JJ/MM/AAAA HH:MM, en lecture seule.
        author (UserSerializer): Représentation imbriquée de l'auteur, en lecture seule.
        assigned_to_contributor (ContributorSerializer): Représentation imbriquée du contributeur assigné,
            en lecture seule.
        assigned_to (PrimaryKeyRelatedField): Identifiant du contributeur attendu en écriture, optionnel.
        comments (CommentSerializer): Liste des commentaires de l'issue, en lecture seule.
    """

    created_time = serializers.DateTimeField(format='%d/%m/%Y %H:%M', read_only=True)
    author = UserSerializer(read_only=True)
    assigned_to_contributor = ContributorSerializer(source='assigned_to',
                                                    read_only=True)
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=Contributor.objects.all(),
                                                     write_only=True,
                                                     required=False,
                                                     allow_null=True
                                                     )
    comments = CommentSerializer(many=True, read_only=True)

    def get_fields(self):
        """Retourne les champs du serializer en filtrant le queryset de assigned_to.

        Surcharge get_fields() pour restreindre les contributeurs assignables
        à ceux qui appartiennent au projet courant, récupéré depuis les kwargs de la vue via le contexte DRF.

        Returns:
            dict: Dictionnaire des champs du serializer, avec le queryset de
                assigned_to filtré par project_pk si disponible dans le contexte.
        """

        fields = super().get_fields()
        view = self.context.get('view')
        if view:
            project_pk = view.kwargs.get('project_pk')
            if project_pk:
                fields['assigned_to'].queryset = Contributor.objects.filter(project_id=project_pk)
        return fields

    class Meta:
        model = Issue
        fields = ('id', 'name', 'description', 'priority', 'tag', 'status', 'created_time', 'author', 'assigned_to',
                  'assigned_to_contributor', 'comments')


class ProjectListSerializer(serializers.ModelSerializer):
    """Serializer allégé pour l'affichage d'un projet en liste.

    Expose uniquement les champs utiles à une vue d'ensemble, sans les détails comme la description,
    les contributeurs ou les issues.

    Attributes:
        created_time (DateTimeField): Date de création au format JJ/MM/AAAA HH:MM, en lecture seule.
    """

    created_time = serializers.DateTimeField(format='%d/%m/%Y %H:%M', read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'name', 'type', 'created_time')


class ProjectDetailSerializer(serializers.ModelSerializer):
    """Serializer complet pour l'affichage et la modification d'un projet.

    Expose l'ensemble des informations d'un projet, incluant l'auteur, la liste des contributeurs et
    la liste allégée des issues associées.
    Tous les champs relationnels sont en lecture seule.

    Attributes:
        created_time (DateTimeField): Date de création au format JJ/MM/AAAA HH:MM, en lecture seule.
        author (UserSerializer): Représentation imbriquée de l'auteur du projet, en lecture seule.
        contributors (ContributorSerializer): Liste des contributeurs du projet, en lecture seule.
        issues (IssueListSerializer): Liste allégée des issues du projet, en lecture seule.
    """

    created_time = serializers.DateTimeField(format='%d/%m/%Y %H:%M', read_only=True)
    author = UserSerializer(read_only=True)
    contributors = ContributorSerializer(many=True, read_only=True)
    issues = IssueListSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'type', 'created_time', 'author', 'contributors', 'issues')
        read_only_fields = ('author', 'created_time', 'contributors', 'issues')
