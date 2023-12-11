from django.contrib.auth import login, authenticate
from django.contrib.auth.models import auth
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .forms import SignupForm, LoginForm
from .models import ArticleComment, Article, SiteUser, Category
from .serialisers import CommentReadSerialiser, CommentWriteSerialiser


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
                json = {
                    'user_id': authenticated_user.id,
                    'username': username,
                    'date_of_birth':authenticated_user.date_of_birth,
                    'preferences':Category.objects.filter(user=authenticated_user.id).values
                    }
                print(json)
                response = HttpResponseRedirect('http://localhost:5173/')
                response.set_cookie('user_id', authenticated_user.id)
                response.content = json

                return response

    return render(request, 'login.html', {'form': form})


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
        article_id = self.kwargs.get('article_id')
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
