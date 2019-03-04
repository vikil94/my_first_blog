from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
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
