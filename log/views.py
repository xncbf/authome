from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.urls import reverse
from django.db import connection
from django.shortcuts import render, HttpResponse
from django.utils import timezone
from django.views.generic.list import View

from main.models import MacroLog, UserPage
from utils.services import dictfetchall


class Log(LoginRequiredMixin, View):
    template_name = "log/log.html"
    login_url = '/accounts/login/'

    def get(self, request, *args, **kwargs):
        context = {}
        qs = MacroLog.objects.filter(macro__user=request.user).order_by('macro', 'user', '-created').distinct('macro',
                                                                                                              'user')
        unsorted_results = qs.all()
        context['macroLog'] = sorted(unsorted_results, key=lambda t: t.created, reverse=True)
        context['userPage'] = UserPage.objects.filter(macro__user=request.user).distinct('user')
        return render(self.request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        with connection.cursor() as cursor:
            if request.is_ajax():
                ddl_user = ','.join(request.POST.get('ddlUser').split(','))
                if ddl_user:
                    where_str = 'AND ML.user_id IN ({0})'.format(ddl_user)
                else:
                    where_str = ''
                cursor.execute("""SELECT
                ML.macro_id,
                ML.created,
                ML.ip,
                M.title,
                U.email
                FROM main_macrolog ML
                LEFT JOIN main_macro M ON M.id = ML.macro_id
                LEFT JOIN auth_user U ON U.id = ML.user_id
                WHERE M.user_id = '{0}' {1}
                ORDER BY ML.created DESC
                LIMIT 20""".format(request.user.pk, where_str))
                obj = dictfetchall(cursor)
                result = self.set_html(obj)
                return HttpResponse(result)

    def set_html(self, obj, html=''):
        for e in obj:
            user = User.objects.get(email=e.get('email'))
            local_time = timezone.localtime(e.get('created'))

            if user.socialaccount_set.all():
                profile_url = user.socialaccount_set.all()[0].get_avatar_url()
            else:
                profile_url = static('images/Jigglypuff.png')
            html += """<li class="collection-item user-list">
                        <a href="{0}">
                            <div>{1}</div>
                            <div class="chip">
                                <img src="{2}">{3}
                            </div>
                            <span class="secondary-content">{4}<br>{5}</span>
                        </a>
                    </li>""".format(reverse('main:user_manage', kwargs={'macro_id': e.get('macro_id')}),
                                    e.get('title') or '제목없음',
                                    profile_url,
                                    e.get('email'),
                                    e.get('ip'),
                                    local_time.strftime('%y-%m-%d %H:%M'))
        if len(obj) == 0:
            html = '<li class="collection-item user-list">사용 흔적이 없어요!</li>'
        return html
