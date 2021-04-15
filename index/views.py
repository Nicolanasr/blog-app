from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'index/index.html')


def new_post(request):
    return render(request, 'index/new_post.html')
