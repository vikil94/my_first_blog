from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from blog.models import Article, Comment
from blog.forms import CommentForm, ArticleForm
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
    form = CommentForm(request.POST)
    if form.is_valid():
        new_comment = form.save()
        return HttpResponseRedirect('/article/' + form)
    else:
        messages.error(request, form.errors)
        return render(request, 'articles.html', {'form': CommentForm()})

        # article = request.POST['article']
        # comment_name = request.POST['comment_name']
        # comment_message = request.POST['comment_message']
        # comment_article = Article.objects.get(pk=request.POST['article'])
        # new_comment = Comment.objects.create(name=comment_name,
        #                                  message=comment_message,
        #                                  article=comment_article)
        # return HttpResponseRedirect('/article/' + article)

def create_article(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            form = form.save()
            return HttpResponseRedirect('/article/' +str(form.pk))
        else:
            print(form.errors)
    else:
        form = ArticleForm()
    return render(request, 'create_article.html', {'form': form})
