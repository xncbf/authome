from django.shortcuts import render
from django.views.generic.list import View
from django.contrib.auth.mixins import LoginRequiredMixin


class Log(LoginRequiredMixin, View):
    template_name = "log/main.html"
    login_url = '/accounts/login/'

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)
