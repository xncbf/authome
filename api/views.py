from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from mypage.models import UserPage, Macro
from .serializers import UserPageSerializer


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