from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from blog.models import Article, Comment
from blog.forms import CommentForm, ArticleForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime


def root(request):
    return HttpResponseRedirect('home')


def home_page(request):
    date_now = str(datetime.datetime.now())
    articles = Article.objects.filter(draft=False).order_by('-published_date').all()
    context = {'name': 'Vikil', 'day': date_now, 'articles': articles}
    response = render(request, 'index.html', context)
    return HttpResponse(response)


def article_page(request, id):
    articles = get_object_or_404(Article, pk=id)
    context = {'article': articles, 'form': CommentForm()}
    response = render(request, 'articles.html', context)
    return HttpResponse(response)


def new_article(request):
    context = {'article': ArticleForm()}
    response = render(request, 'create_article.html', context)
    return HttpResponse(response)


def create_comment(request):
    # form = CommentForm(request.POST)
    # if form.is_valid():
    #     new_comment = form.save()
    #     return HttpResponseRedirect('/article/' + form)
    # else:
    #     messages.error(request, form.errors)
    #     return render(request, 'articles.html', {'form': CommentForm()})

    article = request.POST['article']
    comment_name = request.POST['comment_name']
    comment_message = request.POST['comment_message']
    comment_article = Article.objects.get(pk=request.POST['article'])
    new_comment = Comment.objects.create(name=comment_name,
                                         message=comment_message,
                                         article=comment_article)
    return HttpResponseRedirect('/article/' + article)

@login_required
def create_article(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.user = request.user
            form = form.save()
            return HttpResponseRedirect('/article/' + str(form.pk))
        else:
            print(form.errors)
    else:
        form = ArticleForm()
    return render(request, 'create_article.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
         return HttpResponseRedirect('/home')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            pw = form.cleaned_data['password']
            user = authenticate(username=username, password=pw)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/home')
            else:
                form.add_error('username', 'Login failed')
    else:
        form = LoginForm()

    context = {'form': form}
    http_response = render(request, 'login.html', context)
    return HttpResponse(http_response)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/home')


def signup(request):
    if request.user.is_authenticated:
         return HttpResponseRedirect('/home')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect('/home')
    else:
        form = UserCreationForm()
    html_response = render(request, 'signup.html', {'form': form})
    return HttpResponse(html_response)

@login_required
def edit_article(request, id):
    article = get_object_or_404(Article, id=id)
    if request.method == 'GET':
        if article.user != request.user: # redirects the user to the home page if
                                        # they are not the player who created the game
                                        # therefore they are not able to edit that game
            # TODO: add a temporary message that tells the user they didn't have access
            messages.add_message(request, messages.WARNING, "You cannot edit another persons article!")
            return HttpResponseRedirect('/')
        form = ArticleForm(instance=article)
        context = {'form': form, 'article': article}
        return render(request, 'edit.html', context)

    elif request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            updated_picture = form.save()
            return HttpResponseRedirect(reverse('show', args=[article.id]))
        else:
            context = {'form': form, 'article': article}
            response = render(request, 'edit.html', context)
            return HttpResponse(response)
