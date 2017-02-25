import json

from django.shortcuts import render, HttpResponse
from django.views.generic.list import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers import serialize
from django.db import connection
from main.models import MacroLog, UserPage
from .services import dictfetchall, JSONEncoder


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
                FROM main_macrolog ML
                LEFT JOIN main_macro M ON M.id = ML.macro_id
                LEFT JOIN auth_user U ON U.id = ML.user_id""")
                result = dictfetchall(cursor)
                return HttpResponse(json.dumps(result, ensure_ascii=False, cls=JSONEncoder))
