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
    5월 21일부로 사용 불가능합니다.
    """
    def get(self, request, username, password, macro_id, format=None):
        # TODO: 5월20일부터는 토큰으로만 로그인하도록 변경
        return Response(status=status.HTTP_404_NOT_FOUND)

class GetAuth2(APIView):
    def get_object(self, user, macro_id):
        try:
            return UserPage.objects.get(user__username=user, macro=macro_id)
        except UserPage.DoesNotExist:
            raise Http404

    def block_duplicate(self, request, user):
        """
        동시 접속 차단 로직
        """
        lastLog = MacroLog.objects.filter(user=user, succeeded=True).order_by('-created')
        if lastLog:
            lastLogTime = lastLog.first().created
            if (timezone.now() - lastLogTime).seconds < 3600:
                if lastLog.first().ip != get_ip(request):
                    return False
        return True

    def get(self, request, token, macro_id, format=None):
        user = User.objects.get(extendsuser__token=token)
        # TODO: 토큰이 번거로운사람 또는 OTP 이용하고싶은사람을 위해 OTP 기능 추가 예정
        if user:
            userPage = self.get_object(user, macro_id)

            # 동시 접속 차단 로직
            if not self.block_duplicate(request, user):
                MacroLog.objects.create(user=user, macro=userPage.macro, ip=get_ip(request), succeeded=False)
                return Response(status=status.HTTP_403_FORBIDDEN)

            serializer = AuthSerializer(userPage)
            MacroLog.objects.create(user=user, macro=userPage.macro, ip=get_ip(request), succeeded=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
