"""BlogSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
from blog import views
from django.conf.urls import url, include
from rest_framework import routers
from blog.api import BlogView

router = routers.DefaultRouter()
router.register('blog', BlogView, 'blog')

urlpatterns = [
    path(r'api/v1/', include(router.urls)),
    path('', views.display_blog, name='index'),
    path(r'blog/write/', views.blog_write, name='write_blog'),

]
