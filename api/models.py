from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


class SiteUser(AbstractUser):
    profile_picture = models.ImageField()
    date_of_birth = models.DateField()

    REQUIRED_FIELDS = ['profile_picture', 'date_of_birth']


class ArticleComment(models.Model):
    """
    A model representing a comment a user can make under an article
    """

    article_id = models.IntegerField()  # TODO: Replace with relationship to Article model
    user = models.ForeignKey(to=SiteUser, related_name='comments', on_delete=models.CASCADE)
    comment_text = models.TextField()
    created_date = models.DateField()
    updated_date = models.DateField(null=True, blank=True)
    parent_comment = models.ForeignKey('ArticleComment', related_name='replies', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id:} "{self.comment_text}" (on: {self.article_id}, by: {self.user.id})'

