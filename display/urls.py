"""mysite URL Configuration

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
    2. Add a URL to urlpatterns:  path('myblog/', include('myblog.urls'))
"""
from django.urls import path, re_path
from . import views

app_name = 'display'
urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'.*.html$', views.analysis, name='analysis'),
    re_path(r'.*data/.*csv$', views.csv_data, name='csv_data'),
    re_path(r'.*data/.*json$', views.json_data, name='json_data')
]
