from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from mypage.models import UserPage
from .serializers import UserPageSerializer


class UserPageDetail(APIView):
    """
    해당 매크로에 대한 나의 인증정보를 가져옵니다.
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