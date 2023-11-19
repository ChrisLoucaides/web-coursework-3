from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import ArticleComment
from .serialisers import CommentReadSerialiser, CommentWriteSerialiser
from rest_framework import status


def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})


class CommentsViewSet(ModelViewSet):
    """
    A ViewSet for operations related to article comments
    """

    queryset = ArticleComment.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CommentReadSerialiser
        else:
            return CommentWriteSerialiser

    def get_queryset(self):
        article_id = self.kwargs['article_id']
        if 'pk' in self.kwargs:
            return ArticleComment.objects.filter(article_id=article_id)
        else:
            return ArticleComment.objects.filter(article_id=article_id, parent_comment=None)

    def list(self, request, *args, **kwargs):
        """
        Returns all comments for a given requested article id
        """
        serialiser = self.get_serializer(self.get_queryset(), many=True)
        return Response(serialiser.data)

    def create(self, request, *args, **kwargs):
        """
        Posts a new comment on a requested article id
        """
        serialiser = self.get_serializer(data=request.data)
        serialiser.is_valid(raise_exception=True)
        serialiser.save()

        return Response(serialiser.data, status=status.HTTP_201_CREATED)

