from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from mypage.models import UserPage
from .serializers import UserPageSerializer
from django.utils import timezone
from django.shortcuts import render


class UserPageDetail(APIView):
    """
    해당 매크로에 대한 나의 인증정보를 가져옵니다.
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
        serializer = UserPageSerializer(userPage)
        return Response(serializer.data)
