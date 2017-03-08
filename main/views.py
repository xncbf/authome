from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render, HttpResponseRedirect, redirect, HttpResponse
from django.views.generic.list import ListView, View
from .models import UserPage, Macro
import json


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('intro'))


class MacroManage(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
    model = Macro
    template_name = 'main/macro_manage.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MacroManage, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['macro_list'] = Macro.objects.filter(user=self.request.user)
        return context


def intro(request):
    """
     macro_manage 인덱스페이지
    """
    return render(request, 'main/intro.html', {})


class MacroRegister(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    model = Macro

    def post(self, *args, **kwargs):
        macro_name = self.request.POST.get('macro_name', False)
        macro_detail = self.request.POST.get('macro_detail', False)
        macro = Macro(
            title=macro_name,
            detail=macro_detail,
            user=self.request.user
        )
        macro.save()
        return HttpResponseRedirect(reverse('main:macro_manage'))

    def get(self, *args, **kwargs):
        return render(self.request, 'main/macro_register.html', {

        })


class MacroModify(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    model = Macro

    def post(self, *args, **kwargs):
        macro_name = self.request.POST.get('macro_name', False)
        macro_detail = self.request.POST.get('macro_detail', False)
        self.model.objects.filter(
            id=kwargs['macro_id'],
        ).update(
            title=macro_name,
            detail=macro_detail,
        )
        return HttpResponseRedirect(reverse('main:macro_manage'))

    def get(self, *args, **kwargs):
        macro = Macro.objects.get(id=kwargs['macro_id'])
        return render(self.request, 'main/macro_modify.html', {
            'macro': macro,
        })


class UserManage(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
    model = UserPage
    template_name = 'main/user_manage.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(UserManage, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['macro'] = Macro.objects.get(id=self.kwargs['macro_id'])
        context['users'] = UserPage.objects.filter(macro=self.kwargs['macro_id'])
        return context


class AuthRegister(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def post(self, request, *args, **kwargs):
        macro = Macro.objects.get(id=kwargs['macro_id'])
        if request.is_ajax():
            user_id = request.POST.get('user_id')
            macro_id = kwargs.get('macro_id')
            result = {}
            if User.objects.filter(username=user_id):
                if not UserPage.objects.filter(user__username=user_id, macro=macro_id):
                    result['result'] = True
                else:
                    result['result'] = False
                    result['error'] = "이미 등록된 사용자입니다."
            else:
                result['result'] = False
                result['error'] = "존재하지 않는 사용자입니다"
            return HttpResponse(json.dumps(result, ensure_ascii=False))
        # ajax 요청이 아닌 경우
        else:
            create = {}
            user_id = self.request.POST.get('user_id', False)
            end_date = self.request.POST.get('end_date', False)
            if end_date:
                create['end_date'] = end_date
            try:
                create['user'] = User.objects.get(username=user_id)
                create['macro'] = macro
                user_page = UserPage(**create)
                user_page.save()
            except:
                return render(self.request, 'main/auth_register.html', {
                    'macro': macro,
                    'error': '등록 실패',
                })
            return redirect('main:user_manage', macro_id=kwargs['macro_id'])

    def get(self, request, *args, **kwargs):
        macro = Macro.objects.get(id=kwargs['macro_id'])
        return render(self.request, 'main/auth_register.html', {
            'macro': macro,
        })


class MyPage(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    def get(self, *args, **kwargs):
        return render(self.request, 'main/mypage.html')
    def post(self, *args, **kwargs):
        pass



def page_not_found_view(request):
    return render(request, 'error/404.html')


def error_view(request):
    return render(request, 'error/500.html')


def permission_denied_view(request):
    return render(request, 'error/403.html')


def bad_request_view(request):
    return render(request, 'error/400.html')
