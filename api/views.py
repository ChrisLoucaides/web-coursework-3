import datetime

from django.contrib.auth import login, authenticate
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import auth
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from .forms import SignupForm, LoginForm
from .models import ArticleComment, Article, SiteUser, Category
from .serialisers import CommentReadSerialiser, CommentWriteSerialiser, UserSerialiser, ArticleSerialiser
from typing import Union


def check_auth_status(request) -> JsonResponse:
    """
    Checks if the user is authenticated
    """
    return JsonResponse({'is_authenticated': True})


def user_login(request: WSGIRequest) -> Union[HttpResponseRedirect, HttpResponse]:
    """
    Logs the user in
    """
    form: LoginForm = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username: str = request.POST.get('username')
            password: str = request.POST.get('password')
            authenticated_user: AbstractBaseUser = authenticate(request, username=username, password=password)

            if authenticated_user is not None:
                auth.login(request, authenticated_user)
                response: HttpResponseRedirect = HttpResponseRedirect('http://127.0.0.1:5173/')
                response.set_cookie('user_id', str(authenticated_user.id))

                return response

    return render(request, 'login.html', {'form': form})


def user_signup(request: WSGIRequest) -> Union[HttpResponseRedirect, HttpResponse]:
    """
    Allows a user to sign up to the site
    """
    if request.method == 'POST':
        form: SignupForm = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user: SiteUser = form.save()
            login(request, user)
            return redirect('login')
    else:
        form: SignupForm = SignupForm()
    return render(request, 'signup.html', {'form': form})


def user_logout(request: WSGIRequest) -> HttpResponseRedirect:
    """
    Logs the user out
    """
    auth.logout(request)
    return redirect("")


class UserViewSet(mixins.CreateModelMixin, GenericViewSet):
    """
    A ViewSet for operations related to users
    """
    parser_classes: list = [JSONParser, MultiPartParser, FormParser]

    queryset: QuerySet = SiteUser.objects.all()

    def get_serializer_class(self) -> UserSerialiser.__class__:
        """
        Returns the user serialiser when requested
        """
        return UserSerialiser

    @action(detail=False)
    def current(self, request: HttpRequest, *args, **kwarg) -> Response:
        """
        Returns the current user based on the requester's cookies
        """
        cookie: str = request.COOKIES.get('user_id')
        serialiser = self.get_serializer(SiteUser.objects.get(id=cookie), many=False)

        return Response(serialiser.data)

    @action(detail=False, methods=['PATCH'])
    def update_user(self, request, *args, **kwargs) -> Response:
        """
        Updates the preference details of the current user
        """
        cookie: str = request.COOKIES.get('user_id')
        user: SiteUser = SiteUser.objects.get(id=cookie)

        new_data: dict = request.data

        user.category.set(Category.objects.filter(name__in=new_data['preferences']))

        fields_to_update: list[str] = ['email', 'date_of_birth']

        for field in fields_to_update:
            if field in new_data and new_data[field] != '':
                setattr(user, field, new_data[field])

        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']

        user.save()

        return Response('User details updated', status=status.HTTP_200_OK)

    @action(detail=False, methods=['PUT'])
    def update_profile_picture(self, request: WSGIRequest, *args, **kwargs) -> Response:
        cookie: str = request.COOKIES.get('user_id')
        user = SiteUser.objects.get(id=cookie)

        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']
            user.save()

        return Response('Profile picture updated', status=status.HTTP_200_OK)


class ArticleViewSet(ModelViewSet):
    """
    A ViewSet for operations related to articles
    """
    queryset: QuerySet = Article.objects.all()

    def get_serializer_class(self) -> ArticleSerialiser.__class__:
        """
        Returns the article serialiser
        """
        return ArticleSerialiser

    def list(self, request, *args, **kwargs) -> Response:
        """
        Returns all comments for a given requested article id
        """
        cookie: str = request.COOKIES.get('user_id')
        user: SiteUser = SiteUser.objects.get(id=cookie)
        categories: QuerySet = user.category.values_list('name', flat=True)

        serialiser: ModelSerializer = self.get_serializer(Article.objects.filter(category__name__in=categories),
                                                          many=True)
        return Response(serialiser.data)


class CommentsViewSet(mixins.CreateModelMixin, GenericViewSet):
    """
    A ViewSet for operations related to article comments
    """

    queryset: QuerySet = ArticleComment.objects.all()

    def get_serializer_class(self) -> Union[CommentReadSerialiser.__class__, CommentWriteSerialiser.__class__]:
        """
        Returns the appropriate Comment serialiser
        """
        if self.action in ['list', 'retrieve']:
            return CommentReadSerialiser
        else:
            return CommentWriteSerialiser

    def get_queryset(self) -> QuerySet:
        """
        Returns all comments for a specific article
        """
        article_id: int = self.kwargs.get('article_id')
        if 'pk' in self.kwargs:
            return ArticleComment.objects.filter(article_id=article_id)
        else:
            return ArticleComment.objects.filter(article_id=article_id, parent_comment=None)

    def list(self, request, *args, **kwargs) -> Response:
        """
        Returns all comments for a given requested article id
        """
        serialiser: ModelSerializer = self.get_serializer(self.get_queryset().order_by('-created_date'), many=True,
                                                          context={"request": request})
        return Response(serialiser.data)

    def create(self, request, *args, **kwargs) -> Union[HttpResponse, Response]:
        """
        Posts a new comment on a requested article id
        """
        article: Article = Article.objects.get(id=self.kwargs['article_id'])
        if article is None:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

        user: SiteUser = SiteUser.objects.get(id=request.COOKIES.get('user_id'))
        serialiser: ModelSerializer = self.get_serializer(data=request.data)

        serialiser.is_valid(raise_exception=True)
        comment = serialiser.validated_data  # TODO: What type is this?
        comment['article_id'] = article
        comment['user'] = user
        article_comment: ArticleComment = ArticleComment(**comment)
        article_comment.save()

        return_serialiser: CommentReadSerialiser = CommentReadSerialiser(article_comment, many=False, context={"request": request})
        return Response(return_serialiser.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs) -> Union[HttpResponse, Response]:
        """
        Edits a comment's text and updates the updated_date to now
        """
        comment_id: int = kwargs.get('pk')
        existing_comment: ArticleComment = ArticleComment.objects.get(id=comment_id)
        if existing_comment is None:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        new_text: str = request.data['comment_text']

        existing_comment.comment_text = new_text
        existing_comment.updated_date = datetime.datetime.now()
        existing_comment.save()

        return_serialiser = CommentReadSerialiser(existing_comment, many=False, context={"request": request})
        return Response(return_serialiser.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs) -> Union[HttpResponse, Response]:
        """
        Deletes a comment on an article
        """
        user = SiteUser.objects.get(id=request.COOKIES.get('user_id'))
        comment_id = kwargs.get('pk')
        existing_comment: ArticleComment = ArticleComment.objects.get(id=comment_id)
        if existing_comment is None:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        if existing_comment.user.id is not user.id:
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)

        existing_comment.delete()

        return Response(status=status.HTTP_200_OK)
