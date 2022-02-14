# coding=utf-8

"""django_exercise URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include
from django.views.static import serve
from django.conf import settings
from django.urls import path, re_path
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('snh48/', include(('snh48.urls', 'snh48'), namespace='snh48')),
    path('modian/', include(('modian.urls', 'modian'), namespace='modian')),
    path('admin/', admin.site.urls),
    re_path('static/(?P<path>.*)', serve, {'document_root': settings.STATIC_ROOT}, name='static'),
    re_path('media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
    path('ckeditor/', include('ckeditor_uploader.urls'))
]
urlpatterns += staticfiles_urlpatterns()
