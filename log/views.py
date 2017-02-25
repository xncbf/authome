import json

from django.shortcuts import render, HttpResponse
from django.views.generic.list import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers import serialize
from django.db import connection
from main.models import MacroLog, UserPage
from .services import dictfetchall


class Log(LoginRequiredMixin, View):
    template_name = "log/log.html"
    login_url = '/accounts/login/'

    def get(self, request, *args, **kwargs):
        context = {}
        context['macroLog'] = MacroLog.objects.filter(macro__user=request.user)[:8]
        context['userPage'] = UserPage.objects.filter(macro__user=request.user).distinct('user')
        return render(self.request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        with connection.cursor() as cursor:
            if request.is_ajax():
                ddlUser = request.POST.get('ddlUser')
                where = {}
                where[''] = ddlUser
                cursor.execute("""SELECT
                *
                FROM
                main_MacroLog""")
                result = dictfetchall(cursor)
                # result = serialize("json", MacroLog.objects.filter(macro__user__id__in=ddlUser.split(','))[:8])
                return HttpResponse(json.dumps(result, ensure_ascii=False))
