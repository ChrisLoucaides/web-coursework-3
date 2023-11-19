from rest_framework import serializers
from .models import ArticleComment, SiteUser


class CommentUserSerialiser(serializers.ModelSerializer):
    """
    A Serialiser for users that are NOT the current user, so does not serialise private data
    """
    class Meta:
        model = SiteUser
        fields = ['first_name', 'last_name', 'profile_picture', 'username']


class CommentReadSerialiser(serializers.ModelSerializer):
    """
    Serialises an ArticleComment object into json, fetching the user and all comment fields
    """
    user = CommentUserSerialiser(read_only=True)
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