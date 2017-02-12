from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from main.models import UserPage, MacroLog
from .serializers import AuthSerializer
from django.utils import timezone
from ipware.ip import get_ip
from django.http import Http404
from django.views.generic.base import TemplateView
from rest_framework_docs.api_docs import ApiDocumentation


class GetAuth(APIView):
    """
    예시: /3a526973-98cf-4f0e-8791-5ae7759948d7/
    """
    def get_object(self, macro_id):
        try:
            result = UserPage.objects.get(user__username=self.request.user, macro=macro_id)
            # 현지 시간이 아닌, 절대시간으로 비교함
            # datetime.now() <- 현지시간
            # timezone.now() <- 절대시간
            if(result.end_date.strftime('%Y%m%d%H%M%S') < timezone.now().strftime('%Y%m%d%H%M%S')):
                if result.end_yn == True:
                    UserPage.objects.filter(user__username=self.request.user, macro=macro_id).update(end_yn=False)
                    result = UserPage.objects.get(user__username=self.request.user, macro=macro_id)
            return result
        except UserPage.DoesNotExist:
            raise Http404

    def get(self, request, macro_id, format=None):
        userPage = self.get_object(macro_id)
        serializer = AuthSerializer(userPage)
        MacroLog.objects.create(user=request.user, macro=userPage.macro, ip=get_ip(request))
        return Response(serializer.data)


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