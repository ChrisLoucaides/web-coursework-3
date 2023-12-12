from rest_framework import serializers
from .models import ArticleComment, SiteUser, Category


class UserSerialiser(serializers.ModelSerializer):
    """
    A Serialiser for users
    """

    preferences = serializers.SerializerMethodField()

    def get_preferences(self, obj):
        prefs = list(Category.objects.filter(user=obj.id).values_list('name', flat=True))
        print(prefs)
        return prefs

    class Meta:
        model = SiteUser
        fields = ['first_name', 'last_name', 'profile_picture', 'username', 'preferences']


class CommentReadSerialiser(serializers.ModelSerializer):
    """
    Serialises an ArticleComment object into json, fetching the user and all comment fields
    """
    user = UserSerialiser(read_only=True)
    replies = serializers.SerializerMethodField()

    def get_replies(self, obj):
        serialiser = CommentReadSerialiser(obj.replies.all(), many=True)
        return serialiser.data

    class Meta:
        model = ArticleComment
        fields = '__all__'


class CommentWriteSerialiser(serializers.ModelSerializer):
    """
    Serialises an ArticleComment object into json, without needing the full user object
    """

    class Meta:
        model = ArticleComment
        fields = '__all__'