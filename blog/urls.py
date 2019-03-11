"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from blog.views import root, home_page, article_page, create_article, create_comment


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home_page),
    path('', root),
    path('article/<int:id>', article_page, name='article_details'),
    path('comment/new', create_comment, name='create_comment'),
    path('article/new/', create_article, name='create_article'),
]
