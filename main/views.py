from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponseRedirect, redirect, HttpResponse
from django.views.generic.list import ListView, View
from django.core import serializers
from .forms import LoginForm
from .models import UserPage, Macro
import json


# def user_login(request):
#     form = LoginForm(request.POST or None)
#     if request.POST and form.is_valid():
#         user = form.login(request)
#         if user:
#             if user.is_active:
#                 login(request, user)
#                 # 로그인성공
#                 if request.POST.get('next'):
#                     return HttpResponseRedirect(request.POST.get('next'))
#                 else:
#                     return HttpResponseRedirect('/')
#             else:
#                 # 권한이 없는 아이디
#                 pass
#         else:
#             form = form.clean()
#     return render(request, 'registration/login.html', {
#             'form': form,
#     })
#
#
# def user_join(request):
#     form = UserCreationForm(request.POST)
#     if form.is_valid():
#         user = form.save()
#         password = request.POST.get('password1', False)
#         user = authenticate(username=user.username, password=password)
#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                 # 로그인성공
#                 return HttpResponseRedirect("/")
#             else:
#                 # Return a 'disabled account' error message
#                 pass
#         else:
#             form.clean()
#         return HttpResponseRedirect("/")
#     return render(request, 'registration/join.html', {
#         'form': form,
#     })


class Mypage(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
    # redirect_field_name = 'index'
    model = Macro
    template_name = 'authome/mypage.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(Mypage, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['macro_list'] = Macro.objects.filter(user=self.request.user)
        return context


def intro(request):
    """
     mypage 인덱스페이지
    """
    return render(request, 'main/intro.html', {})


class MacroRegister(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    model = Macro
    template_name = 'authome/macro_register.html'

    def post(self, *args, **kwargs):
        macro_name = self.request.POST.get('macro_name', False)
        macro_detail = self.request.POST.get('macro_detail', False)
        macro = Macro(
            title=macro_name,
            detail=macro_detail,
            user=self.request.user
        )
        macro.save()
        return HttpResponseRedirect("/mypage/")

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name, {

        })


class MacroModify(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    model = Macro
    template_name = 'authome/macro_modify.html'

    def post(self, *args, **kwargs):
        macro_name = self.request.POST.get('macro_name', False)
        macro_detail = self.request.POST.get('macro_detail', False)
        self.model.objects.filter(
            id=kwargs['macro_id'],
        ).update(
            title=macro_name,
            detail=macro_detail,
        )
        return HttpResponseRedirect("/mypage/")

    def get(self, *args, **kwargs):
        macro = Macro.objects.get(id=kwargs['macro_id'])
        return render(self.request, self.template_name, {
            'macro': macro,
        })


class MacroManage(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
    model = UserPage
    template_name = 'authome/macro_manager.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MacroManage, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['macro'] = Macro.objects.get(id=self.kwargs['macro_id'])
        context['users'] = UserPage.objects.filter(macro=self.kwargs['macro_id'])
        return context


class AuthRegister(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    template_name = 'authome/auth_register.html'

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
                return render(self.request, self.template_name, {
                    'macro': macro,
                    'error': '등록 실패',
                })
            return redirect('main:macro_manager', macro_id=kwargs['macro_id'])

    def get(self, request, *args, **kwargs):
        macro = Macro.objects.get(id=kwargs['macro_id'])
        return render(self.request, 'authome/auth_register.html', {
            'macro': macro,
        })


def page_not_found_view(request):
    return render(request, 'error/404.html')


def error_view(request):
    return render(request, 'error/500.html')


def permission_denied_view(request):
    return render(request, 'error/403.html')


def bad_request_view(request):
    return render(request, 'error/400.html')
