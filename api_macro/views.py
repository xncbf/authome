from django.http import Http404
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from ipware.ip import get_ip
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from allauth.socialaccount.models import SocialAccount, SocialToken
from api_macro.serializers import AuthSerializer
from main.models import UserPage, MacroLog


class GetAuth(APIView):
    """
    예시: /macro/auth/test/password/3a526973-98cf-4f0e-8791-5ae7759948d7/
    """
    def get_object(self, user, macro_id):
        try:
            result = UserPage.objects.get(user__username=user, macro=macro_id)
            # 현지 시간이 아닌, 절대시간으로 비교함
            # datetime.now() <- 현지시간
            # timezone.now() <- 절대시간
            if(result.end_date.strftime('%Y%m%d%H%M%S') < timezone.now().strftime('%Y%m%d%H%M%S')):
                if result.end_yn == True:
                    UserPage.objects.filter(user__username=user, macro=macro_id).update(end_yn=False)
                    result = UserPage.objects.get(user__username=user, macro=macro_id)
            return result
        except UserPage.DoesNotExist:
            raise Http404

    def get(self, request, username, password, macro_id, format=None):
        user = authenticate(username=username, password=password)
        if user:
            userPage = self.get_object(user, macro_id)
            serializer = AuthSerializer(userPage)
            MacroLog.objects.create(user=user, macro=userPage.macro, ip=get_ip(request))
            return Response(serializer.data)
        else:
            try:
                social_user = User.objects.get(username=username)
                social_account = SocialAccount.objects.get(user_id=social_user.pk)
                social_token = SocialToken.objects.get(account_id=social_account.pk)
                if social_token.token == password:
                    userPage = self.get_object(social_user.username, macro_id)
                    serializer = AuthSerializer(userPage)
                    MacroLog.objects.create(user=social_user, macro=userPage.macro, ip=get_ip(request))
                    return Response(serializer.data)
                else:
                    raise Exception
            except:
                return Response(status=status.HTTP_403_FORBIDDEN)


class GetList(APIView):
    """
    전체 Endpoint 를 가져옵니다.
    """
    def get(self, request, format=None):
        userPage = UserPage.objects.all()
        # if not len(userPage):
        #     raise Http404
        serializer = AuthSerializer(userPage)
        MacroLog.objects.create(user=request.user, macro=userPage.macro, ip=get_ip(request))
        return Response(serializer.data)
