from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


class Category(models.Model):
    name = models.TextField(max_length=255)

    def __str__(self):
        return self.name


class SiteUser(AbstractUser):
    profile_picture = models.ImageField()
    date_of_birth = models.DateField()
    category = models.ManyToManyField(Category, related_name='user')
    REQUIRED_FIELDS = ['email', 'profile_picture', 'date_of_birth']


class Article(models.Model):
    """
    A model representing a single article
    """
    title_text = models.TextField()
    content_text = models.TextField()
    category = models.ForeignKey(to=Category, related_name='articles', null=True, blank=False, on_delete=models.CASCADE)


class ArticleComment(models.Model):
    """
    A model representing a comment a user can make under an article
    """

    article_id = models.ForeignKey(Article, related_name='comment', null=False, blank=False, on_delete=models.CASCADE)
    user = models.ForeignKey(to=SiteUser, related_name='comments', on_delete=models.CASCADE)
    comment_text = models.TextField()
    created_date = models.DateTimeField()
    updated_date = models.DateTimeField(null=True, blank=True)
    parent_comment = models.ForeignKey('ArticleComment', related_name='replies', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id:} "{self.comment_text}" (on: {self.article_id}, by: {self.user.id})'
