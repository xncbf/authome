import json

from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import render, HttpResponseRedirect, redirect, HttpResponse
from django.views.generic.list import ListView, View
from django.http import HttpResponseNotAllowed, HttpResponseServerError
from .models import UserPage, Macro
from .forms import ChangeNicknameForm
from utils.decorators import check_is_my_macro


def update_session(request):
    if not request.is_ajax() or not request.method == 'POST':
        return HttpResponseNotAllowed(['POST'])

    for e in request.POST.keys():
        request.session[e] = request.POST.get(e)
    return HttpResponse(status=201)


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('intro'))


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


class MacroManage(LoginRequiredMixin, ListView):
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
    model = Macro

    def post(self, *args, **kwargs):
        macro_name = self.request.POST.get('macro_name', False)
        macro_detail = self.request.POST.get('macro_detail', False)
        Macro.objects.create(
            title=macro_name,
            detail=macro_detail,
            user=self.request.user
        )
        return HttpResponseRedirect(reverse('main:macro_manage'))

    def get(self, *args, **kwargs):
        return render(self.request, 'main/macro_register.html', {

        })


class MacroModify(LoginRequiredMixin, View):
    model = Macro

    @check_is_my_macro(macro_id='macro_id')
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

    @check_is_my_macro(macro_id='macro_id')
    def get(self, *args, **kwargs):
        macro = Macro.objects.get(id=kwargs['macro_id'])
        return render(self.request, 'main/macro_modify.html', {
            'macro': macro,
        })


class UserManage(LoginRequiredMixin, ListView):
    model = UserPage
    template_name = 'main/user_manage.html'

    @check_is_my_macro('macro_id')
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(UserManage, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['macro'] = Macro.objects.get(id=self.kwargs['macro_id'])
        context['users'] = UserPage.objects.filter(macro=self.kwargs['macro_id']).order_by('-end_date')
        return context


class AuthRegister(LoginRequiredMixin, View):
    @check_is_my_macro(macro_id='macro_id')
    def post(self, request, *args, **kwargs):
        macro = Macro.objects.get(id=kwargs['macro_id'])
        if request.is_ajax():
            user_email = request.POST.get('user_email')
            macro_id = kwargs.get('macro_id')
            result = {}
            if User.objects.filter(email=user_email):
                if not UserPage.objects.filter(user__email=user_email, macro=macro_id):
                    result['result'] = True
                else:
                    result['result'] = False
                    messages.add_message(self.request, messages.INFO, "이미 등록된 사용자입니다.")
            else:
                result['result'] = False
                messages.add_message(self.request, messages.INFO, "존재하지 않는 사용자입니다")
            return HttpResponse(json.dumps(result, ensure_ascii=False))
        # ajax 요청이 아닌 경우
        else:
            create = {}
            user_email = self.request.POST.get('user_email', False)
            end_date = self.request.POST.get('end_date', False)
            if end_date:
                create['end_date'] = end_date
            try:
                create['user'] = User.objects.get(email=user_email)
                create['macro'] = macro
                UserPage.objects.create(**create)
            except:
                messages.add_message(self.request, messages.INFO, "등록 실패")
                return render(self.request, 'main/auth_register.html', {
                    'macro': macro,
                })
            return redirect('main:user_manage', macro_id=kwargs['macro_id'])

    @check_is_my_macro(macro_id='macro_id')
    def get(self, *args, **kwargs):
        macro = Macro.objects.get(id=kwargs['macro_id'])
        return render(self.request, 'main/auth_register.html', {
            'macro': macro,
        })


class AuthModify(LoginRequiredMixin, View):
    @check_is_my_macro(macro_id='macro_id')
    def post(self, *args, **kwargs):
        macro = Macro.objects.get(id=kwargs['macro_id'])
        user = User.objects.get(email=kwargs['email'])
        end_date = self.request.POST.get('end_date')

        updateDict = {}
        updateDict['user'] = user
        updateDict['end_date'] = end_date
        updateDict['end_yn'] = False

        user_page = UserPage.objects.filter(macro=macro, user=user)
        user_page.update(**updateDict)

        return redirect('main:user_manage', macro_id=kwargs['macro_id'])

    @check_is_my_macro(macro_id='macro_id')
    def get(self, *args, **kwargs):
        macro = kwargs['macro_id']
        user = User.objects.get(email=kwargs['email'])
        userpage = UserPage.objects.get(user__email=kwargs['email'], macro=macro)
        return render(self.request, 'main/auth_modify.html', {
            'macro': macro,
            'user': user,
            'userpage': userpage,
        })


class MyPage(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        return render(self.request, 'main/mypage.html')

    def post(self, *args, **kwargs):
        return HttpResponse('')


def page_not_found_view(request):
    return render(request, 'error/404.html')


def error_view(request):
    return render(request, 'error/500.html')


def permission_denied_view(request):
    return render(request, 'error/403.html')


def bad_request_view(request):
    return render(request, 'error/400.html')
