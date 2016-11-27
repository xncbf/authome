from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from .forms import LoginForm
from .models import UserPage, Macro
from .serializers import UserPageSerializer
from django.views.generic.list import ListView


class UserPageList(APIView):
    """
    여기에 설명을 쓸수있다 api 문서다
    """
    def get(self, request, format=None):
        userPage = UserPage.objects.filter(user__username=self.request.user).order_by('-end_date')
        serializer = UserPageSerializer(userPage, many=True)
        return Response(serializer.data)


class UserPageDetail(APIView):
    """
    코드 조각 조회, 업데이트, 삭제
    """
    def get_object(self, macro_id):
        try:
            return UserPage.objects.get(user__username=self.request.user, macro=macro_id)
        except UserPage.DoesNotExist:
            raise Http404

    def get(self, request, macro_id, format=None):
        userPage = self.get_object(macro_id)
        serializer = UserPageSerializer(userPage)
        return Response(serializer.data)
    #
    # def put(self, request, pk, format=None):
    #     snippet = self.get_object(pk)
    #     serializer = UserPageSerializer(snippet, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def delete(self, request, pk, format=None):
    #     snippet = self.get_object(pk)
    #     snippet.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


def user_login(request):
    form = LoginForm()
    username = request.POST.get('username', False)
    password = request.POST.get('password', False)
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # 로그인성공
            return HttpResponseRedirect("/")
        else:
            # Return a 'disabled account' error message
            pass
    else:
        # Return an 'invalid login' error message.
        # if you want to keep provided username, but clear password field
        form = LoginForm(initial={'username': request.POST.get('username')})
    return render(request, 'login.html', {
        'form': form,
    })


def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/")


def user_join(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        user = form.save()
        password = request.POST.get('password1', False)
        user = authenticate(username=user.username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # 로그인성공
                return HttpResponseRedirect("/")
            else:
                # Return a 'disabled account' error message
                pass

        return HttpResponseRedirect("/")
    return render(request, 'join.html', {
        'form': form,
    })


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
    return render(request, 'mypage/intro.html', {})


@login_required(login_url='/accounts/login/')
def macro_register(request):
    macro_name = request.POST.get('macro_name', False)
    macro_detail = request.POST.get('macro_detail', False)
    macro_payment = request.POST.get('macro_payment', False)
    macro_auth_date = request.POST.get('macro_auth_date', False)
    if macro_name and macro_detail:
        macro = Macro(
            title=macro_name,
            detail=macro_detail,
            fee=macro_payment,
            user=request.user,
            auth_date=macro_auth_date
        )
        macro.save()
        return HttpResponseRedirect("/mypage/")
    return render(request, 'authome/macro_register.html', {

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


@login_required(login_url='/accounts/login/')
def auth_register(request, macro_id):
    user_id = request.POST.get('user_id', False)
    end_date = request.POST.get('end_date', False)
    if user_id and end_date:
        try:
            user = User.objects.get(username=user_id)
            macro = Macro.objects.get(id=macro_id)
            if user:
                user_page = UserPage(user=user, macro=macro, end_date=end_date)
                user_page.save()
                # return HttpResponseRedirect("/mypage/macro_manager/" % macro_id)
                return redirect(MacroManage(request, macro_id))
        except:
            pass


    macro = Macro.objects.get(id=macro_id)
    return render(request, 'authome/auth_register.html', {
        'macro': macro,
    })
