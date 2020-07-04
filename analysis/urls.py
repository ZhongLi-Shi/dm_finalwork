"""sentiment URL Configuration

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
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^analysis_douban/', views.analysis_douban),
    url(r'^index/', views.index),
    url(r'^index_douban/', views.index_douban),
    url(r'^index_hotel/', views.index_hotel),
    url(r'^analysis_sentence/', views.analysis_sentence),
    url(r'^analysis_hotel/', views.analysis_jiudian),
    url(r'^analysis_hotel_all/', views.analysis_jiudian_all),
    url(r'^testjs/', views.analysis_douban),
]
