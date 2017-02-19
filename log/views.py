from django.shortcuts import render, HttpResponse
from django.views.generic.list import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers import serialize
from main.models import MacroLog, UserPage


class Log(LoginRequiredMixin, View):
    template_name = "log/log.html"
    login_url = '/accounts/login/'

    def get(self, request, *args, **kwargs):
        context = {}
        context['macroLog'] = MacroLog.objects.filter(macro__user=request.user)[:8]
        context['userPage'] = UserPage.objects.filter(macro__user=request.user).distinct('user')
        return render(self.request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            ddlUser = request.POST.get('ddlUser')
            data = serialize("json", MacroLog.objects.filter(macro__user__id__in=ddlUser.split(','))[:8])
            return HttpResponse(data)