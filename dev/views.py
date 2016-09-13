from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .forms import LoginForm
from .models import UserPage
from .serializers import UserPageSerializer
import datetime


class UserPage_list(APIView):
    """
    코드 조각을 모두 보여주거나 새 코드 조각을 만듭니다.
    """
    def get(self, request, format=None):
        userPage = UserPage.objects.filter(user__username=self.request.user).order_by('-end_date')
        serializer = UserPageSerializer(userPage, many=True)
        return Response(serializer.data)


class UserPage_detail(APIView):
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


def userlogin(request):
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


def userjoin(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect(index)
    return render(request, 'join.html', {
        'form': form,
    })



@login_required(login_url='/accounts/login/')
def index(request):
    return render(request, 'authome/index.html', {})


def dev_index(request):
    """
     dev 인덱스페이지
    """
    return render(request, 'authome/index.html', {})


def userlogout(request):
    logout(request)
    return redirect(index)


def today(request):
    return render(request, 'today.html', {
        'datetime': datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
    })


def mypage(request):
    return render(request, 'authome/mypage.html', {
    })

