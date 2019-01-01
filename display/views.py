from django.http import HttpResponse
from django.shortcuts import render
import os


# Create your views here.

def index(request):
    return render(request, 'display/index.html', context={})


def analysis(request):
    template = str(request.build_absolute_uri('?')).split('/')[-1]
    return render(request, 'display/' + template, context={})


def csv_data(request):
    data_url = 'display/' + request.path[1:]
    with open(data_url) as file:
        ret_data = file.read()
    return HttpResponse(ret_data, content_type='text/csv')


def json_data(request):
    data_url = 'display/' + request.path[1:]
    with open(data_url) as file:
        ret_data = file.read()
    return HttpResponse(ret_data, content_type='text/json')
