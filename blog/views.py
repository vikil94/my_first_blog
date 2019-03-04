from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from blog.models import Article
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
    context = {'article': articles}
    response = render(request, 'articles.html', context)
    return HttpResponse(response)
