from django.http.response import Http404
from django.shortcuts import render
from django.http import Http404


def login(request):
    return render(request, 'login.html', {})