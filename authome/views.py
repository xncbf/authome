import json

from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseServerError
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.generic.list import View
from .forms import ChangeNicknameForm


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('intro'))


def intro(request):
    return render(request, 'dev/intro.html', {})


def nickname_change(request):
    result = {}
    if request.is_ajax():
        form = ChangeNicknameForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return HttpResponse(status=201)
        else:
            result['form_errors'] = form.errors
            return HttpResponseServerError(json.dumps(result, ensure_ascii=False))


class MyPage(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        return render(self.request, 'dev/mypage.html')

    def post(self, *args, **kwargs):
        return HttpResponse()
