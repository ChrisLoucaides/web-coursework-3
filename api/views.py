import datetime

from django.contrib.auth import login, authenticate
from django.contrib.auth.models import auth
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins
from rest_framework.decorators import action
from .forms import SignupForm, LoginForm
from .models import ArticleComment, Article, SiteUser, Category
from .serialisers import CommentReadSerialiser, CommentWriteSerialiser, UserSerialiser, ArticleSerialiser


def check_auth_status(request):
    return JsonResponse({'is_authenticated': True})


def user_login(request):
    """
    Logs the user in
    """
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            authenticated_user = authenticate(request, username=username, password=password)

            if authenticated_user is not None:
                auth.login(request, authenticated_user)
                response = HttpResponseRedirect('http://127.0.0.1:5173/')
                response.set_cookie('user_id', str(authenticated_user.id))

                return response

    return render(request, 'login.html', {'form': form})


def get_user(request):
    id_from_cookie = request.COOKIES.get('user_id')
    user = SiteUser.objects.get(id = id_from_cookie)
    return user


def user_signup(request):
    """
    Allows a user to sign up to the site
    """
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # TODO WEB-2: Replace with login page?
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def user_logout(request):
    """
    Logs the user out
    """
    auth.logout(request)
    return redirect("")


def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})


def get_articles(request):
    if request.method == 'GET':
        articles = list(Article.objects.values())
        return JsonResponse(articles, safe=False, status=200)
    else:
        return JsonResponse(content="invalid request method", status=400, data="")


class UserViewSet(mixins.CreateModelMixin, GenericViewSet):
    """
    A ViewSet for operations related to users
    """

    queryset = SiteUser.objects.all()

    def get_serializer_class(self):
        return UserSerialiser

    @action(detail=False)
    def current(self, request, *args, **kwarg):
        cookie = request.COOKIES.get('user_id')
        serialiser = self.get_serializer(SiteUser.objects.get(id=cookie), many=False)

        return Response(serialiser.data)

    @action(detail=False, methods=['PATCH'])  # TODO: WEB-9 get rid of this and use below method (update_user)
    def update_categories(self, request, *args, **kwarg):
        cookie = request.COOKIES.get('user_id')
        user = SiteUser.objects.get(id=cookie)
        print("request.data is BELOW")
        print(request.data)
        new_preferences = request.data
        print(type(new_preferences))
        user.category.set(Category.objects.filter(name__in=new_preferences['preferences']))
        user.save()
        print(user.category)

        return Response('User preferences updated')

    @action(detail=False, methods=['PATCH'])
    def update_user(self, request, *args, **kwargs):
        cookie = request.COOKIES.get('user_id')
        user = SiteUser.objects.get(id=cookie)

        new_data = request.data

        user.category.set(Category.objects.filter(name__in=new_data['preferences']))

        fields_to_update = ['email', 'date_of_birth']

        for field in fields_to_update:
            if field in new_data and new_data[field] != '':
                setattr(user, field, new_data[field])

        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']

        user.save()

        return Response('User details updated', status=status.HTTP_200_OK)


class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()

    def get_serializer_class(self):
        return ArticleSerialiser

    def list(self, request, *args, **kwargs):
        """
        Returns all comments for a given requested article id
        """
        cookie = request.COOKIES.get('user_id')
        user = SiteUser.objects.get(id=cookie)
        categories = user.category.values_list('name', flat=True)

        serialiser = self.get_serializer(Article.objects.filter(category__name__in=categories), many=True)
        return Response(serialiser.data)

class CommentsViewSet(mixins.CreateModelMixin, GenericViewSet):
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
        article_id = self.kwargs.get('article_id')
        if 'pk' in self.kwargs:
            return ArticleComment.objects.filter(article_id=article_id)
        else:
            return ArticleComment.objects.filter(article_id=article_id, parent_comment=None)

    def list(self, request, *args, **kwargs):
        """
        Returns all comments for a given requested article id
        """
        serialiser = self.get_serializer(self.get_queryset().order_by('-created_date'), many=True)
        return Response(serialiser.data)

    def create(self, request, *args, **kwargs):
        """
        Posts a new comment on a requested article id
        """
        article: Article = Article.objects.get(id=self.kwargs['article_id'])
        if article is None:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

        user = SiteUser.objects.get(id=request.COOKIES.get('user_id'))
        serialiser = self.get_serializer(data=request.data)

        serialiser.is_valid(raise_exception=True)
        comment = serialiser.validated_data
        comment['article_id'] = article
        comment['user'] = user
        article_comment = ArticleComment(**comment)
        article_comment.save()

        return_serialiser = CommentReadSerialiser(article_comment, many=False)
        return Response(return_serialiser.data, status=status.HTTP_201_CREATED)

    @action(methods=['PATCH'], detail=True)
    def edit(self, request, *args, **kwargs):
        """
        Edits a comment's text and updates the updated_date to now
        """
        comment_id = kwargs.get('pk')
        existing_comment: ArticleComment = ArticleComment.objects.get(id=comment_id)
        if existing_comment is None:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        new_text = request.data['comment_text']

        existing_comment.comment_text = new_text
        existing_comment.updated_date = datetime.datetime.now()
        existing_comment.save()

        return_serialiser = CommentReadSerialiser(existing_comment, many=False)
        return Response(return_serialiser.data, status=status.HTTP_201_CREATED)
