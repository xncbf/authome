from django.shortcuts import render
from django.views.generic.list import View
from django.contrib.auth.mixins import LoginRequiredMixin
from main.models import MacroLog


class Log(LoginRequiredMixin, View):
    template_name = "log/log.html"
    login_url = '/accounts/login/'
    def get(self, request, *args, **kwargs):
        context = {}
        context['macroLog'] = MacroLog.objects.filter(macro__user=request.user)
        return render(self.request, self.template_name, context)
