
from django.contrib.auth import logout
from django.urls import reverse
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.http import HttpResponseNotAllowed

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('intro'))


def intro(request):
    return render(request, 'dev/intro.html', {})
