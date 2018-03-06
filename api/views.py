from django.http import Http404
from django.utils import timezone
from django.contrib.auth.models import User
from django.views.generic.base import TemplateView

from rest_framework_docs.api_docs import ApiDocumentation

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from ipware.ip import get_ip

from .serializers import AuthSerializer
from main.models import UserPage, MacroLog


class DRFDocsView(TemplateView):

    template_name = "rest_framework_docs/custom.html"

    def get_context_data(self, **kwargs):
        context = super(DRFDocsView, self).get_context_data(**kwargs)
        docs = ApiDocumentation()
        endpoints = docs.get_endpoints()

        query = self.request.GET.get("search", "")
        if query and endpoints:
            endpoints = [endpoint for endpoint in endpoints if query in endpoint.path]

        context['query'] = query
        context['endpoints'] = endpoints
        return context


class GetAuth(APIView):
    """17년 5월 21일부로 사용 불가능합니다."""

    def _block_duplicate(self, request, user):
        """동시 접속 차단 로직"""
        lastLog = MacroLog.objects.filter(user=user, succeeded=True).order_by('-created')
        if lastLog:
            lastLogTime = lastLog.first().created
            if (timezone.now() - lastLogTime).seconds < 3600:
                if lastLog.first().ip != get_ip(request):
                    return False
        return True

    def get_object(self, user, macro_id):
        try:
            return UserPage.objects.get(user__email=user.email, macro=macro_id)
        except UserPage.DoesNotExist:
            raise Http404

    def get(self, request, username, password, macro_id):
        user = User.objects.get(extendsuser__token=password)
        if user:
            userPage = self.get_object(user, macro_id)

            # 동시 접속 차단 로직
            if not self._block_duplicate(request, user):
                MacroLog.objects.create(user=user, macro=userPage.macro, ip=get_ip(request), succeeded=False)
                return Response(status=status.HTTP_403_FORBIDDEN)

            serializer = AuthSerializer(userPage)
            MacroLog.objects.create(user=user, macro=userPage.macro, ip=get_ip(request), succeeded=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class GetAuth2(APIView):
    def _block_duplicate(self, request, user):
        """동시 접속 차단 로직"""
        lastLog = MacroLog.objects.filter(user=user, succeeded=True).order_by('-created')
        if lastLog:
            lastLogTime = lastLog.first().created
            if (timezone.now() - lastLogTime).seconds < 3600:
                if lastLog.first().ip != get_ip(request):
                    return False
        return True

    def get_object(self, user, macro_id):
        try:
            return UserPage.objects.get(user__email=user.email, macro=macro_id)
        except UserPage.DoesNotExist:
            raise Http404

    def get(self, request, token, macro_id):
        user = User.objects.get(extendsuser__token=token)
        # TODO: 토큰이 번거로운사람 또는 OTP 이용하고싶은사람을 위해 OTP 기능 추가 예정
        if user:
            userPage = self.get_object(user, macro_id)

            # 동시 접속 차단 로직
            if not self._block_duplicate(request, user):
                MacroLog.objects.create(user=user, macro=userPage.macro, ip=get_ip(request), succeeded=False)
                return Response(status=status.HTTP_423_LOCKED)

            serializer = AuthSerializer(userPage)
            MacroLog.objects.create(user=user, macro=userPage.macro, ip=get_ip(request), succeeded=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
