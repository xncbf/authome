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
            return UserPage.objects.get(user__username=user, macro=macro_id)
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
            return Response(status=status.HTTP_403_FORBIDDEN)
