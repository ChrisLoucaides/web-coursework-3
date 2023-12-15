from rest_framework import serializers
from .models import ArticleComment, SiteUser, Category, Article


class UserSerialiser(serializers.ModelSerializer):
    """
    A Serialiser for users
    """

    preferences = serializers.SerializerMethodField()

    def get_preferences(self, obj):
        prefs = list(Category.objects.filter(user=obj.id).values_list('name', flat=True))
        return prefs

    class Meta:
        model = SiteUser
        fields = ['id', 'first_name', 'last_name', 'profile_picture', 'username', 'preferences']


class ArticleSerialiser(serializers.ModelSerializer):
    """
    Serialises an article, ignoring comments and replacing them with a simple count
    """
    category = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    def get_category(self, obj):
        category_name = obj.category.name
        return category_name

    def get_comment_count(self, obj):
        count = obj.comment.count()
        return count

    class Meta:
        model = Article
        fields = ['id', 'title_text', 'content_text', 'category', 'comment_count']


class CommentReadSerialiser(serializers.ModelSerializer):
    """
    Serialises an ArticleComment object into json, fetching the user and all comment fields
    """
    user = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()

    def get_replies(self, obj):
        serialiser = CommentReadSerialiser(obj.replies.all(), many=True, context=self.context)
        return serialiser.data

    def get_user(self, obj):
        return UserSerialiser(instance=obj.user, read_only=True, context=self.context).data

    class Meta:
        model = ArticleComment
        fields = '__all__'


class CommentWriteSerialiser(serializers.ModelSerializer):
    """
    Serialises an ArticleComment object into json, without needing the full user object
    """

    class Meta:
        model = ArticleComment
        fields = ['comment_text', 'created_date', 'updated_date', 'parent_comment']
